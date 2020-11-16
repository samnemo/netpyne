# execfile('hopbrodnetpyne.py')
# notebook: ~/nrniv/notebooks/nbnetpyne.dol
from netpyne import specs, sim

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration


# Network and connections
netParams.popParams['hop'] = {'cellType': 'PYR', 'cellModel': 'HH', 'numCells': 20}
netParams.connParams['hop->hop'] = {'preConds': {'pop': 'hop'}, 'postConds': {'pop': 'hop'}, 'weight': 0.0, 'synMech': 'inh', 'delay': 5}
netParams.stimSourceParams['bg'] = {'type': 'IClamp', 'delay': 10, 'dur': int(1000), 'amp': 0.2}

# cells
netParams.cellParams['hh_PYR'] = {
  'conds': {'cellType': 'PYR'}, # could have complex rule here for eg PYR cells in certain loc with particular implementation
  'secs': {'soma': {'geom' :  {'diam': 5, 'L': 5}, 'vinit' : -70.6,
                         'mechs':  {'hh' : {'gnabar': 0.10, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}}}}}
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau2': 1.0, 'e': 0}
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau2': 1.0, 'e': -80}
netParams.stimTargetParams['bg->hop'] = {'source': 'bg', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'hop'}}

# Simulation parameters
simConfig.duration = 500     # Duration of the simulation, in ms
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}
                          #'ik_soma':{'sec':'soma','loc':0.5,'var':'ik'}}
                          #'exc_soma':{'sec':'soma','synMech':'exc', 'loc':0.5,'var':'i'}}  # Dict with traces to record
simConfig.addAnalysis('plotTraces', {'include': [0]})

# Create network and run simulation
def create ():
  global pops,cells
  sim.initialize(netParams, simConfig)
  pops = sim.net.createPops()                      # instantiate network populations
  cells = sim.net.createCells()                     # instantiate network cells based on defined populations
  sim.net.addStims()
  sim.net.connectCells()                    # create connections between cells based on params
  sim.setupRecording()                      # setup variables to record for each cell (spikes, V traces, etc)

def run (): sim.simulate()
def plot ():
  sim.analysis.plotRaster()
  sim.analysis.plotRaster(syncLines=True)
  sim.analysis.plotData()


create()
run()
plot()

sim.net.modifyConns({'conds': {'label': 'hop->hop'}, 'weight': 0.5}) # increase inh conns weight increase sync

run()
plot()
