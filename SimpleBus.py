#Import All Of gem5's Objects
import m5
from m5.objects import * #Imports All SimObjects

#Instantiate A System
#"System" Is A Python Class Wrapper For The System C++ SimObject
#You CAN use object oriented coding, this is a bare bones example

system = System()

#Initialize A Clock & Voltage Domain
#"clk_domain" Is A *parmeter* Of The System SimObject
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz' #(...)
cpu_clock_speed = 1000000000 #(...)
#gem5 Knows How To Automatically Convert Units

system.clk_domain.voltage_domain = VoltageDomain()

#Setting Up Memory System
system.mem_mode = 'timing'
#*timing* is best for simulations (bc time matters)

#Memory For The System
system.mem_ranges = [AddrRange('8192MB')] #(...)

#Creating The CPU
system.cpu = TimingSimpleCPU() #(...)

#Creating Memory Bus
system.membus = SystemXBar() #Crossbar Memory Architecture (...)

#Hook Up CPU - "port" is a way to connect objects, all ports have a master and slave
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

#THE FOLLOWING IS A QUIRK FOR x86 IDK WHY
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

#Creating Memory Controller
#Modeling DDR3 RAM with a 64-bit Bus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8() #(...)
system.mem_ctrl.dram.range = system.mem_ranges[0]   #Setting Up Physical Memory Ranges
system.mem_ctrl.port = system.membus.master         #Connecting Memory To Bus

###ALL THE ABOVE IS SETUP FOR THE SYSTEM###
##### NOW WE GIVE ACTUAL INSTRUCTIONS #####
#(...)
system.workload = SEWorkload.init_compatible('tests/test-progs/hello/bin/x86/linux/hello')    #Needed for gem5 V21+ IDK why lol
process = Process() 
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello'] #This is an emulated process (can run full OS on top of gem5 tho)
system.cpu.workload = process
system.cpu.createThreads()

#Creating A Root Object
root = Root(full_system = False, system = system) #(...)

#Instantiate All Of The C++ Needed
m5.instantiate()

#At This Point It Is Ready To Run
print ("\n-----Beginning Simulation (Hello World Process) Now!-----\n")
exit_event = m5.simulate()

###When this runs, it'll pull things from event que until there's nothing left to do
print ("\n------------------------------------------------------------------------------")
print ("Exiting @ Tick %i because %s" % (m5.curTick(), exit_event.getCause()))
##Prints what tick it exited at and for what reason
MicroSec = (m5.curTick()/1000000) #Converts tick time to microseconds
Sec = (MicroSec / 1000000)
cpu_cycles = (Sec * cpu_clock_speed)
I = ((1 / cpu_clock_speed) * cpu_cycles)
cpu_cycles = int(cpu_cycles)
power = (0.8 * I * 1000000)
rounded_power = round(power, 4)

print ("\n--> AKA Event Queue Finished @ Roughly " + str(MicroSec) + " MicroSeconds")
print ("Or " + str(Sec) + " Seconds")
print ("\n--> And " + str(cpu_cycles) + " Cycles Executed")
print ("@ A Fixed Rate Of 0.8 Volts")
print ("\nConsuming ROUGHLY\n--> " + str(rounded_power) + " MicroWatts Of Power")
print ("------------------------------------------------------------------------------")
print("\n******Hey Look Here^^^^^\n")