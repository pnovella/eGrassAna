from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
S1-trigger  alpha runs

"""
hman.load("../data/S1GrassAna_4443_cathode.root","Cath_")
hman.load("../data/S1GrassAna_4443_buffer.root","Buff_")
hman.load("../data/S1GrassAna_4443_active.root","Act_")

hman.load("../data/S1GrassAna_4376_cathode.root","Cath2_")
hman.load("../data/S1GrassAna_4376_buffer.root","Buff2_")
hman.load("../data/S1GrassAna_4376_active.root","Act2_")

hman.style1d()

hman.addLegend("Act_aS1sTime","Active (4443)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("Buff_aS1sTime","Buffer (4443)","LF")
hman.addLegendEntry("Cath_aS1sTime","Cathode (4443)","LF")


hman.draw("Act_aS1sTime","black","yellow")
hman.draw("Buff_aS1sTime","blue","","same",lineType=2)
hman.draw("Cath_aS1sTime","red","","same",lineType=2)

raw_input()

hman.axis("Act_aS1Charge","S1 Charge (PE)","A. U.")
hman.style1d("Act_aS1Charge")
hman.draw("Act_aS1Charge","black","yellow",norm=1,title=0)
hman.draw("Buff_aS1Charge","blue","","same",lineType=2,norm=1)
hman.draw("Cath_aS1Charge","red","","same",lineType=2,norm=1)
hman.ps("aS1Charge.eps")
raw_input()

nalphaAct = hman.integral("Act_aS1sTime")
nalphaBuff = hman.integral("Buff_aS1sTime")
nalphaCath = hman.integral("Cath_aS1sTime")
hman.scale("Act_aS1DT",1./nalphaAct,"Act_aS1DTn")
hman.scale("Buff_aS1DT",1./nalphaBuff,"Buff_aS1DTn")
hman.scale("Cath_aS1DT",1./nalphaCath,"Cath_aS1DTn")

for lbl in ["Act","Buff","Cath"]:
    hman.axisRange("%s_aS1DTn"%lbl,0,150,"x")
    hman.axis("%s_aS1DTn"%lbl,"#DeltaT_{S1-G} (#mus)","Entries/#alpha")
    hman.style1d("%s_aS1DTn"%lbl)

hman.draw("Act_aS1DTn","black","yellow",norm=0,title=0,max=1.4)
hman.draw("Buff_aS1DTn","blue","","same",lineType=2,norm=0)
hman.draw("Cath_aS1DTn","red","","same",lineType=2,norm=0)
hman.ps("aS1DT.eps")

raw_input()

nalphaAct = hman.integral("Act2_aS1sTime")
nalphaABuff = hman.integral("Buff2_aS1sTime")
nalphaCath = hman.integral("Cath2_aS1sTime")
hman.scale("Act2_aS1DT",1./nalphaAct,"Act2_aS1DTn")
hman.scale("Buff2_aS1DT",1./nalphaBuff,"Buff2_aS1DTn")
hman.scale("Cath2_aS1DT",1./nalphaCath,"Cath2_aS1DTn")

hman.addLegend("Act_aS1DTn","Active HV=23.8/2.8 (4443)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("Act2_aS1DTn","Active HV=17.8/2.8 (4376)","LF")

hman.draw("Act_aS1DTn","black","yellow",lineType=1,title=0)
hman.draw("Act2_aS1DTn","black","","same",lineType=2)

hman.ps("aS1DT_Active.eps")

raw_input()

hman.addLegend("Buff_aS1DTn","Buffer HV=23.8/2.8 (4443)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("Buff2_aS1DTn","Buffer HV=17.8/2.8 (4376)","LF")

hman.draw("Buff_aS1DTn","black","yellow",lineType=1,title=0)
hman.draw("Buff2_aS1DTn","black","","same",lineType=2)
hman.ps("aS1DT_Buffer.eps")

raw_input()

hman.addLegend("Cath_aS1DTn","Cathode HV=23.8/2.8 (4443)","LF",
               x0=0.4,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("Cath2_aS1DTn","Cathode HV=17.8/2.8 (4376)","LF")

hman.draw("Cath_aS1DTn","black","yellow",lineType=1,max=2.0,title=0)
hman.draw("Cath2_aS1DTn","black","","same",lineType=2)
hman.ps("aS1DT_Cathode.eps")

raw_input()
#hman.draw("Cath_aS1Charge","black","yellow",lineType=1)
#hman.draw("Cath2_aS1Charge","black","","same",lineType=2)
#raw_input()
