# Hpp4lAnalysis.py
# for hpp4l analysis

from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR
from leptonId import passWZLoose, passWZMedium, passWZTight, passHppLoose, passHppMedium, passHppTight

import sys
import itertools
import operator

import ROOT

class Hpp4lAnalysis(AnalysisBase):
    '''
    Hpp4l analysis
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','hpp4lTree.root')
        outputTreeName = kwargs.pop('outputTreeName','Hpp4lTree')
        super(Hpp4lAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup cut tree
        self.cutTree.add(self.fourLoose,'fourLooseLeptons')
        self.cutTree.add(self.trigger,'trigger')

        # setup analysis tree

        # chan string
        self.tree.add(self.getChannelString, 'channel', ['C',5])
        self.tree.add(self.getGenChannelString, 'genChannel', ['C',5])
        self.tree.add(self.getZChannelString, 'zChannel', ['C',3])

        # event counts
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',30), 'numJetsLoose30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',30), 'numJetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',30), 'numBjetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passLoose)), 'numLooseElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passTight)), 'numTightElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passLoose)), 'numLooseMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passTight)), 'numTightMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'taus',self.passLoose)), 'numLooseTaus', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'taus',self.passTight)), 'numTightTaus', 'I')

        # trigger
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZPass'), 'pass_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVLPass'), 'pass_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVLPass'), 'pass_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoMu20Pass'), 'pass_IsoMu20', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoTkMu20Pass'), 'pass_IsoTkMu20', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele23_WPLoose_GsfPass'), 'pass_Ele23_WPLoose_Gsf', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'DoubleMediumIsoPFTau35_Trk1_eta2p1_RegPass'), 'pass_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg', 'I')
        self.tree.add(self.triggerEfficiency, 'triggerEfficiency', 'F')

        # vbf
        self.addJet('leadJet')
        self.addJet('subleadJet')
        self.addDiJet('dijet','leadJet','subleadJet')
        self.tree.add(lambda rtrow,cands: self.numCentralJets(rtrow,cands,'isLoose',30), 'dijet_numCentralJetsLoose30', 'I')
        self.tree.add(lambda rtrow,cands: self.numCentralJets(rtrow,cands,'isTight',30), 'dijet_numCentralJetsTight30', 'I')

        # 3 lepton
        self.addComposite('4l','hpp1','hpp2','hmm1', 'hmm2')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp1'],cands['hpp2'],cands['hmm1'],cands['hmm2']), '4l_zeppenfeld','F')

        # hpp leptons
        self.addDiLepton('hpp','hpp1','hpp2')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp1'],cands['hpp2']), 'hpp_zeppenfeld','F')
        self.addLepton('hpp1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hpp1']), 'hpp1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hpp1']), 'hpp1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['hpp1']), 'hpp1_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['hpp1']), 'hpp1_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['hpp1']), 'hpp1_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['hpp1']), 'hpp1_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['hpp1']), 'hpp1_tightFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp1']), 'hpp1_zeppenfeld','F')
        self.addLepton('hpp2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hpp2']), 'hpp2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hpp2']), 'hpp2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['hpp2']), 'hpp2_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['hpp2']), 'hpp2_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['hpp2']), 'hpp2_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['hpp2']), 'hpp2_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['hpp2']), 'hpp2_tightFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp2']), 'hpp2_zeppenfeld','F')

        # hmm leptons
        self.addDiLepton('hmm','hmm1','hmm2')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm1'],cands['hmm2']), 'hmm_zeppenfeld','F')
        self.addLepton('hmm1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hmm1']), 'hmm1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hmm1']), 'hmm1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['hmm1']), 'hmm1_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['hmm1']), 'hmm1_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['hmm1']), 'hmm1_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm1']), 'hmm1_zeppenfeld','F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['hmm1']), 'hmm1_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['hmm1']), 'hmm1_tightFakeRate', 'F')
        self.addLepton('hmm2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hmm2']), 'hmm2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hmm2']), 'hmm2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['hmm2']), 'hmm2_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['hmm2']), 'hmm2_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['hmm2']), 'hmm2_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm2']), 'hmm2_zeppenfeld','F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['hmm2']), 'hmm2_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['hmm2']), 'hmm2_tightFakeRate', 'F')

        # wrong combination
        self.addDiLepton('hmm1_hpp1','hmm1','hpp1')
        self.addDiLepton('hmm1_hpp2','hmm1','hpp2')
        self.addDiLepton('hmm2_hpp1','hmm2','hpp1')
        self.addDiLepton('hmm2_hpp2','hmm2','hpp2')

        # z leptons
        self.addDiLepton('z','z1','z2')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['z1'],cands['z2']), 'z_zeppenfeld','F')
        self.addLepton('z1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z1']), 'z1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z1']), 'z1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['z1']), 'z1_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['z1']), 'z1_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['z1']), 'z1_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['z1']), 'z1_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['z1']), 'z1_tightFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['z1']), 'z1_zeppenfeld','F')
        self.addLepton('z2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z2']), 'z2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z2']), 'z2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['z2']), 'z2_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['z2']), 'z2_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['z2']), 'z2_tightScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumFakeRate(rtrow,cands['z2']), 'z2_mediumFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.tightFakeRate(rtrow,cands['z2']), 'z2_tightFakeRate', 'F')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['z2']), 'z2_zeppenfeld','F')

        # met
        self.addMet('met',('pfmet',0))

    ############################
    ### select 4l candidates ###
    ############################
    def selectCandidates(self,rtrow):
        candidate = {
            'hpp1' : (),
            'hpp2' : (),
            'hmm1' : (),
            'hmm2' : (),
            'z1' : (),
            'z2' : (),
            'leadJet' : (),
            'subleadJet' : (),
        }

        # get leptons
        colls = ['electrons','muons','taus']
        pts = {}
        etas = {}
        phis = {}
        p4s = {}
        charges = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        medLeps = self.getPassingCands(rtrow,'Medium')
        if len(leps)<4: return candidate # need at least 4 leptons


        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')
            etas[cand] = self.getObjectVariable(rtrow,cand,'eta')
            phis[cand] = self.getObjectVariable(rtrow,cand,'phi')
            p4s[cand] = self.getObjectVariable(rtrow,cand,'p4')
            charges[cand] = self.getObjectVariable(rtrow,cand,'charge')

        # get the candidates
        hppCands = []
        for quad in itertools.permutations(leps,4):
            # require ++--
            if charges[quad[0]]+charges[quad[1]]!=2: continue
            if charges[quad[2]]+charges[quad[3]]!=-2: continue
            # require deltaR seperation of 0.02
            for i,j in itertools.combinations(range(4),2):
                if deltaR(etas[quad[i]],phis[quad[i]],etas[quad[j]],phis[quad[j]])<0.02: continue
            hppCands += [quad]
        if not hppCands: return candidate

        # sort by closest to same mass
        bestMassDiff = 999999999
        bestCand = []
        for quad in hppCands:
            hppMass = self.getCompositeVariable(rtrow,'mass',quad[0],quad[1])
            hmmMass = self.getCompositeVariable(rtrow,'mass',quad[2],quad[3])
            massdiff = abs(hppMass-hmmMass)
            if massdiff<bestMassDiff:
                bestCand = quad
                bestMassDiff = massdiff

        candidate['hpp1'] = bestCand[0] if pts[bestCand[0]]>pts[bestCand[1]] else bestCand[1]
        candidate['hpp2'] = bestCand[1] if pts[bestCand[0]]>pts[bestCand[1]] else bestCand[0]
        candidate['hmm1'] = bestCand[2] if pts[bestCand[2]]>pts[bestCand[3]] else bestCand[3]
        candidate['hmm2'] = bestCand[3] if pts[bestCand[2]]>pts[bestCand[3]] else bestCand[2]

        # add jet
        jets = self.getCands(rtrow, 'jets', lambda rtrow,cand: self.getObjectVariable(rtrow,cand,'isLoose')>0.5)
        if len(jets)==1:
            candidate['leadJet'] = jets[0]
            candidate['subleadJet'] = ('jets',-1)
        if len(jets)>1:
            candidate['leadJet'] = jets[0]
            candidate['subleadJet'] = jets[1]
        else:
            candidate['leadJet'] = ('jets',-1)
            candidate['subleadJet'] = ('jets',-1)

        # do the z alternative combination
        massDiffs = {}
        for zpair in itertools.combinations(pts.keys(),2):
            if zpair[0][0]!=zpair[1][0]: continue # SF
            if charges[zpair[0]]==charges[zpair[1]]: continue # OS
            zp4 = p4s[zpair[0]] + p4s[zpair[1]]
            zmass = zp4.M()
            massDiffs[zpair] = abs(zmass-ZMASS)

        if not massDiffs:
            candidate['z1'] = ('',-1)
            candidate['z2'] = ('',-1)
            return candidate

        # sort by closest z
        bestZ = sorted(massDiffs.items(), key=operator.itemgetter(1))[0][0]

        z1 = bestZ[0] if pts[bestZ[0]] > pts[bestZ[1]] else bestZ[1]
        z2 = bestZ[1] if pts[bestZ[0]] > pts[bestZ[1]] else bestZ[0]

        candidate['z1'] = z1
        candidate['z2'] = z2

        return candidate

    ##################
    ### lepton IDs ###
    ##################
    def passLoose(self,rtrow,cand):
        #return passWZLoose(self,rtrow,cand)
        return passHppLoose(self,rtrow,cand)

    def passMedium(self,rtrow,cand):
        #return passWZMedium(self,rtrow,cand)
        return passHppMedium(self,rtrow,cand)

    def passTight(self,rtrow,cand):
        #return passWZTight(self,rtrow,cand)
        return passHppTight(self,rtrow,cand)

    def looseScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDLooseIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedVeto',cand) # TODO, fix
        else:
            return 1.

    def mediumScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDTightIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedMedium',cand)
        else:
            return 1.

    def tightScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDTightIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedTight',cand)
        else:
            return 1.

    def mediumFakeRate(self,rtrow,cand):
        return self.fakeRates.getFakeRate(rtrow,cand,'WZMedium','WZLoose')

    def tightFakeRate(self,rtrow,cand):
        return self.fakeRates.getFakeRate(rtrow,cand,'WZTight','WZLoose')

    def getPassingCands(self,rtrow,mode):
        if mode=='Loose':
            passMode = self.passLoose
        elif mode=='Medium':
            passMode = self.passMedium
        elif mode=='Tight':
            passMode = self.passTight
        else:
            return []
        cands = []
        for coll in ['electrons','muons','taus']:
            cands += self.getCands(rtrow,coll,passMode)
        return cands

    def numJets(self,rtrow,mode,pt):
        return len(
            self.getCands(
                rtrow,
                'jets',
                lambda rtrow,cand: self.getObjectVariable(rtrow,cand,mode)>0.5 
                                   and self.getObjectVariable(rtrow,cand,'pt')>pt
            )
        )

    def numCentralJets(self,rtrow,cands,mode,pt):
        if cands['leadJet'][1]<0: return -1
        if cands['subleadJet'][1]<0: return -1
        eta1 = self.getObjectVariable(rtrow,cands['leadJet'],'eta')
        eta2 = self.getObjectVariable(rtrow,cands['subleadJet'],'eta')
        mineta = min(eta1,eta2)
        maxeta = max(eta1,eta2)
        return len(
            self.getCands(
                rtrow,
                'jets',
                lambda rtrow,cand: self.getObjectVariable(rtrow,cand,mode)>0.5
                                   and self.getObjectVariable(rtrow,cand,'pt')>pt
                                   and self.getObjectVariable(rtrow,cand,'eta')>mineta
                                   and self.getObjectVariable(rtrow,cand,'eta')<maxeta
            )
        )
    
    def zeppenfeld(self,rtrow,cands,*probeCands):
        if cands['leadJet'][1]<0: return -10.
        if cands['subleadJet'][1]<0: return -10.
        eta1 = self.getObjectVariable(rtrow,cands['leadJet'],'eta')
        eta2 = self.getObjectVariable(rtrow,cands['subleadJet'],'eta')
        meaneta = (eta1+eta2)/2
        if len(probeCands)>1:
            eta = self.getCompositeVariable(rtrow,'eta',*probeCands)
        else:
            eta = self.getObjectVariable(rtrow,probeCands[0],'eta')
        return eta-meaneta

    ######################
    ### channel string ###
    ######################
    def getChannelString(self,rtrow,cands):
        '''Get the channel string'''
        chanString = ''
        for c in ['hpp1','hpp2','hmm1','hmm2']:
            chanString += self.getCollectionString(cands[c])
        return chanString

    def getGenChannelString(self,rtrow,cands):
        '''Get the gen h++ channel'''
        chanString = ''
        pdgMap = {
            11: 'e',
            13: 'm',
            15: 't',
        }
        if 'HPlusPlusHMinusMinusHTo4L' in self.fileNames[0]: # h++h-- signal sample
            for s in [1,-1]:
                h = -1*s*9900041                     # h++ in pythia8
                for l1 in [s*11, s*13, s*15]:        # lepton 1
                    for l2 in [s*11, s*13, s*15]:    # lepton 2
                        if abs(l2)<abs(l1): continue # skip double counting
                        hasDecay = self.findDecay(rtrow,h,l1,l2)
                        if hasDecay:
                            chanString += pdgMap[abs(l1)]
                            chanString += pdgMap[abs(l2)]
        else:
            chanString = 'a'
        return chanString

    def getZChannelString(self,rtrow,cands):
        '''Get the channel string'''
        chanString = ''
        for c in ['z1','z2']:
            if cands[c][1]<0: return 'aa'
            chanString += self.getCollectionString(cands[c])
        return chanString

    ###########################
    ### analysis selections ###
    ###########################
    def fourLoose(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Loose'))>=4

    def trigger(self,rtrow,cands):
        # accept MC, check trigger for data
        if rtrow.isData<0.5: return True
        triggerNames = {
            'DoubleMuon'     : [
                'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
                'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            ],
            'DoubleEG'       : [
                'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            ],
            'MuonEG'         : [
                'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
                'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            ],
            'SingleMuon'     : [
                'IsoMu20',
                'IsoTkMu20',
            ],
            'SingleElectron' : [
                'Ele23_WPLoose_Gsf',
            ],
            'Tau' : [
                'DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg',
            ],
        }
        # the order here defines the heirarchy
        # first dataset, any trigger passes
        # second dataset, if a trigger in the first dataset is found, reject event
        # so forth
        datasets = [
            'DoubleMuon', 
            'DoubleEG', 
            'MuonEG',
            'SingleMuon',
            'SingleElectron',
            'Tau',
        ]
        # reject triggers if they are in another dataset
        # looks for the dataset name in the filename
        # for MC it accepts all
        reject = True if rtrow.isData>0.5 else False
        for dataset in datasets:
            # if we match to the dataset, start accepting triggers
            if dataset in self.fileNames[0]: reject = False
            for trigger in triggerNames[dataset]:
                var = '{0}Pass'.format(trigger)
                passTrigger = self.getTreeVariable(rtrow,var)
                if passTrigger>0.5:
                    # it passed the trigger
                    # in data: reject if it corresponds to a higher dataset
                    return False if reject else True
            # dont check the rest of data
            if dataset in self.fileNames[0]: break
        return False

    def triggerEfficiency(self,rtrow,cands):
        candList = [cands[c] for c in ['hpp1','hpp2','hmm1','hmm2']]
        numTaus = [c[0] for c in candList].count('taus')
        if numTaus<2:
            triggerList = ['IsoMu20_OR_IsoTkMu20','Ele23_WPLoose','Mu17_Mu8','Ele17_Ele12']
        elif numTaus==2:
            triggerList = ['IsoMu20_OR_IsoTkMu20','Ele23_WPLoose','Mu17_Mu8','Ele17_Ele12','DoublePFTau35']
        elif numTaus==3:
            triggerList = ['IsoMu20_OR_IsoTkMu20','Ele23_WPLoose','DoublePFTau35']
        else:
            triggerList = ['DoublePFTau35']
        return self.triggerScales.getDataEfficiency(rtrow,triggerList,candList)









