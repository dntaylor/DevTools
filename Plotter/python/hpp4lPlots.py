import os
import json
import sys
import logging
from itertools import product, combinations_with_replacement

from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy
import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

blind = True

hpp4lPlotter = Plotter(
    inputDirectory  = 'flat/Hpp4l',
    outputDirectory = 'plots/Hpp4l',
)

#########################
### Define categories ###
#########################

cats = ['I','II','III','IV','V','VI']
catLabelMap = {
    'I'  : 'Cat I',
    'II' : 'Cat II',
    'III': 'Cat III',
    'IV' : 'Cat IV',
    'V'  : 'Cat V',
    'VI' : 'Cat VI',
}
catLabels = [catLabelMap[cat] for cat in cats]
# based on number of taus in each higgs
catContentMap = {
    'I'  : [0,0],
    'II' : [0,1],
    'III': [0,2],
    'IV' : [1,1],
    'V'  : [1,2],
    'VI' : [2,2],
}
# based on flavor of light lepton relative to first
# 0,1,2 = e/m,m/e,t
# each cat = [n,n,n,n]
subCats = {
    'I' : {
        'a': [0,0,0,0], # all same flavor
        'b': [0,0,0,1], # on different flavor
        'c': [0,0,1,1], # hpp and hmm same flavor (cleanest)
        'd': [0,1,0,1], # hpp and hmm flavor violating
    },
    'II' : {
        'a': [0,0,0,2], # single tau, rest same
        'b': [0,0,1,2], # one higgs same flavor, other to opposite flavor/tau
        'c': [0,1,0,2], # one flavor violating, other to light + tau
    },
    'III' : {
        'a': [0,0,2,2], # one same, other taus
        'b': [0,1,2,2], # one flavor violating, other taus
    },
    'IV' : {
        'a': [0,2,0,2], # each to same light plus tau
        'b': [0,2,1,2], # each to different light plus tau
    },
    'V' : {
        'a': [0,2,2,2], # to three taus + light
    },
    'VI' : {
        'a': [2,2,2,2], # to 4 taus
    },
}
subCatLabelMap = {
    'I' : {
        'a': 'llll',
        'b': 'llll\'',
        'c': 'lll\'l\'',
        'd': 'll\'ll\'',
    },
    'II' : {
        'a': 'lll#tau',
        'b': 'lll\'#tau',
        'c': 'll\'l#tau',
    },
    'III' : {
        'a': 'll#tau#tau',
        'b': 'll\'#tau#tau',
    },
    'IV' : {
        'a': 'l#tau l#tau',
        'b': 'l#tau l\'#tau',
    },
    'V' : {
        'a': 'l#tau#tau#tau',
    },
    'VI' : {
        'a': '#tau#tau#tau#tau',
    },
}
subCatChannels = {}
for cat in cats:
    subCatChannels[cat] = {}
    for subCat in subCats[cat]:
        strings = []
        for i,l in enumerate(subCats[cat][subCat]):
            if i==0 and l==0:                          # start with a light lepton
                strings = ['e','m']
            elif i==0 and l==2:                        # start with a tau
                strings = ['t']
            elif i>0:                                  # add a character
                if l==2:                               # add a tau
                    for s in range(len(strings)):
                        strings[s] += 't'
                else:                                  # add a light lepton
                    for s in range(len(strings)):
                        if l==subCats[cat][subCat][0]: # add the same light lepton
                            strings[s] += strings[s][0]
                        else:                          # add a different light lepton
                            strings[s] += 'e' if strings[s][0]=='m' else 'm'
        result = []
        for string in strings:
            hpphmm = ''.join(sorted(string[:2]) + sorted(string[2:]))
            if hpphmm not in result: result += [hpphmm]
            hmmhpp = ''.join(sorted(string[2:]) + sorted(string[:2]))
            if hmmhpp not in result: result += [hmmhpp]
        subCatChannels[cat][subCat] = result

subCatLabelList = []
for cat in cats:
    for subCat in sorted(subCatLabelMap[cat]):
        subCatLabelList += [subCatLabelMap[cat][subCat]]

# get individual channels
chans = []
higgsChannels = [''.join(x) for x in product('emt',repeat=2)]
for hpp in higgsChannels:
    for hmm in higgsChannels:
        chanString = ''.join(sorted(hpp))+''.join(sorted(hmm))
        if chanString not in chans: chans += [chanString]

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

samples = ['TT','TTV','Z','WW','WZ','VVV','ZZ']

for s in samples:
    hpp4lPlotter.addHistogramToStack(s,sigMap[s])

