import logging
import os
import sys
import glob
import json

sys.argv.append('-b')
import ROOT
sys.argv.pop()

ROOT.gROOT.SetBatch(ROOT.kTRUE)

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData, hashFile, hashString, python_mkdir

try:
    from progressbar import ProgressBar, ETA, Percentage, Bar, SimpleProgress
    hasProgress = True
except:
    hasProgress = False

class FlattenTree(object):
    '''Produces flat histograms'''

    def __init__(self,**kwargs):
        self.ntupleDirectory = kwargs.pop('ntupleDirectory','ntuples/Analysis')
        self.treeName = kwargs.pop('treeName','AnalysisTree')
        # dictionaries to hold the sample information
        self.intLumi = getLumi()
        self.sampleLumi = 0
        self.sampleTree = None
        self.histParameters = {}
        self.histParameters2D = {}
        self.outfile = 0
        self.preinitialized = False
        self.selections = []
        self.sample = ''
        self.j = 0
        self.hashDir = '.hash'
        self.files = []

    def __initializeSample(self,sample):
        self.sample = sample
        tchain = ROOT.TChain(self.treeName)
        sampleFile = '{0}/{1}.root'.format(self.ntupleDirectory,sample)
        if os.path.isfile(sampleFile):
            allFiles = [sampleFile]
        else:
            sampleDirectory = '{0}/{1}'.format(self.ntupleDirectory,sample)
            allFiles = glob.glob('{0}/*.root'.format(sampleDirectory))
        summedWeights = 0.
        for f in allFiles:
            tfile = ROOT.TFile.Open(f)
            summedWeights += tfile.Get("summedWeights").GetBinContent(1)
            tfile.Close()
            tchain.Add(f)
        self.sampleLumi = float(summedWeights)/getXsec(sample) if getXsec(sample) else 0.
        self.sampleTree = tchain
        self.files = allFiles
        
    def __exit__(self, type, value, traceback):
        self.__finish()

    def __del__(self):
        self.__finish()

    def __finish(self):
        if self.outfile:
            self.outfile.Close()

    def __write(self,hist,directory=''):
        self.outfile = ROOT.TFile(self.outputFileName,'update')
        if not self.outfile.GetDirectory(directory): self.outfile.mkdir(directory)
        self.outfile.cd('{0}:/{1}'.format(self.outputFileName,directory))
        hist.Write('',ROOT.TObject.kOverwrite)
        self.__finish()

    def __checkHash(self,name,directory,strings=[]):
        #TODO: think of better way
        return False
        outputFileDir = self.outputFileName.rstrip('.root')
        hashFileName = '{0}/{1}/{2}/{3}.json'.format(self.hashDir,outputFileDir,directory,name)
        if os.path.isfile(hashFileName):
            hashvals = json.load(hashFileName)
        else:
            hashvals = {'files':'','strings':''}
        oldFileHash = hashvals['files']
        oldStringHash = hashvals['strings']
        newFileHash = hashFile(*self.files)
        newStringHash = hashString(*strings)
        if oldFileHash==newFileHash and oldStringHash==newStringHash:
            return True
        hashvals['files'] = newFileHash
        hashvals['strings'] = newStringHash
        python_mkdir(os.path.dirname(hashFileName))
        with open(hashFileName,'w') as f:
            json.dump(hashvals,f)
        return False

    def addHistogram(self,name,**params):
        '''
        Add a histogram to flatten
        params:
           variable: variable to plot
           binning: binning for variable
        '''
        self.histParameters[name] = params

    def add2DHistogram(self,name,**params):
        '''
        Add a histogram to flatten 2D
        params:
           xVariable: x variable to plot
           yVariable: y variable to plot
           xBinning: binning for x variable
           yBinning: binning for y variable
        '''
        self.histParameters2D[name] = params

    def clear(self):
        '''Reset the histograms/selections'''
        self.histParameters = {}
        self.histParameters2D = {}
        self.selections = []

    def initializeSample(self,sample,outputFileName):
        '''Initialize input sample to flatten'''
        self.__initializeSample(sample)
        self.outputFileName = outputFileName
        self.preinitialized = True

    def addSelection(self,selection,**kwargs):
        '''Add selection and postfix name to flatten'''
        self.selections += [(selection,kwargs)]

    def flattenAll(self,**kwargs):
        '''Flatten all selections'''
        if hasProgress:
            pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
        else:
            pbar = None
        allJobs = []
        for sel,sel_kwargs in self.selections:
            countOnly = sel_kwargs.pop('countOnly',False)
            for histName,params in self.histParameters.iteritems():
                if countOnly and 'count' not in histName: continue
                allJobs += [[sel,sel_kwargs,histName,params]]
        if hasProgress:
            for args in pbar(allJobs):
                sel,sel_kwargs,histName,params = args
                self.__flatten(sel,histName,params,**sel_kwargs)
        else:
            for args in allJobs:
                sel,sel_kwargs,histName,params = args
                self.__flatten(sel,histName,params,**sel_kwargs)

    def flattenAll2D(self,**kwargs):
        '''Flatten all selections 2D'''
        if hasProgress:
            pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
        else:
            pbar = None
        allJobs = []
        for sel,sel_kwargs in self.selections:
            countOnly = sel_kwargs.pop('countOnly',False)
            for histName,params in self.histParameters2D.iteritems():
                if countOnly and 'count' not in histName: continue
                allJobs += [[sel,sel_kwargs,histName,params]]
        if hasProgress:
            for args in pbar(allJobs):
                sel,sel_kwargs,histName,params = args
                self.__flatten2D(sel,histName,params,**sel_kwargs)
        else:
            for args in allJobs:
                sel,sel_kwargs,histName,params = args
                self.__flatten2D(sel,histName,params,**sel_kwargs)

    def __flatten(self,selection,histName,params,**kwargs):
        '''Produce flat histograms for a given selection.'''
        mccut = kwargs.pop('mccut','')
        datacut = kwargs.pop('datacut','')
        if datacut and isData(self.sample): selection += ' && {0}'.format(datacut)
        if mccut and not isData(self.sample): selection += ' && {0}'.format(mccut)
        scalefactor = kwargs.pop('scalefactor','1' if isData(self.sample) else 'genWeight')
        mcscalefactor = kwargs.pop('mcscalefactor','')
        datascalefactor = kwargs.pop('datascalefactor','')
        if datascalefactor and isData(self.sample): scalefactor = datascalefactor
        if mcscalefactor and not isData(self.sample): scalefactor = mcscalefactor
        directory = kwargs.pop('directory','')
        if not hasProgress: logging.info('Flattening {0} {1} {2}'.format(self.sample,directory,histName))
        tree = self.sampleTree
        if not tree: return
        os.system('mkdir -p {0}'.format(os.path.dirname(self.outputFileName)))
        if not isData(self.sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        name = histName
        self.j += 1
        tempName = '{0}_{1}_{2}'.format(name,self.sample,self.j)
        drawString = '{0}>>{1}({2})'.format(params['variable'],tempName,', '.join([str(x) for x in params['binning']]))
        if 'scale' in params: scalefactor += '*{0}'.format(params['scale'])
        if 'mcscale' in params and not isData(self.sample): scalefactor += '*{0}'.format(params['mcscale'])
        if 'datascale' in params and isData(self.sample): scalefactor += '*{0}'.format(params['datascale'])
        if 'selection' in params: selection += ' && {0}'.format(params['selection'])
        selectionString = '{0}*({1})'.format(scalefactor,selection)
        # check if we need to draw the hist, or if the one in the ntuple is the latest
        hashExists = self.__checkHash(name,directory,strings=[params['variable'],', '.join([str(x) for x in params['binning']]),scalefactor,selection])
        if hashExists:
            self.__finish()
            return
        tree.Draw(drawString,selectionString,'goff')
        # see if hist exists
        if ROOT.gDirectory.Get(tempName):
            hist = ROOT.gDirectory.Get(tempName)
            hist.SetTitle(name)
            hist.SetName(name)
            self.__write(hist,directory=directory)
        else:
            bins = params['binning']
            hist = ROOT.TH1F(tempName,tempName,*bins)
            hist.SetTitle(name)
            hist.SetName(name)
            self.__write(hist,directory=directory)

    def __flatten2D(self,selection,histName,params,**kwargs):
        '''Produce flat 2D histograms for a given selection.'''
        mccut = kwargs.pop('mccut','')
        datacut = kwargs.pop('datacut','')
        if datacut and isData(self.sample): selection += ' && {0}'.format(datacut)
        if mccut and not isData(self.sample): selection += ' && {0}'.format(mccut)
        scalefactor = kwargs.pop('scalefactor','1' if isData(self.sample) else 'genWeight')
        mcscalefactor = kwargs.pop('mcscalefactor','')
        datascalefactor = kwargs.pop('datascalefactor','')
        if datascalefactor and isData(self.sample): scalefactor = datascalefactor
        if mcscalefactor and not isData(self.sample): scalefactor = mcscalefactor
        directory = kwargs.pop('directory','')
        if not hasProgress: logging.info('Flattening {0} {1} {2}'.format(self.sample,directory,histName))
        tree = self.sampleTree
        if not tree: return
        os.system('mkdir -p {0}'.format(os.path.dirname(self.outputFileName)))
        if not isData(self.sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        name = histName
        self.j += 1
        tempName = '{0}_{1}_{2}'.format(name,self.sample,self.j)
        drawString = '{0}:{1}>>{2}({3})'.format(params['yVariable'],params['xVariable'],tempName,', '.join([str(x) for x in params['xBinning']+params['yBinning']]))
        if 'scale' in params: scalefactor += '*{0}'.format(params['scale'])
        if 'mcscale' in params and not isData(self.sample): scalefactor += '*{0}'.format(params['mcscale'])
        if 'datascale' in params and isData(self.sample): scalefactor += '*{0}'.format(params['datascale'])
        if 'selection' in params: selection += ' && {0}'.format(params['selection'])
        selectionString = '{0}*({1})'.format(scalefactor,selection)
        # check if we need to draw the hist, or if the one in the ntuple is the latest
        hashExists = self.__checkHash(name,directory,strings=[params['yvariable'],params['xVariable'],', '.join([str(x) for x in params['xBinning']+params['yBinning']]),scalefactor,selection])
        if hashExists:
            self.__finish()
            return
        tree.Draw(drawString,selectionString,'goff')
        # see if hist exists
        if ROOT.gDirectory.Get(tempName):
            hist = ROOT.gDirectory.Get(tempName)
            hist.SetTitle(name)
            hist.SetName(name)
            self.__write(hist,directory=directory)
        else:
            bins = params['xBinning']+params['yBinning']
            hist = ROOT.TH2F(tempName,tempName,*bins)
            hist.SetTitle(name)
            hist.SetName(name)
            self.__write(hist,directory=directory)
