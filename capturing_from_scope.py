#configuring the oscilloscope



import visa
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


#methods
###############################################################################

def string_to_float(signal):
  signal =  np.array(signal)
  valueA = np.array([])
  valueA = signal[1:]
  valueA = valueA.astype(np.float)
  return valueA 


###############################################################################
#variables
###############################################################################

values = np.array([])
valuesR = np.array([])
s_p1 = np.array([])
s_p2 = np.array([])

analytic_signal_1 = np.array([])
analytic_signal_2 = np.array([])

envelope1 =  np.array([])
envelope2 =  np.array([])

env1_maxp = np.array([])
env2_maxp = np.array([])

###############################################################################
#connection
###############################################################################
rm = visa.ResourceManager()
my_instrument = rm.open_resource('TCPIPO::172.16.20.71::INSTR')#This instruction let you set the ip instruction 
print(my_instrument.query('*IDN?'))
print(my_instrument)
#########################################################################
#timeout and chunk_size
my_instrument.timeout = 45000 #this sets the time the instruction waits for each instruction
my_instrument.chunk_size = 10000 #this sets the lenght of the data that is recieved
#Initialize the instrument to a preset state
##my_instrument.write('*RST') #reset  the instrument 
#my_instrument.write('*CLS')
##configure the  time parameters of the signal
my_instrument.write(":TIMebase:MODE MAIN") 
my_instrument.write(":TIMebase:REFerence LEFT")
my_instrument.write(":TIMebase:POSition 0")
#print(my_instrument.query(":TIMebase:POSition?"))
my_instrument.write(':TIMebase:RANGe 1')#time base to 50us/div
my_instrument.write(':TIMebase:SCALe 800e-9')
my_instrument.write(':TIMebase:DELay 49.3e-6')#delay to zero
#print(my_instrument.query(':TIMebase:RANGe?'))
#print(my_instrument.query(':TIMebase?'))

#vertcial parameters voltage
my_instrument.write(':CHANnel1:PROBe 10')#probe attenuation to 10:1
#my_instrument.write(':CHANnel1:RANGe 40')#Vertical range 1.6 full scale
my_instrument.write(':CHANnel1:SCALe 5')#Voltager per division scale


#trigger parameters
#my_instrument.write(':TRIGger:SWEep NORMal')
#my_instrument.write(':TRIGger:MODE EDGE')
my_instrument.write(":TRIGger:EDGE:SOURce EXTernal")
#my_instrument.write(':TRIGger:LEVel 1')
#my_instrument.write(":TRIGger:SLOPe POSitive")

#acquiring signal
##########################################################################
my_instrument.write(':WAVEFORM:SOURCE CHAN1')
my_instrument.write(":ACQuire:TYPE HRES")
my_instrument.write(":ACQuire:COMPlete 100")
print(my_instrument.query(":ACQuire:TYPE?"))

my_instrument.write(":WAVeform:FORMat ASCII")
my_instrument.write(":WAVeform:POINts:MODE RAW")
my_instrument.write(':ACQ:POIN 10000')
my_instrument.write(":WAVeform:POINts 10000")
print(my_instrument.query(':ACQuire:POINts?'))
print(my_instrument.query(":WAVeform:POINts?"))
print(my_instrument.query(":WAVeform:POINts:MODE?"))
###############################################################################
my_instrument.write(':WAV:XINC?')
ts =  my_instrument.read()
ts = float(ts)
###############################################################################
my_instrument.write(":DIGitize CHANnel1")
values = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
###############################################################################
valuesR = string_to_float(values)
#time vector
N = len(valuesR)
t = np.linspace(0, ts*N*1e6, N)
#hilbert signal 1
###########
t2 = t[0:4000]
t3 = t[4000:len(t)]
#flip signal1
s_p1 = valuesR[0:len(t2)]*-1
analytic_signal_1 = hilbert(s_p1)
envelope1 = np.absolute(analytic_signal_1)
#flip signal2
s_p2 = valuesR[4000:len(t)]
analytic_signal_2 = hilbert(s_p2)
envelope2 = np.absolute(analytic_signal_2)
#plt.plot(t2, s_p1, t2, envelope1, t3, s_p2, t3, envelope2)
#finding times between each wave
#wave1
env1_maxp = np.argmax(envelope1)
#wave2
env2_maxp = np.argmax(envelope2) + len(t2)
#time delay between each signal

tf = t[env2_maxp]-t[env1_maxp]

#plotting
#############
plt.subplot(211)
plt.title("ultrasonic wave")
plt.xlabel("time (us)")
plt.ylabel("voltage (v)")
plt.grid(True)
plt.plot(t, valuesR,'r')
plt.subplot(212)
#plt.title("ultrasonic wave")
plt.xlabel("time (us)")
plt.ylabel("voltage (v)")
plt.grid(True)
plt.plot(t2, s_p1, t2, envelope1, t3, s_p2, t3, envelope2,t[env1_maxp], np.amax(envelope1), 'g^', 5.328666166541637, 3.753403566980277,'b^')


plt.show()




