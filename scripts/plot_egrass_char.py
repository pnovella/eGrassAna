from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from ROOT import gStyle,kRed,TF1

hman = HistoManager(True)


#hman.load("../data/GrassChar_AutoTigger_NoHV_NoSiPM.root")
hman.load("../data/GrassChar_AutoTigger_NoHV.root")
hman.load("../data/GrassChar_AutoTigger_HV.root","HV_")
hman.style1d()
hman.statsPanel(0)

hman.setLogy(True)
hman.draw("GrassChar.S1_PMTMult","black","yellow",title=0)
hman.ps("GrassChar.S1_PMTMult.eps")
raw_input()
hman.setLogy(False)
hman["GrassChar.S1_sT"].Rebin(10)
hman.draw("GrassChar.S1_sT","black","yellow",min=0,max=250,title=0)
hman.ps("GrassChar.S1_sT.eps")
raw_input()
hman.setLogy(True)
hman.axisRange("GrassChar.S1_wT",0,0.95,"x")
hman.style1d("GrassChar.S1_wT")
hman.draw("GrassChar.S1_wT","black","yellow",title=0)
hman.ps("GrassChar.S1_wT.eps")
raw_input()
hman.draw("GrassChar.S1_Amp","black","yellow",title=0)
hman.ps("GrassChar.S1_Amp.eps")
raw_input()
hman.draw("GrassChar.S1_DT","black","yellow",title=0)
#hman.ps("GrassChar.S1_DT.eps")
raw_input()
hman.fitPanel(11111)
hman.fit("GrassChar.S1_DT","expo",1,100)
hman["GrassChar.S1_DT_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPos(0.932,0.9)
hman.draw("GrassChar.S1_DT_fit","black","yellow",title=0)
hman.ps("GrassChar.S1_DT_fit.eps")
raw_input()


hman.setLogy(True)
hman.draw("HV_GrassChar.S2_Amp","black","yellow",title=0)
hman.draw("GrassChar.S2_Amp","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_PMTMult.eps")
raw_input()
hman.addLegend("HV_GrassChar.S1_PMTMult","Gate/Cathode HV On","LF",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("GrassChar.S1_PMTMult","Gate/Cathode HV Off","L")
hman.draw("HV_GrassChar.S1_PMTMult","black","yellow",title=0,norm=1)
hman.draw("GrassChar.S1_PMTMult","black","","same",lineType=2,norm=1)
hman.ps("GrassChar.S1_PMTMult_HVvsNoHV.eps")
raw_input()
hman.setLogy(False)
hman["HV_GrassChar.S1_sT"].Rebin(10)
hman.draw("HV_GrassChar.S1_sT","black","yellow",min=0,max=250,title=0)
hman.draw("GrassChar.S1_sT","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_S1_sT.eps")
raw_input()
hman.setLogy(True)
hman.axisRange("HV_GrassChar.S1_wT",0,0.95,"x")
hman.style1d("HV_GrassChar.S1_wT")
hman.draw("HV_GrassChar.S1_wT","black","yellow",title=0)
hman.draw("GrassChar.S1_wT","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_wT.eps")
raw_input()
hman.draw("HV_GrassChar.S1_Amp","black","yellow",title=0)
hman.draw("GrassChar.S1_Amp","black","","same",lineType=2,title=0)
hman.ps("GrassChar.S1_Amp_HVvsNoHV.eps")
raw_input()
hman.addLegend("HV_GrassChar.S1_DT","Gate/Cathode HV On","LF",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("GrassChar.S1_DT","Gate/Cathode HV Off","L")
hman.draw("HV_GrassChar.S1_DT","black","yellow",title=0,norm=1)
hman.draw("GrassChar.S1_DT","black","","same",lineType=2,title=0,norm=1)
hman.ps("GrassChar.S1_DT_HVvsNoHV.eps")
raw_input()
hman.cclear()
hman.fitPanel(11111)
hman.fit("HV_GrassChar.S1_DT","expo",9,50)
hman["HV_GrassChar.S1_DT_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPos(0.932,0.9)
hman.draw("HV_GrassChar.S1_DT_fit","black","yellow",title=0)
#hman.ps("GrassChar.S1_DT_fit.eps")
raw_input()

hman.subHistos("HV_GrassChar.S1_Amp","GrassChar.S1_Amp",
               "SE_Amp")

hman.setLogy(True)
#hman.draw("SE_Amp","black","yellow")
#hman.drawLine(0,0,20,0,"same",lineType=2)
#raw_input()

ffunc = TF1("f","gaus(0)+gaus(3)",0,6)
ffunc.SetParameter(0,500)
ffunc.SetParameter(1,1.3)
ffunc.SetParameter(2,0.5)
ffunc.SetParameter(3,200)
ffunc.SetParameter(4,2.5)
ffunc.SetParameter(5,0.5)

hman.fit("SE_Amp","f",0.5,3,"SE_Amp_fit")
hman["SE_Amp_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw("SE_Amp_fit","black","yellow",lineType=1,title=0)
hman.drawLine(0,0,20,0,"same",lineType=2)
raw_input()




