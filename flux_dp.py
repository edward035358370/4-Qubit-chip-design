import numpy as np

# every parameters are in Hz, m, or m/s
def reflect_coe(flux, freq, L=33 * 10 ** -3,
                relax=28 * 10 ** 6,
                pure_dephase=3 * 10 ** 6,
                v=(4.426 * 33 * 4 / 7) * 10 ** 6,
                Ec=0.3 * 10 ** 9,
                Ej=25 * 10 ** 9
                ):
    h = 6.626 * 10 ** -34  # planck constant

    Ej_of_flux = Ej * abs(np.cos(np.pi * flux))  # Ej(flux)

    freq_center = (8 * Ej_of_flux * Ec) ** 0.5 - Ec  # qubit frequency

    theta = 2 * 2 * np.pi * L
    Lambda = v / freq_center  # lambda
    theta = theta / Lambda  # phase factor

    relax_of_flux = relax * (np.cos(theta / 2)) ** 2  # relaxation(flux)
    decoh = pure_dephase + relax_of_flux / 2  # decoherence(flux)

    ref_coe = np.zeros(len(freq), dtype=complex)

    for delta in range(len(freq)):
        reflect = relax_of_flux / decoh
        reflect = reflect * (1 - 1j * (freq[delta] - freq_center) / decoh) / (
                    1 + ((freq[delta] - freq_center) / decoh) ** 2)
        ref_coe[delta] = 1 - reflect  # reflect is from Hoi PhD (2.79)
        
    return ref_coe,decoh//(10**6),relax_of_flux//(10**6)


def flux_dependence(freq_start, freq_stop, flux_start, flux_stop,
                 L = 33*10*-3,
                 trace_freq = 1001,
                 trace_flux = 1001
                 ):
    freq = np.linspace(freq_start * 10 ** 9, freq_stop * 10 ** 9, trace_freq)
    flux_tunning = np.linspace(flux_start, flux_stop, trace_flux)
    # create 2D zero matrix
    Mag2D = np.zeros((trace_flux, trace_freq))
    Phase2D = np.zeros((trace_flux, trace_freq))

    # count and plot 2D matrix
    for tunning in range(len(flux_tunning)):
        result = reflect_coe(flux_tunning[tunning], freq, L=L)
        Mag2D[tunning] = abs(result[0])
        Phase2D[tunning] = np.arctan(np.real(result[0]) / np.imag(result[0]))

    return Mag2D,Phase2D

if __name__ == '__main__':
    import PlotTool
    freq = np.linspace(4,8,1001)*10**9
    for i in np.linspace(-0.22,-0.3,5):
        r = reflect_coe(i, freq, L=48*10**-3)
        PlotTool.plt.plot(freq,np.abs(r[0]))
    PlotTool.plt.show()
    '''
    # parameter of two axis
    freq_start = 4
    freq_stop = 8
    flux_start = -0.5
    flux_stop = 0
    length = 33 * 10 ** -3

    for long in range(1,2):
        leng = long * length + 15*10**-3
        Mag2D,Phase2D = flux_dependence(freq_start, freq_stop, flux_start, flux_stop,
                                    L = leng)
        PlotTool.imshow2D(Mag2D,freq_start, freq_stop, flux_stop, flux_start,
                           xlab = 'frequency (GHz)',
                           ylab = 'flux',
                           title = "magnitude(" + "L =" + str(leng * 10 ** 3) + "mm)")

        PlotTool.imshow2D(Phase2D, freq_start, freq_stop, flux_stop, flux_start,
                         xlab='frequency (GHz)',
                         ylab='flux',
                         title="phase(" + "L =" + str(leng * 10 ** 3) + "mm)")
    PlotTool.plt.show()
    '''
