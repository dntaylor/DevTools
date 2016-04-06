import os
import sys
import logging

from DevTools.Plotter.HistMaker import HistMaker
from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

dijetFakeRatePlotter = Plotter(
    inputDirectory  = 'flat/DijetFakeRate',
    outputDirectory = 'plots/DijetFakeRate',
)

dijetFakeRateMaker = HistMaker(
    inputDirectory = 'flat/DijetFakeRate',
    outputFileName = 'root/DijetFakeRate/fakerates.root',
)

sigMap = {
    'W'   : [
             'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'Z'   : [
             'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'TT'  : [
             'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
            ],
    'data': [
             'DoubleMuon',
             'DoubleEG',
             'MuonEG',
             'SingleMuon',
             'SingleElectron',
            ],
}

samples = ['TT','Z','W']

allSamplesDict = {'MC':[]}

for s in samples:
    allSamplesDict['MC'] += sigMap[s]

dijetFakeRatePlotter.addHistogram('MC',allSamplesDict['MC'])
dijetFakeRatePlotter.addHistogram('data',sigMap['data'],style={'linecolor':ROOT.kBlack,'name':'EWK Corrected'})
dijetFakeRatePlotter.addHistogram('data_uncorrected',sigMap['data'],style={'linecolor':ROOT.kRed,'name':'Uncorrected'})



channels = ['e','m']

dirName = {
    'e': 'electron',
    'm': 'muon',
    't': 'tau'
}

labelMap = {
    'e': 'e',
    'm': '#mu',
    't': '#tau',
}

etaBins = {
    'e': [0.,0.5,1.0,1.479,2.0,2.5],
    'm': [0.,1.2,2.4],
}
ptBins = {
    'e': [0,10,15,20,25,30,40,50,60,100],
    'm': [0,10,15,20,25,30,40,100],
}

for lepton in ['medium','tight']:
    for chan in channels:
        xBinning = ptBins[chan]
        xaxis = 'p_{{T}}^{{{0}}}'.format(labelMap[chan])
        yBinning = etaBins[chan]
        yaxis = '|#eta^{{{0}}}|'.format(labelMap[chan])
        values = {}
        errors = {}
        # get the values
        for e in range(len(yBinning)-1):
            # get the histogram
            numname = '{0}/{1}/etaBin{2}/pt'.format(lepton,chan,e)
            denomname = 'loose/{0}/etaBin{1}/pt'.format(chan,e)
            savename = 'filler'
            subtractMap = {
                'data': ['MC'],
            }
            customOrder = ['data']
            hists = dijetFakeRatePlotter.plotRatio(numname,denomname,savename,customOrder=customOrder,subtractMap=subtractMap,rebin=xBinning,getHists=True)
            # get the pt bins
            for p in range(len(xBinning)-1):
                pt = float(xBinning[p]+xBinning[p+1])/2.
                eta = float(yBinning[e]+yBinning[e+1])/2.
                key = (pt,eta)
                values[key] = hists['data'].GetBinContent(p+1)
                errors[key] = hists['data'].GetBinError(p+1)
        # save the values
        savename = 'fakeratePtEta'
        savedir = '{0}/{1}'.format(chan,lepton)
        dijetFakeRateMaker.make2D(savename,values,errors,xBinning,yBinning,savedir=savedir,xaxis=xaxis,yaxis=yaxis)
