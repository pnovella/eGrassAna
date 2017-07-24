from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time

hman = HistoManager(True)

runs = [4001,4003,4004,4005,4006,4008,4010,4011,4012,4013,4014,4015,4016,
        4018,4019,4020]

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
hman.setTitle("myrate","")
hman.drawGraph("myrate","APL",markerType=20,min=0,max=300)
hman.drawLine(4009,0,4009,300,lineType=2,lineColor="blue")
hman.addText(4008,180,"Vacuum in PMT volume",color="blue",size=0.02,rotate=90)
hman.addText(4010,250,"Nitrogen in PMT volume",color="blue",size=0.02,rotate=-90)
hman.addText(4003,260,"^{56}Co in axial port",color="red",size=0.02)
hman.addText(4011,130,"^{56}Co in lateral port",color="red",size=0.02)
hman.addText(4013,260,"^{56}Co in axial port",color="red",size=0.02)
hman.addText(4019,20,"Gate HV Off",color="blue",size=0.02)

hman.ps("bg_grass_co.eps")

raw_input()

hman.addLegend("4012_S1ChRate","No Co source","P",
               x0=0.5,y0=0.8,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4013_S1ChRate","Co in axial port","P")
hman.setGrid(1,1)
hman.setTitle("4013_S1ChRate","")
hman.axis("4013_S1ChRate_graphAxis","PMT Channel","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.draw("4013_S1ChRate_graphAxis",max=60,min=0,title=0)
hman.drawGraph("4013_S1ChRate","P",markerType=20)
hman.drawGraph("4012_S1ChRate","P",markerType=24)
hman.addText(17,35,"Central PMTs",color="red",size=0.025)

hman.ps("bg_grass_co_ch.eps")

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
    hman.graph(gr,runs,rates,0,erates)
    hman.axis(gr+"_graphAxis","Run Nuber","e^{-} grass rate (ms^{-1})")
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

hman.setCanvasSize(1000,500)
hman.zones(2,1)
hname = "4012_S1XYRate"
hman.setTitle(hname,"Run 4012")
hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
hman.style2d(hname)
hman.draw(hname,option="colz")
hname = "4013_S1XYRate"
hman.setTitle(hname,"Run 4013")
hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
hman.style2d(hname)
hman.draw(hname,option="colz")
raw_input()

hman.setCanvasSize(900,500)
hman.zones(6,3)
for run in runs:
    hname = "%i_S1XYRate"%run
    hman.setTitle(hname,"Run %i"%run)
    hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
    hman.style2d(hname)
    hman.draw(hname,option="colz")
raw_input()
