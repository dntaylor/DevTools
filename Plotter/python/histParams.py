# histParams.py
'''
A map of histogram params.
'''
from copy import deepcopy

from DevTools.Plotter.utilities import ZMASS

################
### 1d hists ###
################
params = {
    # default params
    'common' : {
        'count'            : {'variable': '1',               'binning': [1,0,2]}, # just a count of events passing selection
        'numVertices'      : {'variable': 'numVertices',     'binning': [40,0,40]},
        'met'              : {'variable': 'met_pt',          'binning': [500, 0, 500]},
    },
    # overrides for Electron
    'Electron': {
        'pt'               : {'variable': 'e_pt',            'binning': [200,0,1000]},
        'eta'              : {'variable': 'e_eta',           'binning': [60,-3.,3.]},
        'dz'               : {'variable': 'e_dz',            'binning': [50,0,0.5]},
        'dxy'              : {'variable': 'e_dxy',           'binning': [50,0,0.3]},
        'mvaTrig'          : {'variable': 'e_mvaTrigValues', 'binning': [100,-1.,1.]},
    },
    # overrides for Muon
    'Muon': {
        'pt'               : {'variable': 'm_pt',            'binning': [200,0,1000]},
        'eta'              : {'variable': 'm_eta',           'binning': [60,-3.,3.]},
        'dz'               : {'variable': 'm_dz',            'binning': [50,0,0.5]},
        'dxy'              : {'variable': 'm_dxy',           'binning': [50,0,0.3]},
    },
    # overrides for WZ
    'WZ' : {
        'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
        'zLeadingLeptonPt'    : {'variable': 'z1_pt',   'binning': [50, 0, 500]},
        'zSubLeadingLeptonPt' : {'variable': 'z2_pt',   'binning': [50, 0, 500]},
        'wMass'               : {'variable': 'w_mass',  'binning': [50, 0, 200]},
        'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
        'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
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
        'zMass'                 : {'variable': 'z_mass',                         'binning': [500, 0, 500]},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [200, 0, 200]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [500, 0, 500]},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5]},
        'zDeltaR'               : {'variable': 'z_deltaR',                       'binning': [500, 0, 5]},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [1000, 0, 1000]},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [1000, 0, 1000]},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
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
        'hmMass'                : {'variable': 'hm_mass',                        'binning': [1200, 0, 1200]},
        'hmPt'                  : {'variable': 'hm_pt',                          'binning': [1200, 0, 1200]},
        'hmEta'                 : {'variable': 'hm_eta',                         'binning': [1000, -5, 5]},
        'hmLeptonPt'            : {'variable': 'hm1_pt',                         'binning': [1000, 0, 1000]},
        'hmLeptonEta'           : {'variable': 'hm1_eta',                        'binning': [500, -2.5, 2.5]},
        # best z
        'zMass'                 : {'variable': 'z_mass',                         'binning': [500, 0, 500]},
        'mllMinusMZ'            : {'variable': 'fabs(z_mass-{0})'.format(ZMASS), 'binning': [200, 0, 200]},
        'zPt'                   : {'variable': 'z_pt',                           'binning': [500, 0, 500]},
        'zEta'                  : {'variable': 'z_eta',                          'binning': [1000, -5, 5]},
        'zLeadingLeptonPt'      : {'variable': 'z1_pt',                          'binning': [1000, 0, 1000]},
        'zLeadingLeptonEta'     : {'variable': 'z1_eta',                         'binning': [500, -2.5, 2.5]},
        'zSubLeadingLeptonPt'   : {'variable': 'z2_pt',                          'binning': [1000, 0, 1000]},
        'zSubLeadingLeptonEta'  : {'variable': 'z2_eta',                         'binning': [500, -2.5, 2.5]},
        # w
        'wMass'                 : {'variable': 'w_mass',                         'binning': [500, 0, 500]},
        'wPt'                   : {'variable': 'w_pt',                           'binning': [500, 0, 500]},
        'wEta'                  : {'variable': 'w_eta',                          'binning': [1000, -5, 5]},
        'wLeptonPt'             : {'variable': 'w1_pt',                          'binning': [1000, 0, 1000]},
        'wLeptonEta'            : {'variable': 'w1_eta',                         'binning': [500, -2.5, 2.5]},
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
        'pt_v_dz' : {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dz)',  'xBinning': [50,0,500], 'yBinning': [50,0,0.5]},
        'pt_v_dxy': {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dxy)', 'xBinning': [50,0,500], 'yBinning': [50,0,0.3]},
    },
}

##################
### selections ###
##################
selectionParams = {}

#########################
### some utility cuts ###
#########################
eBarrelCut = 'fabs({0}_eta)<1.479'
eEndcapCut = 'fabs({0}_eta)>1.479'
promptCut = '{0}_genMatch==1 && {0}_genIsPrompt==1 && {0}_genDeltaR<0.1'
fakeCut = '({0}_genMatch==0 || ({0}_genMatch==1 && {0}_genIsFromHadron && {0}_genDeltaR<0.1))'

#########################
### electron specific ###
#########################
selectionParams['Electron'] = {
    'default'      : {'args': [promptCut.format('e')],                                       'kwargs': {'directory': 'default/prompt'}},
    'fake'         : {'args': [fakeCut.format('e')],                                         'kwargs': {'directory': 'default/fake'}},
    'barrel'       : {'args': [' && '.join([promptCut.format('e'),eBarrelCut.format('e')])], 'kwargs': {'directory': 'barrel/prompt'}},
    'barrel_fake'  : {'args': [' && '.join([fakeCut.format('e'),eBarrelCut.format('e')])],   'kwargs': {'directory': 'barrel/fake'}},
    'endcap'       : {'args': [' && '.join([promptCut.format('e'),eEndcapCut.format('e')])], 'kwargs': {'directory': 'endcap/prompt'}},
    'edncap_fake'  : {'args': [' && '.join([fakeCut.format('e'),eEndcapCut.format('e')])],   'kwargs': {'directory': 'endcap/fake'}},
}

