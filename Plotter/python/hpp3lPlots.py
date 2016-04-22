import os
import json
import sys
import logging
from itertools import product, combinations_with_replacement

from DevTools.Plotter.Plotter import Plotter
from DevTools.Plotter.higgsUtilities import getChannels, getChannelLabels, getCategories, getCategoryLabels, getSubCategories, getSubCategoryLabels
from copy import deepcopy
import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

blind = True

hpp3lPlotter = Plotter('Hpp3l')

#########################
### Define categories ###
#########################

cats = getCategories('Hpp3l')
catLabels = getCategoryLabels('Hpp3l')
subCatChannels = getSubCategories('Hpp3l')
subCatLabels = getSubCategoryLabels('Hpp3l')
chans = getChannels('Hpp3l')
chanLabels = getChannelLabels('Hpp3l')

sigMap = {
    'WZ'  : [
             'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8',
             'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
             'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
             'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
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
    'W'   : [
             'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'Z'   : [
             'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'TT'  : [
             #'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
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
             'Tau',
            ],
    'HppHmm200GeV' : ['HPlusPlusHMinusMinusHTo4L_M-200_13TeV-pythia8'],
    'HppHmm300GeV' : ['HPlusPlusHMinusMinusHTo4L_M-300_13TeV-pythia8'],
    'HppHmm400GeV' : ['HPlusPlusHMinusMinusHTo4L_M-400_13TeV-pythia8'],
    'HppHmm500GeV' : ['HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'],
    'HppHmm600GeV' : ['HPlusPlusHMinusMinusHTo4L_M-600_13TeV-pythia8'],
    'HppHmm700GeV' : ['HPlusPlusHMinusMinusHTo4L_M-700_13TeV-pythia8'],
    'HppHmm800GeV' : ['HPlusPlusHMinusMinusHTo4L_M-800_13TeV-pythia8'],
    'HppHmm900GeV' : ['HPlusPlusHMinusMinusHTo4L_M-900_13TeV-pythia8'],
    'HppHmm1000GeV': ['HPlusPlusHMinusMinusHTo4L_M-1000_13TeV-pythia8'],
}

samples = ['W','TT','TTV','Z','WW','WZ','VVV','ZZ']

for s in samples:
    hpp3lPlotter.addHistogramToStack(s,sigMap[s])

hpp3lPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],signal=True)

if not blind:
    hpp3lPlotter.addHistogram('data',sigMap['data'])

# per channel counts
countVars = ['default/count'] + ['default/{0}/count'.format(chan) for chan in chans]
countLabels = ['Total'] + chanLabels
savename = 'individualChannels'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per category counts
countVars = ['default/count']
for cat in cats:
    tempCountVars = []
    for subcat in subCatChannels[cat]:
        tempCountVars += ['default/{0}/count'.format(chan) for chan in subCatChannels[cat][subcat]]
    countVars += [tempCountVars]
countLabels = ['Total'] + catLabels
savename = 'individualCategories'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per subcategory counts
countVars = ['default/count']
for cat in cats:
    for subCat in sorted(subCatChannels[cat]):
        countVars += [['default/{0}/count'.format(chan) for chan in subCatChannels[cat][subCat]]]
countLabels = ['Total'] + subCatLabels
savename = 'individualSubCategories'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,ymax=1e6,ymin=0.001)




