# histParams.py
'''
A map of histogram params.
'''
from copy import deepcopy

params = {
    # default params
    'common' : {

    },
    # overrides for Electron
    'Electron': {
        'pt'               : {'variable': 'e_pt',            'binning': [200,0,1000]},
        'eta'              : {'variable': 'e_eta',           'binning': [60,-3.,3.]},
        'dz'               : {'variable': 'e_dz',            'binning': [50,0,0.5]},
        'dxy'              : {'variable': 'e_dxy',           'binning': [50,0,0.3]},
        'mvaTrig'          : {'variable': 'e_mvaTrigValues', 'binning': [100,-1.,1.]},
    },
    # overrides for WZ
    'WZ' : {
        'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
        'zLeadingLeptonPt'    : {'variable': 'z1_pt',   'binning': [50, 0, 500]},
        'zSubLeadingLeptonPt' : {'variable': 'z2_pt',   'binning': [50, 0, 500]},
        'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
        'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
        'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
    },
}


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


# some utility cuts
eBarrelCut = 'fabs({0}_eta)<1.479'
eEndcapCut = 'fabs({0}_eta)>1.479'
promptCut = '{0}_genMatch==1 && {0}_genIsPrompt==1 && {0}_genDeltaR<0.1'
fakeCut = '({0}_genMatch==0 || ({0}_genMatch==1 && {0}_genIsFromHadron && {0}_genDeltaR<0.1))'

# wz specific stuff
wzBaseCut = 'z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100'
wzBaseScaleFactor = 'genWeight'
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

selectionParams = {
    'Electron' : {
        'default'      : {'args': [promptCut.format('e')],                                       'kwargs': {}},
        'fake'         : {'args': [fakeCut.format('e')],                                         'kwargs': {'postfix': 'fake'}},
        'barrel'       : {'args': [' && '.join([promptCut.format('e'),eBarrelCut.format('e')])], 'kwargs': {'postfix': 'barrel'}},
        'barrel_fake'  : {'args': [' && '.join([fakeCut.format('e'),eBarrelCut.format('e')])],   'kwargs': {'postfix': 'barrel_fake'}},
        'endcap'       : {'args': [' && '.join([promptCut.format('e'),eEndcapCut.format('e')])], 'kwargs': {'postfix': 'endcap'}},
        'edncap_fake'  : {'args': [' && '.join([fakeCut.format('e'),eEndcapCut.format('e')])],   'kwargs': {'postfix': 'endcap_fake'}},
    },
    'WZ' : {
        'default'      : {'args': [wzBaseCut],       'kwargs': {'mcscalefactor': '*'.join([wzScaleFactorMap['PPP'],wzBaseScaleFactor])}},
        'PPP'          : {'args': [wzCutMap['PPP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PPP'],wzBaseScaleFactor]), 'postfix': 'PPP'}},
        'PPF'          : {'args': [wzCutMap['PPF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PPF'],wzBaseScaleFactor]), 'postfix': 'PPF'}},
        'PFP'          : {'args': [wzCutMap['PFP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PFP'],wzBaseScaleFactor]), 'postfix': 'PFP'}},
        'FPP'          : {'args': [wzCutMap['FPP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FPP'],wzBaseScaleFactor]), 'postfix': 'FPP'}},
        'PFF'          : {'args': [wzCutMap['PFF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['PFF'],wzBaseScaleFactor]), 'postfix': 'PFF'}},
        'FPF'          : {'args': [wzCutMap['FPF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FPF'],wzBaseScaleFactor]), 'postfix': 'FPF'}},
        'FFP'          : {'args': [wzCutMap['FFP']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FFP'],wzBaseScaleFactor]), 'postfix': 'FFP'}},
        'FFF'          : {'args': [wzCutMap['FFF']], 'kwargs': {'mccut': wzPromptCut, 'mcscalefactor': '*'.join([wzScaleFactorMap['FFF'],wzBaseScaleFactor]), 'postfix': 'FFF'}},
    },
}

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
