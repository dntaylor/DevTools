from DevTools.Plotter.Plotter import Plotter
from copy import deepcopy

blind = True

hpp4lPlotter = Plotter(
    inputDirectory  = 'flat/Hpp4l',
    outputDirectory = 'plots/Hpp4l',
)

hppChans = ['ee','em','me','mm']
chans = []
for hpp in hppChans:
    for hmm in hppChans:
        chans += [hpp+hmm]

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
    'HppHmm200GeV' : ['HPlusPlusHMinusMinusHTo4L_M-200_13TeV-pythia8'],
}

samples = ['TT','TTV','Z','WW','WZ','VVV','ZZ']

for s in samples:
    hpp4lPlotter.addHistogramToStack(s,sigMap[s])

hpp4lPlotter.addHistogram('HppHmm200GeV',sigMap['HppHmm200GeV'],signal=True,scale=10)

if not blind:
    hpp4lPlotter.addHistogram('data',sigMap['data'])

# per channel counts
countVars = ['default/count'] + ['default/{0}/count'.format(chan) for chan in chans]
countLabels = ['Total'] + chanLabels
savename = 'individualChannels'
hpp4lPlotter.plotCounts(countVars,countLabels,savename,numcol=2)


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
