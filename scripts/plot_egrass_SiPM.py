from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager

hman = HistoManager(True)

hman.load("../data/GrassChar_AutoTigger_NoHV_NoSiPM.root","NOSIPM_")
hman.load("../data/GrassChar_AutoTigger_NoHV.root","SIPM_")

hman.addLegend("SIPM_GrassChar.S1_PMTMult","SiPM On","LF",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("NOSIPM_GrassChar.S1_PMTMult","SiPM Off","L")

#hman.setLogy(True)
#hman.draw("SIPM_GrassChar.S2_Amp","black","yellow",title=0)
#hman.draw("NOSIPM_GrassChar.S2_Amp","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_PMTMult.eps")
#raw_input()
hman.draw("SIPM_GrassChar.S1_PMTMult","black","yellow",title=0,norm=1)
hman.draw("NOSIPM_GrassChar.S1_PMTMult","black","","same",lineType=2,norm=1)
#hman.ps("GrassChar.S1_PMTMult_HVvsNoHV.eps")
raw_input()
hman.setLogy(False)
#hman["SIPM_GrassChar.S1_sT"].Rebin(10)
hman.draw("SIPM_GrassChar.S1_sT","black","yellow",min=0,max=250,title=0)
hman.draw("NOSIPM_GrassChar.S1_sT","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_S1_sT.eps")
raw_input()
hman.setLogy(True)
hman.axisRange("SIPM_GrassChar.S1_wT",0,0.95,"x")
hman.style1d("SIPM_GrassChar.S1_wT")
hman.draw("SIPM_GrassChar.S1_wT","black","yellow",title=0)
hman.draw("NOSIPM_GrassChar.S1_wT","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_wT.eps")
raw_input()
hman.draw("SIPM_GrassChar.S1_Amp","black","yellow",title=0)
hman.draw("NOSIPM_GrassChar.S1_Amp","black","","same",lineType=2,title=0)
#hman.ps("GrassChar.S1_Amp.eps")
raw_input()
hman.addLegend("SIPM_GrassChar.S1_DT","SiPM On","LF",
               x0=0.55,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("NOSIPM_GrassChar.S1_DT","SiPM Off","L")
hman.draw("SIPM_GrassChar.S1_DT","black","yellow",title=0,norm=1)
hman.draw("NOSIPM_GrassChar.S1_DT","black","","same",lineType=2,title=0,norm=1)
#hman.ps("GrassChar.S1_DT_HVvsNoHV.eps")

#raw_input()
hman.cclear()
hman.fitPanel(11111)
hman.fit("NOSIPM_GrassChar.S1_DT","expo",9,50)
hman["NOSIPM_GrassChar.S1_DT_fit"].GetFunction("f").SetLineColor(kRed)
hman.statsPos(0.932,0.9)
hman.draw("NOSIPM_GrassChar.S1_DT_fit","black","yellow",title=0)
#hman.ps("GrassChar.S1_DT_fit.eps")
raw_input()

hman.cclear()
hman.setLogy(False)

#------------#

runs = [4466,4467,4468]
for run in runs: hman.load("../data/AutoTrigAna_%i.root"%run,"%i_"%run)

times,rates,erates = [],[],[]
for run in runs:
    rtime,rate = Double(),Double()
    hman["%s_S1Rate"%run].GetPoint(0,rtime,rate)
    erate = hman["%s_S1Rate"%run].GetErrorY(0)
    times.append(rtime)
    rates.append(rate)
    erates.append(erate)

hman.graph("myrate",runs,rates,0,erates)
hman.axis("myrate_graphAxis","Run Number","e^{-} grass rate (ms^{-1})")
hman.setTitle("myrate_graphAxis","Auto-trigger Runs")
#hman["myrate_graphAxis"].GetXaxis().SetTimeDisplay(1);
hman.style1d()
hman.setGrid(1,1)
hman.setTitle("myrate","")
hman.drawGraph("myrate","APL",lineType=2,markerType=20)
hman.addText(4466.1,45,"SiPM On, HHV On",color="blue",size=0.03)
hman.addText(4467.1,25,"SiPM Off, HHV On",color="blue",size=0.03)
hman.addText(4467.5,13,"SiPM Off, HHV Off",color="blue",size=0.03)

hman.ps("bg_grass_sipm.eps")

raw_input()

hman.addLegend("4466_S1ChRate","SiPM On, HHV On (4366)","P",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4467_S1ChRate","SiPM Off, HHV On (4367)","P")
hman.addLegendEntry("4468_S1ChRate","SiPM Off, HHV Off (4368)","P")
hman.drawGraph("4466_S1ChRate","AP",markerType=20,min=0)
hman.drawGraph("4467_S1ChRate","P",markerType=24)
hman.drawGraph("4468_S1ChRate","P",markerType=21)

raw_input()


hman.setCanvasSize(1000,500)
hman.zones(3,1)
for run in runs:
    hname = "%i_S1XYRate"%run
    hman.setTitle(hname,"Run %i"%run)
    hman.axis(hname,"x (cm)","y (cm)","Rate (ms^{-1})")
    hman.style2d(hname)
    hman.draw(hname,option="colz")
raw_input()
