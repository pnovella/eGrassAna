
from ROOT import gStyle,kRed,Double,TDatime,TF1
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
S1-trigger  alpha runs

"""
hman.load("../data/S1GrassAna_4442.root","NoSIPM_")

hman.style1d()

hname = "NoSIPM_aS1DT"
#ofit=hman.fit(hname,"expo(0)+pol0(2)",fr,700,hname+"_fit")
#ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)+pol0(2)",30,400)
#ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)",50,200)
ffunc = TF1("ffunc","expo",50,200)
#ffunc = TF1("ffunc","[0]*exp(-x/[1])+pol0(2)",30,400)
#ffunc.SetParameter(1,10)

r1,r2 = 250,700

ofit=hman.fit(hname,"ffunc",r1,r2,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw(hname+"_fit","black","yellow",lineType=1,title=0)

raw_input()

hman.load("../data/S1GrassAna_4442_Emin2500_Emax3000.root","NoSIPM_E3_")
hman.load("../data/S1GrassAna_4442_Emin3000_Emax3500.root","NoSIPM_E4_")
hman.load("../data/S1GrassAna_4442_Emin3500_Emax4000.root","NoSIPM_E5_")

hman.sumw2()
hman.addHistos("NoSIPM_E3_aS1DT","NoSIPM_E4_aS1DT","NoSIPM_HE_aS1DT")
hman.addHistos("NoSIPM_HE_aS1DT","NoSIPM_E5_aS1DT","NoSIPM_HE_aS1DT")

#hman.axisRange("NoSIPM_HE_aS1DTn",0,150,"x")

hman.style1d()
hman.draw("NoSIPM_HE_aS1DT","black","yellow","",lineType=1,norm=0)

raw_input()

hman.cclear()
hman.setLogy(False)

hname = "NoSIPM_HE_aS1DT"
ofit=hman.fit(hname,"ffunc",r1,r2,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw(hname+"_fit","black","yellow",lineType=1,title=0)
    
raw_input()


