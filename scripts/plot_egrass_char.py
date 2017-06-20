from ROOT import gStyle,kRed,Double,TDatime
from Centella.histoManager import HistoManager
from Centella.system_of_units import *
import time

hman = HistoManager(True)

hman.load("../data/GrassChar_AutoTigger_NoHV.root")

hman.draw("GrassChar.S1_sT","black","yellow")
raw_input()
hman.draw("GrassChar.S1_eT","black","yellow")
raw_input()
hman.draw("GrassChar.S1_wT","black","yellow")
raw_input()
hman.draw("GrassChar.S1_Amp","black","yellow")
raw_input()
hman.draw("GrassChar.S1_DT","black","yellow")
raw_input()
