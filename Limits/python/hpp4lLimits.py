import os
import sys
import logging
import ROOT
import numpy as np
import math

from DevTools.Limits.Limits import Limits
from DevTools.Limits.utilities import readCount
from DevTools.Plotter.utilities import python_mkdir

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Scales(object):
    def __init__(self, br_ee, br_em, br_et, br_mm, br_mt, br_tt):
        self.a_3l = np.array([br_ee, br_em, br_et, br_mm, br_mt, br_tt], dtype=float)
        self.m_4l = np.outer(self.a_3l, self.a_3l)
        self.index = {"ee": 0, "em": 1, "et": 2, "mm": 3, "mt": 4, "tt": 5}
    def scale_Hpp4l(self, hpp, hmm):
        i = self.index[hpp]
        j = self.index[hmm]
        return self.m_4l[i,j] * 36.0
    def scale_Hpp3l(self, hpp, hm='a'):
        i = self.index[hpp]
        scale = 9./2
        if hpp in ['ee','mm','tt']: scale = 9.
        return self.a_3l[i] * scale

masses = [200,300,400,500,600,700,800,900,1000]
modes = ['ee100','em100','et100','mm100','mt100','tt100','BP1','BP2','BP3','BP4']
backgrounds = ['ZZ','Z','TT','TTV','VVV','WZ']

#masses = [200]
#modes = ['ee100']
#backgrounds = ['ZZ','TTV']

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
    'HppHmm300GeV' : ['HPlusPlusHMinusMinusHTo4L_M-300_13TeV-pythia8'],
    'HppHmm400GeV' : ['HPlusPlusHMinusMinusHTo4L_M-400_13TeV-pythia8'],
    'HppHmm500GeV' : ['HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'],
    'HppHmm600GeV' : ['HPlusPlusHMinusMinusHTo4L_M-600_13TeV-pythia8'],
    'HppHmm700GeV' : ['HPlusPlusHMinusMinusHTo4L_M-700_13TeV-pythia8'],
    'HppHmm800GeV' : ['HPlusPlusHMinusMinusHTo4L_M-800_13TeV-pythia8'],
    'HppHmm900GeV' : ['HPlusPlusHMinusMinusHTo4L_M-900_13TeV-pythia8'],
    'HppHmm1000GeV': ['HPlusPlusHMinusMinusHTo4L_M-1000_13TeV-pythia8'],
}

# no tau yet
allowedRecoChannels = {
    'ee100': ['ee'],
    'em100': ['em'],
    'et100': ['ee','em'],
    'mm100': ['mm'],
    'mt100': ['em','mm'],
    'tt100': ['ee','em','mm'],
    'BP1'  : ['ee','em','mm'],
    'BP2'  : ['ee','em','mm'],
    'BP3'  : ['ee','em','mm'],
    'BP4'  : ['ee','em','mm'],
}

allowedHiggsChannels = {
    'ee100': ['ee'],
    'em100': ['em'],
    'et100': ['et'],
    'mm100': ['mm'],
    'mt100': ['mt'],
    'tt100': ['tt'],
    'BP1'  : ['em','et','mm','mt','tt'],
    'BP2'  : ['ee','mm','mt','tt'],
    'BP3'  : ['ee','mm','tt'],
    'BP4'  : ['ee','em','et','mm','mt','tt'],
}

scales = {
    'ee100': Scales(1., 0., 0., 0., 0., 0.),
    'em100': Scales(0., 1., 0., 0., 0., 0.),
    'et100': Scales(0., 0., 1., 0., 0., 0.),
    'mm100': Scales(0., 0., 0., 1., 0., 0.),
    'mt100': Scales(0., 0., 0., 0., 1., 0.),
    'tt100': Scales(0., 0., 0., 0., 0., 1.),
    'BP1'  : Scales(0, 0.01, 0.01, 0.3, 0.38, 0.3),
    'BP2'  : Scales(1./2., 0, 0, 1./8., 1./4., 1./8.),
    'BP3'  : Scales(1./3., 0, 0, 1./3., 0, 1./3.),
    'BP4'  : Scales(1./6., 1./6., 1./6., 1./6., 1./6., 1./6.),
}

