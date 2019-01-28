#controling the oscilloscope to take differente signal 
#by sebastian henao


import visa
import numpy as np
import matplotlib.pyplot as plt

#
###########################################

values = []
vulues1 = []
values2 = []
values3 = []
values4 = []
values5 = []
values6 = []
values7 = []
values8 = []

########################################
#connection
#########################################################################
rm = visa.ResourceManager()
my_instrument = rm.open_resource('TCPIPO::172.16.20.71::INSTR')#This instruction let you set the ip instruction   
print(my_instrument.query('*IDN?'))
print(my_instrument)
#########################################################################
#timeout and chunk_size
my_instrument.timeout = 45000 #this sets the time the programm waits for each instruction 
my_instrument.chunk_size = 10000 #this sets the size of the data that is recieved
#Initialize the instrument to a preset state
for i in range(0,8):
    print(i)
    #my_instrument.write('*CLS')
    #my_instrument.write('*RST') #reset  the instrument 

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
    my_instrument.write(':TRIGger:LEVel 1.65')
#my_instrument.write(":TRIGger:SLOPe POSitive")

#acquiring signal
##########################################################################
    my_instrument.write(':WAVEFORM:SOURCE CHAN1')
    my_instrument.write(":ACQuire:TYPE NORMal")
    #my_instrument.write(":ACQuire:TYPE HRES")
    my_instrument.write(":ACQuire:COMPlete 100")
    print(my_instrument.query(":ACQuire:TYPE?"))

    my_instrument.write(":WAVeform:FORMat ASCII")
    my_instrument.write(":WAVeform:POINts:MODE RAW")
    print(my_instrument.query(':ACQuire:POINts?'))
    my_instrument.write(":WAVeform:POINts 10000")
    print(my_instrument.query(":WAVeform:POINts?"))
    print(my_instrument.query(":WAVeform:POINts:MODE?"))
    my_instrument.write(":DIGitize CHANnel1")
    
    if i == 0:
        values = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
    elif i == 1:
        values1 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
    elif i == 2:
        values2 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
        
    elif i == 3:
        values3 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
        
    elif i == 4:
        values4 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
        
    elif i == 5:
        values5 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
        
    elif i == 6:
        values6 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
    elif i == 7:
        values7 = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
        
    