# plot definitions
plots = {
    # hpp
    'hppMass'               : {'xaxis': 'm_{l^{#pm}l^{#pm}} (GeV)', 'yaxis': 'Events / 20 GeV', 'numcol': 2, 'lumipos': 33, 'rebin': 20, 'logy': True},
    'hppPt'                 : {'xaxis': 'p_{T}^{l^{#pm}l^{#pm}} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
    'hppDeltaR'             : {'xaxis': '#DeltaR(l^{#pm}l^{#pm})', 'yaxis': 'Events', 'rebin': 25},
    'hppLeadingLeptonPt'    : {'xaxis': 'p_{T}^{#Phi_{lead}^{#pm#pm}} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
    'hppSubLeadingLeptonPt' : {'xaxis': 'p_{T}^{#Phi_{sublead}^{#pm#pm}} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
    # hm
    'hmMass'                : {'xaxis': 'm_{T}^{l^{#mp}#nu} (GeV)', 'yaxis': 'Events / 20 GeV', 'numcol': 2, 'lumipos': 33, 'rebin': 20},
    'hmPt'                  : {'xaxis': 'p_{T}^{l^{#mp}#nu} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
    'hmLeptonPt'            : {'xaxis': 'p_{T}^{#Phi_{l}^{-}} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
    # z cand
    'zMass'                 : {'xaxis': 'm_{l^{+}l^{-}} (GeV)', 'yaxis': 'Events / 10 GeV', 'rebin': 10},
    'mllMinusMZ'            : {'xaxis': '|m_{l^{+}l^{-}}-m_{Z}| (GeV)', 'yaxis': 'Events / 5 GeV', 'rebin': 5},
    # w cand
    'wMass'                 : {'xaxis': 'm_{T}^{W} (GeV)', 'yaxis': 'Events / 10 GeV', 'rebin': 10},
    # event
    'numVertices'           : {'xaxis': 'Reconstructed Vertices', 'yaxis': 'Events'},
    'met'                   : {'xaxis': 'E_{T}^{miss} (GeV)', 'yaxis': 'Events / 20 GeV', 'rebin': 20},
}

# signal region
for plot in plots:
    plotname = 'default/{0}'.format(plot)
    hpp3lPlotter.plot(plotname,plot,**plots[plot])
    for cat in cats:
        plotnames = []
        for subcat in subCatChannels[cat]:
            plotnames += ['default/{0}/{1}'.format(chan,plot) for chan in subCatChannels[cat][subcat]]
        savename = '{0}/{1}'.format(cat,plot)
        hpp3lPlotter.plot(plotnames,savename,**plots[plot])

if blind:
    hpp3lPlotter.addHistogram('data',sigMap['data'])


# partially blinded plots
if blind:
    blinders = {
        'hppMass': [150,1200],
        'hmMass': [150,1200],
    }

    for plot in blinders:
        plotname = 'default/{0}'.format(plot)
        savename = '{0}_blinder'.format(plot)
        hpp3lPlotter.plot(plotname,savename,blinder=blinders[plot],**plots[plot])
        for cat in cats:
            plotnames = []
            for subcat in subCatChannels[cat]:
                plotnames += ['default/{0}/{1}'.format(chan,plot) for chan in subCatChannels[cat][subcat]]
            savename = '{0}/{1}_blinder'.format(cat,plot)
            hpp3lPlotter.plot(plotnames,savename,blinder=blinders[plot],**plots[plot])


# low mass control
hpp3lPlotter.clearHistograms()

for s in samples:
    hpp3lPlotter.addHistogramToStack(s,sigMap[s])
hpp3lPlotter.addHistogram('data',sigMap['data'])

# per channel counts
countVars = ['lowmass/count'] + ['lowmass/{0}/count'.format(chan) for chan in chans]
countLabels = ['Total'] + chanLabels
savename = 'lowmass/individualChannels'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=2)

# per category counts
countVars = ['lowmass/count']
for cat in cats:
    tempCountVars = []
    for subcat in subCatChannels[cat]:
        tempCountVars += ['lowmass/{0}/count'.format(chan) for chan in subCatChannels[cat][subcat]]
    countVars += [tempCountVars]
countLabels = ['Total'] + catLabels
savename = 'lowmass/individualCategories'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per subcategory counts
countVars = ['lowmass/count']
for cat in cats:
    for subCat in sorted(subCatChannels[cat]):
        countVars += [['lowmass/{0}/count'.format(chan) for chan in subCatChannels[cat][subCat]]]
countLabels = ['Total'] + subCatLabels
savename = 'lowmass/individualSubCategories'
hpp3lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,ymax=1e6,ymin=0.1)

lowmass_cust = {
    # hpp
    'hppMass'              : {'rangex': [0,300], 'logy': False},
    'hppPt'                : {'rangex': [0,300]},
    'hppLeadingLeptonPt'   : {'rangex': [0,300]},
    'hppSubLeadingLeptonPt': {'rangex': [0,300]},
    # hm
    'hmMass'               : {'rangex': [0,300]},
    'hmPt'                 : {'rangex': [0,300]},
    'hmLeptonPt'           : {'rangex': [0,300]},
    # z
    'zMass'                : {'rangex': [0,200]},
    'mllMinusMZ'           : {'rangex': [0,60]},
    # w
    'wMass'                : {'rangex': [0,200]},
    # event
    'met'                  : {'rangex': [0,200]},
}

for plot in plots:
    plotname = 'lowmass/{0}'.format(plot)
    kwargs = deepcopy(plots[plot])
    if plot in lowmass_cust: kwargs.update(lowmass_cust[plot])
    hpp3lPlotter.plot(plotname,plotname,**kwargs)
    for cat in cats:
        plotnames = []
        for subcat in subCatChannels[cat]:
            plotnames += ['lowmass/{0}/{1}'.format(chan,plot) for chan in subCatChannels[cat][subcat]]
        savename = 'lowmass/{0}/{1}'.format(cat,plot)
        hpp3lPlotter.plot(plotnames,savename,**kwargs)

# normalized plots
hpp3lPlotter.clearHistograms()

allSamplesDict = {'BG':[]}

for s in samples:
    allSamplesDict['BG'] += sigMap[s]

hpp3lPlotter.addHistogram('BG',allSamplesDict['BG'])
hpp3lPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],signal=True)

norm_cust = {
    # hpp
    'hppMass'               : {'yaxis': 'Unit normalized', 'logy':0, 'rebin': 1},
    'hppPt'                 : {'yaxis': 'Unit normalized', 'rebin': 20, 'numcol': 2},
    'hppDeltaR'             : {'yaxis': 'Unit normalized', 'rebin': 5},
    'hppLeadingLeptonPt'    : {'yaxis': 'Unit normalized', 'rebin': 1},
    'hppSubLeadingLeptonPt' : {'yaxis': 'Unit normalized', 'rebin': 1},
    # hm
    'hmMass'                : {'yaxis': 'Unit normalized', 'logy':0, 'rebin': 1},
    'hmPt'                  : {'yaxis': 'Unit normalized', 'rebin': 20, 'numcol': 2},
    'hmLeptonPt'            : {'yaxis': 'Unit normalized', 'rebin': 1},
    # z
    'zMass'                 : {'yaxis': 'Unit normalized', 'rebin': 20, 'numcol': 2},
    'mllMinusMZ'            : {'yaxis': 'Unit normalized', 'rebin': 1},
    # event
    'met'                   : {'yaxis': 'Unit normalized', 'rebin': 1},
    'numVertices'           : {'yaxis': 'Unit normalized'},
}

for plot in plots:
    plotname = 'default/{0}'.format(plot)
    savename = 'normalized/{0}'.format(plot)
    kwargs = deepcopy(plots[plot])
    if plot in norm_cust: kwargs.update(norm_cust[plot])
    hpp3lPlotter.plotNormalized(plotname,savename,**kwargs)
    for cat in cats:
        plotnames = []
        for subcat in subCatChannels[cat]:
            plotnames += ['default/{0}/{1}'.format(chan,plot) for chan in subCatChannels[cat][subcat]]
        savename = 'normalized/{0}/{1}'.format(cat,plot)
        hpp3lPlotter.plotNormalized(plotnames,savename,**kwargs)

# all signal on one plot
hpp3lPlotter.clearHistograms()

sigColors = {
    200 : ROOT.TColor.GetColor('#000000'),
    300 : ROOT.TColor.GetColor('#330000'),
    400 : ROOT.TColor.GetColor('#660000'),
    500 : ROOT.TColor.GetColor('#800000'),
    600 : ROOT.TColor.GetColor('#990000'),
    700 : ROOT.TColor.GetColor('#B20000'),
    800 : ROOT.TColor.GetColor('#CC0000'),
    900 : ROOT.TColor.GetColor('#FF0000'),
    1000: ROOT.TColor.GetColor('#FF3333'),
    1100: ROOT.TColor.GetColor('#FF6666'),
    1200: ROOT.TColor.GetColor('#FF8080'),
    1300: ROOT.TColor.GetColor('#FF9999'),
    1400: ROOT.TColor.GetColor('#FFB2B2'),
    1500: ROOT.TColor.GetColor('#FFCCCC'),
}

masses = [200,300,400,500,600,700,800,900,1000]
for mass in masses:
    hpp3lPlotter.addHistogram('HppHmm{0}GeV'.format(mass),sigMap['HppHmm{0}GeV'.format(mass)],signal=True,style={'linecolor': sigColors[mass]})

for plot in norm_cust:
    plotname = 'default/{0}'.format(plot)
    savename = 'signal/{0}'.format(plot)
    kwargs = deepcopy(plots[plot])
    if plot in norm_cust: kwargs.update(norm_cust[plot])
    hpp3lPlotter.plotNormalized(plotname,savename,**kwargs)
    for cat in cats:
        plotnames = []
        for subcat in subCatChannels[cat]:
            plotnames += ['default/{0}/{1}'.format(chan,plot) for chan in subCatChannels[cat][subcat]]
        savename = 'signal/{0}/{1}'.format(cat,plot)
        hpp3lPlotter.plotNormalized(plotnames,savename,**kwargs)
    if 'hpp' in plot: # plot just the channels of the type
        for higgsChan in ['ee','em','et','mm','mt','tt']:
            plotnames = ['default/{0}/{1}'.format(chan,plot) for chan in chans if chan[:2]==higgsChan]
            savename = 'signal/{0}/{1}'.format(higgsChan,plot)
            hpp3lPlotter.plotNormalized(plotnames,savename,**kwargs)

