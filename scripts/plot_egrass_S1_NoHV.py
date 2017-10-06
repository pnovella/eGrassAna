
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
hman.load("../data/S1GrassAna_4439.root","SIPM_")
hman.load("../data/S1GrassAna_4442_active.root","NoSIPM_Act_")
hman.load("../data/S1GrassAna_4442_cathode.root","NoSIPM_Cath_")
hman.load("../data/S1GrassAna_4439_cathode.root","SIPM_Cath_")
hman.load("../data/S1GrassAna_4439_active.root","SIPM_Act_")
hman.load("../data/S1GrassAna_4442_active_DTmax6.root","NoSIPM_Act_DTmax6_")
hman.load("../data/S1GrassAna_4442_cathode_DTmax60.root","NoSIPM_Cath_DTmax60_")
hman.style1d()

hman.addLegend("NoSIPM_aS1sTime","HHV Off, SIPM Off (4442)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("SIPM_aS1sTime","HHV Off, SIPM On (4439)","LF")

hman.draw("NoSIPM_aS1sTime","black","yellow")
hman.draw("SIPM_aS1sTime","black","","same",lineType=2)
raw_input()
hman.draw("NoSIPM_aS1Charge","black","yellow",max=250,title=0)
hman.draw("SIPM_aS1Charge","black","","same",lineType=2)
#hman.ps("aS1Charge_NoHV.eps")
raw_input()
hman.draw("SIPM_S1sTime","black","yellow")
hman.draw("NoSIPM_S1sTime","black","","same",lineType=2)
raw_input()

hman.axisRange("SIPM_aS1DT",0,700,"x")
hman.axis("SIPM_aS1DT","#DeltaT_{S1-G} (#mus)","A. U.")
hman.style1d("SIPM_aS1DT")

hman.setLogy(True)
hman.setGrid(1,1)
hman.draw("SIPM_aS1DT","black","yellow",title=0)
hman.draw("NoSIPM_aS1DT","black","","same",lineType=2)
#hman.ps("aS1DT_NoHV.eps")
raw_input()

hman.cclear()

hname = "SIPM_aS1DT"
#ofit=hman.fit(hname,"expo(0)+pol0(2)",fr,700,hname+"_fit")
#ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)+pol0(2)",30,400)
ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)",50,200)
#ffunc = TF1("ffunc","[0]*exp(-x/[1])+pol0(2)",30,400)
ffunc.SetParameter(1,5)
ofit=hman.fit(hname,"ffunc",30,80,hname+"_fit")
hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPanel(0)
hman.fitPanel(1111)
hman.statsPos(0.9,0.9,w=.18)
hman.draw(hname+"_fit","black","yellow",lineType=1,title=0)

raw_input()



#hname = "SIPM_aS1DT"
#ofit=hman.fit(hname,"expo(0)+pol0(2)",30,700,hname+"_fit")
#hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
#hman.statsPanel(0)
#hman.fitPanel(1111)
#hman.statsPos(0.9,0.9,w=.18)
#hman.draw(hname+"_fit","black","yellow",title=0)
#raw_input()

#hman.addLegend("NoSIPM_Act_aS1DT","HHV/SiPM Off, Active (4442)","LF",
               #x0=0.45,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
#hman.addLegendEntry("NoSIPM_Cath_aS1DT","HHV/SiPM Off, Cathode (4442)","LF")

#hman.setGrid(1,1)
#hman.draw("NoSIPM_Act_aS1DT","black","yellow",norm=1)
#hman.draw("NoSIPM_Cath_aS1DT","black","","same",lineType=2,norm=1)
#raw_input()

# hman.setGrid(1,1)
# hman.draw("SIPM_Act_aS1DT","black","yellow",norm=0)
# hman.draw("NoSIPM_Act_aS1DT","black","","same",lineType=2,norm=0)
# raw_input()

# hman.setGrid(1,1)
# hman.draw("SIPM_Cath_aS1DT","black","yellow",norm=0)
# hman.draw("NoSIPM_Cath_aS1DT","black","","same",lineType=2,norm=0)
# raw_input()

#hman.cclear()

