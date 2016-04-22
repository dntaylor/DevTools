# histParams.py
'''
A map of histogram params.
'''
from copy import deepcopy
from itertools import product, combinations_with_replacement

from DevTools.Plotter.utilities import ZMASS
from DevTools.Plotter.higgsUtilities import getChannels, getGenChannels

################
### 1d hists ###
################
params = {
    # default params
    'common' : {
        'count'                  : {'variable': '1',               'binning': [1,0,2]}, # just a count of events passing selection
        'numVertices'            : {'variable': 'numVertices',     'binning': [40,0,40]},
        'numVertices_noreweight' : {'variable': 'numVertices',     'binning': [40,0,40],                'mcscale': '1./pileupWeight'},
        'met'                    : {'variable': 'met_pt',          'binning': [500, 0, 500]},
        'metPhi'                 : {'variable': 'met_phi',         'binning': [500, -3.14159, 3.14159]},
    },
    # overrides for Electron
    'Electron': {
        'pt'               : {'variable': 'e_pt',            'binning': [1000,0,1000]},
        'eta'              : {'variable': 'e_eta',           'binning': [60,-3.,3.]},
        #'dz'               : {'variable': 'e_dz',            'binning': [50,0,0.5]},
        #'dxy'              : {'variable': 'e_dxy',           'binning': [50,0,0.3]},
        'mvaTrig'          : {'variable': 'e_mvaTrigValues', 'binning': [100,-1.,1.]},
    },
    # overrides for Muon
    'Muon': {
        'pt'               : {'variable': 'm_pt',            'binning': [1000,0,1000]},
        'eta'              : {'variable': 'm_eta',           'binning': [60,-3.,3.]},
        #'dz'               : {'variable': 'm_dz',            'binning': [50,0,0.5]},
        #'dxy'              : {'variable': 'm_dxy',           'binning': [50,0,0.3]},
    },
    # overrides for Tau
    'Tau': {
        'pt'               : {'variable': 't_pt',            'binning': [1000,0,1000]},
        'eta'              : {'variable': 't_eta',           'binning': [60,-3.,3.]},
        #'dz'               : {'variable': 't_dz',            'binning': [50,0,0.5]},
        #'dxy'              : {'variable': 't_dxy',           'binning': [50,0,0.3]},
    },
    # overrides for DijetFakeRate
    'DijetFakeRate': {
        'pt'               : {'variable': 'l1_pt',   'binning': [2000,0,2000]},
        'eta'              : {'variable': 'l1_eta',  'binning': [600,-3.,3.]},
        'wMass'            : {'variable': 'w_mt',    'binning': [500, 0, 500]},
    },
    # overrides for DY
    'DY' : {
        'zMass'                 : {'variable': 'z_mass',                         'binning': [5000, 0, 500]},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [2000, 0, 200]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [5000, 0, 500]},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5]},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5]},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [10000, 0, 1000]},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [10000, 0, 1000]},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
    },
    # overrides for Charge
    'Charge' : {
        'zMass'                 : {'variable': 'z_mass',                         'binning': [5000, 0, 500]},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [2000, 0, 200]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [5000, 0, 500]},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5]},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5]},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [10000, 0, 1000]},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [10000, 0, 1000]},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
    },
    # overrides for TauCharge
    'TauCharge' : {
        'zMass'                 : {'variable': 'z_mass',                         'binning': [5000, 0, 500]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [5000, 0, 500]},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5]},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5]},
        'zTauMuPt'              : {'variable': 'z1_pt',                          'binning': [10000, 0, 1000]},
        'zTauMuEta'             : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zTauHadPt'             : {'variable': 'z2_pt',                          'binning': [10000, 0, 1000]},
        'zTauHadEta'            : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
        'tauMuMt'               : {'variable': 'w1_mt',                          'binning': [5000, 0, 500]},
        'tauHadMt'              : {'variable': 'w2_mt',                          'binning': [5000, 0, 500]},
    },
    # overrides for WZ
    'WZ' : {
        # z
        'zMass'                 : {'variable': 'z_mass',                         'binning': [500, 0, 500]},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [200, 0, 200]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [500, 0, 500]},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5]},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [500, 0, 500]},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [500, 0, 500]},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
        # w
        'wMass'                 : {'variable': 'w_mt',                           'binning': [500, 0, 500]},
        'wPt'                   : {'variable': 'w_pt',                           'binning': [500, 0, 500]},
        'wLeptonPt'             : {'variable': 'w1_pt',                          'binning': [500, 0, 500]},
        'wLeptonEta'            : {'variable': 'w1_eta',                         'binning': [500, -2.5, 2.5]},
        # event
        'mass'                  : {'variable': '3l_mass',                        'binning': [500, 0, 500]},
        'nJets'                 : {'variable': 'numJetsTight30',                 'binning': [10, 0, 10]},
        'nBjets'                : {'variable': 'numBjetsTight30',                'binning': [10, 0, 10]},
    },
    # overrides for Hpp4l
    'Hpp4l' : {
        # h++
        'hppMass'               : {'variable': 'hpp_mass',                       'binning': [1200, 0, 1200]},
        'hppPt'                 : {'variable': 'hpp_pt',                         'binning': [1200, 0, 1200]},
        'hppEta'                : {'variable': 'hpp_eta',                        'binning': [1000, -5, 5]},
        'hppDeltaR'             : {'variable': 'hpp_deltaR',                     'binning': [500, 0, 5]},
        'hppLeadingLeptonPt'    : {'variable': 'hpp1_pt',                        'binning': [1000, 0, 1000]},
        'hppLeadingLeptonEta'   : {'variable': 'hpp1_eta',                       'binning': [500, -2.5, 2.5]},
        'hppSubLeadingLeptonPt' : {'variable': 'hpp2_pt',                        'binning': [1000, 0, 1000]},
        'hppSubLeadingLeptonEta': {'variable': 'hpp2_eta',                       'binning': [500, -2.5, 2.5]},
        # h--
        'hmmMass'               : {'variable': 'hmm_mass',                       'binning': [1200, 0, 1200]},
        'hmmPt'                 : {'variable': 'hmm_pt',                         'binning': [1200, 0, 1200]},
        'hmmEta'                : {'variable': 'hmm_eta',                        'binning': [1000, -5, 5]},
        'hmmDeltaR'             : {'variable': 'hmm_deltaR',                     'binning': [500, 0, 5]},
        'hmmLeadingLeptonPt'    : {'variable': 'hmm1_pt',                        'binning': [1000, 0, 1000]},
        'hmmLeadingLeptonEta'   : {'variable': 'hmm1_eta',                       'binning': [500, -2.5, 2.5]},
        'hmmSubLeadingLeptonPt' : {'variable': 'hmm2_pt',                        'binning': [1000, 0, 1000]},
        'hmmSubLeadingLeptonEta': {'variable': 'hmm2_eta',                       'binning': [500, -2.5, 2.5]},
        # best z
        'zMass'                 : {'variable': 'z_mass',                         'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [200, 0, 200],    'selection': 'z_mass>0.',},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5],    'selection': 'z_mass>0.',},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5],      'selection': 'z_mass>0.',},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [1000, 0, 1000],  'selection': 'z_mass>0.',},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5], 'selection': 'z_mass>0.',},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [1000, 0, 1000],  'selection': 'z_mass>0.',},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5], 'selection': 'z_mass>0.',},
        # event
        'mass'                  : {'variable': '4l_mass',                        'binning': [2000, 0, 2000]},
    },
    # overrides for Hpp3l
    'Hpp3l' : {
        # h++/h--
        'hppMass'               : {'variable': 'hpp_mass',                       'binning': [1200, 0, 1200]},
        'hppPt'                 : {'variable': 'hpp_pt',                         'binning': [1200, 0, 1200]},
        'hppEta'                : {'variable': 'hpp_eta',                        'binning': [1000, -5, 5]},
        'hppDeltaR'             : {'variable': 'hpp_deltaR',                     'binning': [500, 0, 5]},
        'hppLeadingLeptonPt'    : {'variable': 'hpp1_pt',                        'binning': [1000, 0, 1000]},
        'hppLeadingLeptonEta'   : {'variable': 'hpp1_eta',                       'binning': [500, -2.5, 2.5]},
        'hppSubLeadingLeptonPt' : {'variable': 'hpp2_pt',                        'binning': [1000, 0, 1000]},
        'hppSubLeadingLeptonEta': {'variable': 'hpp2_eta',                       'binning': [500, -2.5, 2.5]},
        # h-/h+
        'hmMass'                : {'variable': 'hm_mt',                          'binning': [1200, 0, 1200]},
        'hmPt'                  : {'variable': 'hm_pt',                          'binning': [1200, 0, 1200]},
        'hmEta'                 : {'variable': 'hm_eta',                         'binning': [1000, -5, 5]},
        'hmLeptonPt'            : {'variable': 'hm1_pt',                         'binning': [1000, 0, 1000]},
        'hmLeptonEta'           : {'variable': 'hm1_eta',                        'binning': [500, -2.5, 2.5]},
        # best z
        'zMass'                 : {'variable': 'z_mass',                         'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [200, 0, 200],    'selection': 'z_mass>0.',},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5],    'selection': 'z_mass>0.',},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [1000, 0, 1000],  'selection': 'z_mass>0.',},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5], 'selection': 'z_mass>0.',},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [1000, 0, 1000],  'selection': 'z_mass>0.',},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5], 'selection': 'z_mass>0.',},
        # w
        'wMass'                 : {'variable': 'w_mt',                           'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'wPt'                   : {'variable': 'w_pt',                           'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
        'wEta'                  : {'variable': 'w_eta',                          'binning': [1000, -5, 5],    'selection': 'z_mass>0.',},
        'wLeptonPt'             : {'variable': 'w1_pt',                          'binning': [1000, 0, 1000],  'selection': 'z_mass>0.',},
        'wLeptonEta'            : {'variable': 'w1_eta',                         'binning': [500, -2.5, 2.5], 'selection': 'z_mass>0.',},
        # event
        'mass'                  : {'variable': '3l_mass',                        'binning': [2000, 0, 2000]},
    },
}

################
### 2D hists ###
################
params2D = {
    # default params
    'common' : {

    },
    # overrides for Electron
    'Electron' : {
        #'pt_v_dz' : {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dz)',  'xBinning': [50,0,500], 'yBinning': [50,0,0.5]},
        #'pt_v_dxy': {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dxy)', 'xBinning': [50,0,500], 'yBinning': [50,0,0.3]},
    },
}

##################
### selections ###
##################
selectionParams = {}
sampleSelectionParams = {}

#########################
### some utility cuts ###
#########################
eBarrelCut = 'fabs({0}_eta)<1.479'
eEndcapCut = 'fabs({0}_eta)>1.479'
promptCut = '{0}_genMatch==1 && {0}_genIsPrompt==1 && {0}_genDeltaR<0.1'
promptTauCut = '{0}_genMatch==1 && {0}_genDeltaR<0.1'
genStatusOneCut = '{0}_genMatch==1 && {0}_genStatus==1 && {0}_genDeltaR<0.1'
fakeCut = '({0}_genMatch==0 || ({0}_genMatch==1 && {0}_genIsFromHadron && {0}_genDeltaR<0.1))'
fakeTauCut = '{0}_genMatch==0'

#########################
### electron specific ###
#########################
selectionParams['Electron'] = {
    'default/prompt' : {'args': [promptCut.format('e')],                                       'kwargs': {}},
    'default/fake'   : {'args': [fakeCut.format('e')],                                         'kwargs': {}},
    'barrel/prompt'  : {'args': [' && '.join([promptCut.format('e'),eBarrelCut.format('e')])], 'kwargs': {}},
    'barrel/fake'    : {'args': [' && '.join([fakeCut.format('e'),eBarrelCut.format('e')])],   'kwargs': {}},
    'endcap/prompt'  : {'args': [' && '.join([promptCut.format('e'),eEndcapCut.format('e')])], 'kwargs': {}},
    'edncap/fake'    : {'args': [' && '.join([fakeCut.format('e'),eEndcapCut.format('e')])],   'kwargs': {}},
}

sels = selectionParams['Electron'].keys()
idCuts = {
    'cutBasedVeto'   : 'e_cutBasedVeto==1',
    'cutBasedLoose'  : 'e_cutBasedLoose==1',
    'cutBasedMedium' : 'e_cutBasedMedium==1',
    'cutBasedTight'  : 'e_cutBasedTight==1',
    'wwLoose'        : 'e_wwLoose==1',
    'heepV60'        : 'e_heepV60==1',
    'NonTrigWP80'    : 'e_mvaNonTrigWP80==1',
    'NonTrigWP90'    : 'e_mvaNonTrigWP90==1',
    'TrigPre'        : 'e_mvaTrigPre==1',
    'TrigWP80'       : 'e_mvaTrigPre==1 && e_mvaTrigWP80==1',
    'TrigWP90'       : 'e_mvaTrigPre==1 && e_mvaTrigWP90==1',
}
for sel in sels:
    for idName in idCuts:
        name = '{0}/{1}'.format(sel,idName)
        selectionParams['Electron'][name] = deepcopy(selectionParams['Electron'][sel])
        args = selectionParams['Electron'][name]['args']
        selectionParams['Electron'][name]['args'][0] = args[0] + ' && ' + idCuts[idName]

#####################
### muon specific ###
#####################
selectionParams['Muon'] = {
    'default/prompt' : {'args': [promptCut.format('m')], 'kwargs': {}},
    'default/fake'   : {'args': [fakeCut.format('m')],   'kwargs': {}},
}

sels = selectionParams['Muon'].keys()
idCuts = {
    'isLooseMuon_looseIso'  : 'm_isLooseMuon==1 && m_isolation<0.4',
    'isMediumMuon_tightIso' : 'm_isMediumMuon==1 && m_isolation<0.15',
    'isTightMuon_tightIso'  : 'm_isTightMuon==1 && m_isolation<0.15',
    'isHighPtMuon_tightIso' : 'm_isHighPtMuon==1 && m_isolation<0.15',
    'wzLooseMuon'           : 'm_isMediumMuon==1 && m_trackRelIso<0.4 && m_isolation<0.4',
    'wzMediumMuon'          : 'm_isMediumMuon==1 && m_trackRelIso<0.4 && m_isolation<0.15 && m_dz<0.1 && (m_pt<20 ? m_dxy<0.01 : m_dxy<0.02)',
}
for sel in sels:
    for idName in idCuts:
        name = '{0}/{1}'.format(sel,idName)
        selectionParams['Muon'][name] = deepcopy(selectionParams['Muon'][sel])
        args = selectionParams['Muon'][name]['args']
        selectionParams['Muon'][name]['args'][0] = args[0] + ' && ' + idCuts[idName]

####################
### tau specific ###
####################
selectionParams['Tau'] = {
    'default/prompt' : {'args': [promptTauCut.format('t')], 'kwargs': {}},
    'default/fake'   : {'args': [fakeTauCut.format('t')],   'kwargs': {}},
}

sels = selectionParams['Tau'].keys()
againstElectron = {
    'vloose': 't_againstElectronVLooseMVA6==1',
    'loose' : 't_againstElectronLooseMVA6==1',
    'medium': 't_againstElectronMediumMVA6==1',
    'tight' : 't_againstElectronTightMVA6==1',
    'vtight': 't_againstElectronVTightMVA6==1',
}
againstMuon = {
    'loose' : 't_againstMuonLoose3==1',
    'tight' : 't_againstMuonTight3==1',
}
oldId = 't_decayModeFinding==1'
oldIsolation = {
    'loose' : 't_byLooseIsolationMVArun2v1DBoldDMwLT==1',
    'medium': 't_byMediumIsolationMVArun2v1DBoldDMwLT==1',
    'tight' : 't_byTightIsolationMVArun2v1DBoldDMwLT==1',
    'vtight': 't_byVTightIsolationMVArun2v1DBoldDMwLT==1',
}
idCuts = {}
cutLists = [
    ('vloose','loose','loose'),
    ('vloose','loose','tight'),
    ('vloose','loose','vtight'),
    ('tight','tight','loose'),
    ('tight','tight','tight'),
    ('tight','tight','vtight'),
]
for cl in cutLists:
    idCuts['old_{0}Electron_{1}Muon_{2}Isolation'.format(*cl)] = ' && '.join([oldId, againstElectron[cl[0]], againstMuon[cl[1]], oldIsolation[cl[2]]])

for sel in sels:
    for idName in idCuts:
        name = '{0}/{1}'.format(sel,idName)
        selectionParams['Tau'][name] = deepcopy(selectionParams['Tau'][sel])
        args = selectionParams['Tau'][name]['args']
        selectionParams['Tau'][name]['args'][0] = args[0] + ' && ' + idCuts[idName]

##############################
### DijetFakeRate specific ###
##############################
frBaseCut = 'w_mt<25 && met_pt<25'
frBaseCutLoose = '{0}'.format(frBaseCut)
frBaseCutMedium = '{0} && l1_passMedium==1'.format(frBaseCut)
frBaseCutTight = '{0} && l1_passTight==1'.format(frBaseCut)
frScaleFactorLoose = 'l1_looseScale*genWeight*pileupWeight*triggerEfficiency'#/triggerPrescale'
frScaleFactorMedium = 'l1_mediumScale*genWeight*pileupWeight*triggerEfficiency'#/triggerPrescale'
frScaleFactorTight = 'l1_tightScale*genWeight*pileupWeight*triggerEfficiency'#/triggerPrescale'
dataScaleFactor = 'triggerPrescale'
selectionParams['DijetFakeRate'] = {
    'loose'      : {'args': [frBaseCutLoose],                   'kwargs': {'mcscalefactor': frScaleFactorLoose,  'datascalefactor': dataScaleFactor}},
    'medium'     : {'args': [frBaseCutMedium],                  'kwargs': {'mcscalefactor': frScaleFactorMedium, 'datascalefactor': dataScaleFactor}},
    'tight'      : {'args': [frBaseCutTight],                   'kwargs': {'mcscalefactor': frScaleFactorTight,  'datascalefactor': dataScaleFactor}},
    'loose/pt20' : {'args': [frBaseCutLoose + ' && l1_pt>20'],  'kwargs': {'mcscalefactor': frScaleFactorLoose,  'datascalefactor': dataScaleFactor}},
    'medium/pt20': {'args': [frBaseCutMedium + ' && l1_pt>20'], 'kwargs': {'mcscalefactor': frScaleFactorMedium, 'datascalefactor': dataScaleFactor}},
    'tight/pt20' : {'args': [frBaseCutTight + ' && l1_pt>20'],  'kwargs': {'mcscalefactor': frScaleFactorTight,  'datascalefactor': dataScaleFactor}},
}

channels = ['e','m']

etaBins = {
    'e': [0.,0.5,1.0,1.479,2.0,2.5],
    'm': [0.,1.2,2.4],
}
ptBins = {
    'e': [10,15,20,25,30,40,50,60,80,100,2000],
    'm': [10,15,20,25,30,40,50,60,80,100,2000],
}

jetPtBins = [10,15,20,25,30,35,40,45,50]

for sel in ['loose','medium','tight','loose/pt20','medium/pt20','tight/pt20']:
    for chan in channels:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['DijetFakeRate'][name] = deepcopy(selectionParams['DijetFakeRate'][sel])
        args = selectionParams['DijetFakeRate'][name]['args']
        selectionParams['DijetFakeRate'][name]['args'][0] = args[0] + '&& channel=="{0}"'.format(chan)
        for jetPt in jetPtBins:
            name = '{0}/{1}/jetPt{2}'.format(sel,chan,jetPt)
            selectionParams['DijetFakeRate'][name] = deepcopy(selectionParams['DijetFakeRate'][sel])
            args = selectionParams['DijetFakeRate'][name]['args']
            selectionParams['DijetFakeRate'][name]['args'][0] = args[0] + '&& channel=="{0}" && leadJet_pt>{1}'.format(chan,jetPt)
        if 'pt20' in sel: continue
        for eb in range(len(etaBins[chan])-1):
            directory = '{0}/{1}/etaBin{2}'.format('/'.join(sel.split('_')),chan,eb)
            name = '{0}/{1}/etaBin{2}'.format(sel,chan,eb)
            selectionParams['DijetFakeRate'][name] = deepcopy(selectionParams['DijetFakeRate'][sel])
            args = selectionParams['DijetFakeRate'][name]['args']
            selectionParams['DijetFakeRate'][name]['args'][0] = args[0] + '&& channel=="{0}" && fabs(l1_eta)>={1} && fabs(l1_eta)<{2}'.format(chan,etaBins[chan][eb],etaBins[chan][eb+1])


###################
### DY specific ###
###################
dyBaseCut = 'z1_passMedium==1 && z2_passMedium==1 && z_deltaR>0.02 && z_mass>12. && z1_pt>20. && z2_pt>10. && z_mass>50.'
dyScaleFactor = 'z1_mediumScale*z2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['DY'] = {
    'default' : {'args': [dyBaseCut], 'kwargs': {'mcscalefactor': dyScaleFactor}},
}

channels = ['ee','mm']

for sel in ['default']:
    for chan in channels:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['DY'][name] = deepcopy(selectionParams['DY'][sel])
        args = selectionParams['DY'][name]['args']
        selectionParams['DY'][name]['args'][0] = args[0] + ' && channel=="{0}"'.format(chan)

#######################
### Charge specific ###
#######################
chargeBaseCut = 'z1_passMedium==1 && z2_passMedium==1 && z_deltaR>0.02 && z1_pt>20. && z2_pt>10.'
OS = 'z1_charge!=z2_charge'
SS = 'z1_charge==z2_charge'
chargeOS = '{0} && {1}'.format(chargeBaseCut,OS)
chargeSS = '{0} && {1}'.format(chargeBaseCut,SS)
emZMassCut = 'fabs(z_mass-{1})<10.'.format(chargeBaseCut,ZMASS)
chargeScaleFactor = 'z1_mediumScale*z2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['Charge'] = {}
temp = {
    'OS' : {'args': [chargeOS],        'kwargs': {'mcscalefactor': chargeScaleFactor}},
    'SS' : {'args': [chargeSS],        'kwargs': {'mcscalefactor': chargeScaleFactor}},
}

channelMap = {
    'ee': ['ee'],
    'mm': ['mm'],
}

for sel in ['OS','SS']:
    for chan in channelMap:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['Charge'][name] = deepcopy(temp[sel])
        args = selectionParams['Charge'][name]['args']
        selectionParams['Charge'][name]['args'][0] = args[0] + '&& {0} && ({1})'.format(emZMassCut,' || '.join('channel=="{0}"'.format(c) for c in channelMap[chan]))

##########################
### TauCharge specific ###
##########################
chargeBaseCut = 'z1_passMedium==1 && z2_passMedium==1 && z_deltaR>0.02 && z1_pt>20. && z2_pt>20.'
OS = 'z1_charge!=z2_charge'
SS = 'z1_charge==z2_charge'
chargeOS = '{0} && {1}'.format(chargeBaseCut,OS)
chargeSS = '{0} && {1}'.format(chargeBaseCut,SS)
tZMassCut = 'fabs(z_mass-60)<25.'.format(chargeBaseCut)
chargeScaleFactor = 'z1_mediumScale*z2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['TauCharge'] = {}
temp = {
    'OS'       : {'args': [chargeOS],                   'kwargs': {'mcscalefactor': chargeScaleFactor}},
    'SS'       : {'args': [chargeSS],                   'kwargs': {'mcscalefactor': chargeScaleFactor}},
    'OS/mtCut' : {'args': [chargeOS + ' && w1_mt<40.'], 'kwargs': {'mcscalefactor': chargeScaleFactor}},
    'SS/mtCut' : {'args': [chargeSS + ' && w1_mt<40.'], 'kwargs': {'mcscalefactor': chargeScaleFactor}},
}

channelMap = {
    'tt': ['mt','tm'],
}

for sel in temp:
    for chan in channelMap:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['TauCharge'][name] = deepcopy(temp[sel])
        args = selectionParams['TauCharge'][name]['args']
        selectionParams['TauCharge'][name]['args'][0] = args[0] + '&& {0} && ({1})'.format(tZMassCut,' || '.join('channel=="{0}"'.format(c) for c in channelMap[chan]))

#########################
### wz specific stuff ###
#########################
wzBaseCut = 'z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-{0})<15 && 3l_mass>100'.format(ZMASS)
wzBaseScaleFactor = 'genWeight*pileupWeight*triggerEfficiency'
wzMCCut = ' && '.join([genStatusOneCut.format(l) for l in ['z1','z2','w1']])

wzTightVar = {
    0: 'z1_passMedium',
    1: 'z2_passMedium',
    2: 'w1_passTight',
}

wzTightScale = {
    0: 'z1_mediumScale',
    1: 'z2_mediumScale',
    2: 'w1_tightScale',
}

wzLooseScale = {
    0: 'z1_looseScale',
    1: 'z2_looseScale',
    2: 'w1_looseScale',
}

wzFakeRate = {
    0: 'z1_mediumFakeRate',
    1: 'z2_mediumFakeRate',
    2: 'w1_tightFakeRate',
}

wzScaleMap = {
    'P': wzTightScale,
    'F': wzLooseScale,
}

wzScaleFactorMap = {}
wzFakeScaleFactorMap = {}
wzCutMap = {}
fakeRegions = ['PPP','PPF','PFP','FPP','PFF','FPF','FFP','FFF']
for region in fakeRegions:
    wzScaleFactorMap[region] = '*'.join([wzScaleMap[region[x]][x] for x in range(3)])
    wzFakeScaleFactorMap[region] = '*'.join(['{0}/(1-{0})'.format(wzFakeRate[f]) for f in range(3) if region[f]=='F'] + ['-1' if region.count('F')%2==0 and region.count('F')>0 else '1'])
    wzCutMap[region] = ' && '.join(['{0}=={1}'.format(wzTightVar[x],1 if region[x]=='P' else 0) for x in range(3)]+[wzBaseCut])
# dy/tt all loose
wzScaleFactorMap['loose'] = '*'.join(['{0}_looseScale'.format(x) for x in ['z1','z2','w1']])
wzScaleFactorMap['medium'] = '*'.join(['{0}_mediumScale'.format(x) for x in ['z1','z2','w1']])
wzScaleFactorMap['tight'] = '*'.join(['{0}_tightScale'.format(x) for x in ['z1','z2','w1']])
dySimpleCut = 'z1_pt>20 && z2_pt>10 && w1_pt>10 && fabs(z_mass-{0})<15 && 3l_mass>100 && met_pt<25 && w_mt<25'.format(ZMASS)
ttSimpleCut = 'z1_pt>20 && z2_pt>10 && w1_pt>10 && fabs(z_mass-{0})>5 && 3l_mass>100'.format(ZMASS)
wzCutMap['dy'] = dySimpleCut
wzCutMap['tt'] = ttSimpleCut

selectionParams['WZ'] = {
    'default' : {'args': [wzCutMap['PPP']],       'kwargs': {'mcscalefactor': '*'.join([wzScaleFactorMap['PPP'],wzBaseScaleFactor])}},
}

for region in fakeRegions:
    selectionParams['WZ'][region] = {
        'args': [wzCutMap[region]], 
        'kwargs': {
            'mccut': wzMCCut, 
            'mcscalefactor': '*'.join([wzScaleFactorMap[region],wzFakeScaleFactorMap[region],wzBaseScaleFactor,'1' if region=='PPP' else '-1']),
            'datascalefactor': wzFakeScaleFactorMap[region], 
        }
    }

controls = ['dy','tt']
for control in controls:
    selectionParams['WZ'][control] = {
        'args': [wzCutMap[control]],
        'kwargs': {
            'mccut': wzMCCut,
            'mcscalefactor': '*'.join([wzScaleFactorMap['loose'],wzBaseScaleFactor]),
        }
    }

channels = ['eee','eem','mme','mmm']
sels = selectionParams['WZ'].keys()
for sel in sels:
    for chan in channels:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['WZ'][name] = deepcopy(selectionParams['WZ'][sel])
        args = selectionParams['WZ'][name]['args']
        selectionParams['WZ'][name]['args'][0] = args[0] + ' && channel=="{0}"'.format(chan)

#############
### hpp4l ###
#############
hpp4lBaseCut = 'hpp1_passMedium==1 && hpp2_passMedium==1 && hmm1_passMedium==1 && hmm2_passMedium==1 && hpp_deltaR>0.02 && hmm_deltaR>0.02'
hpp4lLowMassControl = '{0} && (hpp_mass<100 || hmm_mass<100)'.format(hpp4lBaseCut)
hpp4lMatchSign = 'hpp1_genCharge==hpp1_charge && hpp2_genCharge==hpp2_charge && hmm1_genCharge==hmm1_charge && hmm2_genCharge==hmm2_charge'
hpp4lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hmm1_mediumScale*hmm2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['Hpp4l'] = {
    'default'   : {'args': [hpp4lBaseCut],                           'kwargs': {'mcscalefactor': hpp4lScaleFactor}},
    'lowmass'   : {'args': [hpp4lLowMassControl],                    'kwargs': {'mcscalefactor': hpp4lScaleFactor}},
    #'matchSign' : {'args': [hpp4lBaseCut + ' && ' + hpp4lMatchSign], 'kwargs': {'mcscalefactor': hpp4lScaleFactor}},
}

masses = [200,300,400,500,600,700,800,900,1000]

# setup old working points
hpp4lOldSelections = {}
for mass in masses:
    hpp4lOldSelections[mass] = '{base} && (hpp1_pt+hpp2_pt+hmm1_pt+hmm2_pt)>0.6*{mass}+130. && hpp_mass>0.9*{mass} && hpp_mass<1.1*{mass} && hmm_mass>0.9*{mass} && hmm_mass<1.1*{mass}'.format(base=hpp4lBaseCut,mass=mass)
    selectionParams['Hpp4l']['old/{0}'.format(mass)] = {'args': [hpp4lOldSelections[mass]], 'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'countOnly': True}}

# setup reco channel selections
channels = getChannels('Hpp4l')

sels = selectionParams['Hpp4l'].keys()
for sel in sels:
    for chan in channels:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['Hpp4l'][name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = selectionParams['Hpp4l'][name]['args']
        selectionParams['Hpp4l'][name]['args'][0] = args[0] + ' && ' + '(' + ' || '.join(['channel=="{0}"'.format(c) for c in channels[chan]]) + ')'

# setup gen channel selections
genChans = getGenChannels('Hpp4l')
genChannelsPP = genChans['PP']
genChannelsAP = genChans['AP']

hpp4l_pp_selections = {}
hpp4l_ap_selections = {}
sels = selectionParams['Hpp4l'].keys()
for sel in sels:
    for chan in genChannelsPP:
        name = '{0}/gen_{1}'.format(sel,chan)
        hpp4l_pp_selections[name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = hpp4l_pp_selections[name]['args']
        hpp4l_pp_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp4l_pp_selections[name]['kwargs']['countOnly'] = True
    for chan in genChannelsAP:
        name = '{0}/gen_{1}'.format(sel,chan)
        hpp4l_ap_selections[name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = hpp4l_ap_selections[name]['args']
        hpp4l_ap_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp4l_ap_selections[name]['kwargs']['countOnly'] = True
sampleSelectionParams['Hpp4l'] = {}
for mass in masses:
    sampleName = 'HPlusPlusHMinusMinusHTo4L_M-{0}_13TeV-pythia8'.format(mass)
    sampleSelectionParams['Hpp4l'][sampleName] = deepcopy(hpp4l_pp_selections)

#############
### hpp3l ###
#############
hpp3lBaseCut = 'hpp1_passMedium==1 && hpp2_passMedium==1 && hm1_passMedium==1 && hpp_deltaR>0.02'
hpp3lLowMassControl = '{0} && hpp_mass<100'.format(hpp3lBaseCut)
hpp3lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hm1_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['Hpp3l'] = {
    'default' : {'args': [hpp3lBaseCut],        'kwargs': {'mcscalefactor': hpp3lScaleFactor}},
    'lowmass' : {'args': [hpp3lLowMassControl], 'kwargs': {'mcscalefactor': hpp3lScaleFactor}},
}

# setup reco channel selections
channels = getChannels('Hpp3l')

for sel in ['default','lowmass']:
    for chan in channels:
        name = '{0}/{1}'.format(sel,chan)
        selectionParams['Hpp3l'][name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = selectionParams['Hpp3l'][name]['args']
        selectionParams['Hpp3l'][name]['args'][0] = args[0] + ' && ' + '(' + ' || '.join(['channel=="{0}"'.format(c) for c in channels[chan]]) + ')'

# setup gen channel selections
genChans = getGenChannels('Hpp3l')
genChannelsPP = genChans['PP']
genChannelsAP = genChans['AP']

hpp3l_pp_selections = {}
hpp3l_ap_selections = {}
sels = selectionParams['Hpp3l'].keys()
for sel in sels:
    for chan in genChannelsPP:
        name = '{0}/gen_{1}'.format(sel,chan)
        hpp3l_pp_selections[name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = hpp3l_pp_selections[name]['args']
        hpp3l_pp_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp3l_pp_selections[name]['kwargs']['countOnly'] = True
    for chan in genChannelsAP:
        name = '{0}/gen_{1}'.format(sel,chan)
        hpp3l_ap_selections[name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = hpp3l_ap_selections[name]['args']
        hpp3l_ap_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp3l_ap_selections[name]['kwargs']['countOnly'] = True
sampleSelectionParams['Hpp3l'] = {}
for mass in [200,300,400,500,600,700,800,900,1000]:
    sampleName = 'HPlusPlusHMinusMinusHTo4L_M-{0}_13TeV-pythia8'.format(mass)
    sampleSelectionParams['Hpp3l'][sampleName] = deepcopy(hpp3l_pp_selections)

#############################
### functions to retrieve ###
#############################
def getHistParams(analysis):
    histParams = deepcopy(params['common'])
    if analysis in params: histParams.update(params[analysis])
    return histParams

def getHistParams2D(analysis):
    histParams = deepcopy(params2D['common'])
    if analysis in params2D: histParams.update(params2D[analysis])
    return histParams

def getHistSelections(analysis,sample):
    params = {}
    if analysis in selectionParams:
        params.update(selectionParams[analysis])
    if analysis in sampleSelectionParams:
        if sample in sampleSelectionParams[analysis]:
            params.update(sampleSelectionParams[analysis][sample])
    return params
