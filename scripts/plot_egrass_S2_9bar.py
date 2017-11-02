from ROOT import gStyle,kRed,Double,TDatime,TGaxis
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

"""
Kr @ 9 bar for different gate HV
"""

hman = HistoManager(True)


#--------------------- 7 bar vs 9 bar (28/7 kV) --------------------#

runs = [4743,4746]
frs = [(200,650),(200,650)]
bars = [7.2,9.1]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)
hman.load("../data/S2GrassAna_3389.root","3389_")


#--------------------- S2-grass rate --------------------#

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

    
hman.graph("AS2Rate",bars,rates,0,erates)
hman.setTitle("AS2Rate_graphAxis","Auto-trigger Runs")
hman.axis("AS2Rate_graphAxis","Pressure (bar)","S2 e^{-} grass rate (ms^{-1})")
hman.setTitle("AS2Rate","")
hman.graph("PBRate",bars,pbrates,0,pberates)
hman.setTitle("PBRate_graphAxis","Auto-trigger Runs")
hman.axis("PBRate_graphAxis","Run Number","e^{-} grass rate (ms^{-1})")

hman.addLegend("AS2Rate","S2-induced grass","PL",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("PBRate","Ambient grass","P")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS2Rate","APL",markerType=20,lineType=2,min=0,max=120)
hman.drawGraph("PBRate","P",markerType=24,lineType=1,min=0,max=100)

hman.ps("s2_grass_kr_rate_9bar.eps")

raw_input()

#--------------------- S2-grass lifetime --------------------#

hman.cclear()

hname = "3389_S1DT"
ofit=hman.fit(hname,"expo(0)+pol0(2)",100,500,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])*microsecond/millisecond
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
elt *= microsecond/millisecond
hman.graph("LT7",[7.2],[lt],0,[elt])
hman.graph("LT7g",[7.0],[lt],0,[elt])

lts,elts = [],[]
lts2,elts2 = [],[]
for run,fr in zip(runs,frs):
    hname = "%i_S1DT"%run#
    ofit=hman.fit(hname,"expo(0)+pol0(2)",fr[0],fr[1],hname+"_fit")
    ofit2=hman.fit(hname,"expo(0)",fr[0],fr[1],hname+"_fit2")
    hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.statsPos(0.9,0.9,w=.18)
    hman.draw(hname+"_fit","black","yellow")
    lt = abs(1./ofit["parameters"][1])
    elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lts.append(lt*microsecond/millisecond)
    elts.append(elt*microsecond/millisecond)
    lt2 = abs(1./ofit2["parameters"][1])
    elt2 = sqrt( ((1./ofit2["parameters"][1]**2)*ofit2["errors"][1])**2)
    lts2.append(lt2)
    elts2.append(elt2)
    
    raw_input()

#TGaxis.SetMaxDigits(3);

hman.graph("LTe",bars,lts2,0,elts2)
hman.graph("LT",bars,lts,0,elts)
hman.axis("LT_graphAxis","Pressure (bar)","S2 e- grass lifetime (ms)")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("LT","")

hman.addLegend("LT","Run 4743/4746","P",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("LT7","Run 3389","P")
#hman.addLegendEntry("LTe","Run 4743/4746 exp fit","P")
hman.drawGraph("LT","AP",markerType=20,min=0,max=3)
#hman.drawGraph("LTe","P",markerType=26,min=0,max=3000)
hman.drawGraph("LT7","P",markerType=24)

hman.ps("s2_grass_kr_ltime_9bar.eps")

raw_input()

hman.cclear()

#--------------------- 7 bar vs 9 bar (28/7 kV) --------------------#

runs = [4778,4779,4782,4780,4774]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)
hvs = [6.0,6.5,7.0,7.5,8.5]
frs = [(150,650),(150,650),(150,650),(150,650),(150,650)]
lts,elts = [],[]

for run,fr in zip(runs,frs):
    hname = "%i_S1DT"%run#
    ofit=hman.fit(hname,"expo(0)+pol0(2)",fr[0],fr[1],hname+"_fit")
    hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.statsPos(0.9,0.9,w=.18)
    hman.draw(hname+"_fit","black","yellow")
    lt = abs(1./ofit["parameters"][1])
    elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lts.append(lt*microsecond/millisecond)
    elts.append(elt*microsecond/millisecond)
    raw_input()

hman.graph("LT",hvs,lts,0,elts)
hman.axis("LT_graphAxis","Gate HV (kV)","S2 e- grass lifetime (ms)")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("LT","")

hman.addLegend("LT","9 bar (4774/82)","P",
               x0=0.63,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("LT7","7 bar (3389)","P")
hman.drawGraph("LT","AP",markerType=20,min=0,max=2.0)
hman.drawGraph("LT7g","P",markerType=24)

hman.ps("s2_grass_kr_ltime_gate.eps")

raw_input()
