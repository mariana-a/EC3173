#r# This example depicts half and full wave rectification.

####################################################################################################

import matplotlib.pyplot as plt

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

####################################################################################################

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

####################################################################################################

#figure1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 10))
figure1, ((ax1 , ax2)) = plt.subplots(2, figsize=(20, 10))
####################################################################################################

##------------------- CAMBIAR AQUI  parametros de la fuente de pulsos de voltaje--------------------
## Solo cambiar la frecuencia  y el ratios del duty cycle (por defecto esta puesto en 0.5)


ratio = 0.5
amplitude_=10@u_V
frequency = 50@u_Hz
periodo = frequency.period
duty_cycle = ratio * periodo

####################################################################################################

circuit = Circuit('half-wave rectification')
circuit.include(spice_library['BAV21'])

source = circuit.PulseVoltageSource('input', 'in', circuit.gnd, -amplitude_, amplitude_, duty_cycle, periodo)
#circuit.X('D1', '1N4148', 'in', 'output')
#circuit.X('D1', '1N4148', 'in', 't')
circuit.D('D1', 'in', 't', model='BAV21')
circuit.V(1, 't', 'output', 0@u_V)    #Test probe para medir la corriente
circuit.R('load', 'output', circuit.gnd, 100@u_Ω)
""""
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

ax1.set_title('Half-Wave Rectification')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(analysis['in'])
ax1.plot(analysis.output)
ax1.legend(('input', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-amplitude_*1.1), float(amplitude_*1.1))
"""
####################################################################################################

#f# circuit_macros('half-wave-rectification.m4')

circuit.C('1', 'output', circuit.gnd, 1@u_mF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=periodo/200, end_time=periodo*2)

ax1.set_title('Half-Wave Rectification with filtering')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(analysis['in'])
ax1.plot(analysis.output)
ax1.legend(('input', 'output'), loc=(.05,.1))
ax1.set_ylim(float(-amplitude_*1.1), float(amplitude_*1.1))


###Current ----------------------------------------------
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=periodo/200, end_time=periodo*2)

ax2.set_title('Current in Diode during rectification')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Current[A]')
ax2.grid()
ax2.plot(analysis.branches[('v1')], 'k')
#ax3.plot(analysis.output, 'r')
ax2.legend(('Diode Current'), loc=(.05,.1))
ax2.set_ylim(float(-20), float(25))

plt.tight_layout()
#-----------------------------------------------------------




plt.show()