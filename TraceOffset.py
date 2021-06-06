import flux_dp
import numpy as np
import pylab as plt
from matplotlib.widgets import Cursor


# parameter of two axis
def make2D(first_leng,step,
           freq_start = 3.7,
           freq_stop = 7.7,
           flux_start = -0.5,
           flux_stop = 0,
           trace_freq = 101,
           trace_flux = 101,
           start = 1,
           stop = 4):
    
    Mag2D_res = np.zeros([trace_flux,trace_freq])
    title = " "
    for long in range(start,stop):
        leng = (long - 1) * step + first_leng
        Mag2D, Phase2D = flux_dp.flux_dependence(freq_start, freq_stop, flux_start, flux_stop,leng,
                                                 trace_freq,
                                                 trace_flux)
        #for offset
        quant = (long-1)*int(trace_flux/10)
        title += str(int(leng*10**3)) + ","
        app = []
        for remove in range(quant):
            Mag2D = np.delete(Mag2D,0,0)
            app.append([])
            for i in range(trace_freq):
                app[remove].append(1.)
    
        Mag2D = np.array(list(Mag2D) + app)
        Mag2D_res += Mag2D
    
    return Mag2D_res,title
if __name__ == '__main__':
    freq_start = 3.7
    freq_stop = 7.7
    flux_start = -0.5
    flux_stop = 0
    step = 11 * 10 ** -3
    first_leng = 22*10**-3
    
    start,stop = 1,4
    
    
    trace_freq = 101
    trace_flux = 101
    
    res = make2D(first_leng,step,
                 trace_freq = 101,
                 trace_flux = 101)
    title = res[1] + "mm"
    fig, ax = plt.subplots(1, 1, subplot_kw=dict(facecolor="lemonchiffon"))
    fig.set_figheight(15)
    fig.set_figwidth(15)
    ax.set_title(title)
    im = ax.imshow(res[0], extent=(freq_start, freq_stop, flux_stop, flux_start), aspect='auto')
    cursor = Cursor(ax, useblit=True)
    ax.set_xlabel("freqency (GHz)")
    ax.set_ylabel("flux")
    fig.colorbar(im)
    
    plt.show()
