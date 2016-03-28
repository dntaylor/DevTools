import os
import sys
import logging
import ROOT

from DevTools.Limits.Limits import Limits

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


hpp4lLimits = Limits()

# setup analysis
logging.info('Add eras')
hpp4lLimits.addEra('13TeV')
logging.info('Add analyses')
hpp4lLimits.addAnalysis('pp')

# setup channels
logging.info('Add channels')
channels = ['eeee']
for chan in channels:
    hpp4lLimits.addChannel(chan)

# setup signal
logging.info('Add signals')
signals = ['pp200']
for signal in signals:
    hpp4lLimits.addProcess(signal,signal=True)

# setup background
logging.info('Add backgrounds')
backgrounds = ['ZZ','Z','TT','TTV','VVV','WZ']
for background in backgrounds:
    hpp4lLimits.addProcess(background)

# add systematics
logging.info('Add systematics')

# lumi
lumisyst = {
    (('all',),('13TeV',),('all',),('all',)): 1.027,
}
hpp4lLimits.addSystematic('lumi_{era}','lnN',systematics=lumisyst)

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
    'pp200' : ['HPlusPlusHMinusMinusHTo4L_M-200_13TeV-pythia8'],
}

def getValue(process,era,analysis,channel):
    val = 0.
    histName = 'default/{0}/count'.format(channel)
    for sample in sigMap[process]:
        fileName = 'flat/Hpp4l/{0}.root'.format(sample)
        tfile = ROOT.TFile.Open(fileName)
        hist = tfile.Get(histName)
        val += hist.Integral()
        tfile.Close()
    return val

# set values
logging.info('Set values')
for era in ['13TeV']:
    for analysis in ['pp']:
        for channel in channels:
            for proc in signals+backgrounds:
                value = getValue(proc,era,analysis,channel)
                hpp4lLimits.setExpected(proc,era,analysis,channel,value)
            obs = getValue('data',era,analysis,channel)
            hpp4lLimits.setObserved(era,analysis,channel,obs)

# print the datacard
logging.info('Print card')
hpp4lLimits.printCard('hpp4l.txt')
