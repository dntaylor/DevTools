import os
import sys
import logging

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

dijetFakeRatePlotter = Plotter(
    inputDirectory  = 'flat/DijetFakeRate',
    outputDirectory = 'plots/DijetFakeRate',
)

chans = ['e','m']

labelMap = {
    'e': 'e',
    'm': '#mu',
    't': '#tau',
}
chanLabels = [''.join([labelMap[c] for c in chan]) for chan in chans]

sigMap = {
    'WZ'  : [
             'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8',
             'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
             #'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
             #'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
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
             #'WWToLNuQQ_13TeV-powheg',
            ],
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

for s in samples:
    dijetFakeRatePlotter.addHistogramToStack(s,sigMap[s])

dijetFakeRatePlotter.addHistogram('data',sigMap['data'])

# plot definitions
plots = {
    'pt'      : {'xaxis': 'p_{T} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [0,150]},
    'eta'     : {'xaxis': '|#eta|', 'yaxis': 'Events', 'rebin': 5, 'rangex': [-2.5,2.5]},
}

# signal region
for plot in plots:
    for lepton in ['loose','medium','tight']:
        for chan in chans:
            plotname = '{0}/{1}/{2}'.format(lepton,chan,plot)
            savename = '{0}/{1}/{2}'.format(lepton,chan,plot)
            dijetFakeRatePlotter.plot(plotname,savename,**plots[plot])

# ratios of SS/OS as func of pt/eta
dijetFakeRatePlotter.clearHistograms()

allSamplesDict = {'MC':[]}

for s in samples:
    allSamplesDict['MC'] += sigMap[s]

dijetFakeRatePlotter.addHistogram('MC',allSamplesDict['MC'],style={'linecolor': ROOT.kRed})
dijetFakeRatePlotter.addHistogram('data',sigMap['data'],style={'linecolor':ROOT.kBlack})

ptbins = [10,20,30,40,50,60,80,100,200,1000]
etabins = [-2.5,-2.0,-1.479,-1.0,-0.5,0.,0.5,1.0,1.479,2.0,2.5]

medium_cust = {
    'pt'     : {'yaxis': 'N_{Medium}/N_{Loose}', 'rebin': ptbins},
    'eta'    : {'yaxis': 'N_{Medium}/N_{Loose}', 'rebin': etabins},
}
tight_cust = {
    'pt'     : {'yaxis': 'N_{Tight}/N_{Loose}', 'rebin': ptbins},
    'eta'    : {'yaxis': 'N_{Tight}/N_{Loose}', 'rebin': etabins},
}

for plot in ['pt','eta']:
    for lepton in ['medium','tight']:
        kwargs = deepcopy(plots[plot])
        if lepton=='medium':
            if plot in medium_cust: kwargs.update(medium_cust[plot])
        if lepton=='tight':
            if plot in tight_cust: kwargs.update(tight_cust[plot])
        for chan in chans:
            numname = '{0}/{1}/{2}'.format(lepton,chan,plot)
            denomname = 'loose/{0}/{1}'.format(chan,plot)
            savename = 'ratio/{0}/{1}'.format(lepton,plot)
            dijetFakeRatePlotter.plotRatio(numname,denomname,savename,ymax=1.,**kwargs)


