from DevTools.Plotter.Plotter import Plotter

effPlotter = Plotter(
    inputDirectory  = 'efficiency',
    outputDirectory = 'plots/Efficiency',
    saveFileName    = 'efficiencies.root',
)

sigMap = {
    'QCD' : [
             'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8',
             'QCD_Pt-15to3000_TuneCUETP8M1_Flat_13TeV_pythia8',
            ],
    'Z'   : [
             'DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
             'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
             'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            ],
    'TT'  : [
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

effPlotter.addHistogram('Z',sigMap['Z'])
effPlotter.addHistogram('TT',sigMap['TT'])
effPlotter.addHistogram('QCD',sigMap['QCD'])
effPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'])

customLabels = {
    'Z'           : 'DY (prompt)', 
    'TT'          : 't#bar{t} (from jet)', 
    'QCD'         : 'QCD (unmatched)', 
    'HppHmm500GeV': '#Phi^{++}#Phi^{--} (prompt)',
}


xaxisMap = {
    'pt'            : 'p_{T} (GeV)',
    'sigmaIEtaIEta' : '#sigma_{i#eta i#eta}',
    'absDEtaIn'     : '|#Delta#eta_{in}|',
    'absDPhiIn'     : '|#Delta#phi_{in}|',
    'hOverE'        : 'E_{HCAL}/E_{ECAL}',
    'relIsoEA'      : 'Rel. Iso.',
    'relIsoDB'      : 'Rel. Iso.',
    'trackRelIso'   : 'Rel. Iso. (tracker)',
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
    numJet = 'h_{0}_jet_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomJet = 'h_{0}_jet_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    numMap = {'Z':num, 'TT':numJet, 'QCD': numFake, 'HppHmm500GeV':num}
    denomMap = {'Z':denom, 'TT':denomJet, 'QCD': denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{e}_{T} (GeV)',customLabels=customLabels,rebin=5)
for region in ['barrel','endcap']:
    for var in ['pt','sigmaIEtaIEta','absDEtaIn','absDPhiIn','hOverE','relIsoEA','ooEmooP','absDxy','absDz','conversionVeto']:
        varname = 'h_electron_{0}_{1}'.format(var,region)
        effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=1)


# muons
for varname in ['wzLoose','wzMedium','highPt_tightiso','tight_tightiso']:
    plotname = 'muon_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    numFake = 'h_{0}_fake_numerator'.format(plotname)
    numJet = 'h_{0}_jet_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    denomJet = 'h_{0}_jet_denominator'.format(plotname)
    numMap = {'Z':num, 'TT':numJet, 'QCD': numFake, 'HppHmm500GeV':num}
    denomMap = {'Z':denom, 'TT':denomJet, 'QCD': denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#mu}_{T} (GeV)',customLabels=customLabels,rebin=5)
for var in ['pt','relIsoDB','absDxy','absDz','trackRelIso']:
    varname = 'h_muon_{0}'.format(var)
    effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=1)

# taus
for varname in ['vlooseElectronLooseMuonOld_tightIso','tightElectronTightMuonOld_tightIso','vlooseElectronLooseMuonNew_tightIso','tightElectronLooseMuonNew_tightIso']:
    plotname = 'tau_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    numFake = 'h_{0}_fake_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    numMap = {'Z':num, 'TT': numFake, 'QCD': numFake, 'HppHmm500GeV':num}
    denomMap = {'Z':denom, 'TT': denomFake, 'QCD': denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#tau}_{T} (GeV)',customLabels=customLabels,customOrder=['Z','QCD','HppHmm500GeV'],rebin=5)
for var in ['pt','absDxy','absDz']:
    varname = 'h_tau_{0}'.format(var)
    effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=1)
