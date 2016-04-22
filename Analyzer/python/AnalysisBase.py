# AnalysisBase.py

import logging
import os
import sys
import math
import time

sys.argv.append('-b')
import ROOT
sys.argv.pop()
from array import array

from CutTree import CutTree
from AnalysisTree import AnalysisTree

from PileupWeights import PileupWeights
from FakeRates import FakeRates
from LeptonScales import LeptonScales
from TriggerScales import TriggerScales
from TriggerPrescales import TriggerPrescales

from utilities import deltaR, deltaPhi

try:
    from progressbar import ProgressBar, ETA, Percentage, Bar, SimpleProgress
    hasProgress = True
except:
    hasProgress = False

class AnalysisBase(object):
    '''
    Analysis Tree
    '''

    def __init__(self,**kwargs):
        inputFileNames = kwargs.pop('inputFileNames',[])
        inputTreeDirectory = kwargs.pop('inputTreeDirectory','miniTree')
        inputTreeName = kwargs.pop('inputTreeName','MiniTree')
        inputLumiName = kwargs.pop('inputTreeName','LumiTree')
        outputFileName = kwargs.pop('outputFileName','analysisTree.root')
        outputTreeName = kwargs.pop('outputTreeName','AnalysisTree')
        if hasProgress:
            self.pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(outputTreeName),' ',SimpleProgress(),' events ',Percentage(),' ',Bar(),' ',ETA()]))
        # input files
        self.fileNames = []
        if isinstance(inputFileNames, basestring): # inputFiles is a file name
            if os.path.isfile(inputFileNames):     # single file
                if inputFileNames[-4:] == 'root':  # file is a root file
                    self.fileNames += [inputFileNames]
                else:                          # file is list of files
                    with open(inputFileNames,'r') as f:
                        for line in f:
                            self.fileNames += [line.strip()]
        else:
            self.fileNames = inputFileNames # already a python list or a cms.untracked.vstring()
        if not isinstance(outputFileName, basestring): # its a cms.string(), get value
            outputFileName = outputFileName.value()
        # input tchain
        self.treename = '{0}/{1}'.format(inputTreeDirectory,inputTreeName)
        tchainLumi = ROOT.TChain('{0}/{1}'.format(inputTreeDirectory,inputLumiName))
        self.totalEntries = 0
        logging.info('Getting Lumi information')
        for fName in self.fileNames:
            if fName.startswith('/store'): fName = 'root://cmsxrootd.hep.wisc.edu//{0}'.format(fName)
            tfile = ROOT.TFile.Open(fName)
            tree = tfile.Get(self.treename)
            self.totalEntries += tree.GetEntries()
            tfile.Close('R')
            tchainLumi.Add(fName)
        # get the lumi info
        self.numLumis = tchainLumi.GetEntries()
        self.numEvents = 0
        self.summedWeights = 0
        for entry in xrange(self.numLumis):
            tchainLumi.GetEntry(entry)
            self.numEvents += tchainLumi.nevents
            self.summedWeights += tchainLumi.summedWeights
        logging.info("Will process {0} lumi sections with {1} events ({2}).".format(self.numLumis,self.numEvents,self.summedWeights))
        self.flush()
        # other input files
        self.pileupWeights = PileupWeights()
        self.fakeRates = FakeRates()
        self.leptonScales = LeptonScales()
        self.triggerScales = TriggerScales()
        self.triggerPrescales = TriggerPrescales()
        # tfile
        self.outfile = ROOT.TFile(outputFileName,"recreate")
        # cut tree
        self.cutTree = CutTree()
        # analysis tree
        self.tree = AnalysisTree(outputTreeName)
        self.eventsStored = 0

        # some things we always need:
        # pileup
        self.tree.add(lambda rtrow,cands: self.pileupWeights.weight(rtrow)[0], 'pileupWeight', 'F')
        self.tree.add(lambda rtrow,cands: self.pileupWeights.weight(rtrow)[1], 'pileupWeightUp', 'F')
        self.tree.add(lambda rtrow,cands: self.pileupWeights.weight(rtrow)[2], 'pileupWeightDown', 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'vertices_count'), 'numVertices', 'I')

        # gen
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'nTrueVertices'), 'numTrueVertices', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'NUP'), 'NUP', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'isData'), 'isData', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'genWeight'), 'genWeight', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'numGenJets'), 'numGenJets', 'I')
        # scale shifts
        weightMap = {
            0: {'muR':1.0, 'muF':1.0},
            1: {'muR':1.0, 'muF':2.0},
            2: {'muR':1.0, 'muF':0.5},
            3: {'muR':2.0, 'muF':1.0},
            4: {'muR':2.0, 'muF':2.0},
            5: {'muR':2.0, 'muF':0.5},
            6: {'muR':0.5, 'muF':1.0},
            7: {'muR':0.5, 'muF':2.0},
            8: {'muR':0.5, 'muF':0.5},
        }
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',0), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[0]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',1), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[1]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',2), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[2]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',3), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[3]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',4), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[4]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',5), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[5]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',6), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[6]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',7), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[7]), 'F')
        self.tree.add(lambda rtrow,cands: self.getTreeVectorVariable(rtrow,'genWeights',8), 'genWeight_muR{muR:3.1f}_muF{muF:3.1f}'.format(**weightMap[8]), 'F')


    def __exit__(self, type, value, traceback):
        self.finish()

    def __del__(self):
        self.finish()

    def finish(self):
        logging.info('Finishing')
        logging.info('Writing {0} events'.format(self.eventsStored))
        self.outfile.cd()
        cutflowHist = ROOT.TH1F('summedWeights','summedWeights',1,0,1)
        cutflowHist.SetBinContent(1,self.summedWeights)
        self.outfile.Write()
        self.outfile.Close()
        self.leptonScales.finish()

    def flush(self):
        sys.stdout.flush()
        sys.stderr.flush()

    #############################
    ### primary analysis loop ###
    #############################
    def analyze(self):
        '''
        The primary analyzer loop.
        '''
        logging.info('Beginning Analysis')
        start = time.time()
        new = start
        old = start
        if hasProgress:
            self.pbar.maxval = self.totalEntries
            self.pbar.start()
            total = 0
            for f, fName in enumerate(self.fileNames):
                if fName.startswith('/store'): fName = 'root://cmsxrootd.hep.wisc.edu//{0}'.format(fName)
                tfile = ROOT.TFile.Open(fName,'READ')
                tree = tfile.Get(self.treename)
                treeEvents = tree.GetEntries()
                rtrow = tree
                for r in xrange(treeEvents):
                    total += 1
                    rtrow.GetEntry(r)
                    self.pbar.update(total)
                    self.perRowAction(rtrow)
                tfile.Close('R')
        else:
            total = 0
            for f, fName in enumerate(self.fileNames):
                if fName.startswith('/store'): fName = 'root://cmsxrootd.hep.wisc.edu//{0}'.format(fName)
                logging.info('Processing file {0} of {1}'.format(f+1, len(self.fileNames)))
                tfile = ROOT.TFile.Open(fName,'READ')
                tree = tfile.Get(self.treename)
                treeEvents = tree.GetEntries()
                rtrow = tree
                for r in xrange(treeEvents):
                    total += 1
                    if total==2: start = time.time() # just ignore first event for timing
                    rtrow.GetEntry(r)
                    if total % 1000 == 1:
                        cur = time.time()
                        elapsed = cur-start
                        remaining = float(elapsed)/total * float(self.totalEntries) - float(elapsed)
                        mins, secs = divmod(int(remaining),60)
                        hours, mins = divmod(mins,60)
                        logging.info('Processing event {0}/{1} - {2}:{3:02d}:{4:02d} remaining'.format(total,self.totalEntries,hours,mins,secs))
                        self.flush()
                    self.perRowAction(rtrow)
                tfile.Close('R')

    def perRowAction(self,rtrow):
        '''Per row action, can be overridden'''
        # select candidates
        cands = self.selectCandidates(rtrow)

        # store event?
        goodToStore = self.cutTree.evaluate(rtrow,cands)

        # do we store the tree?
        if not goodToStore: return

        self.tree.fill(rtrow,cands)
        self.eventsStored += 1
        #self.outfile.Flush()

    def selectCandidates(self,rtrow):
        '''
        Select candidates
            format should be:
            candidates = {
                "objectName" : ("collectionName", position),
                ...
            }
        '''
        logging.warning("You must override selectCandidates.")
        return {}

    #################
    ### utilities ###
    #################
    def findDecay(self,rtrow,m_pdgid,d1_pdgid,d2_pdgid):
        '''Check if requested decay present in event'''
        for g in range(rtrow.genParticles_count):
            if m_pdgid==rtrow.genParticles_pdgId[g]:
                if (
                    (d1_pdgid==rtrow.genParticles_daughter_1[g]
                    and d2_pdgid==rtrow.genParticles_daughter_2[g])
                    or (d1_pdgid==rtrow.genParticles_daughter_2[g]
                    and d2_pdgid==rtrow.genParticles_daughter_1[g])
                   ):
                    return True
        return False

    ########################
    ### object variables ###
    ########################
    def getObjectVariable(self, rtrow, cand, var):
        '''
        Simple utility to get variables
        '''
        if len(cand)!=2:
            return 0
        coll, pos = cand
        key = '{0}_{1}_{2}'.format(coll,var,pos)

        # get a TLorentzVector
        if var=='p4':
            pt     = self.getObjectVariable(rtrow,cand,'pt')
            eta    = self.getObjectVariable(rtrow,cand,'eta')
            phi    = self.getObjectVariable(rtrow,cand,'phi')
            energy = self.getObjectVariable(rtrow,cand,'energy')
            val = ROOT.TLorentzVector()
            val.SetPtEtaPhiE(pt,eta,phi,energy)
            return val
        elif var=='p4_uncorrected':
            pt     = self.getObjectVariable(rtrow,cand,'pt_uncorrected')
            eta    = self.getObjectVariable(rtrow,cand,'eta_uncorrected')
            phi    = self.getObjectVariable(rtrow,cand,'phi_uncorrected')
            energy = self.getObjectVariable(rtrow,cand,'energy_uncorrected')
            val = ROOT.TLorentzVector()
            val.SetPtEtaPhiE(pt,eta,phi,energy)
            return val

        # if invalid, return 0
        elif pos<0:
            val = 0
            return val

        # override muon pt/eta/phi/energy for rochester correction
        elif coll=='muons' and var in ['pt','eta','phi','energy']:
            val = getattr(rtrow,'{0}_rochester{1}'.format(coll,var.capitalize()))[pos]
            return val
        elif coll=='muons' and var in ['pt_uncorrected','eta_uncorrected','phi_uncorrected','energy_uncorrected']:
            val = getattr(rtrow,'{0}_{1}'.format(coll,var.split('_')[0]))[pos]
            return val

        # the variable is in the input tree
        elif hasattr(rtrow,'{0}_{1}'.format(coll,var)):
            val = getattr(rtrow,'{0}_{1}'.format(coll,var))[pos]
            return val


        # didnt catch it
        else:
            val = 0
            return val

        return val

    def getCompositeVariable(self,rtrow,var,*cands,**kwargs):
        '''Create a composite candidate'''
        uncorrected = kwargs.pop('uncorrected',False)

        vec = ROOT.TLorentzVector()
        components = []
        p4Name = 'p4_uncorrected' if uncorrected else 'p4'
        for cand in cands:
            candp4 = self.getObjectVariable(rtrow,cand,p4Name)
            components += [candp4]
            vec += candp4

        if var=='p4':
            val = vec
            return val
        elif var in ['mass','Mass','m','M']:
            val = vec.M()
            return val
        elif var in ['pt','Pt']:
            val = vec.Pt()
            return val
        elif var in ['eta','Eta']:
            val = vec.Eta()
            return val
        elif var in ['phi','Phi']:
            val = vec.Phi()
            return val
        elif var in ['energy','Energy']:
            val = vec.Energy()
            return val
        elif len(cands)==2:
            if var in ['deltaR','dR','dr','DR']:
                eta1 = self.getObjectVariable(rtrow,cands[0],'eta')
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                eta2 = self.getObjectVariable(rtrow,cands[1],'eta')
                phi2 = self.getObjectVariable(rtrow,cands[1],'phi')
                val = deltaR(eta1,phi1,eta2,phi2)
                return val
            elif var in ['deltaPhi','dPhi','dphi','DPhi']:
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                phi2 = self.getObjectVariable(rtrow,cands[1],'phi')
                val = deltaPhi(phi1,phi2)
                return val
            elif var in ['deltaEta','dEta','deta','DEta']:
                eta1 = self.getObjectVariable(rtrow,cands[0],'eta')
                eta2 = self.getObjectVariable(rtrow,cands[1],'eta')
                val = abs(eta1-eta2)
                return val
            else:
                val = 0
                return val
        else:
            val = 0
            return val

        return val

    def getCompositeMetVariable(self,rtrow,var,met,*cands,**kwargs):
        '''Get composite met variables'''

        candVec = self.getCompositeVariable(rtrow,'p4',*cands)

        metVec = ROOT.TLorentzVector()
        metPt = self.getObjectVariable(rtrow,met,'et')
        metPhi = self.getObjectVariable(rtrow,met,'phi')
        metVec.SetPtEtaPhiM(metPt,0,metPhi,0)

        vec = candVec + metVec

        if var=='p4':
            val = vec
            return val
        elif var in ['mt','Mt','mT','MT']:
            #val = math.sqrt(2*candVec.Pt()*metPt*(1-math.cos(deltaPhi(candVec.Phi(),metPhi))))
            val = math.sqrt(abs((candVec.Et()+metVec.Et())**2 - (vec.Pt())**2))
            return val
        elif var in ['mass','Mass','m','M']:
            val = vec.M()
            return val
        elif var in ['pt','Pt']:
            val = vec.Pt()
            return val
        elif var in ['eta','Eta']:
            val = vec.Eta()
            return val
        elif var in ['phi','Phi']:
            val = vec.Phi()
            return val
        elif var in ['energy','Energy']:
            val = vec.Energy()
            return val
        elif len(cands)==1:
            if var in ['deltaPhi','dPhi','dphi','DPhi']:
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                phi2 = metPhi
                val = deltaPhi(phi1,phi2)
                return val
            else:
                val = 0
                return val
        else:
            val = 0
            return val

        return val

    def getTreeVectorVariable(self, rtrow, var, pos):
        '''
        Get event wide variables
        '''
        if hasattr(rtrow,var):
            val = getattr(rtrow,var)[pos] if len(getattr(rtrow,var))>pos else 0
        else:
            val = 0
            logging.info("{0} not found.".format(var))

        return val


    def getTreeVariable(self, rtrow, var):
        '''
        Get event wide variables
        '''
        if hasattr(rtrow,var):
            val = getattr(rtrow,var)
        else:
            val = 0
            logging.info("{0} not found.".format(var))

        return val

    def getCands(self,rtrow,coll,func):
        cands = []
        numColl = getattr(rtrow,'{0}_count'.format(coll))
        for c in range(numColl):
            cand = (coll,c)
            if func(rtrow,cand): cands += [cand]
        return cands

    def getCollectionString(self,cand):
        if cand[0]=='electrons': return 'e'
        elif cand[0]=='muons':   return 'm'
        elif cand[0]=='taus':    return 't'
        elif cand[0]=='photons': return 'g'
        elif cand[0]=='jets':    return 'j'
        else:                    return 'a'

    ##########################
    ### add object to tree ###
    ##########################
    def addMet(self,label,met):
        '''Add Met variables'''
        self.addMetVar(label,met,'pt','et','F')
        self.addMetVar(label,met,'phi','phi','F')

    def addMetVar(self,label,met,varLabel,var,rootType):
        '''Add a single met var'''
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,met,var), '{0}_{1}'.format(label,varLabel), rootType)

    def addJet(self,label):
        '''Add variables relevant for jets'''
        self.addCandVar(label,'pt','pt','F')
        self.addCandVar(label,'eta','eta','F')
        self.addCandVar(label,'phi','phi','F')
        self.addCandVar(label,'energy','energy','F')

    def addLepton(self,label):
        '''Add variables relevant for leptons'''
        self.addCandVar(label,'pt','pt','F')
        self.addCandVar(label,'eta','eta','F')
        self.addCandVar(label,'phi','phi','F')
        self.addCandVar(label,'energy','energy','F')
        self.addCandVar(label,'charge','charge','I')
        self.addCandVar(label,'dz','dz','F')
        self.addFlavorDependentCandVar(label,'dxy',      {'electrons':'dB2D',          'muons':'dB2D', 'taus':'dxy',  '':''},'F')
        self.addFlavorDependentCandVar(label,'isolation',{'electrons':'relPFIsoRhoR03','muons':'relPFIsoDeltaBetaR04','':''},'F')
        self.addFlavorDependentCandVar(label,'genMatch',       {'electrons':'genMatch',       'muons':'genMatch',  'taus':'genJetMatch', '':''},'I')
        self.tree.add(lambda rtrow,cands: self.genDeltaR(rtrow,cands[label]) if cands[label][0] in ['electrons','muons'] else self.genJetDeltaR(rtrow,cands[label]), '{0}_genDeltaR'.format(label), 'F')
        self.addFlavorDependentCandVar(label,'genStatus',      {'electrons':'genStatus',      'muons':'genStatus', 'taus':'genJetStatus','':''},'I')
        self.addFlavorDependentCandVar(label,'genPdgId',       {'electrons':'genPdgId',       'muons':'genPdgId',  'taus':'genJetPdgId', '':''},'I')
        self.addFlavorDependentCandVar(label,'genPt',          {'electrons':'genPt',          'muons':'genPt',     'taus':'genJetPt',    '':''},'F')
        self.addFlavorDependentCandVar(label,'genEta',         {'electrons':'genEta',         'muons':'genEta',    'taus':'genJetEta',   '':''},'F')
        self.addFlavorDependentCandVar(label,'genPhi',         {'electrons':'genPhi',         'muons':'genPhi',    'taus':'genJetPhi',   '':''},'F')
        self.addFlavorDependentCandVar(label,'genEnergy',      {'electrons':'genEnergy',      'muons':'genEnergy', 'taus':'genJetEnergy','':''},'F')
        self.addFlavorDependentCandVar(label,'genCharge',      {'electrons':'genCharge',      'muons':'genCharge', 'taus':'genJetCharge','':''},'I')
        self.addFlavorDependentCandVar(label,'genIsPrompt',    {'electrons':'genIsPrompt',    'muons':'genIsPrompt',    '':''},'I')
        self.addFlavorDependentCandVar(label,'genIsFromTau',   {'electrons':'genIsFromTau',   'muons':'genIsFromTau',   '':''},'I')
        self.addFlavorDependentCandVar(label,'genIsFromHadron',{'electrons':'genIsFromHadron','muons':'genIsFromHadron','':''},'I')

    def genDeltaR(self,rtrow,cand):
        '''Get the gen level deltaR'''
        if self.getObjectVariable(rtrow,cand,'genMatch')==0: return 0.
        eta = self.getObjectVariable(rtrow,cand,'eta')
        genEta = self.getObjectVariable(rtrow,cand,'genEta')
        phi = self.getObjectVariable(rtrow,cand,'phi')
        genPhi = self.getObjectVariable(rtrow,cand,'genPhi')
        return deltaR(eta,phi,genEta,genPhi)

    def genJetDeltaR(self,rtrow,cand):
        '''Get the gen level deltaR'''
        if self.getObjectVariable(rtrow,cand,'genJetMatch')==0: return 0.
        eta = self.getObjectVariable(rtrow,cand,'eta')
        genEta = self.getObjectVariable(rtrow,cand,'genJetEta')
        phi = self.getObjectVariable(rtrow,cand,'phi')
        genPhi = self.getObjectVariable(rtrow,cand,'genJetPhi')
        return deltaR(eta,phi,genEta,genPhi)

    def addCandVar(self,label,varLabel,var,rootType):
        '''Add a variable for a cand'''
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],var), '{0}_{1}'.format(label,varLabel), rootType)

    def addFlavorDependentCandVar(self,label,varLabel,varMap,rootType):
        '''Add a variable for a cand based on flavor'''
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],varMap[cands[label][0]]) if cands[label][0] in varMap else 0., '{0}_{1}'.format(label,varLabel), rootType)

    def addDiJet(self,label,obj1,obj2):
        '''Add variables relevant for a dijet candidate'''
        self.addDiCandVar(label,obj1,obj2,'mass','mass','F')
        self.addDiCandVar(label,obj1,obj2,'pt','pt','F')
        self.addDiCandVar(label,obj1,obj2,'eta','eta','F')
        self.addDiCandVar(label,obj1,obj2,'phi','phi','F')
        self.addDiCandVar(label,obj1,obj2,'deltaR','deltaR','F')
        self.addDiCandVar(label,obj1,obj2,'deltaEta','deltaEta','F')
        self.addDiCandVar(label,obj1,obj2,'deltaPhi','deltaPhi','F')
        self.addDiCandVar(label,obj1,obj2,'energy','energy','F')

    def addDiLepton(self,label,obj1,obj2):
        '''Add variables relevant for a dilepton candidate'''
        self.addDiCandVar(label,obj1,obj2,'mass','mass','F')
        self.addDiCandVar(label,obj1,obj2,'pt','pt','F')
        self.addDiCandVar(label,obj1,obj2,'eta','eta','F')
        self.addDiCandVar(label,obj1,obj2,'phi','phi','F')
        self.addDiCandVar(label,obj1,obj2,'deltaR','deltaR','F')
        self.addDiCandVar(label,obj1,obj2,'deltaEta','deltaEta','F')
        self.addDiCandVar(label,obj1,obj2,'deltaPhi','deltaPhi','F')
        self.addDiCandVar(label,obj1,obj2,'energy','energy','F')

    def addDiCandVar(self,label,obj1,obj2,varLabel,var,rootType,**kwargs):
        '''Add a variable for a dilepton candidate'''
        self.tree.add(lambda rtrow,cands: self.getCompositeVariable(rtrow,var,cands[obj1],cands[obj2],**kwargs), '{0}_{1}'.format(label,varLabel), rootType)

    def addLeptonMet(self,label,obj,met):
        '''Add variables related to a lepton + met'''
        self.addCandMetVar(label,obj,met,'mass','mass','F')
        self.addCandMetVar(label,obj,met,'pt','pt','F')
        self.addCandMetVar(label,obj,met,'eta','eta','F')
        self.addCandMetVar(label,obj,met,'deltaPhi','deltaPhi','F')
        self.addCandMetVar(label,obj,met,'mt','mt','F')

    def addCandMetVar(self,label,obj,met,varLabel,var,rootType,**kwargs):
        '''Add a single lepton met var'''
        self.tree.add(lambda rtrow,cands: self.getCompositeMetVariable(rtrow,var,met,cands[obj],**kwargs), '{0}_{1}'.format(label,varLabel), rootType)

    def addComposite(self,label,*objs):
        '''Add variables realated to multi object variables'''
        self.addCompositeVar(label,objs,'mass','mass','F')
        self.addCompositeVar(label,objs,'pt','pt','F')
        self.addCompositeVar(label,objs,'eta','eta','F')
        self.addCompositeVar(label,objs,'phi','phi','F')
        self.addCompositeVar(label,objs,'energy','energy','F')

    def addCompositeVar(self,label,objs,varLabel,var,rootType,**kwargs):
        '''Add single variable for multiple objects'''
        self.tree.add(lambda rtrow,cands: self.getCompositeVariable(rtrow,var,*[cands[obj] for obj in objs],**kwargs), '{0}_{1}'.format(label,varLabel), rootType)