#hname = "NoSIPM_Act_aS1DT"
#ofit=hman.fit(hname,"expo(0)+pol0(2)",20,700,hname+"_fit")
#hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
#hman.statsPanel(0)
#hman.fitPanel(1111)
#hman.statsPos(0.9,0.9,w=.18)
#hman.draw(hname+"_fit","black","yellow",title=0)
#raw_input()

#hname = "NoSIPM_Cath_aS1DT"
#ofit=hman.fit(hname,"expo(0)+pol0(2)",30,700,hname+"_fit")
#hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
#hman.statsPanel(0)
#hman.fitPanel(1111)
#hman.statsPos(0.9,0.9,w=.18)
#hman.draw(hname+"_fit","black","yellow",lineType=1,title=0)
#raw_input()

# try to see if grass charge is different for prompt and delayed
#hman.statsPanel(111111)
#hman.draw("NoSIPM_Cath_aS1EGQ","black","yellow",lineType=1,norm=0)
#raw_input()
#hman.draw("NoSIPM_Cath_DTmax60_aS1EGQ","black","yellow",lineType=1,norm=0)
#raw_input()
#hman.draw("NoSIPM_Act_DTmax6_aS1EGQ","black","yellow",lineType=1,norm=0)
#raw_input()

#
hman.load("../data/S1GrassAna_4442_Emin400_Emax1500.root","NoSIPM_E1_")
hman.load("../data/S1GrassAna_4442_Emin1500_Emax2500.root","NoSIPM_E2_")
hman.load("../data/S1GrassAna_4442_Emin2500_Emax3000.root","NoSIPM_E3_")
hman.load("../data/S1GrassAna_4442_Emin3000_Emax3500.root","NoSIPM_E4_")
hman.load("../data/S1GrassAna_4442_Emin3500_Emax4000.root","NoSIPM_E5_")

#hman.sumw2()

nalpha1 = hman.integral("NoSIPM_E1_aS1sTime")
nalpha2 = hman.integral("NoSIPM_E2_aS1sTime")
nalpha3 = hman.integral("NoSIPM_E3_aS1sTime")
nalpha4 = hman.integral("NoSIPM_E4_aS1sTime")
nalpha5 = hman.integral("NoSIPM_E5_aS1sTime")
hman.scale("NoSIPM_E1_aS1DT",1./nalpha1,"NoSIPM_E1_aS1DTn")
hman.scale("NoSIPM_E2_aS1DT",1./nalpha2,"NoSIPM_E2_aS1DTn")
hman.scale("NoSIPM_E3_aS1DT",1./nalpha3,"NoSIPM_E3_aS1DTn")
hman.scale("NoSIPM_E4_aS1DT",1./nalpha4,"NoSIPM_E4_aS1DTn")
hman.scale("NoSIPM_E5_aS1DT",1./nalpha5,"NoSIPM_E5_aS1DTn")

hman.axisRange("NoSIPM_E1_aS1DTn",0,150,"x")

hman.style1d()

