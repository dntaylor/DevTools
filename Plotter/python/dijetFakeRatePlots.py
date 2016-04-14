import os
import sys
import logging

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

dijetFakeRatePlotter = Plotter('DijetFakeRate')

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

allSamplesDict = {'MC':[]}

for s in samples:
    allSamplesDict['MC'] += sigMap[s]

for s in samples:
    dijetFakeRatePlotter.addHistogramToStack(s,sigMap[s])

dijetFakeRatePlotter.addHistogram('data',sigMap['data'])

# plot definitions
plots = {
    'pt'      : {'xaxis': 'p_{T} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [0,150]},
    'eta'     : {'xaxis': '|#eta|', 'yaxis': 'Events', 'rebin': 5, 'rangex': [-2.5,2.5]},
    'met'     : {'xaxis': 'E_{T}^{miss} (GeV)', 'yaxis': 'Events/0.2 GeV', 'rebin': 2, 'rangex': [0,200]},
    'wMass'   : {'xaxis': 'm_{T}^{l^{+},MET} (GeV)', 'yaxis': 'Events/0.5 GeV', 'rebin': 5, 'rangex': [0,200]},
}

# signal region
for plot in plots:
    for lepton in ['loose','medium','tight']:
        for chan in chans:
            plotname = '{0}/{1}/{2}'.format(lepton,chan,plot)
            savename = '{0}/{1}/{2}'.format(lepton,chan,plot)
            dijetFakeRatePlotter.plot(plotname,savename,**plots[plot])


# plots of multiple ptcuts on same plot
dijetFakeRatePlotter.clearHistograms()
jetPts = [10,15,20,25,30,35,40,45,50]
jetPts = [10,20,30,40,50]
jetPtColors = {
    10 : ROOT.TColor.GetColor('#000000'),
    15 : ROOT.TColor.GetColor('#330000'),
    20 : ROOT.TColor.GetColor('#660000'),
    25 : ROOT.TColor.GetColor('#800000'),
    30 : ROOT.TColor.GetColor('#990000'),
    35 : ROOT.TColor.GetColor('#B20000'),
    40 : ROOT.TColor.GetColor('#CC0000'),
    45 : ROOT.TColor.GetColor('#FF0000'),
    50 : ROOT.TColor.GetColor('#FF3333'),
}
for jetPt in jetPts:
    name = 'jetPt{0}'.format(jetPt)
    dijetFakeRatePlotter.addHistogram(name,sigMap['data'],style={'linecolor':jetPtColors[jetPt],'linestyle':3,'name':'Jet p_{{T}} > {0} GeV'.format(jetPt)})
# add the z + tt samples from WZ
dijetFakeRatePlotter.addHistogram('dataDY',sigMap['data'],style={'linecolor':ROOT.kBlue,'linestyle':1,'name':'Data (DY)'},analysis='WZ')
#dijetFakeRatePlotter.addHistogram('dataTT',sigMap['data'],style={'linecolor':ROOT.kGreen,'linestyle':1,'name':'Data (TT)'},analysis='WZ')


ptbins = [0,20,25,30,40,60]
jet_cust = {
    'pt'      : {'yaxis': 'Unit Normalized', 'rebin': 5, 'rangex': [0,60], 'logy': 0},
}

ptVarMap = {
    0 : 'zLeadingLeptonPt',
    1 : 'zSubLeadingLeptonPt',
    2 : 'wLeptonPt',
}

leptonBin = {
    'e' : {
        0 : ['eee','eem'],
        1 : ['eee','eem'],
        2 : ['eee','mme'],
    },
    'm' : {
        0 : ['mme','mmm'],
        1 : ['mme','mmm'],
        2 : ['eem','mmm'],
    },
}

for plot in ['pt']:
    kwargs = deepcopy(plots[plot])
    if plot in jet_cust: kwargs.update(jet_cust[plot])
    for lepton in ['loose']:
        for chan in chans:
            plotname = {}
            for jetPt in jetPts:
                #plotname['jetPt{0}'.format(jetPt)] = '{0}/pt20/{1}/jetPt{2}/{3}'.format(lepton,chan,jetPt,plot)
                plotname['jetPt{0}'.format(jetPt)] = '{0}/{1}/jetPt{2}/{3}'.format(lepton,chan,jetPt,plot)
            dyvars = ['dy/{1}/{2}'.format(lepton,wzchan,ptVarMap[p]) for wzchan,p in [(c,i) for i in range(3) for c in leptonBin[chan][i]]]
            ttvars = ['tt/{1}/{2}'.format(lepton,wzchan,ptVarMap[p]) for wzchan,p in [(c,i) for i in range(3) for c in leptonBin[chan][i]]]
            plotname['dataDY'] = dyvars
            #plotname['dataTT'] = ttvars
            savename = '{0}/{1}/allJetPts_{2}'.format(lepton,chan,plot)
            dijetFakeRatePlotter.plotNormalized(plotname,savename,legendpos=34,numcol=2,**kwargs)
            for lepBin in range(3):
                plotname = {}
                for jetPt in jetPts:
                    #plotname['jetPt{0}'.format(jetPt)] = '{0}/pt20/{1}/jetPt{2}/{3}'.format(lepton,chan,jetPt,plot)
                    plotname['jetPt{0}'.format(jetPt)] = '{0}/{1}/jetPt{2}/{3}'.format(lepton,chan,jetPt,plot)
                dyvars = ['dy/{1}/{2}'.format(lepton,wzchan,ptVarMap[p]) for wzchan,p in [(c,lepBin) for c in leptonBin[chan][lepBin]]]
                ttvars = ['tt/{1}/{2}'.format(lepton,wzchan,ptVarMap[p]) for wzchan,p in [(c,lepBin) for c in leptonBin[chan][lepBin]]]
                plotname['dataDY'] = dyvars
                #plotname['dataTT'] = ttvars
                savename = '{0}/{1}/allJetPts_{2}_{3}'.format(lepton,chan,plot,lepBin)
                dijetFakeRatePlotter.plotNormalized(plotname,savename,legendpos=34,numcol=2,**kwargs)

# ratios of tight/loose as func of pt/eta
dijetFakeRatePlotter.clearHistograms()
dijetFakeRatePlotter.addHistogram('MC',allSamplesDict['MC'])
dijetFakeRatePlotter.addHistogram('data',sigMap['data'],style={'linecolor':ROOT.kBlack,'name':'EWK Corrected'})
dijetFakeRatePlotter.addHistogram('data_uncorrected',sigMap['data'],style={'linecolor':ROOT.kRed,'name':'Uncorrected'})

ptbins = [0,10,15,20,25,30,40,50,60,100]#,200,1000]
etabins = [-2.5,-2.0,-1.479,-1.0,-0.5,0.,0.5,1.0,1.479,2.0,2.5]

medium_cust = {
    'pt'     : {'yaxis': 'N_{Medium}/N_{Loose}', 'rebin': ptbins, 'xrange': [0,100]},
    'eta'    : {'yaxis': 'N_{Medium}/N_{Loose}', 'rebin': etabins},
}
tight_cust = {
    'pt'     : {'yaxis': 'N_{Tight}/N_{Loose}', 'rebin': ptbins, 'xrange': [0,100]},
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
            savename = 'ratio/{0}/{1}/{2}'.format(lepton,chan,plot)
            subtractMap = {
                'data': ['MC'],
            }
            customOrder = ['data_uncorrected','data']
            dijetFakeRatePlotter.plotRatio(numname,denomname,savename,ymax=1.,customOrder=customOrder,legendpos=34,numcol=2,subtractMap=subtractMap,**kwargs)
            for etabin in range(5):
                if plot=='eta': continue
                if chan=='m' and etabin>1: continue
                numname = '{0}/{1}/etaBin{2}/{3}'.format(lepton,chan,etabin,plot)
                denomname = 'loose/{0}/etaBin{1}/{2}'.format(chan,etabin,plot)
                savename = 'ratio/{0}/{1}/{2}_etabin{3}'.format(lepton,chan,plot,etabin)
                dijetFakeRatePlotter.plotRatio(numname,denomname,savename,ymax=1.,customOrder=customOrder,legendpos=34,numcol=2,subtractMap=subtractMap,**kwargs)