hpp4lPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],signal=True)#,scale=10)

if not blind:
    hpp4lPlotter.addHistogram('data',sigMap['data'])

# per channel counts
countVars = ['default/count'] + ['default/{0}/count'.format(chan) for chan in chans]
countLabels = ['Total'] + chanLabels
savename = 'individualChannels'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per category counts
countVars = ['default/count'] + ['default/{0}/count'.format(cat) for cat in cats]
countLabels = ['Total'] + catLabels
savename = 'individualCategories'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per subcategory counts
countVars = ['default/count']
for cat in cats:
    for subCat in sorted(subCatChannels[cat]):
        countVars += [['default/{0}/count'.format(chan) for chan in subCatChannels[cat][subCat]]]
countLabels = ['Total'] + subCatLabelList
savename = 'individualSubCategories'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10,ymin=0.001)




plots = {
    # hpp
    'hppMass'               : {'xaxis': 'm_{l^{+}l^{+}} (GeV)', 'yaxis': 'Events/20 GeV', 'numcol': 2, 'lumipos': 33, 'rebin': 20, 'logy': True},
    'hppPt'                 : {'xaxis': 'p_{T}^{l^{+}l^{+}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    'hppDeltaR'             : {'xaxis': '#DeltaR(l^{+}l^{+})', 'yaxis': 'Events', 'rebin': 25},
    'hppLeadingLeptonPt'    : {'xaxis': 'p_{T}^{#Phi_{lead}^{++}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    'hppSubLeadingLeptonPt' : {'xaxis': 'p_{T}^{#Phi_{sublead}^{++}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    # hmm
    'hmmMass'               : {'xaxis': 'm_{l^{-}l^{-}} (GeV)', 'yaxis': 'Events/20 GeV', 'numcol': 2, 'lumipos': 33, 'rebin': 20, 'logy': True},
    'hmmPt'                 : {'xaxis': 'p_{T}^{l^{-}l^{-}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    'hmmDeltaR'             : {'xaxis': '#DeltaR(l^{-}l^{-})', 'yaxis': 'Events', 'rebin': 25},
    'hmmLeadingLeptonPt'    : {'xaxis': 'p_{T}^{#Phi_{lead}^{--}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    'hmmSubLeadingLeptonPt' : {'xaxis': 'p_{T}^{#Phi_{sublead}^{--}} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
    # z cand
    'zMass'                 : {'xaxis': 'm_{l^{+}l^{-}} (GeV)', 'yaxis': 'Events/10 GeV', 'rebin': 10},
    'mllMinusMZ'            : {'xaxis': '|m_{l^{+}l^{-}}-m_{Z}| (GeV)', 'yaxis': 'Events/5 GeV', 'rebin': 5},
    # event
    'numVertices'           : {'xaxis': 'Reconstructed Vertices', 'yaxis': 'Events'},
    'met'                   : {'xaxis': 'E_{T}^{miss} (GeV)', 'yaxis': 'Events/20 GeV', 'rebin': 20},
}

# signal region
for plot in plots:
    plotname = 'default/{0}'.format(plot)
    hpp4lPlotter.plot(plotname,plot,**plots[plot])
    for cat in cats:
        plotname = 'default/{0}/{1}'.format(cat,plot)
        savename = '{0}/{1}'.format(cat,plot)
        hpp4lPlotter.plot(plotname,savename,**plots[plot])

if blind:
    hpp4lPlotter.addHistogram('data',sigMap['data'])


# partially blinded plots
if blind:
    blinders = {
        'hppMass': [150,1200],
        'hmmMass': [150,1200],
    }
    
    for plot in blinders:
        plotname = 'default/{0}'.format(plot)
        savename = '{0}_blinder'.format(plot)
        hpp4lPlotter.plot(plotname,savename,blinder=blinders[plot],**plots[plot])
        for cat in cats:
            plotname = 'default/{0}/{1}'.format(cat,plot)
            savename = '{0}/{1}_blinder'.format(cat,plot)
            hpp4lPlotter.plot(plotname,savename,blinder=blinders[plot],**plots[plot])


# low mass control
hpp4lPlotter.clearHistograms()

for s in samples:
    hpp4lPlotter.addHistogramToStack(s,sigMap[s])
hpp4lPlotter.addHistogram('data',sigMap['data'])

# per channel counts
countVars = ['lowmass/count'] + ['lowmass/{0}/count'.format(chan) for chan in chans]
countLabels = ['Total'] + chanLabels
savename = 'lowmass/individualChannels'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=2)

# per category counts
countVars = ['lowmass/count'] + ['lowmass/{0}/count'.format(cat) for cat in cats]
countLabels = ['Total'] + catLabels
savename = 'lowmass/individualCategories'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10)

# per subcategory counts
countVars = ['default/count']
for cat in cats:
    for subCat in sorted(subCatChannels[cat]):
        countVars += [['lowmass/{0}/count'.format(chan) for chan in subCatChannels[cat][subCat]]]
countLabels = ['Total'] + subCatLabelList
savename = 'lowmass/individualSubCategories'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=3,logy=1,legendpos=34,yscale=10,ymin=0.001)



lowmass_cust = {
    # hpp
    'hppMass'              : {'rangex': [0,300], 'logy': False},
    'hppPt'                : {'rangex': [0,300]},
    'hppLeadingLeptonPt'   : {'rangex': [0,300]},
    'hppSubLeadingLeptonPt': {'rangex': [0,300]},
    # hmm
    'hmmMass'              : {'rangex': [0,300], 'logy': False},
    'hmmPt'                : {'rangex': [0,300]},
    'hmmLeadingLeptonPt'   : {'rangex': [0,300]},
    'hmmSubLeadingLeptonPt': {'rangex': [0,300]},
    # z
    'zMass'                : {'rangex': [60,120]},
    'mllMinusMZ'           : {'rangex': [0,60]},
    # event
    'met'                  : {'rangex': [0,200]},
}

for plot in plots:
    plotname = 'lowmass/{0}'.format(plot)
    kwargs = deepcopy(plots[plot])
    if plot in lowmass_cust: kwargs.update(lowmass_cust[plot])
    hpp4lPlotter.plot(plotname,plotname,**kwargs)
    for cat in cats:
        plotname = 'lowmass/{0}/{1}'.format(cat,plot)
        hpp4lPlotter.plot(plotname,plotname,**kwargs)


# normalized plots
hpp4lPlotter.clearHistograms()

samples = ['TT','TTV','Z','WW','WZ','VVV','ZZ']
allSamplesDict = {'BG':[]}

for s in samples:
    allSamplesDict['BG'] += sigMap[s]

hpp4lPlotter.addHistogram('BG',allSamplesDict['BG'])
hpp4lPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],signal=True)

norm_cust = {
    # hpp
    'hppMass'               : {'yaxis': 'Unit normalized', 'logy':0, 'rebin': 1},
    'hppPt'                 : {'yaxis': 'Unit normalized', 'rebin': 20, 'numcol': 2},
    'hppDeltaR'             : {'yaxis': 'Unit normalized', 'rebin': 5},
    'hppLeadingLeptonPt'    : {'yaxis': 'Unit normalized', 'rebin': 1},
    'hppSubLeadingLeptonPt' : {'yaxis': 'Unit normalized', 'rebin': 1},
    # hmm
    'hmmMass'               : {'yaxis': 'Unit normalized', 'logy':0, 'rebin': 1},
    'hmmPt'                 : {'yaxis': 'Unit normalized', 'rebin': 20, 'numcol': 2},
    'hmmDeltaR'             : {'yaxis': 'Unit normalized', 'rebin': 5},
    'hmmLeadingLeptonPt'    : {'yaxis': 'Unit normalized', 'rebin': 1},
    'hmmSubLeadingLeptonPt' : {'yaxis': 'Unit normalized', 'rebin': 1},
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
    hpp4lPlotter.plotNormalized(plotname,savename,**kwargs)
    for cat in cats:
        plotname = 'default/{0}/{1}'.format(cat,plot)
        savename = 'normalized/{0}/{1}'.format(cat,plot)
        hpp4lPlotter.plotNormalized(plotname,savename,**kwargs)

# all signal on one plot
hpp4lPlotter.clearHistograms()

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
    hpp4lPlotter.addHistogram('HppHmm{0}GeV'.format(mass),sigMap['HppHmm{0}GeV'.format(mass)],signal=True,style={'linecolor': sigColors[mass]})

for plot in norm_cust:
    plotname = 'default/{0}'.format(plot)
    savename = 'signal/{0}'.format(plot)
    kwargs = deepcopy(plots[plot])
    if plot in norm_cust: kwargs.update(norm_cust[plot])
    hpp4lPlotter.plotNormalized(plotname,savename,**kwargs)
    for cat in cats:
        plotname = 'default/{0}/{1}'.format(cat,plot)
        savename = 'signal/{0}/{1}'.format(cat,plot)
        hpp4lPlotter.plotNormalized(plotname,savename,**kwargs)
