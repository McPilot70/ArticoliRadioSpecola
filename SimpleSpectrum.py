from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
from rtlsdr import RtlSdr
import numpy as np

sdr = RtlSdr()
# configure device RTL 
sdr.sample_rate = 2.4e6  # Hz
# Imposta la frequenza iniziale 
sdr.center_freq = 98.0e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

# Prepara il grafico 
fig = plt.figure()
graph_out = fig.add_subplot(1, 1, 1)


# metodo richiamato quando viene premuto enter sul testo ( dopo aver inserito la frequenza )
def submit(text):
    sdr.center_freq =  eval(text)
    

# Predisposizione casella di testo dove inserire la frequenza
axbox = plt.axes([0.3, 0.90, 0.2, 0.075])
text_box = TextBox(axbox, 'Frequenza :')
text_box.set_val(str(sdr.center_freq))
text_box.on_submit(submit)




# metodo richiamato 
def animate(i):
    # pulisci grafico
    graph_out.clear()
    # prendi i campioni dal Ricevitore ( doungle USB )
    samples = sdr.read_samples(256*1024)
    # permette di stampare a video. Il PSD (Power Spectral Density )
    # estensione di numPy consente di passare dal dominio del tempo al dominio della frequenza
    # per ottenere lo spettro del segnale ricevuto 
    graph_out.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                  1e6, Fc=sdr.center_freq/1e6)
 


# predisposizione sistema di ricezione dati e visualizzazione 
try:
    # Permette di richiamare rieptutamente il metodo sopra che 
    # si preoccupa di aggiornare il grafico con i nuovi campioni 
    # appena ricevuti 
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()
except KeyboardInterrupt:
    # premuto tasto per uscita 
    pass
finally:
    # uscita dall'applicazione 
    sdr.close() 