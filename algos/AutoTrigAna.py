
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Centella.system_of_units import *
from Utils import *

class AutoTrigAna(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        """
            
        self.name='AutoTrigAna'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.recoLabel = self.strings["RECO_LABEL"]
        except KeyError: self.recoLabel = "RecoSignal"

        try: self.draw = self.ints["DRAW"]
        except KeyError: self.draw = True

        #if self.recoLabel=="RecoSignal": self.unit = nanosecond # !!!!
        #else: self.unit = microsecond

        self.rowindow = 3200*microsecond
         
        self.npmt = 11 # !!!!
        
        self.chids,self.pos = [],[]
        
    def initialize(self):

        """
        """
        
        self.m.log(1,'+++Init method of AutoTrigAna algorithm+++')

        self.bookHistos()
        self.nAnaTrig = 0
        
        return

    def execute(self,event=""):

        """ 
        """

        self.nAnaTrig += 1 
        
        if not self.chids: 

            sensors = self.run.GetGeometry().GetSensors()
            self.chids = [i for i,s in sensors][:self.npmt]
            self.pos = [s.GetPosition() for i,s in sensors][:self.npmt]
            self.m.log(0,"PMT Channels in run:",self.chids)
            self.time = event.GetTime()*millisecond/second
            
        signals = getGoodSignals(event,self.recoLabel)
        S1s = [s for s in signals if s.GetSignalType()==gate.S1]
        S2s = [s for s in signals if s.GetSignalType()==gate.S2]
        
        self.hman.fill("nS1trig",len(S1s))
        self.hman.fill("nS2trig",len(S2s))
        
        S1sCh = [0]*len(self.chids)
        for S1 in S1s:
            chIDs = list(S1.GetCatHitMap().GetChannels(0))# RecoSignal!
            for ch in self.chids:
                if ch in chIDs: S1sCh[self.chids.index(ch)] += 1
     
        for  ch in range(self.npmt):
            self.hman.fill("nS1trigCh%i"%ch,S1sCh[ch])
            
        maxs1 = max(S1sCh)
        try: self.hman.fill("nS1MaxTot",maxs1*1./len(S1s))
        except ZeroDivisionError: pass        
    
        
    def finalize(self):
        
        self.m.log(1,'+++End method of AutoTrigAna algorithm+++')

        self.computeRates()
        
        if self.draw: self.drawHistos()

        return

    def computeRates(self):
        
        totaltime = self.rowindow*(self.nAnaTrig)/millisecond
        
        conts = self.hman.getContents("nS1trig")
        bins =  self.hman.getLowEdges("nS1trig")
        nS1s = sum([b*c for b,c in zip(bins,conts)])

        conts = self.hman.getContents("nS2trig")
        bins =  self.hman.getLowEdges("nS2trig")
        nS2s = sum([b*c for b,c in zip(bins,conts)])
        
        s1rate, s2rate = nS1s/totaltime, nS2s / totaltime
        s1erate, s2erate = sqrt(nS1s)/totaltime, sqrt(nS2s)/totaltime
        
        self.m.log(1,"S1-like pulse rate: %0.2f +/- %0.2f"%(s1rate,s1erate))
        self.m.log(1,"S2-like pulse rate: %0.2f +/- %0.2f"%(s2rate,s2erate))

        chs1rates,chs1erates = [],[]
        for ch in range(self.npmt):
            conts = self.hman.getContents("nS1trigCh%i"%ch)
            bins =  self.hman.getLowEdges("nS1trigCh%i"%ch)
            nS1s = sum([b*c for b,c in zip(bins,conts)])

            s1chrate,s1cherate  = nS1s/totaltime, sqrt(nS1s)/totaltime
            chs1rates.append(s1chrate)
            chs1erates.append(s1cherate)
           
            x, y = self.pos[ch].x(), self.pos[ch].y()
            self.hman.fill("S1XYRate",x,y,w=s1chrate)
            #self.hman.fill("S1XYNP",x,y,w=nS1s)
                        
        self.hman.graph("S1ChRate",self.chids,chs1rates,0,chs1erates)
        self.hman.axis("S1ChRate_graphAxis","PMT","S1 e- grass rate (ms^{-1})")

        self.hman.graph("S1Rate",[self.time],[s1rate],0,[s1erate])
        self.hman.axis("S1Rate_graphAxis","Time","S1 e- grass rate (ms^{-1})")
        
        return 
    
    def drawHistos(self):
        
        self.hman.style1d()
        self.hman.style2d()
        
        #self.hman.draw("S1XYNP",option="colz")
        #raw_input()
                       
        self.hman.statsPanel(111111)
        self.hman.draw("nS1trig")
        self.wait()
        self.hman.draw("nS2trig")
        self.wait()

        self.hman.zones(3,4)
        for ch in range(self.npmt):
            hname = "nS1trigCh%i"%ch
            self.hman.setTitle(hname,"S1-like signals Ch%i"%self.chids[ch])
            self.hman.draw(hname)
        self.wait()
      
        self.hman.cclear()
        self.hman.drawGraph("S1Rate","AP",markerType=20)
        self.wait()
        self.hman.drawGraph("S1ChRate","AP",markerType=20)
        self.wait()
        self.hman.statsPanel(0)
        self.hman.draw("S1XYRate",option="colz")
        self.wait()
        self.hman.draw("nS1MaxTot")
        self.wait()
        
                       
    def bookHistos(self):

        self.hman.h1("nS1trig","S1-like signals; Number of signals; Entries",
                     10000,0,10000)
        self.hman.h1("nS2trig","S2-like signals; Number of signals; Entries",
                     100,0,100)

        self.hman.h1("nS1MaxTot","MT;Max.Pulses/Tot.Pulses;Entries",100,0,1)
        self.hman.h1("nS2MaxTot","MT;Max.Pulses/Tot.Pulses;Entries",100,0,1)
        
        for ch in range(self.npmt):
            hname = "nS1trigCh%i"%ch
            title = "S1-like signals Ch%i; Number of signals; Entries"%ch
            self.hman.h1(hname,title,10000,0,10000)
            hname = "nS2trigCh%i"%ch
            title = "S2-like signals Ch%i; Number of signals; Entries"%ch
            self.hman.h1(hname,title,100,0,100)
            
        hname = "S1XYRate"
        self.hman.h2(hname,"S1 e- grass rate; x (cm); y (cm); Rate (ms^{-1})",
                     10,-200,200,10,-200,200)

        #hname = "S1XYNP"
        #self.hman.h2(hname,"S1 N pulses; x (cm); y (cm)",
        #             10,-200,200,10,-200,200)
            
        return
