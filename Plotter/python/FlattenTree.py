import logging
import os
import sys
import glob

import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData

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

    def __initializeSample(self,sample):
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
        
    def addHistogram(self,name,**params):
        self.histParameters[name] = params

    def add2DHistogram(self,name,**params):
        self.histParameters2D[name] = params

    def clearHistograms(self):
        self.histParameters = {}
        self.histParameters2D = {}

    def flatten(self,sample,outputFileName,selection,**kwargs):
        '''Produce flat histograms for a given selection.'''
        scalefactor = kwargs.pop('scalefactor','1' if isData(sample) else 'genWeight')
        postfix = kwargs.pop('postfix','')
        logging.info('Flattening {0} {1}'.format(sample,postfix))
        # initialize sample
        self.__initializeSample(sample)
        # copy try from selection
        tree = self.sampleTree.CopyTree(selection)
        if not tree: return
        # setup outputs
        os.system('mkdir -p {0}'.format(os.path.dirname(outputFileName)))
        outfile = ROOT.TFile(outputFileName,'update')
        if not isData(sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        # make each histogram
        for histName, params in self.histParameters.iteritems():
            name = histName
            if postfix: name += '_{0}'.format(postfix)
            drawString = '{0}>>{1}({2})'.format(params['variable'],name,', '.join([str(x) for x in params['binning']]))
            selectionString = '{0}*({1})'.format(scalefactor,'1')
            tree.Draw(drawString,selectionString,'goff')
        outfile.Write('',ROOT.TObject.kOverwrite)
        outfile.Close()

    def flatten2D(self,sample,outputFileName,selection,**kwargs):
        '''Produce flat 2D histograms for a given selection.'''
        logging.info('Flattening {0}'.format(sample))
        scalefactor = kwargs.pop('scalefactor','1' if isData(sample) else 'genWeight')
        # initialize sample
        self.__initializeSample(sample)
        # copy try from selection
        tree = self.sampleTree.CopyTree(selection)
        if not tree: return
        # setup outputs
        os.system('mkdir -p {0}'.format(os.path.dirname(outputFileName)))
        outfile = ROOT.TFile(outputFileName,'update')
        if not isData(sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        # make each histogram
        for histName, params in self.histParameters2D.iteritems():
            drawString = '{0}:{1}>>{2}({3})'.format(params['yVariable'],params['xVariable'],histName,', '.join([str(x) for x in params['xBinning']+params['yBinning']]))
            selectionString = '{0}*({1})'.format(scalefactor,'1')
            tree.Draw(drawString,selectionString,'goff')
        outfile.Write('',ROOT.TObject.kOverwrite)
        outfile.Close()
