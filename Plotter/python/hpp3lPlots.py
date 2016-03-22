from DevTools.Plotter.Plotter import Plotter

blind = True

hpp3lPlotter = Plotter(
    inputDirectory  = 'flat/Hpp3l',
    outputDirectory = 'plots/Hpp3l',
    saveFileName    = 'plots.root',
)

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
    'HppHmm500GeV' : ['HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'],
}

for s in ['TT','TTV','Z','WW','WZ','VVV','ZZ']:
    hpp3lPlotter.addHistogramToStack(s,sigMap[s])

hpp3lPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],signal=True)

if not blind:
    hpp3lPlotter.addHistogram('data',sigMap['data'])

plots = {
    'hppMass': {'xaxis': 'm_{l^{#pm}l^{#pm}} (GeV)', 'yaxis': 'Events/20 GeV', 'logy': True, 'numcol': 2, 'lumipos': 33, 'rebin': 2},
}


for plot in plots:
    hpp3lPlotter.plot(plot,plot,**plots[plot])


if blind:
    hpp3lPlotter.addHistogram('data',sigMap['data'])

    blinders = {
        'hppMass': [150,1200],
    }
    
    for plot in blinders:
        savename = '{0}_blinder'.format(plot)
        hpp3lPlotter.plot(plot,savename,blinder=blinders[plot],**plots[plot])
