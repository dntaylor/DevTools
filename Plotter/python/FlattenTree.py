import logging
import os
import sys

sys.argv.append('-b')
import ROOT
sys.argv.pop()

ROOT.gROOT.SetBatch(ROOT.kTRUE)

from DevTools.Plotter.NtupleWrapper import NtupleWrapper

try:
    from progressbar import ProgressBar, ETA, Percentage, Bar, SimpleProgress
    hasProgress = True
except:
    hasProgress = False

class FlattenTree(object):
    '''Produces flat histograms'''

    def __init__(self,analysis,sample,**kwargs):
        self.analysis = analysis
        self.sample = sample
        self.ntuple = NtupleWrapper(analysis,sample,**kwargs)
        self.histParameters = []
        self.histParameters2D = []
        self.selections = []
        self.countOnly = []

    def __exit__(self, type, value, traceback):
        self.__finish()

    def __del__(self):
        self.__finish()

    def __finish(self):
        pass

    def addHistogram(self,name,**kwargs):
        '''
        Add a histogram to flatten
        '''
        self.histParameters += [name]

    def add2DHistogram(self,name,**kwargs):
        '''
        Add a histogram to flatten 2D
        '''
        self.histParameters2D += [name]

    def addSelection(self,selection,**kwargs):
        '''Add selection and postfix name to flatten'''
        countOnly = kwargs.pop('countOnly',False)
        self.selections += [selection]
        if countOnly:
            self.countOnly += [selection]

    def clear(self):
        '''Reset the histograms/selections'''
        self.histParameters = []
        self.histParameters2D = []
        self.selections = []
        self.countOnly = []

    def flattenAll(self,**kwargs):
        '''Flatten all selections'''
        if hasProgress:
            pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
        else:
            pbar = None
        allJobs = []
        for sel in self.selections:
            for histName in self.histParameters:
                if sel in self.countOnly and 'count' not in histName: continue
                allJobs += [[sel,histName]]
        if hasProgress:
            for args in pbar(allJobs):
                sel,histName = args
                self.ntuple.flatten(histName,sel)
        else:
            for args in allJobs:
                sel,histName = args
                self.flatten(histName,sel)

    def flattenAll2D(self,**kwargs):
        '''Flatten all selections 2D'''
        if hasProgress:
            pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(self.sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
        else:
            pbar = None
        allJobs = []
        for sel in self.selections:
            for histName in self.histParameters2D:
                if sel in self.countOnly and 'count' not in histName: continue
                allJobs += [[sel,histName]]
        if hasProgress:
            for args in pbar(allJobs):
                sel,histName = args
                self.ntuple.flatten2D(histName,sel)
        else:
            for args in allJobs:
                sel,histName = args
                self.flatten2D(histName,sel)
