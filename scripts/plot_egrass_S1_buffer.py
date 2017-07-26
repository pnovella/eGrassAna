from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
alpha runs
"""

runs = [4367,4368,4369,4370,4371,4372,4373,4374,4377,4376,4366]
for run in runs: hman.load("../data/S1GrassAna_%i.root"%run,"%i_"%run)

HVs = [12.8,17.8,23.8]
runs = [4377,4376,4366]

hman.addLegend("4377_aS1DT","Cath. HV = 12.8 kV (4377)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4376_aS1DT","Cath. HV = 17.8 kV (4376)","LF")
hman.addLegendEntry("4366_aS1DT","Cath. HV = 23.8 kV (4366)","LF")

hman.style1d()
hman.setGrid(1,1)
hman.draw("4377_aS1DT","black","red",norm=0)
#raw_input()
hman.draw("4376_aS1DT","black","yellow","same",norm=0)
#raw_input()
hman.draw("4366_aS1DT","black","green","same",norm=0)
raw_input()

hman.cclear()
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
hman.setTitle("AS1Rate_graphAxis","S1 e^{-} grass rate")
hman.axis("AS1Rate_graphAxis","Cathode Voltage (kV)",
          "S1 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS1Rate","APL",markerType=20,lineType=2,min=0,max=400)


raw_input()

hman.graph("PBRate",HVs,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","Background e^{-} grass")
hman.axis("PBRate_graphAxis","Cathode Voltage (kV)",
          "e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("PBRate","APL",markerType=20,lineType=2,min=0,max=100)

raw_input()


ws = []
runs = [4377,4376,4366]
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
hman.graph("AS1Width",HVs,ws,0,0)
hman.setTitle("AS1Width_graphAxis","S1 e^{-} grass width")
hman.axis("AS1Width_graphAxis","Cathode Voltage (kV)",
          "S1 e^{-} grass width (#mus)")
hman.style1d()
hman.drawGraph("AS1Width","APL",markerType=20,lineType=2)
raw_input()




#------------------------------------------------------#
#--------------------  Grass @ gate -------------------#
#------------------------------------------------------#

HVs = [0,1.1,1.6,2.2,2.8]
runs = [4371,4372,4373,4374,4366]

hman.cclear()
hman.setLogy(False)
hman.addLegend("4372_S1sTime","HV = 23.8/1.1 kV (4372)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
# show light generated in the gate when same field as in buffer
hman.draw("4372_S1sTime","black","yellow","")

raw_input()

hman.cclear()
hman.addLegend("4370_S1sTime","HV = 21.0/0.0 kV (4370)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4369_S1sTime","HV = 22.1/1.1 kV (4369)","LF")
hman.addLegendEntry("4368_S1sTime","HV = 22.6/1.6 kV (4368)","LF")
hman.addLegendEntry("4367_S1sTime","HV = 23.2/2.2 kV (4367)","LF")
hman.addLegendEntry("4366_S1sTime","HV = 23.8/2.8 kV (4366)","LF")


hman.draw("4366_S1sTime","black","green",norm=0)
hman.draw("4367_S1sTime","black","aqua","same",lineType=1,norm=0)
hman.draw("4368_S1sTime","black","red","same",lineType=1,norm=0)
hman.draw("4369_S1sTime","black","yellow","same",lineType=1,norm=0)
hman.draw("4370_S1sTime","black","blue","same",lineType=1,norm=0)
raw_input()

