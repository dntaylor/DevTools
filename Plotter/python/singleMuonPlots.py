from DevTools.Plotter.Plotter import Plotter

blind = True

mPlotter = Plotter('SingleMuon')

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

mPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'])

plots = {
    'pt_v_dxy': {'xaxis':'p_{T} (GeV)', 'yaxis': '|#Delta_{xy}|'},
    'pt_v_dz' : {'xaxis':'p_{T} (GeV)', 'yaxis': '|#Delta_{z}|'},
}

for plot,kwargs in plots.iteritems():
    mPlotter.plot2D(plot,'hpp_{0}'.format(plot),logz=0,**kwargs)

mPlotter.clearHistograms()

mPlotter.addHistogram('Z',sigMap['Z'])

for plot,kwargs in plots.iteritems():
    mPlotter.plot2D(plot,'dy_{0}'.format(plot),logz=1,**kwargs)
