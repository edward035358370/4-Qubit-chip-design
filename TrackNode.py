import flux_dp
import sys

def node_antinode(freq_start,freq_stop,flux_start,flux_stop,
                  length = 33 * 10 ** -3,num_trace = 1001):
    freq = flux_dp.np.linspace(freq_start,freq_stop,1001)*10**9
    flux_tunned = flux_dp.np.linspace(flux_start,flux_stop,1001)
    Mag2D = []
    node = []
    antinode = []
    record = 0
    record_S21 = 0
    for flux in flux_tunned:
        reflect,_,_ = flux_dp.reflect_coe(flux, freq,L = length)
        Mag = abs(reflect)
        Mag2D.append(Mag)
        temp = list(Mag)
        min_ = min(temp)
        if min_ >= 0.9:
            if abs(freq[temp.index(min_)] - record) >= 200*10**6:
                record = freq[temp.index(min_)]
                record_S21 = min_
                node.append(record)
            elif min_ - record_S21 >= 0:

                record = freq[temp.index(min_)]
                record_S21 = min_
                node.pop()
                node.append(record)
    
    for anti in range(1,len(node)):
        antinode.append((node[anti-1] + node[anti])/2)
    return node,antinode,flux_dp.np.array(Mag2D)


  
#node_anti_res = [[[4000000000.0, 5688000000.0], [4844000000.0]], [[4000000000.0, 4744000000.0, 6640000000.000001], [4372000000.0, 5692000000.0]], [[4000000000.0, 4428000000.0, 5688000000.0, 6955999999.999999], [4214000000.0, 5058000000.0, 6322000000.0]], [[4000000000.0, 4268000000.0, 5220000000.0, 6168000000.0, 7112000000.0], [4134000000.0, 4744000000.0, 5694000000.0, 6640000000.0]]]

def node_antinode_compare(node_anti_res,n ,pos,ran,get):
    for longer in ran[:n] + ran[n+1:]:
        for other in range(len(node_anti_res[longer][1])):
            temp = abs(node_anti_res[n][0][pos] - node_anti_res[longer][1][other])
            if temp <= 10*10**6:
                get[n].append([longer,node_anti_res[longer][1][other]])

    return get



def get(length_compare,original_length,
        trace_flux = 1001,
        trace_freq = 1001,
        freq_start = 3.7,
        freq_stop = 8,
        flux_start = -0.5,
        flux_stop = 0):
    
    f = open("./txt_res/from %s.txt"%(original_length),"a")
    for length in length_compare:
        node_anti_res = []
        title = " "
        for i in range(1,4):
            leng = (i-1) * length + original_length
            res = node_antinode(freq_start,freq_stop,flux_start,flux_stop,leng)
            node_anti_res.append([res[0],res[1]])
            title += str(int(leng*10**3)) + " "
            
        get = {0:[],1:[],2:[]}
        ran = []
        for i in range(len(node_anti_res)):
            ran.append(i)
        for n in range(len(node_anti_res)):
            for pos in range(len(node_anti_res[n][0])):
                get = node_antinode_compare(node_anti_res,n ,pos,ran, get)
        f.write("long: %s(mm), get=%s\n"%(title,get))
        f.write("  \n")
        print(title)
        print(get)
    f.close()

freq_start = 3.7
freq_stop = 7.7
flux_start = -0.5
flux_stop = 0

length_compare = flux_dp.np.linspace(10,50,41) * 10 ** -3
original_length = flux_dp.np.linspace(10,50,41) * 10 ** -3

trace_freq = 1001
trace_flux = 1001

for qubit_pos in original_length:
    get(length_compare,qubit_pos)