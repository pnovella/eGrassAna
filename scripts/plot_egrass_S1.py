from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
alpha runs
"""

HVs = [15,22,24]
runs = [3875,3879,4356]
for run in runs: hman.load("../data/S1GrassAna_%i.root"%run,"%i_"%run)

hman.style1d()
hman.draw("3879_S1sTime","black","yellow")

raw_input()

rates,erates = [],[]
pbrates,pberates = [],[]
for run in runs:

    time,pbrate = Double(),Double()
    hman["%s_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_S1PBRate"%run].GetErrorY(0)
    pbrates.append(pbrate)
    pberates.append(pberate)
    
    time,rate = Double(),Double()
    hman["%s_S1AS1Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_S1AS1Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))


hman.graph("AS1Rate",HVs,rates,0,erates)
hman.setTitle("AS1Rate_graphAxis","Auto-trigger Runs")
hman.axis("AS1Rate_graphAxis","Cathode Voltage (kV)",
          "S1 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS1Rate","APL",markerType=20,lineType=2,min=0,max=700)


raw_input()

hman.graph("PBRate",HVs,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","Auto-trigger Runs")
hman.axis("PBRate_graphAxis","Cathode Voltage (kV)",
          "e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("PBRate","APL",markerType=20,lineType=2,min=0,max=300)

raw_input()

hman.draw("4356_aS1DT","black","yellow",norm=1)
hman.draw("3879_aS1DT","blue","","same",lineType=2,norm=1)
hman.draw("3875_aS1DT","red","","same",lineType=3,norm=1)
raw_input()

hman.load("../data/S1GrassAna_4155.root","4155_")
hman.draw("4356_aS1DT","black","yellow",norm=1)
hman.draw("4155_aS1DT","red","","same",lineType=2,norm=1)
raw_input()

ws = []
runs = [3875,3879,4155,4356]
nbg = 20
bl = 13 
for run in runs:
    cont = hman.getContents("%i_aS1DT"%run)
    bg = sum(cont[-nbg:])/nbg
    for i,c in zip(range(len(cont)-1),cont[1:]):
        if c<bg:
            ws.append(i)
            break
print ws
vds = [ 13./w for w in ws ]
print vds
raw_input()

#------------------- Bulk Alphas ------------------#

HVs = [15,22]
runs = [3875,3879]
for run in runs: hman.load("../data/S1GrassAna_%i_BulkAlphas.root"%run,
                           "%i_B_"%run)


hman.addLegend("3879_B_aS1DT","Cathode HV = 22 kV (3879)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("3875_B_aS1DT","Cathode HV = 15 kV (3879)","LF")

hman.draw("3879_B_aS1DT","black","yellow",norm=1)
hman.draw("3875_B_aS1DT","black","","same",lineType=3,norm=1)
raw_input()


#------- prove 4mus structure does not depend on cathode HV

hman.cclear()
runs = [3875,3879]
HVs = [15,22]
for run in runs: hman.load("../data/S1GrassAna_%i_Bulk_DTMax6.root"%run,
                           "%i_BDT6_"%run)

rates,erates = [],[]
for run in runs:
    time,pbrate = Double(),Double()
    hman["%s_BDT6_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_BDT6_S1PBRate"%run].GetErrorY(0)
    time,rate = Double(),Double()
    hman["%s_BDT6_S1AS1Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_BDT6_S1AS1Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))

hman.graph("BDT6AS1Rate",HVs,rates,0,erates)
hman.setTitle("BDT6AS1Rate_graphAxis","Auto-trigger Runs")
hman.axis("BDT6AS1Rate_graphAxis","Cathode Voltage (kV)",
          "S1 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("BDT6AS1Rate","AP",markerType=20,lineType=1)
raw_input()

#------- prove 4mus structure does not depend on gate HV

hman.load("../data/S1GrassAna_4371_Bulk_DTMax6.root","4371_BDT6_")
hman.style1d()
hman.draw("3879_BDT6_aS1DT","black","yellow",norm=1)
hman.draw("4371_BDT6_aS1DT","red","","same",lineType=3,norm=1)
raw_input()
# TO DO!!! COmpare consecutive run with s1-trigger!!!!!!

#------- prove no grass for bulk alphas

runs,HVs = [3875,3879],[15,22]
for run in runs: hman.load("../data/S1GrassAna_%i_Bulk_DTMin10.root"%run,
                           "%i_BDTMin10_"%run)

rates,erates = [],[]
for run in runs:

    time,pbrate = Double(),Double()
    hman["%s_BDTMin10_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_BDTMin10_S1PBRate"%run].GetErrorY(0)
    
    time,rate = Double(),Double()
    hman["%s_BDTMin10_S1AS1Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_BDTMin10_S1AS1Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))

print rates, erates
hman.graph("BAS1Rate",HVs,rates,0,erates)
hman.setTitle("BAS1Rate_graphAxis","Auto-trigger Runs")
hman.axis("BAS1Rate_graphAxis","Cathode Voltage (kV)",
          "S1 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("BAS1Rate","APL",markerType=20,lineType=2,min=-30,max=10)
raw_input()


#------- S1 prompt grass vs z
for i in range(1,6):
    hman.load("../data/S1GrassAna_3879_Bulk%i.root"%i,"3879_B%i_"%i)
rates,erates = [],[]
for i in range(1,6):
    time,pbrate = Double(),Double()
    hman["3879_B%i_S1PBRate"%i].GetPoint(0,time,pbrate)
    pberate = hman["3879_B%i_S1PBRate"%i].GetErrorY(0)
    time,rate = Double(),Double()
    hman["3879_B%i_S1AS1Rate"%i].GetPoint(0,time,rate)
    erate = hman["3879_B%i_S1AS1Rate"%i].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))
    
hman.h1("PS1EG","Prompt S1 grass rate; Drift Time (#mus);Rate (ms^{-1})",
        5,30,530)
hman.setContents("PS1EG",rates)
hman.setErrors("PS1EG",erates)
hman.style1d("PS1EG")
hman.draw("PS1EG")
raw_input()
