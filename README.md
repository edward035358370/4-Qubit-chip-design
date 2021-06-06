# 4-Qubit-chip-design

# flux_dp.py
flux_dp.py is for counting the reflection coefficient for 1D and 2D plot function.
## Parameters you can choose:
  ### A:reflect_coe
	1, pure dephasing rate, unit:Hz
	2, relaxation rate, unit:Hz
	3, Ec, unit:Hz
	4, Ej, unit:Hz
	5, distance between the mirror and qubit, unit:m
	6, light's velocity, unit:m/s
	8, flux please input float type parameter, unit:
	9, frequency please input array type parameter, unit:Hz
  ### B:flux_dependence
	1, freq_start, unit:Hz
	2, freq_stop, unit:Hz
	3, flux_start, unit:
	4, flux_stop, unit:
	5, L, unit: m
	6, trace_freq, resolution
	7, trace_flux, resolution
# PlotTool.py
There are two plot function with well labeled function in PlotTool.py .

# TraceOffset.py
For more easier to see the qubit reflection with different parameters and give the offset to the Mag2D plot.
I give the cursor when we plot it, but still don't know how to plot with cursor by calling function way.
# TrackNode.py
We set three qubit have different distance between mirror. For both qubit can be at the node and the other can be at the antinode.
This code use the not efficient way but working way to get the three qubit distance components.
# tkinter_plot.py
choose the first qubit distance between mirror,  and choose the next distance for next qubit.
I use tkinter for control these two parameters for showing the 2D plot, but you need to click the figure function and then click the axes inside because of the reason I don't know.
Still can't show the cursor.
