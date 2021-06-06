import matplotlib.pyplot as plt


def imshow2D(matrix2D, freq_start, freq_stop, flux_stop, flux_start,
             title="2D",
             xlab="GHz",
             ylab="flux"):
    plt.figure()
    plt.title(title)
    plt.imshow(matrix2D, extent=(freq_start, freq_stop, flux_stop, flux_start), aspect='auto')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.colorbar()

def imshow2D_cursor(matrix2D, freq_start, freq_stop, flux_stop, flux_start,
             title="2D",
             xlab="GHz",
             ylab="flux"):
    fig, ax = plt.subplots(1, 1, subplot_kw=dict(facecolor="lemonchiffon"))
    fig.set_figheight(15)
    fig.set_figwidth(15)
    ax.set_title(title)
    im = ax.imshow(matrix2D, extent=(freq_start, freq_stop, flux_stop, flux_start), aspect='auto')

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    fig.colorbar(im)


def plot1D(freq, S21, labeling):
    plt.figure()
    plt.plot(freq, S21, label=labeling)
    plt.legend()
    plt.xlabel("frequency (GHz)")
    plt.ylabel("reflection")
    plt.xlim((4, 8))
