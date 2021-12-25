import numpy as np
import pylab as plt
from matplotlib.widgets import Cursor

class FluxDp():
    def __init__(self,freq_start, freq_stop, flux_start, flux_stop,
                L=33 * 10 ** -3,
                relax=28 * 10 ** 6,
                v= 0.89488*10**8,
                trace_freq = 501,
                trace_flux = 501,
                pure_dephase=2.7 * 10 ** 6,
                #(4.426 * 33 * 4 / 7) * 10 ** 6,
                Ec = 0.3 * 10 ** 9,
                Ej = 25 * 10 ** 9):
        
        self.flux_tunning = np.linspace(flux_start, flux_stop, trace_flux)
        self.freq = np.linspace(freq_start * 10 ** 9, freq_stop * 10 ** 9, trace_freq)
        self.trace_flux = trace_flux
        self.trace_freq = trace_freq
        self.L = L
        self.relax = relax
        self.pure_dephase = pure_dephase
        self.v = v
        self.Ec = Ec
        self.Ej = Ej
        self.freq_start = freq_start
        self.freq_stop = freq_stop
        self.flux_stop = flux_stop
        self.flux_start = flux_start
        
    def reflect_coe(self,flux,L,v):
        #h = 6.626 * 10 ** -34  # planck constant
    
        Ej_of_flux = self.Ej * abs(np.cos(np.pi * flux))  # Ej(flux)
    
        freq_center = (8 * Ej_of_flux * self.Ec) ** 0.5 - self.Ec  # qubit frequency
        theta = 2*2 * np.pi * L
        Lambda = v / freq_center  # lambda
        theta = theta / Lambda  # phase factor
    
        relax_of_flux = self.relax * (np.cos(theta / 2)) ** 2  # relaxation(flux)
        decoh = self.pure_dephase + relax_of_flux / 2  # decoherence(flux)
    
        ref_coe = np.zeros(len(self.freq), dtype=complex)
    
        for delta in range(len(self.freq)):
            reflect = relax_of_flux / decoh
            reflect = reflect * (1 - 1j * (self.freq[delta] - freq_center) / decoh) / (
                        1 + ((self.freq[delta] - freq_center) / decoh) ** 2)
            ref_coe[delta] = 1 - reflect  # reflect is from Hoi PhD (2.79)
        
        return ref_coe,decoh//(10**6),relax_of_flux//(10**6)
    
    def flux_dependence(self,L,v):
        # create 2D zero matrix
        Mag2D = np.zeros((self.trace_flux, self.trace_freq))
        Phase2D = np.zeros((self.trace_flux, self.trace_freq))
        
        # count and plot 2D matrix
        for tunning in range(len(self.flux_tunning)):
            result = self.reflect_coe(self.flux_tunning[tunning],L,v)
            Mag2D[tunning] = abs(result[0])
            Phase2D[tunning] = np.arctan(np.real(result[0]) / np.imag(result[0]))
    
        return Mag2D,Phase2D
    
    def OffSet(self,variable,mode = "length"):
        
        Mag2D_res = np.zeros([self.trace_flux,self.trace_freq])
        title = " "
        count = 1
        for var in variable:
            if mode == "length":
                Mag2D, Phase2D = self.flux_dependence(var,self.v)
                title += str(int(var*10**3)) + ","
            else:
                Mag2D, Phase2D = self.flux_dependence(self.L,var)
                title += str(int(var/(10**8))) + ","
            
            #for offset
            quant = (count-1)*int(self.trace_flux/20)
            
            app = []
            for remove in range(quant):
                Mag2D = np.delete(Mag2D,0,0)
                app.append([])
                for i in range(self.trace_freq):
                    app[remove].append(1.)
        
            Mag2D = np.array(list(Mag2D) + app)
            Mag2D_res += Mag2D
            count += 1
        if mode == "length":
            title += "(mm)"
        else:
            title += "(10^8 m/s)"
        return Mag2D_res, title
    
    def plot1D(self,flux):

        for i in flux:
            plt.plot(self.freq,self.reflect_coe(i,self.L,self.v)[0])
        plt.show()
         
    def plot2D(self,offset,*arg):
        if offset == True:
            Mag2D, Phase2D = self.flux_dependence(self.L,self.v)
            title = str(int(self.L*10**3)) + "mm"
        else:
            parameter = arg[0]
            res = self.OffSet(parameter[0],mode = parameter[1])
            Mag2D = res[0]
            title = str(parameter[1]) + res[1]
           
        fig, ax = plt.subplots(1, 1, subplot_kw=dict(facecolor="lemonchiffon"))
        fig.set_figheight(15)
        fig.set_figwidth(15)    
        ax.set_title(title)
        im = ax.imshow(Mag2D, extent=(self.freq_start, self.freq_stop, self.flux_stop, self.flux_start), aspect='auto')
        ax.set_xlabel("freqency (GHz)")
        ax.set_ylabel("flux")
        fig.colorbar(im)
        plt.show()
    
if __name__ == '__main__':
    
    flux_dp_tool = FluxDp(freq_start = 4, 
                          freq_stop = 8,
                          flux_start = -0.5, 
                          flux_stop = 0,
                          L = 33*10**-3,
                          v = 0.6*10**8
                          )
    L_list = np.array([0,22,44,66])*10**-3
    v_list = np.array([0.6,1,1.5])*10**8
    
    """plot trace"""
    #flux_dp_tool.plot1D([-0.3,0,0.2])
    
    """plot 2D"""
    #flux_dp_tool.plot2D(True)
    
    """plot 2D with changing velocity"""
    #flux_dp_tool.plot2D(False,[v_list,"velocity"])
    
    """plot 2D with changing length"""
    flux_dp_tool.plot2D(False,[L_list,"length"])