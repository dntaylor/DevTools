import logging
import os
import sys
import glob

import ROOT

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData

class FlattenTree(object):
    '''Produces flat histograms'''

    def __init__(self,**kwargs):
        self.ntupleDirectory = kwargs.pop('ntupleDirectory','ntuples/WZ')
        self.treeName = kwargs.pop('treeName','WZTree')
        # dictionaries to hold the sample information
        self.intLumi = getLumi()
        self.sampleLumi = 0
        self.sampleTree = None
        # add variables
        self.histParameters = {
            'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
            'zLeadingLeptonPt'    : {'variable': 'z1_pt',   'binning': [50, 0, 500]},
            'zSubLeadingLeptonPt' : {'variable': 'z2_pt',   'binning': [50, 0, 500]},
            'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
            'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
            'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
        }
        # data samples
        self.dataSamples = ['DoubleMuon','DoubleEG','MuonEG','SingleMuon','SingleElectron','Tau']

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

    def flatten(self,sample,outputFileName,selection,**kwargs):
        '''Produce flat histograms for a given selection.'''
        scalefactor = kwargs.pop('scalefactor','1' if isData(sample) else 'genWeight')
        self.__initializeSample(sample)
        os.system('mkdir -p {0}'.format(os.path.dirname(outputFileName)))
        outfile = ROOT.TFile(outputFileName,'recreate')
        if not isData(sample): scalefactor = '{0}*{1}'.format(scalefactor,float(self.intLumi)/self.sampleLumi)
        for histName, params in self.histParameters.iteritems():
            drawString = '{0}>>{1}({2})'.format(params['variable'],histName,', '.join([str(x) for x in params['binning']]))
            selectionString = '{0}*({1})'.format(scalefactor,selection)
            self.sampleTree.Draw(drawString,selectionString,'goff')
        outfile.Write()
        outfile.Close()