hman.addLegend("NoSIPM_E1_aS1DTn","E_{S1}=400-1500 PE","LF",
               x0=0.55,y0=0.65,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("NoSIPM_E2_aS1DTn","E_{S1}=1500-2500 PE","LF")
hman.addLegendEntry("NoSIPM_E3_aS1DTn","E_{S1}=2500-3000 PE","LF")
hman.addLegendEntry("NoSIPM_E4_aS1DTn","E_{S1}=3000-3500 PE","LF")
hman.addLegendEntry("NoSIPM_E5_aS1DTn","E_{S1}=3500-4000 PE","LF")

hman.draw("NoSIPM_E1_aS1DTn","black","yellow","",lineType=1,norm=0)
hman.draw("NoSIPM_E2_aS1DTn","blue","","same",lineType=1,norm=0)
hman.draw("NoSIPM_E3_aS1DTn","green","","same",lineType=1,norm=0)
hman.draw("NoSIPM_E4_aS1DTn","aqua","","same",lineType=1,norm=0)
hman.draw("NoSIPM_E5_aS1DTn","red","","same",lineType=1,norm=0)

#hman.ps("aS1DT_NoHV_Eranges.eps")

raw_input()

hman.cclear()
hman.setLogy(False)

lts,elts,maxs = [],[],[]
frs=[30,30,30,30,30]
for i,fr in zip(range(1,6),frs):
    hname = "NoSIPM_E%i_aS1DT"%i
    #ofit=hman.fit(hname,"expo(0)+pol0(2)",fr,700,hname+"_fit")
    #ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)+pol0(2)",30,400)
    ffunc = TF1("ffunc","[0]/pow(1+x/[1],2)",30,80)
    #ffunc = TF1("ffunc","[0]*exp(-x/[1])+pol0(2)",30,400)
    ffunc.SetParameter(1,5)
    ofit=hman.fit(hname,"ffunc",fr,80,hname+"_fit")
    hman[hname+"_fit"].GetFunction("f").SetLineColor(kRed)
    hman.statsPanel(0)
    hman.fitPanel(1111)
    hman.statsPos(0.9,0.9,w=.18)
    hman.draw(hname+"_fit","black","yellow",lineType=1,title=0)
    #lt = abs(1./ofit["parameters"][1])
    #elt = sqrt( ((1./ofit["parameters"][1]**2)*ofit["errors"][1])**2)
    lt = ofit["parameters"][1]
    elt = ofit["errors"][1]
    lts.append(lt)
    elts.append(elt)
    cnts = hman.getContents(hname)
    maxs.append(list(cnts).index(max(cnts)))
    raw_input()

hman.hr1("LT",";Energy (PE); e^{-} grass lifetime (#mus)",
         [400,1500,2500,3000,3500,4000])
hman.setContents("LT",lts)
hman.setErrors("LT",elts)
hman.style1d()
hman.draw("LT")
#hman.ps("aS1DT_NoHV_Lifetime.eps")
raw_input()



ngrass,engrass=[],[]
ngrass.append(hman.integral("NoSIPM_E1_aS1DTn"))
ngrass.append(hman.integral("NoSIPM_E2_aS1DTn"))
ngrass.append(hman.integral("NoSIPM_E3_aS1DTn"))
ngrass.append(hman.integral("NoSIPM_E4_aS1DTn"))
ngrass.append(hman.integral("NoSIPM_E5_aS1DTn"))

engrass.append(sqrt(hman.integral("NoSIPM_E1_aS1DT"))/nalpha1)
engrass.append(sqrt(hman.integral("NoSIPM_E2_aS1DT"))/nalpha2)
engrass.append(sqrt(hman.integral("NoSIPM_E3_aS1DT"))/nalpha3)
engrass.append(sqrt(hman.integral("NoSIPM_E4_aS1DT"))/nalpha4)
engrass.append(sqrt(hman.integral("NoSIPM_E5_aS1DT"))/nalpha5)

hman.cclear()

hman.hr1("GM",";Energy (PE); Grass Multiplicity / S1_{#alpha}",
         [400,1500,2500,3000,3500,4000])
hman.setContents("GM",ngrass)
hman.setErrors("GM",engrass)
hman.style1d("GM")
hman.draw("GM")
#hman.ps("aS1_grass_multiplicity_NoHHV.eps")
raw_input()

hman.graph("MaxT",[1500,2500,3000,3500,4000],maxs)
hman.axis("MaxT_graphAxis","Energy (PE)"," #DeltaT @ Maximum(#mus)")
hman.style1d()
hman.drawGraph("MaxT","APL",lineType=2,markerType=20)

raw_input()

hman.load("../data/S1GrassAna_4379.root","2.8_")
hman.load("../data/S1GrassAna_4378.root","7.8_")
hman.load("../data/S1GrassAna_4371.root","23.8_")
hman.load("../data/S1GrassAna_4371_cathode.root","23.8c_")
hman.load("../data/S1GrassAna_4370.root","21.0_")

nalpha = hman.integral("SIPM_aS1sTime")
nalpha1 = hman.integral("2.8_aS1sTime")
nalpha2 = hman.integral("7.8_aS1sTime")
nalpha3 = hman.integral("23.8_aS1sTime")
nalpha4 = hman.integral("21.0_aS1sTime")
nalpha5 = hman.integral("23.8c_aS1sTime")
hman.scale("SIPM_aS1DT",1./nalpha,"SIPM_aS1DTn")
hman.scale("2.8_aS1DT",1./nalpha1,"2.8_aS1DTn")
hman.scale("7.8_aS1DT",1./nalpha2,"7.8_aS1DTn")
hman.scale("23.8_aS1DT",1./nalpha3,"23.8_aS1DTn")
hman.scale("21.0_aS1DT",1./nalpha4,"21.0_aS1DTn")
hman.scale("23.8c_aS1DT",1./nalpha5,"23.8c_aS1DTn")

hman.style1d()

hman.addLegend("SIPM_aS1Charge","HHV Off (4439)","LF",
               x0=0.5,y0=0.8,x1=0.933,y1=0.9,tsize=0.03)
#hman.addLegendEntry("21.0_aS1Charge","HV=21.0/0 kV (4370)","LF")
#hman.addLegendEntry("23.8_aS1Charge","HV=23.8/0 kV (4371)","LF")
#hman.addLegendEntry("7.8_aS1Charge","HV=7.8/2.8 kV (4378)","LF")

#hman.draw("SIPM_aS1sTime","black","yellow","",lineType=1)
#hman.draw("2.8_aS1sTime","black","","same",lineType=2)
#hman.draw("7.8_aS1sTime","red","","same",lineType=3)
#raw_input()
hman.draw("SIPM_aS1Charge","black","yellow",lineType=1,max=250)
#hman.draw("23.8_aS1Charge","black","","same",lineType=2)
#hman.draw("7.8_aS1Charge","red","","same",lineType=3)
hman.ps("aS1Charge_NoHV.eps")

raw_input()
hman.setLogy(True)

hman.axis("SIPM_aS1DTn","#DeltaT_{S1-G} (#mus)","Entries/#alpha")
hman.axis("23.8_aS1DTn","#DeltaT_{S1-G} (#mus)","Entries/#alpha")
hman.axisRange("23.8_aS1DTn",0,700,"x")

#hman.axisRange("SIPM_aS1DTn",0,325,"x")
hman.style1d()

hman.addLegend("SIPM_aS1DTn","HHV Off (4439)","LF",
               x0=0.5,y0=0.8,x1=0.933,y1=0.9,tsize=0.03)
#hman.addLegendEntry("21.0_aS1DTn","HV=21.0/0 kV (4370)","LF")
#hman.addLegendEntry("23.8_aS1DTn","HV=23.8/0 kV (4371)","LF")

hman.setGrid(1,1)
hman.draw("SIPM_aS1DTn","black","yellow")
#hman.draw("21.0_aS1DTn","black","","same",lineType=2)
#hman.draw("23.8_aS1DTn","black","","same",lineType=3)
#hman.draw("7.8_aS1DTn","red","","same",lineType=3)
hman.ps("aS1DT_NoHV.eps")
raw_input()

hman.setLogy(False)
hman.addLegend("23.8_aS1DTn","HV=23.8/0 Act+Buff (4371)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("23.8c_aS1DTn","HV=23.8/0 Cathode (4371)","LF")
hman.draw("23.8_aS1DTn","black","yellow","",lineType=1,title=0)
hman.draw("23.8c_aS1DTn","black","","same",lineType=2)
hman.ps("aS1DT_NoGateHV.eps")
raw_input()

hman.axisRange("23.8_aS1DTn",200,700,"x")
hman.style1d()
hman.draw("23.8_aS1DTn","black","yellow","",max=0.35,lineType=1,title=0)
hman.draw("23.8c_aS1DTn","black","","same",lineType=2)
hman.ps("aS1DT_NoGateHV_zoom.eps")

raw_input()

#ffunc = TF1("ffunc","[0]*exp(-x/[1])",200,500)
ffunc = TF1("ffunc","expo",200,500)
hman.fit("23.8c_aS1DT","ffunc",300,500,"23.8c_aS1DT_fit")
hman.draw("23.8c_aS1DT_fit","black","yellow","",lineType=1,title=0)
raw_input()
