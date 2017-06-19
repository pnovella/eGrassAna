from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time

hman = HistoManager(True)

runs = [4213,4218,4219,4220,4221,4222,4223] 
for run in runs: hman.load("../jobOptions/AutoTrigAna_%i.root"%run,"%i_"%run)


time0,rate = Double(),Double()
hman["%s_S1Rate"%runs[0]].GetPoint(0,time0,rate)
times,rates,erates = [],[],[]
for run in runs:
    rtime,rate = Double(),Double()
    hman["%s_S1Rate"%run].GetPoint(0,rtime,rate)
    erate = hman["%s_S1Rate"%run].GetErrorY(0)
    times.append((rtime-time0)/60)
    rates.append(rate)
    erates.append(erate)

hman.graph("myrate",[-0.5]+times,[0]+rates,0,[0]+erates)
hman.axis("myrate_graphAxis","Time (min)","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.drawGraph("myrate","AP",markerType=20,min=30,max=40)

raw_input()

time1,time2,rate = Double(),Double(),Double()
hman["%s_S1Rate"%runs[0]].GetPoint(0,time1,rate)
hman["%s_S1Rate"%runs[-1]].GetPoint(0,time2,rate)
hman.graph("Axis",[time1,time2],[0,0],0,0)
hman["Axis_graphAxis"].GetXaxis().SetTimeDisplay(1);
hman["Axis_graphAxis"].GetXaxis().SetTimeFormat("%H:%M");
hman.axis("Axis_graphAxis","Time","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.draw("Axis_graphAxis",max=40,min=30)
for run in runs: hman.drawGraph("%i_S1Rate"%run,"P",markerType=20)
raw_input()

