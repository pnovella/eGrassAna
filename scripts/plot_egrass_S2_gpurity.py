from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
Kr and Na runs
Co?
"""

runs = [3389,4446]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)

rates,erates = [],[]
pbrates,pberates = [],[]
times = []
for run in runs:

    time,pbrate = Double(),Double()
    hman["%s_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_S1PBRate"%run].GetErrorY(0)
    pbrates.append(pbrate)
    pberates.append(pberate)
    times.append(time)
    
    time,rate = Double(),Double()
    hman["%s_S1AS2Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_S1AS2Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))

    
hman.graph("AS2Rate",times,rates,0,erates)
hman.setTitle("AS2Rate_graphAxis","")
hman.axis("AS2Rate_graphAxis","Date","S2 e^{-} grass rate (ms^{-1})")
hman.setTitle("AS2Rate","")
hman["AS2Rate_graphAxis"].GetXaxis().SetTimeDisplay(1);
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS2Rate","APL",markerType=20,lineType=2)

hman.ps("s2_grass_kr_gpurity.eps")

raw_input()

hman.graph("PBRate",times,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","")
hman.axis("PBRate_graphAxis","Date","e^{-} grass rate (ms^{-1})")
hman["PBRate_graphAxis"].GetXaxis().SetTimeDisplay(1);
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("PBRate","APL",markerType=20,lineType=2)

hman.ps("bg_grass_kr_gpurity.eps")

raw_input()