for mode in modes:
    for mass in masses:
        logging.info('Producing datacard for {0} - {1} GeV'.format(mode,mass))
        limits = Limits()
    
        limits.addEra('13TeV')
        limits.addAnalysis('Hpp4l')
        
        genChannels = []
        for hpp in allowedHiggsChannels[mode]:
            for hmm in allowedHiggsChannels[mode]:
                chan = hpp+hmm
                genChannels += [chan]

        recoChannels = []
        for hpp in allowedRecoChannels[mode]:
            for hmm in allowedRecoChannels[mode]:
                chan = hpp+hmm
                recoChannels += [chan]
                limits.addChannel(chan)

        signals = ['HppHmm{0}GeV'.format(mass)]
        for sig in signals:
            limits.addProcess(sig,signal=True)
        
        for background in backgrounds:
            limits.addProcess(background)

        # set values and stat error
        staterr = {}
        for era in ['13TeV']:
            for analysis in ['Hpp4l']:
                for channel in recoChannels:
                    for proc in backgrounds:
                        value,err = readCount(['flat/Hpp4l/{0}.root'.format(s) for s in sigMap[proc]],['old/{mass}/{chan}'.format(mass=mass,chan=channel)],doError=True)
                        limits.setExpected(proc,era,analysis,channel,value)
                        if value: staterr[((proc,),(era,),(analysis,),(channel,))] = 1+err/value
                    for proc in signals:
                        totalValue = 0.
                        err2 = 0.
                        for genChannel in genChannels:
                            value,err = readCount(['flat/Hpp4l/{0}.root'.format(s) for s in sigMap[proc]],['old/{mass}/{chan}/gen_{genchan}'.format(mass=mass,chan=channel,genchan=genChannel)],doError=True)
                            scale = scales[mode].scale_Hpp4l(genChannel[:2],genChannel[2:])
                            totalValue += scale*value
                            err2 += (scale*err)**2
                        limits.setExpected(proc,era,analysis,channel,totalValue)
                        if totalValue: staterr[((proc,),(era,),(analysis,),(channel,))] = 1.+err2**0.5/totalValue
                    obs = readCount(['flat/Hpp4l/{0}.root'.format(s) for s in sigMap['data']],['old/{mass}/{chan}'.format(mass=mass,chan=channel)])
                    limits.setObserved(era,analysis,channel,obs)

        # systematics
        # stat errs
        limits.addSystematic('stat_{process}','lnN',systematics=staterr)

        # lumi 2.7% for 2015
        lumisyst = {
            (('all',),('13TeV',),('all',),('all',)): 1.027,
        }
        limits.addSystematic('lumi_{era}','lnN',systematics=lumisyst)

        # electron id 2%/leg
        elecsyst = {}
        for c in range(4):
            systChans = tuple([chan for chan in recoChannels if chan.count('e')==c+1])
            if not systChans: continue
            elecsyst[(('all',),('13TeV',),('Hpp4l',),systChans)] = 1.+math.sqrt((c+1)*0.02**2)
        if elecsyst: limits.addSystematic('elec_id','lnN',systematics=elecsyst)

        # muon id 1+0.5%/leg
        muonsyst = {}
        for c in range(4):
            systChans = tuple([chan for chan in recoChannels if chan.count('m')==c+1])
            if not systChans: continue
            muonsyst[(('all',),('13TeV',),('Hpp4l',),systChans)] = 1.+math.sqrt((c+1)*(0.01**2 + 0.005**2))
        if muonsyst: limits.addSystematic('muon_id','lnN',systematics=muonsyst)

        # print the datacard
        directory = 'datacards/{0}/{1}'.format('Hpp4l',mode)
        python_mkdir(directory)
        limits.printCard('{0}/{1}.txt'.format(directory,mass))
