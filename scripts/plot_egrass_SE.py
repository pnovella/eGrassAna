from ROOT import gStyle,kRed,TF1
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
S1-trigger  alpha runs

"""
hman.load("../jobOptions/SingleElecSignal_HV.root","HV_")
hman.load("../jobOptions/SingleElecSignal_NoHV.root","NoHV_")

hman.style1d()

hman.setLogy(True)
hman.draw("HV_SingleElecSignal.SE_Amp","black","yellow")
hman.draw("NoHV_SingleElecSignal.SE_Amp","black","","same",lineType=2)

raw_input()

hman.sumw2()
hman.scale("NoHV_SingleElecSignal.SE_Amp",1./3500,"NoHV_SE_Amp")
hman.scale("HV_SingleElecSignal.SE_Amp",1./500,"HV_SE_Amp")

hman.subHistos("HV_SE_Amp","NoHV_SE_Amp","SE_Amp")

hman.setLogy(False)
hman.draw("SE_Amp","black","yellow")
hman.drawLine(0,0,20,0,"same",lineType=2)
raw_input()

ffunc = TF1("f","gaus(0)+gaus(3)",0,6)
ffunc.SetParameter(0,500)
ffunc.SetParameter(1,2.5)
ffunc.SetParameter(2,0.5)
ffunc.SetParameter(3,200)
ffunc.SetParameter(4,3.8)
ffunc.SetParameter(5,0.5)

hman.fit("SE_Amp","f",0,5.5,"SE_Amp_fit")
hman["SE_Amp_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw("SE_Amp_fit","black","yellow",lineType=1,title=0)
raw_input()


