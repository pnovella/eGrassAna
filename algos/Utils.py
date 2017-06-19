from math import log,sqrt
from ROOT import gSystem
gSystem.Load("$GATE_DIR/lib/libGATE")
from ROOT import gate

def isGoodRecoType(signal,label):

    if label: return signal.find_sstore(label) 

    else: return ( not signal.find_sstore("RecoSignal")) # !!! 

def getFWHM(sigma): return 2*sqrt(2*log(2))*sigma 
    
        
def getGoodSignals(event,recolabel=""):
    signals = [s for s in event.GetSignals() \
                   if (s.GetSignalType()!=gate.NOSTYPE \
                           and isGoodRecoType(s,recolabel))]

    return signals
