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
    hname = "%i_S1DT"%run
    ofit=hman.fit(hname,"expo(0)+pol0(2)",200,1600,hname+"_fit")
    #hman[hname+"_fit_func"].SetLineColor(kRed)
    hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.statsPos(0.9,0.9,w=.18)
    hman.draw(hname+"_fit","black","yellow",title=0)
    lt = abs(1./ofit["parameters"][1])
    elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lts.append(lt)
    elts.append(elt)
    raw_input()

hman.setGrid(1,1)
hman.draw("3879_S1DT_fit","black","yellow",title=0)
hman.ps("s2_grass_alpha_ltime_fit.eps")
raw_input()

hman.graph("LT",HVs,lts,0,elts)
hman.axis("LT_graphAxis","Cathode Voltage (kV)","S2 e- grass lifetime (#mus)")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("LT","")
hman.drawGraph("LT","AP",markerType=20,max=700,min=500)

hman.ps("s2_grass_alpha_ltime.eps")

raw_input()

#--------------------- kr and na --------------------#

runs = [3360,3389,3614]
frs = [(100,1800),(100,500),(240,500)]
for run in runs: hman.load("../data/S2GrassAna_%i.root"%run,"%i_"%run)

lts,elts = [],[]

for run,fr in zip(runs,frs):
    hname = "%i_S1DT"%run#
    ofit=hman.fit(hname,"expo(0)+pol0(2)",fr[0],fr[1],hname+"_fit")
    #hman[hname+"_fit_func"].SetLineColor(kRed)
    hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.statsPos(0.9,0.9,w=.18)
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
hman.setTitle("LT2","")
hman.drawGraph("LT2","AP",markerType=20,min=300,max=600)
hman.addText(3350,500,"Kr (3.2 ms)",color="blue",size=0.03)
hman.addText(3400,420,"Kr (1.2 ms)",color="blue",size=0.03)
hman.addText(3550,460,"Na (1.2 ms)",color="blue",size=0.03)

hman.ps("s2_grass_kr_na_ltime.eps")

raw_input()

#---------------------S1-trigger alphas--------------------#

runs = [4366,4367,4461,4462,4475,4476]
for run in runs:
    hman.load("../data/S2GrassS1TrigAna_%i.root"%run,"%i_"%run)



hman.draw("4476_S2Charge","black","yellow")
hman.draw("4462_S2Charge","black","","same",lineType=1)
hman.draw("4461_S2Charge","black","","same",lineType=2)
hman.draw("4475_S2Charge","black","","same",lineType=4)
raw_input()
#hman.draw("4476_S2Width","black","yellow")
#hman.draw("4462_S2Width","black","","same",lineType=1)
#hman.draw("4461_S2Width","black","","same",lineType=2)
#hman.draw("4475_S2Width","black","","same",lineType=4)
#raw_input()
#hman.draw("4476_S2sTime","black","yellow")
#hman.draw("4462_S2sTime","black","","same",lineType=1)
# hman.draw("4461_S2sTime","black","","same",lineType=2)
# hman.draw("4475_S2sTime","black","","same",lineType=4)
# raw_input()

#hman.draw("4476_S1DT","black","yellow")
#hman.draw("4462_S1DT","black","","same",lineType=1)
#hman.draw("4461_S1DT","black","","same",lineType=2)
#hman.draw("4475_S1DT","black","","same",lineType=4)
#raw_input()


lts0,elts0 = [],[]
lts,elts = [],[]

hname="3360_S1sTime" # 7.0 kV
ofit=hman.fit(hname,"expo(0)",1190,1400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()

hname="4476_S1DT" # 2.8 kV
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
###lts.append(lt)
###elts.append(elt)
raw_input()
hname="4462_S1DT" # 2.7 kV
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()
hname="4461_S1DT" # 2.5 kV
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()
hname="4475_S1DT" # 2.3 kV
#hman[hname].Rebin(2)
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()

hname="4367_S1DT"# 2.2 kV
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()

hname="4366_S1DT"# 2.8 kV
ofit=hman.fit(hname,"expo(0)",190,400,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.draw(hname+"_fit","black","yellow")
lt = abs(1./ofit["parameters"][1])
elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
lts.append(lt)
elts.append(elt)
raw_input()

hvs = [7.0,2.7,2.5,2.3,2.2,2.8]
hman.graph("LT3",hvs,lts,0,elts)
hman.axis("LT3_graphAxis","Gate HV (kV)","S2 e- grass lifetime (#mus)")
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("LT3","")

hman.drawGraph("LT3","AP",markerType=20)
raw_input()

