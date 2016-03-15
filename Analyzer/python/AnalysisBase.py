# AnalysisBase.py

import logging
import os
import sys
import math
import time

import ROOT
from array import array

from CutTree import CutTree
from AnalysisTree import AnalysisTree

from PileupWeights import PileupWeights
from LeptonScales import LeptonScales

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
        self.tchain = ROOT.TChain('{0}/{1}'.format(inputTreeDirectory,inputTreeName))
        tchainLumi = ROOT.TChain('{0}/{1}'.format(inputTreeDirectory,inputLumiName))
        for fName in self.fileNames:
            if fName.startswith('/store'): fName = 'root://cmsxrootd.hep.wisc.edu//{0}'.format(fName)
            self.tchain.Add(fName)
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
        self.leptonScales = LeptonScales()
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
        treeEvents = self.tchain.GetEntries()
        rtrow = self.tchain
        if hasProgress:
            for r in self.pbar(xrange(treeEvents)):
                rtrow.GetEntry(r)
                self.perRowAction(rtrow)
        else:
            for r in xrange(treeEvents):
                if r==2: start = time.time() # just ignore first event for timing
                rtrow.GetEntry(r)
                if r % 1000 == 1:
                    cur = time.time()
                    elapsed = cur-start
                    remaining = float(elapsed)/r * float(treeEvents) - float(elapsed)
                    mins, secs = divmod(int(remaining),60)
                    hours, mins = divmod(mins,60)
                    logging.info('Processing event {0}/{1} - {2}:{3:02d}:{4:02d} remaining'.format(r,treeEvents,hours,mins,secs))
                    self.flush()

                self.perRowAction(rtrow)

    def perRowAction(self,rtrow):
        '''Per row action, can be overridden'''
        self.cache = {} # cache variables so you dont read from tree as much

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
        if key in self.cache: return self.cache[key]

        # get a TLorentzVector
        if var=='p4':
            pt     = self.getObjectVariable(rtrow,cand,'pt')
            eta    = self.getObjectVariable(rtrow,cand,'eta')
            phi    = self.getObjectVariable(rtrow,cand,'phi')
            energy = self.getObjectVariable(rtrow,cand,'energy')
            val = ROOT.TLorentzVector()
            val.SetPtEtaPhiE(pt,eta,phi,energy)

        # if invalid, return 0
        elif pos<0:
            val = 0

        # override muon pt/eta/phi/energy for rochester correction
        elif coll=='muons' and var in ['pt','eta','phi','energy']:
            val = getattr(rtrow,'{0}_rochester{1}'.format(coll,var.capitalize()))[pos]
        elif coll=='muons' and var in ['pt_uncorrected','eta_uncorrected','phi_uncorrected','energy_uncorrected']:
            val = getattr(rtrow,'{0}_{1}'.format(coll,var.split('_')[0]))[pos]

        # the variable is in the input tree
        elif hasattr(rtrow,'{0}_{1}'.format(coll,var)):
            val = getattr(rtrow,'{0}_{1}'.format(coll,var))[pos]


        # didnt catch it
        else:
            val = 0

        self.cache[key] = val
        return val

    def getCompositeVariable(self,rtrow,var,*cands):
        '''Create a composite candidate'''

        key = '_'.join(['{0}_{1}'.format(*cand) for cand in cands] + [var])
        if key in self.cache: return self.cache[key]

        vec = ROOT.TLorentzVector()
        for cand in cands:
            vec += self.getObjectVariable(rtrow,cand,'p4')

        if var=='p4':
            val = vec
        elif var in ['mass','Mass','m','M']:
            val = vec.M()
        elif var in ['pt','Pt']:
            val = vec.Pt()
        elif var in ['eta','Eta']:
            val = vec.Eta()
        elif var in ['phi','Phi']:
            val = vec.Phi()
        elif var in ['energy','Energy']:
            val = vec.Energy()
        elif len(cands)==2:
            if var in ['deltaR','dR','dr','DR']:
                eta1 = self.getObjectVariable(rtrow,cands[0],'eta')
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                eta2 = self.getObjectVariable(rtrow,cands[1],'eta')
                phi2 = self.getObjectVariable(rtrow,cands[1],'phi')
                val = deltaR(eta1,phi1,eta2,phi2)
            elif var in ['deltaPhi','dPhi','dphi','DPhi']:
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                phi2 = self.getObjectVariable(rtrow,cands[1],'phi')
                val = deltaPhi(phi1,phi2)
            elif var in ['deltaEta','dEta','deta','DEta']:
                eta1 = self.getObjectVariable(rtrow,cands[0],'eta')
                eta2 = self.getObjectVariable(rtrow,cands[1],'eta')
                val = abs(eta1-eta2)
            else:
                val = 0
        else:
            val = 0

        self.cache[key] = val
        return val

    def getCompositeMetVariable(self,rtrow,var,met,*cands):
        '''Get composite met variables'''

        key = '_'.join(['{0}_{1}'.format(*cand) for cand in cands] + ['{0}_{1}'.format(*met)] + [var])
        if key in self.cache: return self.cache[key]

        candVec = self.getCompositeVariable(rtrow,'p4',*cands)

        metVec = ROOT.TLorentzVector()
        metPt = self.getObjectVariable(rtrow,met,'et')
        metPhi = self.getObjectVariable(rtrow,met,'phi')
        metVec.SetPtEtaPhiM(metPt,0,metPhi,0)

        vec = candVec + metVec

        if var=='p4':
            val = vec
        elif var in ['mt','Mt','mT','MT']:
            #val = math.sqrt(2*candVec.Pt()*metPt*(1-math.cos(deltaPhi(candVec.Phi(),metPhi))))
            val = math.sqrt(abs((candVec.Et()+metVec.Et())**2 - (vec.Pt())**2))
        elif var in ['mass','Mass','m','M']:
            val = vec.M()
        elif var in ['pt','Pt']:
            val = vec.Pt()
        elif var in ['eta','Eta']:
            val = vec.Eta()
        elif var in ['phi','Phi']:
            val = vec.Phi()
        elif var in ['energy','Energy']:
            val = vec.Energy()
        elif len(cands)==1:
            if var in ['deltaPhi','dPhi','dphi','DPhi']:
                phi1 = self.getObjectVariable(rtrow,cands[0],'phi')
                phi2 = metPhi
                val = deltaPhi(phi1,phi2)
            else:
                val = 0
        else:
            val = 0

        self.cache[key] = val
        return val


    def getTreeVariable(self, rtrow, var):
        '''
        Get event wide variables
        '''
        key = var
        if key in self.cache: return self.cache[key]

        if hasattr(rtrow,var):
            val = getattr(rtrow,var)
        else:
            val = 0
            logging.info("{0} not found.".format(var))

        self.cache[key] = val
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
        #self.addCandVar(label,'dxy','dxy','F')
        self.addFlavorDependentCandVar(label,'dxy',{'electrons':'dB2D','muons':'dB2D','taus':'dxy','':''},'F')
        self.addCandVar(label,'genMatch','genMatch','I')
        self.tree.add(lambda rtrow,cands: self.genDeltaR(rtrow,cands[label]), '{0}_genDeltaR'.format(label), 'F')
        self.addCandVar(label,'genStatus','genStatus','I')
        self.addCandVar(label,'genPdgId','genPdgId','I')
        self.addCandVar(label,'genPt','genPt','F')
        self.addCandVar(label,'genEta','genEta','F')
        self.addCandVar(label,'genPhi','genPhi','F')
        self.addCandVar(label,'genEnergy','genEnergy','F')
        self.addCandVar(label,'genCharge','genCharge','I')
        self.addCandVar(label,'genIsPrompt','genIsPrompt','I')
        self.addCandVar(label,'genIsFromTau','genIsFromTau','I')
        self.addCandVar(label,'genIsFromHadron','genIsFromHadron','I')
        self.addFlavorDependentCandVar(label,'isolation',{'electrons':'relPFIsoRhoR03','muons':'relPFIsoDeltaBetaR04','':''},'F')

    def genDeltaR(self,rtrow,cand):
        '''Get the gen level deltaR'''
        eta = self.getObjectVariable(rtrow,cand,'eta')
        genEta = self.getObjectVariable(rtrow,cand,'genEta')
        phi = self.getObjectVariable(rtrow,cand,'phi')
        genPhi = self.getObjectVariable(rtrow,cand,'genPhi')
        return deltaR(eta,phi,genEta,genPhi)

    def addCandVar(self,label,varLabel,var,rootType):
        '''Add a variable for a cand'''
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],var), '{0}_{1}'.format(label,varLabel), rootType)

    def addFlavorDependentCandVar(self,label,varLabel,varMap,rootType):
        '''Add a variable for a cand based on flavor'''
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],varMap[cands[label][0]]), '{0}_{1}'.format(label,varLabel), rootType)

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

    def addDiCandVar(self,label,obj1,obj2,varLabel,var,rootType):
        '''Add a variable for a dilepton candidate'''
        self.tree.add(lambda rtrow,cands: self.getCompositeVariable(rtrow,var,cands[obj1],cands[obj2]), '{0}_{1}'.format(label,varLabel), rootType)

    def addLeptonMet(self,label,obj,met):
        '''Add variables related to a lepton + met'''
        self.addCandMetVar(label,obj,met,'mass','mass','F')
        self.addCandMetVar(label,obj,met,'pt','pt','F')
        self.addCandMetVar(label,obj,met,'eta','eta','F')
        self.addCandMetVar(label,obj,met,'deltaPhi','deltaPhi','F')
        self.addCandMetVar(label,obj,met,'mt','mt','F')

    def addCandMetVar(self,label,obj,met,varLabel,var,rootType):
        '''Add a single lepton met var'''
        self.tree.add(lambda rtrow,cands: self.getCompositeMetVariable(rtrow,var,met,cands[obj]), '{0}_{1}'.format(label,varLabel), rootType)

    def addComposite(self,label,*objs):
        '''Add variables realated to multi object variables'''
        self.addCompositeVar(label,objs,'mass','mass','F')
        self.addCompositeVar(label,objs,'pt','pt','F')
        self.addCompositeVar(label,objs,'eta','eta','F')
        self.addCompositeVar(label,objs,'phi','phi','F')
        self.addCompositeVar(label,objs,'energy','energy','F')

    def addCompositeVar(self,label,objs,varLabel,var,rootType):
        '''Add single variable for multiple objects'''
        self.tree.add(lambda rtrow,cands: self.getCompositeVariable(rtrow,var,*[cands[obj] for obj in objs]), '{0}_{1}'.format(label,varLabel), rootType)

