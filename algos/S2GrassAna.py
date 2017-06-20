
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Utils import *

class S2GrassAna(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """      
        """
         
        self.name='S2GrassAna'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.maxS2 = self.ints["MAX_N_S2"] 
        except KeyError: self.maxS2 = 1
        
        try: self.recoLabel = self.strings["RECO_LABEL"]
        except KeyError: self.recoLabel = "RecoSignal"

        try: self.btime = self.doubles["BUFFER_TIME"]
        except KeyError: self.btime = 1200*microsecond

        try: self.s2EGTmin = self.doubles["S2_GRASS_TIME_MIN"]
        except KeyError: self.s2EGTmin = 700*microsecond
        # S2-induced EG measured in region afer S2
        
        try: self.cntEGTmax = self.doubles["CNT_GRASS_TIME_MAX"]
        except KeyError: self.cntEGTmax = 100*microsecond
        # constant EG measured in prebuffer region
        
        try:  self.hS2QMax = self.doubles["HISTO_S2_Q_MAX"]
        except KeyError: self.hS2QMax = 20000

        try: self.draw = self.ints["DRAW"]
        except KeyError: self.draw = True
        
        if self.recoLabel: self.unit = nanosecond # !!!!
        else: self.unit = microsecond

        
    def initialize(self):

        """        
        """
        
        self.m.log(1,'+++Init method of S2GrassAna algorithm+++')

        self.bookHistos()

        self.nAnaTrig = 0
        
        return

    def execute(self,event=""):

        """
        """

        self.nAnaTrig += 1
        
        signals = getGoodSignals(event,self.recoLabel)
        S1s = [s for s in signals if s.GetSignalType()==gate.S1]
        S2s = [s for s in signals if s.GetSignalType()==gate.S2]
                
        if len(S2s)>self.maxS2:
            self.m.fatalError("event should have %i S2s at most"%self.maxS2)
      
        s2q = sum([s.GetAmplitude() for s in S2s])
        s2time = S2s[0].GetStartTime()
        assert s2time < self.s2EGTmin # algo assumes S2 triggers

        self.hman.fill("S2Charge",s2q)
        self.hman.fill("S2sTime",s2time/microsecond)
        
        S1sAS2 =[s1 for s1 in S1s if s1.GetStartTime()>self.s2EGTmin]
        S1sPB =[s1 for s1 in S1s if s1.GetStartTime()<self.cntEGTmax]

        self.hman.fill("nS1sPB",len(S1sPB))
        self.hman.fill("nS1sAS2",len(S1sAS2))
        self.hman.fill("S2QvsM",s2q,len(S1sAS2))
        
        return True

    def finalize(self):

        
        self.m.log(1,'+++End method of S2GrassAna algorithm+++')

        self.computeRates()

        if self.draw: self.drawHistos()
        
        return

    def computeRates(self):

        rowindow = self.btime - self.s2EGTmin
        totaltime = rowindow*(self.nAnaTrig)/millisecond
        conts = self.hman.getContents("nS1sAS2")
        bins =  self.hman.getLowEdges("nS1sAS2")
        nS1s = sum([b*c for b,c in zip(bins,conts)])        
        s1rate, s1erate = nS1s/totaltime, sqrt(nS1s)/totaltime 

        self.m.log(1,"S2 e- grass rate: %0.2f +/- %0.2f ms-1"
                   %(s1rate,s1erate))

        rowindow = self.cntEGTmax
        totaltime = rowindow*(self.nAnaTrig)/millisecond
        conts = self.hman.getContents("nS1sPB")
        bins =  self.hman.getLowEdges("nS1sPB")
        nS1s = sum([b*c for b,c in zip(bins,conts)])        
        s1rate, s1erate = nS1s/totaltime, sqrt(nS1s)/totaltime 

        self.m.log(1,"Const e- grass rate: %0.2f +/- %0.2f ms-1"
                   %(s1rate,s1erate))
        
        return

    def drawHistos(self):

        self.hman.style1d()
        self.hman.statsPanel(111111)
        self.hman.draw("S2sTime","black","yellow")
        self.wait()
        self.hman.draw("S2Charge","black","yellow")
        self.wait()
        self.hman.draw("nS1sAS2","black","yellow")
        self.hman.draw("nS1sPB","black","","same",lineType=2)
        self.wait()
        self.hman.draw("S2QvsM",option="col")
        self.wait()
        
        return 
    
    def bookHistos(self):

        labels = "S1-like signals in pre-buffer; Number of signals; Entries"
        self.hman.h1("nS1sPB",labels,1000,0,1000)
        labels = "S1-like signals afer S2; Number of signals; Entries"
        self.hman.h1("nS1sAS2",labels,1000,0,1000)
        
        labels = "S2 Start Time; S2 Start Time (#mus);Entries"
        self.hman.h1("S2sTime",labels,
                     int(self.btime/microsecond),0,self.btime/microsecond)
        labels = "S2 Charge; S2 Charge (PE);Entries"
        self.hman.h1("S2Charge",labels,200,0,self.hS2QMax)

        labels = "S2 Q vs EG Mult;S2 Charge (PE); e^{-} grass multiplicity"
        self.hman.h2("S2QvsM",labels,200,0,self.hS2QMax,100,0,100)
        
        return 
