import os
import sys
import logging

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

chargePlotter = Plotter('TauCharge')

chans = ['tt']

labelMap = {
    'e': 'e',
    'm': '#mu',
    't': '#tau',
}
chanLabels = ['#tau_{#mu}#tau_{h}']

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

samples = ['W','WW','TT','Z']
#samples = ['TT','Z']

for s in samples:
    chargePlotter.addHistogramToStack(s,sigMap[s])

chargePlotter.addHistogram('data',sigMap['data'])

# plot definitions
plots = {
    # z cand
    'zMass'                 : {'xaxis': 'm_{#tau_{#mu}#tau_{h}} (GeV)', 'yaxis': 'Events / 2 GeV', 'rebin': 20, 'rangex': [35,85]},
    'zTauMuPt'              : {'xaxis': 'p_{T}^{#tau_{#mu}} (GeV)',     'yaxis': 'Events / 2 GeV', 'rebin': 20, 'rangex': [0,150]},
    'zTauMuEta'             : {'xaxis': '|#eta^{#tau_{#mu}}|',          'yaxis': 'Events',         'rebin': 5,  'rangex': [-2.5,2.5]},
    'zTauHadPt'             : {'xaxis': 'p_{T}^{#tau_{h}} (GeV)',       'yaxis': 'Events / 2 GeV', 'rebin': 20, 'rangex': [0,150]},
    'zTauHadEta'            : {'xaxis': '|#eta^{#tau_{h}}|',            'yaxis': 'Events',         'rebin': 5,  'rangex': [-2.5,2.5]},
    # met
    'met'                   : {'xaxis': 'E_{T}^{miss} (GeV)',           'yaxis': 'Events / 2 GeV', 'rebin': 20, 'rangex': [0,300]},
    'tauMuMt'               : {'xaxis': 'm_{T}^{#mu} (GeV)',            'yaxis': 'Events / 5 GeV', 'rebin': 50, 'rangex': [0,200]},
}

# signal region
for plot in plots:
    for sign in ['SS','OS','SS/mtCut','OS/mtCut']:
        for chan in chans:
            plotname = '{0}/{1}/{2}'.format(sign,chan,plot)
            savename = '{0}/{1}/{2}'.format(sign,chan,plot)
            chargePlotter.plot(plotname,savename,**plots[plot])

# ratios of SS/OS as func of pt/eta
chargePlotter.clearHistograms()

allSamplesDict = {'MC':[]}

for s in samples:
    allSamplesDict['MC'] += sigMap[s]

chargePlotter.addHistogram('MC',allSamplesDict['MC'],style={'linecolor': ROOT.kRed})
chargePlotter.addHistogram('data',sigMap['data'],style={'linecolor':ROOT.kBlack})

ptbins = [10,20,40,60,100,1000]
etabins = [-2.5,-2.0,-1.479,-1.0,-0.5,0.,0.5,1.0,1.479,2.0,2.5]

ratio_cust = {
    'zTauMuPt'   : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': ptbins},
    'zTauMuEta'  : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': etabins},
    'zTauHadPt'  : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': ptbins},
    'zTauHadEta' : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': etabins},
}

for plot in ['Pt','Eta']:
    for lepton in ['zTauMu','zTauHad']:
        kwargs = deepcopy(plots[lepton+plot])
        if lepton+plot in ratio_cust: kwargs.update(ratio_cust[lepton+plot])
        for chan in chans:
            numname = 'SS/mtCut/{0}/{1}{2}'.format(chan,lepton,plot)
            denomname = 'OS/mtCut/{0}/{1}{2}'.format(chan,lepton,plot)
            savename = 'ratio/{0}/{1}{2}'.format(chan,lepton,plot)
            chargePlotter.plotRatio(numname,denomname,savename,ymax=0.25,**kwargs)


