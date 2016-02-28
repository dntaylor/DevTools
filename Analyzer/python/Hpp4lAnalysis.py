# Hpp4lAnalysis.py
# for hpp4l analysis

from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR
from leptonId import passWZLoose, passWZMedium, passWZTight

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
        self.tree.add(self.getWZChannelString, 'zChannel', ['C',3])

        # event counts
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',15), 'numJetsLoose15', 'I')
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',15), 'numJetsTight15', 'I')
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',15), 'numBjetsTight15', 'I')
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',20), 'numJetsLoose20', 'I')
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',20), 'numJetsTight20', 'I')
        #self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',20), 'numBjetsTight20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',30), 'numJetsLoose30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',30), 'numJetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',30), 'numBjetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passLoose)), 'numLooseElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passMedium)), 'numMediumElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passTight)), 'numTightElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passLoose)), 'numLooseMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passMedium)), 'numMediumMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passTight)), 'numTightMuons', 'I')

        # pileup
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'vertices_count'), 'numVertices', 'I')

        # gen
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'nTrueVertices'), 'numTrueVertices', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'NUP'), 'NUP', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'isData'), 'isData', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'genWeight'), 'genWeight', 'I')

        # trigger
        triggers = [
            'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
            'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
            'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            'IsoMu20',
            'IsoTkMu20',
            'IsoMu27',
            'Ele23_WPLoose_Gsf',
        ]
        for trigger in triggers:
            self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'{0}Pass'.format(trigger)), 'pass{0}'.format(trigger), 'I')

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
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp1']), 'hpp1_zeppenfeld','F')
        self.addLepton('hpp2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hpp2']), 'hpp2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hpp2']), 'hpp2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hpp2']), 'hpp2_zeppenfeld','F')

        # hmm leptons
        self.addDiLepton('hmm','hmm1','hmm2')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm1'],cands['hmm2']), 'hmm_zeppenfeld','F')
        self.addLepton('hmm1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hmm1']), 'hmm1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hmm1']), 'hmm1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm1']), 'hmm1_zeppenfeld','F')
        self.addLepton('hmm2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['hmm2']), 'hmm2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['hmm2']), 'hmm2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['hmm2']), 'hmm2_zeppenfeld','F')

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
        self.tree.add(lambda rtrow,cands: self.zeppenfeld(rtrow,cands,cands['z1']), 'z1_zeppenfeld','F')
        self.addLepton('z2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z2']), 'z2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z2']), 'z2_passTight', 'I')
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
        colls = ['electrons','muons']
        pts = {}
        p4s = {}
        charges = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        medLeps = self.getPassingCands(rtrow,'Medium')
        if len(leps)<4: return candidate # need at least 4 leptons


        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')
            p4s[cand] = self.getObjectVariable(rtrow,cand,'p4')
            charges[cand] = self.getObjectVariable(rtrow,cand,'charge')

        # get the candidates
        hppCands = []
        for quad in itertools.permutations(leps,4):
            if charges[quad[0]]+charges[quad[1]]!=2: continue
            if charges[quad[2]]+charges[quad[3]]!=-2: continue
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
    # TODO: these are still WZ
    def passLoose(self,rtrow,cand):
        return passWZLoose(self,rtrow,cand)

    def passMedium(self,rtrow,cand):
        return passWZMedium(self,rtrow,cand)

    def passTight(self,rtrow,cand):
        return passWZTight(self,rtrow,cand)

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
        for coll in ['electrons','muons']:
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

    def getWZChannelString(self,rtrow,cands):
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
                'IsoMu27',
            ],
            'SingleElectron' : [
                'Ele23_WPLoose_Gsf',
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
        return False











