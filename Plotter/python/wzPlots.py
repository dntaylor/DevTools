from DevTools.Plotter.Plotter import Plotter

wzPlotter = Plotter(
    inputDirectory  = 'flat/WZ',
    outputDirectory = 'plots/WZ',
    saveFileName    = 'plots.root',
)

sigMap = {
    'WZ'  : ['WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8'],
    'ZZ'  : ['ZZTo4L_13TeV_powheg_pythia8',
             'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
             'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
             'ZZTo2L2Nu_13TeV_powheg_pythia8',
             'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8'],
    'VVV' : ['WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'],
    'TTV' : ['TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'],
    'ZG'  : ['ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'],
    'WW'  : ['WWTo2L2Nu_13TeV-powheg'],
    'Z'   : ['DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'],
    'TT'  : ['TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'],
    'data': ['DoubleMuon',
             'DoubleEG',
             'MuonEG',
             'SingleMuon',
             'SingleElectron'],
}

samples = ['TTV','ZG','VVV','ZZ','WZ']

datadrivenSamples = []
for s in samples + ['data']:
    datadrivenSamples += sigMap[s]
wzPlotter.addHistogramToStack('datadriven',datadrivenSamples)

for s in samples:
    wzPlotter.addHistogramToStack(s,sigMap[s])

wzPlotter.addHistogram('data',sigMap['data'])

plotStyles = {
    'zMass': {'xaxis': 'm_{l^{+}l^{-}}', 'yaxis': 'Events/1 GeV', 'rangex':[60,120]},
}

def getDataDrivenPlot(plot):
    histMap = {}
    plotdirs = plot.split('/')
    for s in samples + ['data']: histMap[s] = '/'.join(plotdirs[:-1]+['PPP']+plotdirs[-1:])
    regions = ['PPF','PFP','FPP','PFF','FPF','FFP','FFF']
    histMap['datadriven'] = ['/'.join(plotdirs[:-1]+[reg]+plotdirs[-1:]) for reg in regions]
    return histMap

for plot in ['zMass']:
    plotvars = getDataDrivenPlot(plot)
    savename = plot
    wzPlotter.plot(plotvars,savename,**plotStyles[plot])
