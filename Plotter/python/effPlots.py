from DevTools.Plotter.Plotter import Plotter

effPlotter = Plotter(
    inputDirectory  = 'efficiency',
    outputDirectory = 'plots/Efficiency',
    saveFileName    = 'efficiencies.root',
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
    'HppHmm500GeV' : ['HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'],
}

effPlotter.addHistogram('WZ',sigMap['WZ'])
effPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'])

for varname in ['wzLoose','wzMedium','wzTight','heepV60','mvaTrigWP80','mvaTrigWP90','mvaNonTrigWP80','mvaNonTrigWP90']:
    plotname = 'electron_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    effPlotter.plotRatio(num,denom,plotname,numcol=2,legendpos=34,ymax=1.2,yaxis='Efficiency',xaxis='p_{T} (GeV)')
for varname in ['wzLoose','wzMedium','highPt_tightiso','tight_tightiso']:
    plotname = 'muon_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    effPlotter.plotRatio(num,denom,plotname,numcol=2,legendpos=34,ymax=1.2,yaxis='Efficiency',xaxis='p_{T} (GeV)')
