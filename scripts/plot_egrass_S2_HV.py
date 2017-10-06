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
hman.setTitle("AS2Rate","")
hman.drawGraph("AS2Rate","APL",markerType=20,lineType=2,min=50,max=200)

hman.ps("s2_grass_alpha_HV.eps")

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
        rates.append(rate-pbrate)
        erates.append(sqrt(erate**2+pberate**2))
        
    hman.graph("%i_AS2ChRate"%run,pmts,rates,0,erates)
    hman.setTitle("%i_AS2ChRate"%run,"")
    hman.axis("%i_AS2ChRate_graphAxis"%run,
              "Run Number","S2 e^{-} grass rate (ms^{-1})")
    hman.style1d()
    hman.drawGraph("%i_AS2ChRate"%run,"AP",markerType=20)
    #hman.ps("s2_grass_%i_ch.eps"%run)
    raw_input()
    hman.subHistos("%i_S1AS2XYRate"%run,"%i_S1PBXYRate"%run,"%i_XYRate"%run)
    hman.draw("%i_XYRate"%run,option="colz",title=0)
    #hman.ps("s2_grass_%i_xy.eps"%run)
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

#------------------- gate HV: S1 trigger ------------------#


runs = [4475,4461,4462,4476]
for run in runs:
    hman.load("../data/S2GrassS1TrigAna_%i.root"%run,"%i_"%run)

#hman.draw("4476_S1DT","black","yellow")
#hman.draw("4462_S1DT","black","","",lineType=1)
#hman.draw("4461_S1DT","black","","same",lineType=2)
#hman.draw("4475_S1DT","black","","same",lineType=4)
#raw_input()

HVs = [2.3,2.5,2.7,2.8]
ngs,engs = [],[]
rs,ers = [],[]
for run in runs:
    ngs.append(hman["%i_GM"%run].GetMean())
    engs.append(hman["%i_GM"%run].GetRMS())
    rs.append(ngs[-1]/400*1000)
    ers.append(engs[-1]/400*1000)
    
    
hman.graph("NG",HVs,ngs,0,engs)
hman.axis("NG_graphAxis","Gate HV (kV)","Number of grass signals / #alpha")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("NG","")
hman.drawGraph("NG","AP",markerType=20,min=0)
hman.ps("s2_grass_mult_HV.eps")
raw_input()

hman.graph("GR",HVs,rs,0,ers)
hman.axis("GR_graphAxis","Gate HV (kV)","S2 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("GR","")
hman.drawGraph("GR","AP",markerType=20,min=0)
hman.ps("s2_grass_alpha_gate_HV.eps")
raw_input()
