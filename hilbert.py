#hilbert transform 
#by sebastian Henao Santa

import visa
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from tempfile import TemporaryFile
#methods  and classes for capturing and processing the signal
###########################################################################
def string_to_float(signal):
  signalA = signal[1:]
  signalR = np.empty([])
  for i in range(0, len(signalA)):
    signalA[i] = float(signalA[i])
  signalR = signalA  
  return signalR

###########################################################################
"""
class conn_osci(object):
  def __init__(self, ipNumber, chuck_size, timeout):  
    self.ipNumber = ipNumber
    self.chuck_size = chuck_size
    self.timeout = timeout
    
  def init_instru(self):
    rm = visa.ResourceManager()  
    instrument = rm.open_resource('TCPIPO::172.16.20.'+self.ipNumber+'::INSTR')
    instrument.chunk_size = int(self.chuck_size)
    instrument.timeout = int(self.timeout)
    #my_instrument = rm.open_resource('TCPIPO::172.16.20.71::INSTR')
    ipadd = input("Write the las number of the ip address without spaces: ")
    chunk = input("Write the chunck size: ")
    timeout = input("Write the timeout: ")

  intrument1 = conn_osci(ipadd, chunk, timeout)
  intrument1.init_instru()    

"""
#variables
###########################################################################
ori_signal = np.empty([]) # signal vector
ori_signalB = np.empty([])# signal vector b
time =  np.empty([])#time vector
ts = 0 #sampling time
n = 0 #lenVector
analityc_signal = np.empty([])
amplitud_envelope = np.empty([])
outfile = TemporaryFile()
###########################################################################


##flow ejecution
#connection
###########################################################################
#connection
#########################################################################
rm = visa.ResourceManager()
my_instrument = rm.open_resource('TCPIPO::172.16.20.71::INSTR')#This instruction let you set the ip instruction 
print(my_instrument.query('*IDN?'))
print(my_instrument)
#########################################################################
#timeout and chunk_size
my_instrument.timeout = 45000 #this sets the time the instruction waits for each instruction
my_instrument.chunk_size = 1000 #this sets the lenght of the data that is recieved
#Initialize the instrument to a preset state
##my_instrumenHt.write('*RST') #reset  the instrument 
#my_instrument.write('*CLS')
##configure the  time parameters of the signal
my_instrument.write(":TIMebase:MODE MAIN") 
my_instrument.write(":TIMebase:REFerence CENTER")
my_instrument.write(":TIMebase:POSition 0")
#print(my_instrument.query(":TIMebase:POSition?"))
my_instrument.write(':TIMebase:RANGe 1')#time base to 50us/div
my_instrument.write(':TIMebase:SCALe 500e-6')
my_instrument.write(':TIMebase:DELay 0')#delay to zero
#print(my_instrument.query(':TIMebase:RANGe?'))
#print(my_instrument.query(':TIMebase?'))

#vertcial parameters voltage
my_instrument.write(':CHANnel1:PROBe 10')#probe attenuation to 10:1
my_instrument.write(':CHANnel1:RANGe 40')#Vertical range 1.6 full scale
my_instrument.write(':CHANnel1:SCALe 1')#Voltager per division scale


#trigger parameters
#my_instrument.write(':TRIGger:SWEep NORMal')
#my_instrument.write(':TRIGger:MODE EDGE')
my_instrument.write(":TRIGger:EDGE:SOURce CHANnel1")
my_instrument.write(':TRIGger:LEVel 1.66')
#my_instrument.write(":TRIGger:SLOPe POSitive")

#acquiring signal
##########################################################################
my_instrument.write(':WAVEFORM:SOURCE CHAN1')
my_instrument.write(":ACQuire:TYPE HRES")
my_instrument.write(":ACQuire:COMPlete 100")
print(my_instrument.query(":ACQuire:TYPE?"))
##########################################################################
my_instrument.write(":WAVeform:FORMat ASCII")
my_instrument.write(":WAVeform:POINts:MODE RAW")
print(my_instrument.query(':ACQuire:POINts?'))
my_instrument.write(":WAVeform:POINts 10000")
print(my_instrument.query(":WAVeform:POINts?"))
print(my_instrument.query(":WAVeform:POINts:MODE?"))

#adquiring sampling time
my_instrument.write(':WAV:XINC?')# get the sampling time
ts =  my_instrument.read() 
ts =  float(ts)
#adquiring points from the oscilloscope
my_instrument.write(":DIGitize CHANnel1")
ori_signal = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
ori_signalB = string_to_float(ori_signal)
#centering signal
ori_signalB = ori_signalB - np.mean(ori_signalB)
#configuring time vector
n = len(ori_signalB)
time = np.linspace(0, n*ts, n)
#analytic_signal
analityc_signal = hilbert(ori_signalB)
amplitud_envelope = np.abs(analityc_signal)

np.savetxt("signal.txt", ori_signalB, delimiter=',')
np.savetxt("time.txt", time, delimiter=',')

plt.plot(time, ori_signalB, time, amplitud_envelope)
plt.show()

#np.save(outfile, time)









    


