from DevTools.Plotter.Plotter import Plotter
import ROOT

sigPlotter = Plotter(
    'Efficiency',
    inputDirectory  = 'efficiency',
    outputDirectory = 'plots/Efficiency/signal',
)

effPlotter = Plotter(
    'Efficiency',
    inputDirectory  = 'efficiency',
    outputDirectory = 'plots/Efficiency',
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
    'HppHmm200GeV' : ['HPlusPlusHMinusMinusHTo4L_M-200_13TeV-pythia8'],
    'HppHmm300GeV' : ['HPlusPlusHMinusMinusHTo4L_M-300_13TeV-pythia8'],
    'HppHmm400GeV' : ['HPlusPlusHMinusMinusHTo4L_M-400_13TeV-pythia8'],
    'HppHmm500GeV' : ['HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'],
    'HppHmm600GeV' : ['HPlusPlusHMinusMinusHTo4L_M-600_13TeV-pythia8'],
    'HppHmm700GeV' : ['HPlusPlusHMinusMinusHTo4L_M-700_13TeV-pythia8'],
    'HppHmm800GeV' : ['HPlusPlusHMinusMinusHTo4L_M-800_13TeV-pythia8'],
    'HppHmm900GeV' : ['HPlusPlusHMinusMinusHTo4L_M-900_13TeV-pythia8'],
    'HppHmm1.0TeV' : ['HPlusPlusHMinusMinusHTo4L_M-1000_13TeV-pythia8'],
}

effPlotter.addHistogram('Z',sigMap['Z'],style={'name':'DY (prompt)'})
effPlotter.addHistogram('TT',sigMap['TT'],style={'name':'t#bar{t} (from jet)'})
effPlotter.addHistogram('QCD',sigMap['QCD'],style={'name':'QCD (unmatched)'})
effPlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],style={'name':'#Phi^{++}#Phi^{--} (prompt)'})

sigcolors = [
    ROOT.TColor.GetColor('#000000'),
    #ROOT.TColor.GetColor('#1A0000'),
    ROOT.TColor.GetColor('#330000'),
    #ROOT.TColor.GetColor('#4C0000'),
    ROOT.TColor.GetColor('#660000'),
    ROOT.TColor.GetColor('#800000'),
    ROOT.TColor.GetColor('#990000'),
    ROOT.TColor.GetColor('#B20000'),
    ROOT.TColor.GetColor('#CC0000'),
    #ROOT.TColor.GetColor('#E60000'),
    ROOT.TColor.GetColor('#FF0000'),
    #ROOT.TColor.GetColor('#FF1919'),
    ROOT.TColor.GetColor('#FF3333'),
    #ROOT.TColor.GetColor('#FF4D4D'),
    ROOT.TColor.GetColor('#FF6666'),
    ROOT.TColor.GetColor('#FF8080'),
    ROOT.TColor.GetColor('#FF9999'),
    ROOT.TColor.GetColor('#FFB2B2'),
    ROOT.TColor.GetColor('#FFCCCC'),
]


