import os
import sys
import logging
from DevTools.Plotter.Plotter import Plotter
import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


ePlotter = Plotter('Electron')

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

#ePlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'])
ePlotter.addHistogram('HppHmm500GeVBarrel',sigMap['HppHmm500GeV'],style={'name':'#Phi^{++}#Phi^{--} (Barrel)','linecolor':sigcolors[3],'fillcolor':sigcolors[3]})
ePlotter.addHistogram('HppHmm500GeVEndcap',sigMap['HppHmm500GeV'],style={'name':'#Phi^{++}#Phi^{--} (Endcap)','linecolor':sigcolors[6],'fillcolor':sigcolors[6]})

#
#ePlotter.addHistogram('HppHmm200GeV', sigMap['HppHmm200GeV'],style={'name':'#Phi^{++}#Phi^{--} (200 GeV)', 'linecolor':sigcolors[0], 'fillcolor':sigcolors[0]})
#ePlotter.addHistogram('HppHmm300GeV', sigMap['HppHmm300GeV'],style={'name':'#Phi^{++}#Phi^{--} (300 GeV)', 'linecolor':sigcolors[1], 'fillcolor':sigcolors[1]})
#ePlotter.addHistogram('HppHmm400GeV', sigMap['HppHmm400GeV'],style={'name':'#Phi^{++}#Phi^{--} (400 GeV)', 'linecolor':sigcolors[2], 'fillcolor':sigcolors[2]})
#ePlotter.addHistogram('HppHmm500GeV', sigMap['HppHmm500GeV'],style={'name':'#Phi^{++}#Phi^{--} (500 GeV)', 'linecolor':sigcolors[3], 'fillcolor':sigcolors[3]})
#ePlotter.addHistogram('HppHmm600GeV', sigMap['HppHmm600GeV'],style={'name':'#Phi^{++}#Phi^{--} (600 GeV)', 'linecolor':sigcolors[4], 'fillcolor':sigcolors[4]})
#ePlotter.addHistogram('HppHmm700GeV', sigMap['HppHmm700GeV'],style={'name':'#Phi^{++}#Phi^{--} (700 GeV)', 'linecolor':sigcolors[5], 'fillcolor':sigcolors[5]})
#ePlotter.addHistogram('HppHmm800GeV', sigMap['HppHmm800GeV'],style={'name':'#Phi^{++}#Phi^{--} (800 GeV)', 'linecolor':sigcolors[6], 'fillcolor':sigcolors[6]})
#ePlotter.addHistogram('HppHmm900GeV', sigMap['HppHmm900GeV'],style={'name':'#Phi^{++}#Phi^{--} (900 GeV)', 'linecolor':sigcolors[7], 'fillcolor':sigcolors[7]})
#ePlotter.addHistogram('HppHmm1.0TeV', sigMap['HppHmm1.0TeV'],style={'name':'#Phi^{++}#Phi^{--} (1 TeV)',   'linecolor':sigcolors[8], 'fillcolor':sigcolors[8]})

rocplots = {
    'dxy'     : {'legendpos':34,'numcol':3,'invert':True},
    'dz'      : {'legendpos':34,'numcol':3,'invert':True},
    'mvaTrig' : {'legendpos':34,'numcol':3,'invert':False},
}

#for plot,kwargs in rocplots.iteritems():
#    sig = {'HppHmm500GeVBarrel':'{0}_barrel'.format(plot), 'HppHmm500GeVEndcap':'{0}_endcap'.format(plot)}
#    bg = {'HppHmm500GeVBarrel':'{0}_barrel_fake'.format(plot), 'HppHmm500GeVEndcap':'{0}_endcap_fake'.format(plot)}
#    ePlotter.plotROC(sig, bg, 'roc_{0}'.format(plot), **kwargs)

ePlotter.clearHistograms()

ePlotter.addHistogram('HppHmm500GeV',sigMap['HppHmm500GeV'],style={'name': '#Phi^{++}#Phi^{--} (prompt)'})
ePlotter.addHistogram('TT',sigMap['TT'],style={'name':'t#bar{t} (fake)'})

idNames = [
    'cutBasedVeto',
    'cutBasedLoose',
    'cutBasedMedium',
    'cutBasedTight',
    'wwLoose',
    'heepV60',
    'NonTrigWP80',
    'NonTrigWP90',
    'TrigPre',
    'TrigWP80',
    'TrigWP90',
]

for idName in idNames:
    num = {'HppHmm500GeV': 'default/prompt/{0}/pt'.format(idName), 'TT': 'default/fake/{0}/pt'.format(idName)}
    denom = {'HppHmm500GeV': 'default/prompt/pt', 'TT': 'default/fake/pt'}
    savename = idName
    ePlotter.plotRatio(num,denom,savename,rebin=10,xaxis='p_{T} (GeV)',numcol=2)
