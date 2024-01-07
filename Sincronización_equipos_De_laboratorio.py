# NI-DAQmx Python Documentation: https://nidaqmx-python.readthedocs.io/en/latest/index.html
# NI USB-621x User Manual: https://www.ni.com/pdf/manuals/371931f.pdf
import numpy as np
import nidaqmx
import matplotlib.pyplot as plt

#para saber el ID de la placa conectada (DevX)

def getdaq():
    equipos = []
    system = nidaqmx.system.System.local()
    for device in system.devices:
        equipos.append(device)
        
    return equipos
	

## Medicion por tiempo/samples de una sola vez
def medirHBT(duracion, fs):
    chanelH =  "Dev2/ai0"
    chanelB =  "Dev2/ai1"
    chanelT =  "Dev2/ai2"
    
    cant_puntos = duracion*fs    
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFF 
        task.ai_channels.add_ai_voltage_chan("Dev2/ai0",min_val=- 1.0, max_val=1.0,  terminal_config = modo)
        task.ai_channels.add_ai_voltage_chan("Dev2/ai1", min_val=- 1.0, max_val=1.0, terminal_config = modo)
        task.ai_channels.add_ai_voltage_chan("Dev2/ai2", min_val=- 1.0, max_val=1.0, terminal_config = modo)
               
        task.timing.cfg_samp_clk_timing(rate = fs ,samps_per_chan = int(cant_puntos), sample_mode = nidaqmx.constants.AcquisitionType.FINITE )

        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE, timeout = duracion+2)           
    datos = np.asarray(datos)
    return datos

## Medicion por tiempo/samples de una sola vez
def medir_oscilacion(duracion, fs):
    chanelH =  "Dev2/ai0"
    
    cant_puntos = duracion*fs    
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration(10106) 
        task.ai_channels.add_ai_voltage_chan("Dev2/ai0",min_val= -0.20, max_val= 10.0,  terminal_config = modo)
        
        task.timing.cfg_samp_clk_timing(rate = fs ,samps_per_chan = int(cant_puntos), sample_mode = nidaqmx.constants.AcquisitionType.FINITE )

        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE, timeout = duracion+2)           

    return datos

#%%
'''
print(getdaq())
datos = medir_oscilacion(5.0, 100000.0)
print(datos)
plt.plot(range(len(datos)),datos)

'''