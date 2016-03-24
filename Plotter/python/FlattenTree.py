import logging
import os
import sys
import glob

sys.argv.append('-b')
import ROOT
sys.argv.pop()

ROOT.gROOT.SetBatch(ROOT.kTRUE)

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData

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
            for histName,params in self.histParameters.iteritems():
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
        for sel,directory in self.selections:
            for histName,params in self.histParameters2D.iteritems():
                allJobs += [[sel,directory,histName,params]]
        if hasProgress:
            for args in pbar(allJobs):
                sel,directory,histName,params = args
                self.__flatten2D(sel,histName,params,directory=directory,**kwargs)
        else:
            for args in allJobs:
                sel,directory,histName,params = args
                self.__flatten2D(sel,histName,params,directory=directory,**kwargs)

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
        selectionString = '{0}*({1})'.format(scalefactor,selection)
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
        selectionString = '{0}*({1})'.format(scalefactor,selection)
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
