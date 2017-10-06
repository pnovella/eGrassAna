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

runs = [3389,3614]
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

    

hman.graph("AS2Rate",runs,rates,0,erates)
hman.setTitle("AS2Rate_graphAxis","Auto-trigger Runs")
hman.axis("AS2Rate_graphAxis","Run Number","S2 e^{-} grass rate (ms^{-1})")
hman.setTitle("AS2Rate","")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS2Rate","APL",markerType=20,lineType=2,min=0,max=500)
hman.addText(3380,100,"^{83}Kr",color="red",size=0.03)
hman.addText(3610,350,"^{22}Na",color="red",size=0.03)

hman.ps("s2_grass_kr_na.eps")

raw_input()

hman.graph("PBRate",runs,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","Auto-trigger Runs")
hman.axis("PBRate_graphAxis","Run Number","e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("PBRate","APL",markerType=20,lineType=2,min=0,max=100)
hman.addText(3380,50,"^{83}Kr",color="red",size=0.03)
hman.addText(3610,50,"^{22}Na",color="red",size=0.03)

raw_input()


for run in runs:
    rates,erates = [],[]
    pbrates,pberates = [],[]
    pmts=[]
    for i in range(11):
        pmt,pbrate = Double(),Double()
        hman["%s_S1PBChRate"%run].GetPoint(i,pmt,pbrate)
        pberate = hman["%s_S1PBChRate"%run].GetErrorY(0)
        pbrates.append(pbrate)
        pberates.append(pberate)
        pmts.append(pmt)
        
        pmt,rate = Double(),Double()
        hman["%s_S1AS2ChRate"%run].GetPoint(i,pmt,rate)
        erate = hman["%s_S1AS2ChRate"%run].GetErrorY(0)
        print rate, pbrate
        rates.append(rate-pbrate)
        erates.append(sqrt(erate**2+pberate**2))

    print sum(pbrates)
        
    hman.graph("%i_AS2ChRate"%run,pmts,rates,0,erates)
    hman.setTitle("%i_AS2ChRate"%run,"")
    hman.axis("%i_AS2ChRate_graphAxis"%run,
              "PMT Number","S2 e^{-} grass rate (ms^{-1})")
    hman.style1d()
    hman.drawGraph("%i_AS2ChRate"%run,"AP",markerType=20)
    hman.ps("s2_grass_%i_ch.eps"%run)
    raw_input()
    hman.subHistos("%i_S1AS2XYRate"%run,"%i_S1PBXYRate"%run,"%i_XYRate"%run)
    hman.draw("%i_XYRate"%run,option="colz",title=0)
    hman.ps("s2_grass_%i_xy.eps"%run)
    raw_input()
    
for run in runs:
    hman.setTitle("%i_S1AS2ChRate"%run,"")
    hman.drawGraph("%i_S1AS2ChRate"%run,"AP",markerType=20)
    raw_input()
    hman.draw("%i_S1AS2XYRate"%run,option="colz")
    raw_input()


# for run in runs:
#     hman.drawGraph("%i_S1PBChRate"%run,"AP")    
#     raw_input()
#     hman.drawGraph("%i_S1PBXYRate"%run,option="colz")
#     raw_input()


