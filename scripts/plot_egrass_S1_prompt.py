from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
alpha runs
"""

#HVs = [15,22,24]
#runs = [3875,3879,4356]
#for run in runs: hman.load("../data/S1GrassAna_%i.root"%run,"%i_"%run)

# #hman.style1d()
# #hman.draw("3879_S1sTime","black","yellow")

# #raw_input()

# rates,erates = [],[]
# pbrates,pberates = [],[]
# for run in runs:

#     time,pbrate = Double(),Double()
#     hman["%s_S1PBRate"%run].GetPoint(0,time,pbrate)
#     pberate = hman["%s_S1PBRate"%run].GetErrorY(0)
#     pbrates.append(pbrate)
#     pberates.append(pberate)
    
#     time,rate = Double(),Double()
#     hman["%s_S1AS1Rate"%run].GetPoint(0,time,rate)
#     erate = hman["%s_S1AS1Rate"%run].GetErrorY(0)
#     rates.append(rate-pbrate)
#     erates.append(sqrt(erate**2+pberate**2))


# hman.graph("AS1Rate",HVs,rates,0,erates)
# hman.setTitle("AS1Rate_graphAxis","Auto-trigger Runs")
# hman.axis("AS1Rate_graphAxis","Cathode Voltage (kV)",
#           "S1 e^{-} grass rate (ms^{-1})")
# hman.style1d()
# hman.setGrid(1,1)
# hman.drawGraph("AS1Rate","APL",markerType=20,lineType=2,min=0,max=700)


# raw_input()

# hman.graph("PBRate",HVs,pbrates,0,pberates)
# hman.setTitle("PBRate_graphAxis","Auto-trigger Runs")
# hman.axis("PBRate_graphAxis","Cathode Voltage (kV)",
#           "e^{-} grass rate (ms^{-1})")
# hman.style1d()
# hman.setGrid(1,1)
# hman.drawGraph("PBRate","APL",markerType=20,lineType=2,min=0,max=300)

# raw_input()

# hman.draw("4356_aS1DT","black","yellow",norm=1)
# hman.draw("3879_aS1DT","blue","","same",lineType=2,norm=1)
# hman.draw("3875_aS1DT","red","","same",lineType=3,norm=1)
# raw_input()

# hman.load("../data/S1GrassAna_4155.root","4155_")
# hman.draw("4356_aS1DT","black","yellow",norm=1)
# hman.draw("4155_aS1DT","red","","same",lineType=2,norm=1)
# raw_input()

# ws = []
# runs = [3875,3879,4155,4356]
# nbg = 20
# bl = 13 
# for run in runs:
#     cont = hman.getContents("%i_aS1DT"%run)
#     bg = sum(cont[-nbg:])/nbg
#     for i,c in zip(range(len(cont)-1),cont[1:]):
#         if c<bg:
#             ws.append(i)
#             break
# print ws
# vds = [ 13./w for w in ws ]
# print vds
# raw_input()

#------------------------------------------------------#
#-------------------- Prompt S1 Grass -----------------#
#------------------------------------------------------#


#------------------- Bulk Alphas ------------------#

#------- prove 4mus structure is there for bulk alphas

HVs = [15,22]
runs = [3875,3879]
for run in runs:
    hman.load("../data/S1GrassAna_%i_BulkAlphas.root"%run,"%i_B_"%run)
hman.style1d()

for run in runs:
    nalpha = hman.integral("%i_B_aS1sTime"%run)
    hman.scale("%i_B_aS1DT"%run,1./nalpha,"%i_B_aS1DTn"%run)

hman.axisRange("3879_B_aS1DTn",0,25,"x")
hman.axis("3879_B_aS1DTn","#DeltaT_{S1-G}","Entries/#alpha")
hman.style1d("3879_B_aS1DTn")

hman.addLegend("3879_B_aS1DTn","HV = 22.0/2.8 kV (3879)","LF",
               x0=0.45,y0=0.7,x1=0.932,y1=0.9,tsize=0.03)
hman.addLegendEntry("3875_B_aS1DTn","HV = 15.0/2.8 kV (3875)","LF")
hman.setGrid(1,1)
hman.draw("3879_B_aS1DTn","black","yellow",title=0,min=0,max=1.4)
hman.draw("3875_B_aS1DTn","black","","same",lineType=3)

hman.ps("s1_grass_prompt_dt.eps")

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
hman.setTitle("BDT6AS1Rate_graphAxis","")
hman.axis("BDT6AS1Rate_graphAxis","Cathode Voltage (kV)",
          "S1 prompt e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("BDT6AS1Rate","AP",markerType=20,lineType=1,min=500,max=700)

hman.ps("s1_grass_prompt_chv.eps")

raw_input()

#------- prove 4mus structure does not depend on gate HV 

hman.load("../data/S1GrassAna_4371_Bulk_DTMax6.root","4371_BDT6_")
hman.style1d()

hman.draw("3879_BDT6_aS1DT","black","yellow",norm=1)
hman.draw("4371_BDT6_aS1DT","red","","same",lineType=3,norm=1)

raw_input()
# TO DO!!! COmpare consecutive run with s1-trigger!!!!!!

#------- prove 4mus structure does not depend on gate HV (S1-trigger runs)

runs = [4366,4371]
#for run in runs: hman.load("../data/S1GrassAna_%i.root"%run,"%i_"%run)

hman.load("../data/S1GrassAna_4366.root","4366_")
hman.load("../data/S1GrassAna_4371.root","4371_")


#hman.draw("4371_aS1DT")
#raw_input()

for run in runs:
    nalpha = hman.integral("%i_aS1sTime"%run)
    hman.scale("%i_aS1DT"%run,1./nalpha,"%i_aS1DTn"%run)


hman.axisRange("4366_aS1DTn",0,25,"x")
hman.axisRange("4371_aS1DTn",0,25,"x")
hman.axis("4366_aS1DTn","#DeltaT_{S1-G}","Entries / #alpha")
hman.axis("4371_aS1DTn","#DeltaT_{S1-G}","Entries / #alpha")

hman.style1d()

hman.addLegend("4371_aS1DTn","HV = 23.8/0.0 kV (4371)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
#hman.addLegendEntry("4371_aS1DTn","HV = 23.8/0.0 kV (4371)","LF")

# show prmpt gras strucutre is there event when no gate HV
hman.style1d()
hman.setGrid(1,1)
#hman.draw("4366_aS1DTn","black","yellow",title=0)
hman.draw("4371_aS1DTn","black","yellow","",lineType=1,title=0,min=0,max=1.4)

hman.ps("s1_grass_prompt_ghv.eps")

raw_input()

# show prompt grass has larger charge
hman.cclear()
hman.load("../data/S1GrassAna_4371_DTMax6.root","4371_DT6_")
hman.load("../data/S1GrassAna_4371_DTMin10.root","4371_DT10_")
hman.axis("4371_DT6_aS1EGQ","Grass Charge (PE)","A.U.")
hman.style1d("4371_DT6_aS1EGQ")
hman.addLegend("4371_DT6_aS1EGQ","#DeltaT < 6 #mus (4371)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4371_DT10_aS1EGQ","#DeltaT > 10 #mus (4371)","LF")
hman.setLogy(True)
hman.draw("4371_DT6_aS1EGQ","black","yellow",norm=1,title=0)
hman.draw("4371_DT10_aS1EGQ","black","","same",lineType=2,norm=1)

hman.ps("s1_grass_prompt_q.eps")

raw_input()

#------- prove no grass for bulk alphas

# runs,HVs = [3875,3879],[15,22]
# for run in runs: hman.load("../data/S1GrassAna_%i_Bulk_DTMin10.root"%run,
#                            "%i_BDTMin10_"%run)

# rates,erates = [],[]
# for run in runs:

#     time,pbrate = Double(),Double()
#     hman["%s_BDTMin10_S1PBRate"%run].GetPoint(0,time,pbrate)
#     pberate = hman["%s_BDTMin10_S1PBRate"%run].GetErrorY(0)
    
#     time,rate = Double(),Double()
#     hman["%s_BDTMin10_S1AS1Rate"%run].GetPoint(0,time,rate)
#     erate = hman["%s_BDTMin10_S1AS1Rate"%run].GetErrorY(0)
#     rates.append(rate-pbrate)
#     erates.append(sqrt(erate**2+pberate**2))

# print rates, erates
# hman.graph("BAS1Rate",HVs,rates,0,erates)
# hman.setTitle("BAS1Rate_graphAxis","Auto-trigger Runs")
# hman.axis("BAS1Rate_graphAxis","Cathode Voltage (kV)",
#           "S1 e^{-} grass rate (ms^{-1})")
# hman.style1d()
# hman.setGrid(1,1)
# hman.drawGraph("BAS1Rate","APL",markerType=20,lineType=2,min=-30,max=10)
# raw_input()


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
hman.cclear()
hman.setLogy(False)
hman.draw("PS1EG")
raw_input()
