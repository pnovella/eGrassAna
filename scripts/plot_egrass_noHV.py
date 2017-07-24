from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time

hman = HistoManager(True)

runs = [4213,4218,4219,4220,4221,4222,4223] 
for run in runs: hman.load("../data/AutoTrigAna_%i.root"%run,"%i_"%run)


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
hman.setTitle("myrate_graphAxis","Auto-trigger Runs")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("myrate","")
hman.drawGraph("myrate","AP",markerType=20,min=30,max=40)

hman.ps("bg_grass_time.eps")

raw_input()

time1,time2,rate = Double(),Double(),Double()
hman["%s_S1Rate"%runs[0]].GetPoint(0,time1,rate)
hman["%s_S1Rate"%runs[-1]].GetPoint(0,time2,rate)
hman.graph("Axis",[time1,time2],[0,0],0,0)
hman["Axis_graphAxis"].GetXaxis().SetTimeDisplay(1);
hman["Axis_graphAxis"].GetXaxis().SetTimeFormat("%H:%M");
hman.axis("Axis_graphAxis","Time","e^{-} grass rate (ms^{-1})")
hman.setTitle("Axis_graphAxis","Auto-trigger Runs")
hman.style1d()
hman.draw("Axis_graphAxis",max=40,min=30)
for run in runs: hman.drawGraph("%i_S1Rate"%run,"P",markerType=20)

raw_input()

runrates,runerates = [],[]   
for run in runs:
    gr = hman["%s_S1ChRate"%run]
    pmtrates, pmterates=[],[]
    pmts = []
    for i in range(gr.GetN()):
        PMT, rate = Double(),Double()
        gr.GetPoint(i,PMT,rate)
        erate = gr.GetErrorY(i)
        pmtrates.append(rate)
        pmterates.append(erate)
        pmts.append(PMT)
    runrates.append(pmtrates)
    runerates.append(pmterates)

pmtrates = [ [ rates[i] for rates in runrates ] for i in range(len(pmts))]
pmterates = [ [ erates[i] for erates in runerates ] for i in range(len(pmts))]

for pmt,rates,erates in zip(pmts,pmtrates,pmterates):
    gr = "pmtrate_ch%i"%int(pmt)
    hman.graph(gr,[-0.5]+times,[0]+rates,0,[0]+erates)
    hman.axis(gr+"_graphAxis","Time (min)","e^{-} grass rate (ms^{-1})")
    hman.setTitle(gr+"_graphAxis","Channel %i Rate"%int(pmt))
    
    
hman.style1d()
    
for pmt in pmts:
    hman.drawGraph("pmtrate_ch%i"%int(pmt),"AP",markerType=20+i)
    raw_input()

hman.setTitle("pmtrate_ch%i"%int(pmts[0]),"Rate for all PMTs")
hman.drawGraph("pmtrate_ch%i"%int(pmts[0]),"AP",markerType=20,max=6,min=1)
for ch,i in zip(pmts[1:],range(len(pmts[1:]))):
    hman.drawGraph("pmtrate_ch%i"%int(ch),"P",markerType=20+i)
    
    
raw_input()

hman.setCanvasSize(800,500)
hman.zones(3,2)
for run in runs[1:]:
    hname = "%i_S1XYRate"%run
    hman.setTitle(hname,"Run %i"%run)
    hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
    hman.style2d(hname)
    hman.draw(hname,option="colz")
raw_input()