#########################
### wz specific stuff ###
#########################
wzBaseCut = 'z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100'
wzBaseScaleFactor = 'genWeight*pileupWeight'
wzPromptCut = ' && '.join([promptCut.format(l) for l in ['z1','z2','w1']])

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

wzScaleMap = {
    'P': wzTightScale,
    'F': wzLooseScale,
}

wzScaleFactorMap = {}
wzCutMap = {}
for region in ['PPP','PPF','PFP','FPP','PFF','FPF','FFP','FFF']:
    wzScaleFactorMap[region] = '*'.join([wzScaleMap[region[x]][x] for x in range(3)])
    wzCutMap[region] = ' && '.join(['{0}=={1}'.format(wzTightVar[x],1 if region[x]=='P' else 0) for x in range(3)]+[wzBaseCut])

selectionParams['WZ'] = {
    'default' : {'args': [wzBaseCut],       'kwargs': {'mcscalefactor': '*'.join([wzScaleFactorMap['PPP'],wzBaseScaleFactor]), 'directory': 'default'}},
    'PPP'     : {'args': [wzCutMap['PPP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PPP'],wzBaseScaleFactor]), 'directory': 'PPP'}},
    'PPF'     : {'args': [wzCutMap['PPF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PPF'],wzBaseScaleFactor]), 'directory': 'PPF'}},
    'PFP'     : {'args': [wzCutMap['PFP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PFP'],wzBaseScaleFactor]), 'directory': 'PFP'}},
    'FPP'     : {'args': [wzCutMap['FPP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FPP'],wzBaseScaleFactor]), 'directory': 'FPP'}},
    'PFF'     : {'args': [wzCutMap['PFF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PFF'],wzBaseScaleFactor]), 'directory': 'PFF'}},
    'FPF'     : {'args': [wzCutMap['FPF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FPF'],wzBaseScaleFactor]), 'directory': 'FPF'}},
    'FFP'     : {'args': [wzCutMap['FFP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FFP'],wzBaseScaleFactor]), 'directory': 'FFP'}},
    'FFF'     : {'args': [wzCutMap['FFF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FFF'],wzBaseScaleFactor]), 'directory': 'FFF'}},
}

#############
### hpp4l ###
#############
hpp4lBaseCut = 'hpp1_passMedium==1 && hpp2_passMedium==1 && hmm1_passMedium==1 && hmm2_passMedium==1'
hpp4lLowMassControl = '{0} && hpp_mass<170 && hmm_mass<170'.format(hpp4lBaseCut)
hpp4lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hmm1_mediumScale*hmm2_mediumScale*genWeight*pileupWeight'
selectionParams['Hpp4l'] = {
    'default' : {'args': [hpp4lBaseCut],        'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'directory': 'default'}},
    'lowmass' : {'args': [hpp4lLowMassControl], 'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'directory': 'lowmass'}},
}

channels = []
higgsChannels = ['ee','em','me','mm']
for hpp in higgsChannels:
    for hmm in higgsChannels:
        channels += [hpp+hmm]

for sel in ['default','lowmass']:
    for chan in channels:
        directory = '{0}/{1}'.format(sel,chan)
        name = '{0}_{1}'.format(sel,chan)
        selectionParams['Hpp4l'][name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = selectionParams['Hpp4l'][name]['args']
        selectionParams['Hpp4l'][name]['args'][0] = args[0] + ' && channel=="{0}"'.format(chan)
        selectionParams['Hpp4l'][name]['kwargs']['directory'] = directory

#############
### hpp3l ###
#############
hpp3lBaseCut = 'hpp1_passMedium==1 && hpp2_passMedium==1 && hm1_passMedium==1'
hpp3lLowMassControl = '{0} && hpp_mass<170 && hm_mass<170'.format(hpp3lBaseCut)
hpp3lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hm1_mediumScale*genWeight*pileupWeight'
selectionParams['Hpp3l'] = {
    'default' : {'args': [hpp3lBaseCut],        'kwargs': {'mcscalefactor': hpp3lScaleFactor, 'directory': 'default'}},
    'lowmass' : {'args': [hpp3lLowMassControl], 'kwargs': {'mcscalefactor': hpp3lScaleFactor, 'directory': 'lowmass'}},
}

channels = []
higgsChannels = ['ee','em','me','mm']
higgsChannels2 = ['e', 'm']
for hpp in higgsChannels:
    for hm in higgsChannels2:
        channels += [hpp+hm]

for sel in ['default','lowmass']:
    for chan in channels:
        directory = '{0}/{1}'.format(sel,chan)
        name = '{0}_{1}'.format(sel,chan)
        selectionParams['Hpp3l'][name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = selectionParams['Hpp3l'][name]['args']
        selectionParams['Hpp3l'][name]['args'][0] = args[0] + ' && channel=="{0}"'.format(chan)
        selectionParams['Hpp3l'][name]['kwargs']['directory'] = directory

#############################
### functions to retrieve ###
#############################
def getHistParams(analysis):
    histParams = deepcopy(params['common'])
    if analysis in params: histParams.update(params[analysis])
    return histParams

def getHistParams2D(analysis):
    histParams = deepcopy(params2D['common'])
    if analysis in params: histParams.update(params2D[analysis])
    return histParams

def getHistSelections(analysis):
    return selectionParams[analysis] if analysis in selectionParams else {}
