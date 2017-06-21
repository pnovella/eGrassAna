from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

"""
Alphas for differnt drift HV
"""

hman = HistoManager(True)

runs = [3879,3875,3880]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)

rates,erates = [],[]
pbrates,pberates = [],[]
for run in runs:

    time,pbrate = Double(),Double()
    hman["%s_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_S1PBRate"%run].GetErrorY(0)
    pbrates.append(pbrate)
    pberates.append(pberate)
    
    time,rate = Double(),Double()
    hman["%s_S1AS2Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_S1AS2Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))

    print rate, pbrate
    
HVs = [22,15,8]
hman.graph("AS2Rate",HVs,rates,0,erates)
hman.setTitle("AS2Rate_graphAxis","Auto-trigger Runs")
hman.axis("AS2Rate_graphAxis",
          "Cathode Voltage (kV)","S2 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS2Rate","APL",markerType=20,lineType=2,min=50,max=200)

raw_input()

hman.graph("PBRate",HVs,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","Auto-trigger Runs")
hman.axis("PBRate_graphAxis",
          "Cathode Voltage (kV)","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("PBRate","APL",markerType=20,lineType=2,min=10,max=400)
raw_input()


for run in runs:
    hman.drawGraph("%i_S1AS2ChRate"%run,"AP",markerType=20)
    raw_input()
    hman.drawGraph("%i_S1AS2XYRate"%run,option="colz")
    raw_input()


for run in runs:
    hman.drawGraph("%i_S1PBChRate"%run,"AP")    
    raw_input()
    hman.drawGraph("%i_S1PBXYRate"%run,option="colz")
    raw_input()


