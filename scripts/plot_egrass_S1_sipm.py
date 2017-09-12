from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time
from math import sqrt

hman = HistoManager(True)

"""
alpha runs
"""

hman.load("../data/S1GrassAna_4442.root","NoSIPM_")
hman.load("../data/S1GrassAna_4439.root","SIPM_")
hman.style1d()
hman.draw("NoSIPM_aS1sTime","black","yellow")
hman.draw("SIPM_aS1sTime","black","","same",lineType=2)
raw_input()
hman.draw("NoSIPM_aS1Charge","black","yellow")
hman.draw("SIPM_aS1Charge","black","","same",lineType=2)
raw_input()
hman.draw("SIPM_S1sTime","black","yellow")
hman.draw("NoSIPM_S1sTime","black","","same",lineType=2)
raw_input()


# hman.load("../data/S1GrassAna_4442_S2allowed.root","NoSIPM_")
# hman.load("../data/S1GrassAna_4442_S2notallowed.root","NoSIPM_Act_")
# hman.load("../data/S1GrassAna_4439_S2allowed.root","SIPM_")
# hman.load("../data/S1GrassAna_4439_S2notallowed.root","SIPM_Act_")
# # S2 are actually cathode alphas with long trail of "after-pulses"
# hman.style1d()

# hman.statsPanel(111111)
# hman.draw("NoSIPM_aS1sTime","black","yellow")
# hman.draw("NoSIPM_Act_aS1sTime","black","","same",lineType=2)
# raw_input()
# hman.draw("NoSIPM_aS1Charge","black","yellow")
# hman.draw("NoSIPM_Act_aS1Charge","black","","same",lineType=2)
# raw_input()
# hman.draw("NoSIPM_S2sTime","black","yellow")
# raw_input()
# hman.draw("NoSIPM_S2Charge","black","yellow")
# raw_input()
# hman.draw("NoSIPM_S1sTime","black","yellow")
# hman.draw("NoSIPM_Act_S1sTime","black","","same",lineType=2)
# raw_input()

# hman.draw("SIPM_aS1sTime","black","yellow")
# hman.draw("SIPM_Act_aS1sTime","black","","same",lineType=2)
# raw_input()
# hman.draw("SIPM_aS1Charge","black","yellow")
# hman.draw("SIPM_Act_aS1Charge","black","","same",lineType=2)
# raw_input()

# hman.draw("SIPM_S1sTime","black","yellow")
# hman.draw("SIPM_Act_S1sTime","black","","same",lineType=2)
# raw_input()

# hman.draw("NoSIPM_S1sTime","black","yellow")
# hman.draw("SIPM_S1sTime","black","","same",lineType=2)
# raw_input()
# hman.draw("NoSIPM_Act_S1sTime","black","yellow")
# hman.draw("SIPM_Act_S1sTime","black","","same",lineType=2)
# raw_input()

#--------------------------#

runs = [4366,4439,4442,4443]
for run in runs: hman.load("../data/S1GrassAna_%i.root"%run,"%i_"%run)
hman.load("../data/S1GrassAna_4366_Cathode.root","4366_Cath_")
hman.load("../data/S1GrassAna_4443_Cathode.root","4443_Cath_")

hman.addLegend("4439_aS1DT","HV Off. SiPM On (4439)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4442_aS1DT","HV Off. SiPM Off (4442)","LF")
hman.addLegendEntry("4443_aS1DT","HV On, SiPM Off (4443)","LF")

hman.style1d()
hman.setGrid(1,1)
hman.draw("4439_aS1DT","black","yellow",norm=0)
hman.draw("4442_aS1DT","black","","same",lineType=2,norm=0)
hman.draw("4443_aS1DT","black","","same",lineType=3,norm=0)
raw_input()

hman.addLegend("4366_aS1DT","HV On. SiPM On (4366)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4443_aS1DT","HV On. SiPM Off (4443)","LF")

hman.style1d()
hman.setGrid(1,1)

hman.draw("4366_aS1DT","black","yellow",norm=0)
hman.draw("4443_aS1DT","black","","same",lineType=2,norm=0)
raw_input()

hman.draw("4366_Cath_aS1DT","black","yellow",norm=0)
hman.draw("4443_Cath_aS1DT","black","","same",lineType=2,norm=0)
raw_input()


hman.cclear()
rates,erates = [],[]
pbrates,pberates = [],[]
for run in runs:

    time,pbrate = Double(),Double()
    hman["%s_S1PBRate"%run].GetPoint(0,time,pbrate)
    pberate = hman["%s_S1PBRate"%run].GetErrorY(0)
    pbrates.append(pbrate)
    pberates.append(pberate)
    
    time,rate = Double(),Double()
    hman["%s_S1AS1Rate"%run].GetPoint(0,time,rate)
    erate = hman["%s_S1AS1Rate"%run].GetErrorY(0)
    rates.append(rate-pbrate)
    erates.append(sqrt(erate**2+pberate**2))


hman.graph("AS1Rate",runs[1:-1],rates[1:-1],0,erates[1:-1])
hman.setTitle("AS1Rate_graphAxis","S1 e^{-} grass rate")
hman.axis("AS1Rate_graphAxis","Run Number",
          "S1 e^{-} grass rate (ms^{-1})")
hman.style1d()
hman.setGrid(1,1)
hman.drawGraph("AS1Rate","AP",markerType=20,lineType=2,min=0)

raw_input()


runson = [runs[0],runs[-1]]
rateson = [pbrates[0],pbrates[-1]]
erateson = [pberates[0],pberates[-1]]

hman.graph("PBRateOn",runson,rateson,0,erateson)
hman.setTitle("PBRateOn_graphAxis","Background e^{-} grass")
hman.axis("PBRateOn_graphAxis","Run Number",
          "e^{-} grass rate (ms^{-1})")


runsoff = runs[1:-1]
ratesoff = pbrates[1:-1]
eratesoff = pberates[1:-1]

hman.graph("PBRateOff",runsoff,ratesoff,0,eratesoff)
hman.setTitle("PBRateOff_graphAxis","Background e^{-} grass")
hman.axis("PBRateOff_graphAxis","Run Number",
          "e^{-} grass rate (ms^{-1})")

print "Ratio with gate HV off:", ratesoff[0]/ratesoff[1]
print "Ratio with gate HV on:", rateson[0]/rateson[1]

hman.style1d()
hman.setGrid(1,1)
hman.addLegend("PBRateOn","HV Off. Gate HV On","LP",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("PBRateOff","HV Off. Gate HV Off","LP")
hman.drawGraph("PBRateOn","APL",markerType=24,lineType=2,min=0)
hman.drawGraph("PBRateOff","PL",markerType=20,lineType=2,min=0)

hman.addText(4365,45,"SiPM On",color="red",size=0.03)
hman.addText(4425,35,"SiPM On",color="red",size=0.03)
hman.addText(4425,15,"SiPM Off",color="blue",size=0.03)

raw_input()

hman.addLegend("4366_aS2DT","HV On. SiPM On (4366)","LF",
               x0=0.5,y0=0.7,x1=0.933,y1=0.9,tsize=0.03)
hman.addLegendEntry("4443_aS2DT","HV On. SiPM Off (4443)","LF")
hman.draw("4366_aS2DT","black","yellow",norm=0)
hman.draw("4443_aS2DT","black","","same",lineType=2,norm=0)

raw_input()

hman.draw("4366_Cath_aS2DT","black","yellow",norm=0)
hman.draw("4443_Cath_aS2DT","black","","same",lineType=2,norm=0)
raw_input()



