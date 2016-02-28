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
effPlotter.addHistogram('TT',sigMap['TT'])
effPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'])

xaxisMap = {
    'pt'            : 'p_{T} (GeV)',
    'sigmaIEtaIEta' : '#sigma_{i#eta i#eta}',
    'absDEtaIn'     : '|#Delta#eta_{in}|',
    'absDPhiIn'     : '|#Delta#phi_{in}|',
    'hOverE'        : 'E_{HCAL}/E_{ECAL}',
    'relIsoEA'      : 'Rel. Iso.',
    'ooEmooP'       : '1/E-1/p',
    'absDxy'        : '|#Delta_{xy}|',
    'absDz'         : '|#Delta_{z}|',
    'conversionVeto': 'Pass Conversion Veto',
}

# electrons
for varname in ['wzLoose','wzMedium','wzTight','heepV60','mvaTrigWP80','mvaTrigWP90','mvaNonTrigWP80','mvaNonTrigWP90']:
    plotname = 'electron_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    numFake = 'h_{0}_fake_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    numMap = {'WZ':num, 'TT':numFake, 'HppHmm500GeV':num}
    denomMap = {'WZ':denom, 'TT':denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=3,legendpos=34,ymax=1.2,ymin=0.,yaxis='Efficiency',xaxis='p_{T} (GeV)')
for region in ['barrel','endcap']:
    for var in ['pt','sigmaIEtaIEta','absDEtaIn','absDPhiIn','hOverE','relIsoEA','ooEmooP','absDxy','absDz','conversionVeto']:
        varname = 'h_electron_{0}_{1}'.format(var,region)
        effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var])


# muons
for varname in ['wzLoose','wzMedium','highPt_tightiso','tight_tightiso']:
    plotname = 'muon_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    numFake = 'h_{0}_fake_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    numMap = {'WZ':num, 'TT':numFake, 'HppHmm500GeV':num}
    denomMap = {'WZ':denom, 'TT':denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=3,legendpos=34,ymax=1.2,ymin=0.,yaxis='Efficiency',xaxis='p_{T} (GeV)')
