import tkinter as tk
import pylab as plt
import numpy as np
from TraceOffset import make2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Cursor

fig, ax1 = plt.subplots(1) # create figure
plt.tight_layout()
canvas = FigureCanvas(fig)



# parameter of two axis

    
def calculate_bmi_number():
    ax1.cla()
    #fig.clf()
    global freq_start
    global freq_stop
    global flux_start
    global flux_stop
    global trace_freq
    global trace_flux
    
    step = float(step_entry.get())*10**-3
    first = float(first_entry.get())*10**-3
    res = make2D(first,step,
                 freq_start = freq_start,
                 freq_stop = freq_stop,
                 flux_start = flux_start,
                 flux_stop = flux_stop,
                 trace_freq = trace_freq,
                 trace_flux = trace_flux,
                 start = 1,
                 stop = 4)
    
    ax1.set_title(res[1])
    im = ax1.imshow(res[0],extent=(freq_start, freq_stop, flux_stop, flux_start), aspect='auto')
    ax1.set_xlabel("freqency (GHz)")
    ax1.set_ylabel("flux")
    #fig.colorbar(im)
    
freq_start = 3.7
freq_stop = 7.7
flux_start = -0.6
flux_stop = 0
length = 33 * 10 ** -3


trace_freq = 251
trace_flux = 251

window = tk.Tk()


window.title('BMI App')
window.geometry('300x100')
window.configure(background='white')

# 以下為 weight_frame 群組
step_frame = tk.Frame(window)
step_frame.pack(side=tk.TOP)
step_label = tk.Label(step_frame, text='step (mm)')
step_label.pack(side=tk.LEFT)
step_entry = tk.Entry(step_frame)
step_entry.pack(side=tk.LEFT)

first_frame = tk.Frame(window)
first_frame.pack(side=tk.TOP)
first_label = tk.Label(first_frame, text='first(mm)')
first_label.pack(side=tk.LEFT)
first_entry = tk.Entry(first_frame)
first_entry.pack(side=tk.LEFT)

result_label = tk.Label(window)
result_label.pack()

calculate_btn = tk.Button(window, text='count soon', command=calculate_bmi_number)
calculate_btn.pack()

canvas.draw()
window.mainloop()