import logging
import os
import sys
import glob

import ROOT

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
        self.currVal = 0

    def __initializeSample(self,sample):
        self.sample = sample
        tchain = ROOT.TChain(self.treeName)
        sampleDirectory = '{0}/{1}'.format(self.ntupleDirectory,sample)
        summedWeights = 0.
        for f in glob.glob('{0}/*.root'.format(sampleDirectory)):
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

    def __open(self,outputFileName):
        self.outfile = ROOT.TFile(outputFileName,'update')

    def __write(self):
        self.outfile.Write('',ROOT.TObject.kOverwrite)
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

    def addSelection(self,selection,postfix=''):
        '''Add selection and postfix name to flatten'''
        self.selections += [(selection,postfix)]

    def flattenAll(self,**kwargs):
        '''Flatten all selections'''
        if hasProgress:
            maxval = len(self.selections)*len(self.histParameters)
            self.pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
            self.pbar.maxval = maxval
            self.pbar.start()
        else:
            self.pbar = None
        self.currVal = 0
        for sel,post in self.selections:
            self.__flatten(sel,postfix=post,**kwargs)

    def flattenAll2D(self,**kwargs):
        '''Flatten all selections 2D'''
        if hasProgress:
            maxval = len(self.selections)*len(self.histParameters2D)
            self.pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
            self.pbar.maxval = maxval
            self.pbar.start()
        else:
            self.pbar = None
        for sel,post in self.selections:
            self.__flatten2D(sel,postfix=post,**kwargs)

    def __flatten(self,selection,**kwargs):
        '''Produce flat histograms for a given selection.'''
        scalefactor = kwargs.pop('scalefactor','1' if isData(self.sample) else 'genWeight')
        postfix = kwargs.pop('postfix','')
        if not hasProgress: logging.info('Flattening {0} {1}'.format(self.sample,postfix))
        # copy try from selection
        #tree = self.sampleTree.CopyTree(selection)
        tree = self.sampleTree
        if not tree: return
        # setup outputs
        os.system('mkdir -p {0}'.format(os.path.dirname(self.outputFileName)))
        self.__open(self.outputFileName)
        if not isData(self.sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        # make each histogram
        for histName, params in self.histParameters.iteritems():
            name = histName
            if postfix: name += '_{0}'.format(postfix)
            drawString = '{0}>>{1}({2})'.format(params['variable'],name,', '.join([str(x) for x in params['binning']]))
            selectionString = '{0}*({1})'.format(scalefactor,'1')
            tree.Draw(drawString,selectionString,'goff')
            self.currVal += 1
            if hasProgress: self.pbar.update(self.currVal)
        self.__write()

    def __flatten2D(self,selection,**kwargs):
        '''Produce flat 2D histograms for a given selection.'''
        if not hasProgress: logging.info('Flattening {0}'.format(self.sample))
        scalefactor = kwargs.pop('scalefactor','1' if isData(self.sample) else 'genWeight')
        postfix = kwargs.pop('postfix','')
        # copy try from selection
        #tree = self.sampleTree.CopyTree(selection)
        tree = self.sampleTree
        if not tree: return
        # setup outputs
        os.system('mkdir -p {0}'.format(os.path.dirname(self.outputFileName)))
        self.__open(self.outputFileName)
        if not isData(self.sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        # make each histogram
        for histName, params in self.histParameters2D.iteritems():
            drawString = '{0}:{1}>>{2}({3})'.format(params['yVariable'],params['xVariable'],histName,', '.join([str(x) for x in params['xBinning']+params['yBinning']]))
            selectionString = '{0}*({1})'.format(scalefactor,'1')
            tree.Draw(drawString,selectionString,'goff')
            self.currVal += 1
            if hasProgress: self.pbar.update(self.currVal)
        self.__write()
