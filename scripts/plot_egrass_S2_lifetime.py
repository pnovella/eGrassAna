from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

"""
Kr 
Na
Alphas for different drift HV
"""

hman = HistoManager(True)

#---------------------alphas--------------------#

runs = [3879,3875,3880]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)

HVs = [22,15,8]
lts,elts = [],[]

for run in runs:
    hname = "%i_S1sTime"%run
    ofit=hman.fit(hname,"expo(0)+pol0(2)",1500,2700,hname+"_fit")
    hman[hname+"_fit_func"].SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.draw(hname+"_fit","black","yellow")
    lt = abs(1./ofit["parameters"][1])
    elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lts.append(lt)
    elts.append(elt)
    raw_input()

hman.graph("LT",HVs,lts,0,elts)
hman.axis("LT_graphAxis","Cathode Voltage (kV)","S2 e- grass lifetime (#mus)")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("LT","AP",markerType=20)
raw_input()

#--------------------- kr --------------------#

runs = [3360,3389,3614]
frs = [(1400,3200),(750,1200),(900,1200)]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)

lts,elts = [],[]

for run,fr in zip(runs,frs):
    hname = "%i_S1sTime"%run#
    ofit=hman.fit(hname,"expo(0)+pol0(2)",fr[0],fr[1],hname+"_fit")
    hman[hname+"_fit_func"].SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.draw(hname+"_fit","black","yellow")
    lt = abs(1./ofit["parameters"][1])
    elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lts.append(lt)
    elts.append(elt)
    raw_input()

hman.graph("LT2",runs,lts,0,elts)
hman.axis("LT2_graphAxis","Run Number","S2 e- grass lifetime (#mus)")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("LT2","AP",markerType=20,min=300,max=600)
hman.addText(3350,500,"Kr (3.2 ms)",color="blue",size=0.03)
hman.addText(3400,420,"Kr (1.2 ms)",color="blue",size=0.03)
hman.addText(3550,460,"Na (1.2 ms)",color="blue",size=0.03)
raw_input()
