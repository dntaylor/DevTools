
import os
import sys
import logging

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

wzPlotter = Plotter('WZ')

sigMap = {
    'WZ'  : [
             'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8',
             #'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
             #'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
             #'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
            ],
    'ZG'  : [
             'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'ZZ'  : [
             'ZZTo4L_13TeV_powheg_pythia8',
             'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
             'ZZTo2L2Nu_13TeV_powheg_pythia8',
             'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
            ],
    'VVV' : [
             'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
             'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
            ],
    'TTV' : [
             #'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8',
             #'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
             'ttWJets_13TeV_madgraphMLM',
             'ttZJets_13TeV_madgraphMLM',
            ],
    'WW'  : [
             'WWTo2L2Nu_13TeV-powheg',
             'WWToLNuQQ_13TeV-powheg',
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

samples = ['TTV','ZG','VVV','ZZ','WZ']
samples = ['TTV','VVV','ZZ','WZ']

datadrivenSamples = []
for s in samples + ['data']:
    datadrivenSamples += sigMap[s]
wzPlotter.addHistogramToStack('datadriven',datadrivenSamples)

for s in samples:
    wzPlotter.addHistogramToStack(s,sigMap[s])

wzPlotter.addHistogram('data',sigMap['data'])

plotStyles = {
    # Z
    'zMass'               : {'xaxis': 'm_{l^{+}l^{-}}', 'yaxis': 'Events/1 GeV', 'rangex':[60,120]},
    'mllMinusMZ'          : {'xaxis': '|m_{l^{+}l^{-}}-m_{Z}|', 'yaxis': 'Events/1 GeV', 'rangex':[0,60]},
    'zPt'                 : {'xaxis': 'p_{T}^{Z}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    'zLeadingLeptonPt'    : {'xaxis': 'p_{T}^{Z lead}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    'zSubLeadingLeptonPt' : {'xaxis': 'p_{T}^{Z sublead}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    # W
    'wMass'               : {'xaxis': 'm_{T}^{W}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    'wPt'                 : {'xaxis': 'p_{T}^{W}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    'wLeptonPt'           : {'xaxis': 'p_{T}^{W lepton}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    # event
    'met'                 : {'xaxis': 'E_{T}^{miss}', 'yaxis': 'Events/10 GeV', 'rebin':10, 'rangex':[0,200]},
    'mass'                : {'xaxis': 'm_{3l}', 'yaxis': 'Events/20 GeV', 'rebin':20, 'rangex':[0,500]},
    'nJets'               : {'xaxis': 'Number of Jets (p_{T} > 30 GeV)', 'yaxis': 'Events', 'rangex':[0,8]},
}

def getDataDrivenPlot(plot):
    histMap = {}
    plotdirs = plot.split('/')
    for s in samples + ['data']: histMap[s] = '/'.join(plotdirs[:-1]+['PPP']+plotdirs[-1:])
    regions = ['PPF','PFP','FPP','PFF','FPF','FFP','FFF']
    histMap['datadriven'] = ['/'.join(plotdirs[:-1]+[reg]+plotdirs[-1:]) for reg in regions]
    return histMap

for plot in plotStyles:
    plotvars = getDataDrivenPlot(plot)
    savename = 'datadriven/{0}'.format(plot)
    wzPlotter.plot(plotvars,savename,**plotStyles[plot])

wzPlotter.clearHistograms()

samples = ['TT','TTV','Z','WW','VVV','ZZ','WZ']

for s in samples:
    wzPlotter.addHistogramToStack(s,sigMap[s])

wzPlotter.addHistogram('data',sigMap['data'])

for plot in plotStyles:
    plotname = 'default/{0}'.format(plot)
    savename = plot
    wzPlotter.plot(plotname,savename,**plotStyles[plot])

