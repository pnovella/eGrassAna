
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Utils import *

class GrassChar(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        """
            
        self.name='GrassChar'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.draw = self.ints["DRAW"]
        except KeyError: self.draw = True

        try: self.hS1Qmax = self.doubles["HISTO_S1_QMAX"]
        except KeyError: self.hS1Qmax = 10

        try: self.hTmax = self.doubles["HISTO_TMAX"]
        except KeyError: self.hTmax = 3200

        try: self.recoLabel = self.strings["RECO_LABEL"]
        except KeyError: self.recoLabel = "RecoSignal"
        
    def initialize(self):

        """
        """
        
        self.m.log(1,'+++Init method of GrassChar algorithm+++')

        self.bookHistos()
        
        return

    def execute(self,event=""):

        """
        """

        signals = getGoodSignals(event,self.recoLabel)
        S1s = [s for s in signals if s.GetSignalType()==gate.S1]

        sTs = sorted([s1.GetStartTime()/microsecond for s1 in S1s])
        dts = [ sTs[i+1]-sTs[i] for i in range(len(sTs)-1) ]
        
        for dt in dts: self.hman.fill(self.alabel("S1_DT"),dt)
        
        for s1 in S1s:
            q = s1.GetAmplitude()
            st, et = s1.GetStartTime(), s1.GetEndTime()
            self.hman.fill(self.alabel("S1_sT"),st/microsecond)
            self.hman.fill(self.alabel("S1_eT"),et/microsecond)
            self.hman.fill(self.alabel("S1_wT"),(et-st)/microsecond)
            self.hman.fill(self.alabel("S1_Amp"),q)
        
        return True

    def finalize(self):

        
        self.m.log(1,'+++End method of GrassChar algorithm+++')

        if self.draw: self.drawHistos()
        
        return

    def drawHistos(self):

        self.hman.style1d()

        self.hman.draw(self.alabel("S1_sT"),"black","yellow")
        self.wait()
        self.hman.draw(self.alabel("S1_eT"),"black","yellow")
        self.wait()
        self.hman.draw(self.alabel("S1_wT"),"black","yellow")
        self.wait()
        self.hman.draw(self.alabel("S1_Amp"),"black","yellow")
        self.wait()
        self.hman.draw(self.alabel("S1_DT"),"black","yellow")
        self.wait()
                                      
        return 
    
    def bookHistos(self):

        self.hman.h1(self.alabel("S1_sT"),
                     "S1-like Signal Start Time;Time (#mus); A. U.",
                     int(self.hTmax),0,self.hTmax)
        
        self.hman.h1(self.alabel("S1_eT"),
                     "S1-like Signal End Time; Time (#mus); A. U.",
                     int(self.hTmax),0,self.hTmax)

        self.hman.h1(self.alabel("S1_wT"),
                     "S1-like Signal Width;Width (#mus); A. U.",120,0,3)
        
        self.hman.h1(self.alabel("S1_Amp"),
                     "S1-like Amplitude;Charge (PE);A. U.",200,0,self.hS1Qmax)

        self.hman.h1(self.alabel("S1_DT"),
                     "S1-like Time difference; #DeltaT (#mus);A. U.",200,0,50)

        
        return