sigPlotter.addHistogram('HppHmm200GeV', sigMap['HppHmm200GeV'],style={'name':'#Phi^{++}#Phi^{--} (200 GeV)', 'linecolor':sigcolors[0], 'fillcolor':sigcolors[0]})
sigPlotter.addHistogram('HppHmm300GeV', sigMap['HppHmm300GeV'],style={'name':'#Phi^{++}#Phi^{--} (300 GeV)', 'linecolor':sigcolors[1], 'fillcolor':sigcolors[1]})
sigPlotter.addHistogram('HppHmm400GeV', sigMap['HppHmm400GeV'],style={'name':'#Phi^{++}#Phi^{--} (400 GeV)', 'linecolor':sigcolors[2], 'fillcolor':sigcolors[2]})
sigPlotter.addHistogram('HppHmm500GeV', sigMap['HppHmm500GeV'],style={'name':'#Phi^{++}#Phi^{--} (500 GeV)', 'linecolor':sigcolors[3], 'fillcolor':sigcolors[3]})
sigPlotter.addHistogram('HppHmm600GeV', sigMap['HppHmm600GeV'],style={'name':'#Phi^{++}#Phi^{--} (600 GeV)', 'linecolor':sigcolors[4], 'fillcolor':sigcolors[4]})
sigPlotter.addHistogram('HppHmm700GeV', sigMap['HppHmm700GeV'],style={'name':'#Phi^{++}#Phi^{--} (700 GeV)', 'linecolor':sigcolors[5], 'fillcolor':sigcolors[5]})
sigPlotter.addHistogram('HppHmm800GeV', sigMap['HppHmm800GeV'],style={'name':'#Phi^{++}#Phi^{--} (800 GeV)', 'linecolor':sigcolors[6], 'fillcolor':sigcolors[6]})
sigPlotter.addHistogram('HppHmm900GeV', sigMap['HppHmm900GeV'],style={'name':'#Phi^{++}#Phi^{--} (900 GeV)', 'linecolor':sigcolors[7], 'fillcolor':sigcolors[7]})
sigPlotter.addHistogram('HppHmm1.0TeV', sigMap['HppHmm1.0TeV'],style={'name':'#Phi^{++}#Phi^{--} (1 TeV)',   'linecolor':sigcolors[8], 'fillcolor':sigcolors[8]})

xaxisMap = {
    'pt'            : 'p_{T} (GeV)',
    'eta'           : '#eta',
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
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{e}_{T} (GeV)',rebin=5)
    sigPlotter.plotRatio(num,denom,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{e}_{T} (GeV)',rebin=5)
for region in ['barrel','endcap']:
    for var in ['pt','sigmaIEtaIEta','absDEtaIn','absDPhiIn','hOverE','relIsoEA','ooEmooP','absDxy','absDz','conversionVeto']:
        varname = 'h_electron_{0}_{1}'.format(var,region)
        effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=0)
        sigPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],logy=0)
for var in ['eta']:
    varname = 'h_electron_{0}'.format(var)
    effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=0)
    sigPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],logy=0)


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
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#mu}_{T} (GeV)',rebin=5)
    sigPlotter.plotRatio(num,denom,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#mu}_{T} (GeV)',rebin=5)
for var in ['pt','eta','relIsoDB','absDxy','absDz','trackRelIso']:
    varname = 'h_muon_{0}'.format(var)
    effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=0)
    sigPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],logy=0)

# taus
for varname in ['vlooseElectronLooseMuonOld_tightIso','tightElectronTightMuonOld_tightIso','vlooseElectronLooseMuonNew_tightIso','tightElectronTightMuonNew_tightIso']:
    plotname = 'tau_{0}'.format(varname)
    num = 'h_{0}_numerator'.format(plotname)
    numFake = 'h_{0}_fake_numerator'.format(plotname)
    denom = 'h_{0}_denominator'.format(plotname)
    denomFake = 'h_{0}_fake_denominator'.format(plotname)
    numMap = {'Z':num, 'TT': numFake, 'QCD': numFake, 'HppHmm500GeV':num}
    denomMap = {'Z':denom, 'TT': denomFake, 'QCD': denomFake, 'HppHmm500GeV':denom}
    effPlotter.plotRatio(numMap,denomMap,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#tau}_{T} (GeV)',customOrder=['Z','QCD','HppHmm500GeV'],rebin=5)
    sigPlotter.plotRatio(num,denom,plotname,numcol=2,legendpos=34,ymax=1.3,ymin=0.,yaxis='Efficiency',xaxis='p^{#tau}_{T} (GeV)',rebin=5)
for var in ['pt','eta','absDxy','absDz']:
    varname = 'h_tau_{0}'.format(var)
    effPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],customOrder=['Z','HppHmm500GeV'],logy=0)
    sigPlotter.plotNormalized(varname,varname,legendps=34,yaxis='Unit Normalized',xaxis=xaxisMap[var],logy=0)
