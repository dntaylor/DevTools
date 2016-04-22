import os
import sys
import logging

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

chargePlotter = Plotter('Charge')

chans = ['ee','mm','tt']
#chans = ['ee','mm']

labelMap = {
    'e': 'e',
    'm': '#mu',
    't': '#tau',
}
chanLabels = [''.join([labelMap[c] for c in chan]) for chan in chans]
#chanLabels[-1] = '#tau_{#mu}#tau_{h}'

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

samples = ['TT','TTV','Z','WW','WZ','VVV','ZZ']
#samples = ['TT','Z']

for s in samples:
    chargePlotter.addHistogramToStack(s,sigMap[s])

chargePlotter.addHistogram('data',sigMap['data'])

# plot definitions
plots = {
    # z cand
    'zMass'                 : {'xaxis': 'm_{l^{+}l^{-}} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [81,101]},
    'zLeadingLeptonPt'      : {'xaxis': 'p_{T}^{Z_{lead}} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [0,150]},
    'zLeadingLeptonEta'     : {'xaxis': '|#eta^{Z_{lead}}|', 'yaxis': 'Events', 'rebin': 5, 'rangex': [-2.5,2.5]},
    'zSubLeadingLeptonPt'   : {'xaxis': 'p_{T}^{Z_{sublead}} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [0,150]},
    'zSubLeadingLeptonEta'  : {'xaxis': '|#eta^{Z_{sublead}}|', 'yaxis': 'Events', 'rebin': 5, 'rangex': [-2.5,2.5]},
}

# signal region
for plot in plots:
    for sign in ['SS','OS']:
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

ptbins = [10,20,30,40,50,60,80,100,200,1000]
etabins = [-2.5,-2.0,-1.479,-1.0,-0.5,0.,0.5,1.0,1.479,2.0,2.5]

ratio_cust = {
    'zLeadingLeptonPt'     : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': ptbins},
    'zLeadingLeptonEta'    : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': etabins},
    'zSubLeadingLeptonPt'  : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': ptbins},
    'zSubLeadingLeptonEta' : {'yaxis': 'N_{SS}/N_{OS}', 'rebin': etabins},
}

for plot in ['Pt','Eta']:
    for lepton in ['zLeadingLepton','zSubLeadingLepton']:
        kwargs = deepcopy(plots[lepton+plot])
        if lepton+plot in ratio_cust: kwargs.update(ratio_cust[lepton+plot])
        for chan in chans:
            numname = 'SS/{0}/{1}{2}'.format(chan,lepton,plot)
            denomname = 'OS/{0}/{1}{2}'.format(chan,lepton,plot)
            savename = 'ratio/{0}/{1}{2}'.format(chan,lepton,plot)
            chargePlotter.plotRatio(numname,denomname,savename,ymax=0.07,**kwargs)


