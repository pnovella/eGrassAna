from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time

hman = HistoManager(True)

runs = [4212,4213,4218,4223,4224,4237,4238,4239,4261]

for run in runs: hman.load("../data/AutoTrigAna_%i.root"%run,"%i_"%run)

rates,erates = [],[]
for run in runs:
    rtime,rate = Double(),Double()
    hman["%s_S1Rate"%run].GetPoint(0,rtime,rate)
    erate = hman["%s_S1Rate"%run].GetErrorY(0)
    rates.append(rate)
    erates.append(erate)
    
hman.graph("Rate",runs,rates,0,erates)
hman.setTitle("Rate","")
hman.setTitle("Rate_graphAxis","Auto-trigger Runs")
hman.axis("Rate_graphAxis","Run Number","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.setLogy(1)
hman.drawGraph("Rate","APL",markerType=20,min=10,max=1000)
hman.drawLine(4212.5,10,4212.5,1000,lineType=2,lineColor="blue")
hman.addText(4213,250,"HV Off",color="blue",size=0.02,rotate=-90)
hman.drawLine(4223.5,10,4223.5,1000,lineType=2,lineColor="blue")
hman.addText(4224,250,"HV On",color="blue",size=0.02,rotate=-90)
hman.drawLine(4235,10,4235,1000,lineType=2,lineColor="blue")
hman.addText(4236,250,"HV Off",color="blue",size=0.02,rotate=-90)
hman.drawLine(4241,10,4241,1000,lineType=2,lineColor="blue")
hman.addText(4242,250,"HV On",color="blue",size=0.02,rotate=-90)
hman.addText(4239,650,"Na axial port w/o shielding",color="red",size=0.025)
hman.addText(4250,60,"Na axial port w/ shielding",color="red",size=0.025)

hman.ps("bg_grass_na.eps")

raw_input()
hman.addLegend("4237_S1ChRate","No Na source","P",
               x0=0.45,y0=0.35,x1=0.933,y1=0.5,tsize=0.03)
hman.addLegendEntry("4238_S1ChRate","Na source w/o shielding","P")
hman.setGrid(1,1)

hman.setTitle("4237_S1ChRate_graphAxis","")
hman.axis("4237_S1ChRate_graphAxis","PMT Channel","e^{-} grass rate (ms^{-1})")
hman.style1d("4237_S1ChRate_graphAxis")
hman.draw("4237_S1ChRate_graphAxis",max=300)
hman.drawGraph("4237_S1ChRate","P",markerType=24,max=300)
hman.drawGraph("4238_S1ChRate","P",markerType=20)
hman.addText(17,120,"Central PMTs",color="red",size=0.025)
#hman.ps("egrass_rate_autotrigger_ch.eps")

hman.ps("bg_grass_na_ch.eps")

raw_input()


hman.setCanvasSize(1000,500)
hman.zones(3,1)
hname = "4237_S1XYRate"
hman.setTitle(hname,"Run 4237")
hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
hman.style2d(hname)
hman.draw(hname,option="colz")
hname = "4238_S1XYRate"
hman.setTitle(hname,"Run 4238")
hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
hman.style2d(hname)
hman.draw(hname,option="colz")
hname = "4261_S1XYRate"
hman.setTitle(hname,"Run 4261")
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
