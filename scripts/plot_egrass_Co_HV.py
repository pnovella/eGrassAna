from ROOT import kRed,Double
from Centella.histoManager import HistoManager

from math import sqrt

hman = HistoManager(True)
runs = [3945,3957]
for run in runs: hman.load("../data/AutoTrigAna_%i.root"%run,"%i_"%run)

rates,erates = [],[]
for run in runs:
    rtime,rate = Double(),Double()
    hman["%s_S1Rate"%run].GetPoint(0,rtime,rate)
    erate = hman["%s_S1Rate"%run].GetErrorY(0)
    rates.append(rate)
    erates.append(erate)


hman.graph("myrate",runs,rates,0,erates)
hman.axis("myrate_graphAxis","Run Number","e^{-} grass rate (ms^{-1})")
hman.setTitle("myrate_graphAxis","Auto-trigger Runs")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("myrate","APL",markerType=20,min=160,max=175)
hman.addText(3945,170,"Gate HV Off",color="red",size=0.02)
hman.addText(3945,169,"Cathode HV Off",color="red",size=0.02)
hman.addText(3955,166,"Gate HV Off",color="red",size=0.02)
hman.addText(3955,165,"Cathode HV 15kV",color="red",size=0.02)
raw_input()
