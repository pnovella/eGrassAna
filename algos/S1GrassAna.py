
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Utils import *

class S1GrassAna(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """      
        """
         
        self.name='S1GrassAna'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.maxS2 = self.ints["MAX_N_S2"] 
        except KeyError: self.maxS2 = 1
        
        try: self.recoLabel = self.strings["RECO_LABEL"]
        except KeyError: self.recoLabel = "RecoSignal"
                
        try: self.draw = self.ints["DRAW"]
        except KeyError: self.draw = True
        
        try: self.btime = self.doubles["BUFFER_TIME"]
        except KeyError: self.btime = 1200*microsecond
        try:  self.hS2QMax = self.doubles["HISTO_S2_Q_MAX"]
        except KeyError: self.hS2QMax = 200000
        # just to set histogram axis
        
        try: self.s1EGTmax = self.doubles["S1_GRASS_TIME_MAX"]
        except KeyError: self.s1EGTmax = 1200*microsecond
        # time cut for timing optimization

        try: self.s1EGWindow = self.doubles["S1_GRASS_TIME_WINDOW"]
        except KeyError: self.s1EGWindow = 200*microsecond
        # winow for integration of the EG rate
        
        try: self.cntEGTmax = self.doubles["CNT_GRASS_TIME_MAX"]
        except KeyError: self.cntEGTmax = 100*microsecond
        # constant EG measured in prebuffer region

        try: self.s1EGQmax = self.doubles["EG_CHARGE_MIN"]
        except KeyError:  self.s1EGQmax = 20
        # minimum charge defining grass pulses (1PE)

        try: self.aS1Qmin = self.doubles["S1_ALPHA_CHARGE_MIN"]
        except KeyError: self.aS1Qmin = 100
        # minimum charge for alpha S1

        try: self.aS1Qmax = self.doubles["S1_ALPHA_CHARGE_MAX"]
        except KeyError: self.aS1Qmax = 1e9
        # minimum charge for alpha S1
        
        try: self.aS1Tmin = self.doubles["S1_ALPHA_TIME_MIN"]
        except KeyError: self.aS1Tmin = 650*microsecond
        # minimum time for alpha S1

        try: self.aS1Tmax = self.doubles["S1_ALPHA_TIME_MAX"]
        except KeyError: self.aS1Tmax = 655*microsecond
        # maximum time for alpha S1
        
   
    def initialize(self):

        """        
        """
        
        self.m.log(1,'+++Init method of S1GrassAna algorithm+++')

        self.nAnaTrig = 0
        self.chids = []
        self.npmt = 11 # !!!!

        self.bookHistos()
        
        return

    def execute(self,event=""):

        """
        """
    
        if not self.chids: 

            sensors = self.run.GetGeometry().GetSensors()
            self.chids = [i for i,s in sensors][:self.npmt]
            self.pos = [s.GetPosition() for i,s in sensors][:self.npmt]
            self.m.log(0,"PMT Channels in run:",self.chids)
            self.time = event.GetTime()*millisecond/second
        
        
        signals = getGoodSignals(event,self.recoLabel)
        S1s = [s for s in signals if s.GetSignalType()==gate.S1 and\
               s.GetStartTime()<self.s1EGTmax]
        S2s = [s for s in signals if s.GetSignalType()==gate.S2]
                
        if len(S2s)>self.maxS2:
            self.m.fatalError("event should have %i S2s at most"%self.maxS2)
            # this is in case alpha S2 is splitted into >1 pulses


        for s1 in S1s: self.hman.fill("S1sTime",s1.GetStartTime()/microsecond)

        # need to selected events with cathode alphas
        S1sTQ = [(s.GetStartTime(),s.GetAmplitude()) for s in S1s]
        aS1 = S1sTQ.pop(S1sTQ.index(max(S1sTQ,key = lambda x: x[1])))
        
        if aS1[1]<self.aS1Qmin  or aS1[1]>self.aS1Qmax or\
           aS1[0]<self.aS1Tmin or aS1[0]>self.aS1Tmax:
            return False # no good alpha


        s2q = 0
        if len(S2s):
            s2q = sum([s.GetAmplitude() for s in S2s])
            s2time = S2s[0].GetStartTime()
            self.hman.fill("S2Charge",s2q)
            self.hman.fill("S2sTime",s2time/microsecond)
        
        ##
        #saS1 = S1sTQ.pop(S1sTQ.index(max(S1sTQ,key = lambda x: x[1])))
        #if saS1[1]>self.aS1Qmin: return # 2 alpha s1 !!!!!
        ###
        
        self.nAnaTrig += 1

        self.hman.fill("aS1sTime",aS1[0]/microsecond)
        self.hman.fill("aS1Charge",aS1[1])
        
        S1sAS1 =[s1 for s1 in S1s \
                 if aS1[0]< s1.GetStartTime()< aS1[0]+self.s1EGWindow\
                 and s1.GetAmplitude() < self.s1EGQmax] 
        S1sPB =[s1 for s1 in S1s if s1.GetStartTime()<self.cntEGTmax \
                and s1.GetAmplitude() < self.s1EGQmax]

        lt = 0
        for s1 in S1sAS1:
            self.hman.fill("aS1DT",(s1.GetStartTime()-aS1[0])/microsecond)
            self.hman.fill("aS1EGQ",s1.GetAmplitude())
            self.hman.fill("aS1EGT",s1.GetStartTime()/microsecond)
            self.hman.fill("aS1EGW",
                           (s1.GetEndTime()-s1.GetStartTime())/microsecond)
            if lt:
                st = s1.GetStartTime()
                dt = (st-lt)/microsecond
                if aS1[0]+10*microsecond<st<aS1[0]+120*microsecond:
                    self.hman.fill("S1S1DTBuffer",dt)
                elif aS1[0]+130*microsecond<st<aS1[0]+500*microsecond:
                    self.hman.fill("S1S1DTActive",dt)
                elif st>aS1[0]+600*microsecond:
                    self.hman.fill("S1S1DTOut",dt)
            lt=s1.GetStartTime()

        #----
        if s2q: # tere is an alpha S2
            S1sAS2 =[s1 for s1 in S1sAS1 \
                     if s1.GetStartTime()>s2time  \
                     and s1.GetAmplitude() < self.s1EGQmax]
            for s1 in S1sAS2:
                self.hman.fill("aS2DT",(s1.GetStartTime()-s2time)/microsecond)
        #---- 
        
        
        self.hman.fill("nS1sPB",len(S1sPB))
        self.hman.fill("nS1sAS1",len(S1sAS1))
        self.hman.fill("S1QvsM",aS1[1],len(S1sAS1))
        if len(S2s): self.hman.fill("S2QvsM",s2q,len(S1sAS1))
        
        S1sAS1Ch = [0]*len(self.chids)
        for S1 in S1sAS1:
            chIDs = list(S1.GetCatHitMap().GetChannels(0))# RecoSignal!
            for ch in self.chids:
                if ch in chIDs: S1sAS1Ch[self.chids.index(ch)] += 1
        for  ch in range(self.npmt):
            self.hman.fill("nS1sAS1Ch%i"%ch,S1sAS1Ch[ch])

        S1sPBCh = [0]*len(self.chids)
        for S1 in S1sPB:
            chIDs = list(S1.GetCatHitMap().GetChannels(0))# RecoSignal!
            for ch in self.chids:
                if ch in chIDs: S1sPBCh[self.chids.index(ch)] += 1
        for  ch in range(self.npmt):
            self.hman.fill("nS1sPBCh%i"%ch,S1sPBCh[ch])
        
        return True
    
    def finalize(self):

        
        self.m.log(1,'+++End method of S1GrassAna algorithm+++')

        self.computeRates()

        if self.draw: self.drawHistos()
        
        return

    
    def computeRates(self):

        rowindow = self.s1EGWindow
        totaltime = rowindow*(self.nAnaTrig)/millisecond
        conts = self.hman.getContents("nS1sAS1")
        bins =  self.hman.getLowEdges("nS1sAS1")
        nS1s = sum([b*c for b,c in zip(bins,conts)])        
        s1rate, s1erate = nS1s/totaltime, sqrt(nS1s)/totaltime 

        self.hman.graph("S1AS1Rate",[self.time],[s1rate],0,[s1erate])
        self.hman.axis("S1AS1Rate_graphAxis","Time",
                       "S1 e- grass rate (ms^{-1})")
        
        self.m.log(1,"S1 e- grass rate: %0.2f +/- %0.2f ms-1"
                   %(s1rate,s1erate))

        rowindow = self.cntEGTmax
        totaltime = rowindow*(self.nAnaTrig)/millisecond
        conts = self.hman.getContents("nS1sPB")
        bins =  self.hman.getLowEdges("nS1sPB")
        nS1s = sum([b*c for b,c in zip(bins,conts)])        
        s1rate, s1erate = nS1s/totaltime, sqrt(nS1s)/totaltime 

        self.hman.graph("S1PBRate",[self.time],[s1rate],0,[s1erate])
        self.hman.axis("S1PBRate_graphAxis","Time","S1 e- grass rate (ms^{-1})")
        
        self.m.log(1,"Const e- grass rate: %0.2f +/- %0.2f ms-1"
                   %(s1rate,s1erate))

        chs1rates,chs1erates = [],[]
        pbchs1rates,pbchs1erates = [],[]
        for ch in range(self.npmt):
            
            conts = self.hman.getContents("nS1sAS1Ch%i"%ch)
            bins =  self.hman.getLowEdges("nS1sAS1Ch%i"%ch)
            nS1s = sum([b*c for b,c in zip(bins,conts)])
            s1chrate,s1cherate  = nS1s/totaltime, sqrt(nS1s)/totaltime
            chs1rates.append(s1chrate)
            chs1erates.append(s1cherate)
            x, y = self.pos[ch].x(), self.pos[ch].y()
            self.hman.fill("S1AS1XYRate",x,y,w=s1chrate)

            conts = self.hman.getContents("nS1sPBCh%i"%ch)
            bins =  self.hman.getLowEdges("nS1sPBCh%i"%ch)
            nS1s = sum([b*c for b,c in zip(bins,conts)])
            s1chrate,s1cherate  = nS1s/totaltime, sqrt(nS1s)/totaltime
            pbchs1rates.append(s1chrate)
            pbchs1erates.append(s1cherate)
            x, y = self.pos[ch].x(), self.pos[ch].y()
            self.hman.fill("S1PBXYRate",x,y,w=s1chrate)
                      
        self.hman.graph("S1AS1ChRate",self.chids,chs1rates,0,chs1erates)
        self.hman.axis("S1AS1ChRate_graphAxis",
                       "PMT","S1 e- grass rate (ms^{-1})")
        self.hman.graph("S1PBChRate",self.chids,pbchs1rates,0,pbchs1erates)
        self.hman.axis("S1PBChRate_graphAxis",
                       "PMT","S1 e- grass rate (ms^{-1})")
        

        return

    def drawHistos(self):

        self.hman.style1d()
        self.hman.style2d()
        self.hman.statsPanel(111111)
        self.hman.draw("S2sTime","black","yellow")
        self.wait()
        self.hman.draw("S2Charge","black","yellow")
        self.wait()
        self.hman.draw("S1sTime","black","yellow")
        self.wait()
        self.hman.draw("aS1sTime","black","yellow")
        self.wait()
        self.hman.draw("aS1Charge","black","yellow")
        self.wait()
        self.hman.setGrid(1,1)
        self.hman.draw("aS1DT","black","yellow")
        self.wait()
        self.hman.draw("aS1EGQ","black","yellow")
        self.wait()
        self.hman.draw("aS1EGT","black","yellow")
        self.wait()          
        self.hman.draw("aS1EGW","black","yellow")
        self.wait()    
        self.hman.draw("nS1sAS1","black","yellow")
        self.hman.draw("nS1sPB","black","","same",lineType=2)
        self.wait()
        self.hman.draw("S2QvsM",option="col")
        self.wait()
        self.hman.draw("S1QvsM",option="col")
        self.wait()
        self.hman.drawGraph("S1PBRate","AP",markerType=20)
        self.wait()
        self.hman.drawGraph("S1AS1Rate","AP",markerType=20)
        self.wait()
        self.hman.drawGraph("S1AS1ChRate","AP",markerType=20)
        self.wait()
        self.hman.statsPanel(0)
        self.hman.draw("S1AS1XYRate",option="colz")
        self.wait()
        self.hman.drawGraph("S1PBChRate","AP",markerType=20)
        self.wait()
        self.hman.statsPanel(0)
        self.hman.draw("S1PBXYRate",option="colz")
        self.wait()
        self.hman.draw("S1S1DTBuffer","black","yellow")
        self.wait()
        self.hman.draw("S1S1DTActive","black","yellow")
        self.wait()
        self.hman.draw("S1S1DTOut","black","yellow")
        self.wait()
        self.hman.setGrid(1,1)
        self.hman.draw("aS2DT","black","yellow")
        self.wait()
        return 
    
    def bookHistos(self):

        labels = "S1-like signals in pre-buffer; Number of signals; Entries"
        self.hman.h1("nS1sPB",labels,1000,0,1000)
        labels = "S1-like signals afer S2; Number of signals; Entries"
        self.hman.h1("nS1sAS1",labels,1000,0,1000)

        labels = "S1 Start Time; S1 Start Time (#mus);Entries"
        self.hman.h1("S1sTime",labels,
                     int(self.btime/microsecond),0,self.btime/microsecond)

        labels = "Alha S1 Start Time; S1 Start Time (#mus);Entries"
        self.hman.h1("aS1sTime",labels,
                     int(self.btime/microsecond),0,self.btime/microsecond)
        labels = "Alpha S1 Charge; S1 Charge (PE);Entries"
        self.hman.h1("aS1Charge",labels,300,0,3000)


        labels = "Alpha S1 grass #DeltaT; #DeltaT_{S1-G} (#mus);Entries"
        self.hman.h1("aS1DT",labels,
                     int(self.s1EGWindow/microsecond),
                     0,self.s1EGWindow/microsecond)

        labels = "Alpha S1 Grass Charge; S1 Charge (PE);Entries"
        self.hman.h1("aS1EGQ",labels,800,0,20)
        labels = "Alpha S1 Grass Time; S1 Start Time (#mus);Entries"
        self.hman.h1("aS1EGT",labels,
                     int(self.btime/microsecond),0,self.btime/microsecond)
        labels = "Alpha S1 Grass Width; S1 width (#mus);Entries"
        self.hman.h1("aS1EGW",labels,40,0,1)
                           
        labels = "S2 Start Time; S2 Start Time (#mus);Entries"
        self.hman.h1("S2sTime",labels,
                     int(self.btime/microsecond),0,self.btime/microsecond)
        labels = "S2 Charge; S2 Charge (PE);Entries"
        self.hman.h1("S2Charge",labels,200,0,self.hS2QMax)

        labels = "S2 Q vs EG Mult;S2 Charge (PE); e^{-} grass multiplicity"
        self.hman.h2("S2QvsM",labels,200,0,self.hS2QMax,200,0,2000)

        labels = "S1 Q vs EG Mult;S1 Charge (PE); e^{-} grass multiplicity"
        self.hman.h2("S1QvsM",labels,300,0,3000,200,0,2000)
        
        for ch in range(self.npmt):
            hname = "nS1sAS1Ch%i"%ch
            title = "AS1 S1-like signals Ch%i; Number of signals; Entries"%ch
            self.hman.h1(hname,title,10000,0,10000)
            hname = "nS1sPBCh%i"%ch
            title = "PB S1-like signals Ch%i; Number of signals; Entries"%ch
            self.hman.h1(hname,title,10000,0,10000)
            
        hname = "S1PBXYRate"
        self.hman.h2(hname,"S1 e- grass rate; x (cm); y (cm); Rate (ms^{-1})",
                     10,-200,200,10,-200,200)
        hname = "S1AS1XYRate"
        self.hman.h2(hname,"S1 e- grass rate; x (cm); y (cm); Rate (ms^{-1})",
                     10,-200,200,10,-200,200)

        self.hman.h1("S1S1DTBuffer","S1 e- grass #DeltaT;#DeltaT (#mus);A. U.",
                     200,0,50)
        self.hman.h1("S1S1DTActive","S1 e- grass #DeltaT;#DeltaT (#mus);A. U.",
                     200,0,50)
        self.hman.h1("S1S1DTOut","S1 e- grass #DeltaT;#DeltaT (#mus);A. U.",
                     200,0,50)

        labels = "Alpha S2 grass #DeltaT; #DeltaT_{S2-G} (#mus);Entries"
        self.hman.h1("aS2DT",labels,800,0,800)
        
        return 
