# histParams.py
'''
A map of histogram params.
'''
from copy import deepcopy
from itertools import product, combinations_with_replacement

from DevTools.Plotter.utilities import ZMASS

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
        'hmMass'                : {'variable': 'hm_mass',                        'binning': [1200, 0, 1200]},
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
        'wMass'                 : {'variable': 'w_mass',                         'binning': [500, 0, 500],    'selection': 'z_mass>0.',},
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
        'pt_v_dz' : {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dz)',  'xBinning': [50,0,500], 'yBinning': [50,0,0.5]},
        'pt_v_dxy': {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dxy)', 'xBinning': [50,0,500], 'yBinning': [50,0,0.3]},
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

###################
### DY specific ###
###################
dyBaseCut = 'z1_passMedium==1 && z2_passMedium==1 && z_deltaR>0.02 && z_mass>12. && z1_pt>20. && z2_pt>10. && z_mass>50.'
dyScaleFactor = 'z1_mediumScale*z2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['DY'] = {
    'default' : {'args': [dyBaseCut],        'kwargs': {'mcscalefactor': dyScaleFactor, 'directory': 'default'}},
}

channels = ['ee','mm']

for sel in ['default']:
    for chan in channels:
        directory = '{0}/{1}'.format(sel,chan)
        name = '{0}_{1}'.format(sel,chan)
        selectionParams['DY'][name] = deepcopy(selectionParams['DY'][sel])
        args = selectionParams['DY'][name]['args']
        selectionParams['DY'][name]['args'][0] = args[0] + ' && channel=="{0}"'.format(chan)
        selectionParams['DY'][name]['kwargs']['directory'] = directory


#########################
### wz specific stuff ###
#########################
wzBaseCut = 'z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100'
wzBaseScaleFactor = 'genWeight*pileupWeight*triggerEfficiency'
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
hpp4lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hmm1_mediumScale*hmm2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['Hpp4l'] = {
    'default' : {'args': [hpp4lBaseCut],        'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'directory': 'default'}},
    'lowmass' : {'args': [hpp4lLowMassControl], 'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'directory': 'lowmass'}},
}

masses = [200,300,400,500,600,700,800,900,1000]

# setup old working points
hpp4lOldSelections = {}
for mass in masses:
    hpp4lOldSelections[mass] = '{base} && (hpp1_pt+hpp2_pt+hmm1_pt+hmm2_pt)>0.6*{mass}+130. && hpp_mass>0.9*{mass} && hpp_mass<1.1*{mass} && hmm_mass>0.9*{mass} && hmm_mass<1.1*{mass}'.format(base=hpp4lBaseCut,mass=mass)
    selectionParams['Hpp4l']['old_{0}'.format(mass)] = {'args': [hpp4lOldSelections[mass]], 'kwargs': {'mcscalefactor': hpp4lScaleFactor, 'directory': 'old/{0}'.format(mass), 'countOnly': True}}

# setup reco channel selections
channels = {}
higgsChannels = [''.join(x) for x in product('em',repeat=2)]
for hpp in higgsChannels:
    for hmm in higgsChannels:
        chanString = ''.join(sorted(hpp))+''.join(sorted(hmm))
        if chanString not in channels: channels[chanString] = []
        channels[chanString] += [hpp+hmm]

sels = selectionParams['Hpp4l'].keys()
for sel in sels:
    for chan in channels:
        directory = '{0}/{1}'.format('/'.join(sel.split('_')),chan)
        name = '{0}_{1}'.format(sel,chan)
        selectionParams['Hpp4l'][name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = selectionParams['Hpp4l'][name]['args']
        selectionParams['Hpp4l'][name]['args'][0] = args[0] + ' && ' + '(' + ' || '.join(['channel=="{0}"'.format(c) for c in channels[chan]]) + ')'
        selectionParams['Hpp4l'][name]['kwargs']['directory'] = directory

# setup gen channel selections
genChannelsPP = []
genChannelsAP = []
genHiggsChannels = [''.join(x) for x in combinations_with_replacement('emt',2)]
genHiggsChannels2 = [''.join(x) for x in combinations_with_replacement('emt',1)]
for hpp in genHiggsChannels:
    for hmm in genHiggsChannels:
        genChannelsPP += [hpp+hmm]
    for hm in genHiggsChannels2:
        genChannelsAP += [hpp+hm]

hpp4l_pp_selections = {}
hpp4l_ap_selections = {}
sels = selectionParams['Hpp4l'].keys()
for sel in sels:
    for chan in genChannelsPP:
        directory = '{0}/gen_{1}'.format(selectionParams['Hpp4l'][sel]['kwargs']['directory'],chan)
        name = '{0}_gen_{1}'.format(sel,chan)
        hpp4l_pp_selections[name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = hpp4l_pp_selections[name]['args']
        hpp4l_pp_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp4l_pp_selections[name]['kwargs']['directory'] = directory
        hpp4l_pp_selections[name]['kwargs']['countOnly'] = True
    for chan in genChannelsAP:
        directory = '{0}/gen_{1}'.format(selectionParams['Hpp4l'][sel]['kwargs']['directory'],chan)
        name = '{0}_gen_{1}'.format(sel,chan)
        hpp4l_ap_selections[name] = deepcopy(selectionParams['Hpp4l'][sel])
        args = hpp4l_ap_selections[name]['args']
        hpp4l_ap_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp4l_ap_selections[name]['kwargs']['directory'] = directory
        hpp4l_ap_selections[name]['kwargs']['countOnly'] = True
sampleSelectionParams['Hpp4l'] = {}
for mass in masses:
    sampleName = 'HPlusPlusHMinusMinusHTo4L_M-{0}_13TeV-pythia8'.format(mass)
    sampleSelectionParams['Hpp4l'][sampleName] = deepcopy(hpp4l_pp_selections)

#############
### hpp3l ###
#############
hpp3lBaseCut = 'hpp1_passMedium==1 && hpp2_passMedium==1 && hm1_passMedium==1'
hpp3lLowMassControl = '{0} && hpp_mass<170 && hm_mass<170'.format(hpp3lBaseCut)
hpp3lScaleFactor = 'hpp1_mediumScale*hpp2_mediumScale*hm1_mediumScale*genWeight*pileupWeight*triggerEfficiency'
selectionParams['Hpp3l'] = {
    'default' : {'args': [hpp3lBaseCut],        'kwargs': {'mcscalefactor': hpp3lScaleFactor, 'directory': 'default'}},
    'lowmass' : {'args': [hpp3lLowMassControl], 'kwargs': {'mcscalefactor': hpp3lScaleFactor, 'directory': 'lowmass'}},
}

# setup reco channel selections
channels = {}
higgsChannels = [''.join(x) for x in product('em',repeat=2)]
higgsChannels2 = [''.join(x) for x in product('em',repeat=1)]
for hpp in higgsChannels:
    for hm in higgsChannels2:
        chanString = ''.join(sorted(hpp))+''.join(sorted(hm))
        if chanString not in channels: channels[chanString] = []
        channels[chanString] += [hpp+hm]

for sel in ['default','lowmass']:
    for chan in channels:
        directory = '{0}/{1}'.format(sel,chan)
        name = '{0}_{1}'.format(sel,chan)
        selectionParams['Hpp3l'][name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = selectionParams['Hpp3l'][name]['args']
        selectionParams['Hpp3l'][name]['args'][0] = args[0] + ' && ' + '(' + ' || '.join(['channel=="{0}"'.format(c) for c in channels[chan]]) + ')'
        selectionParams['Hpp3l'][name]['kwargs']['directory'] = directory

# setup gen channel selections
genChannelsPP = []
genChannelsAP = []
genHiggsChannels = [''.join(x) for x in combinations_with_replacement('emt',2)]
genHiggsChannels2 = [''.join(x) for x in combinations_with_replacement('emt',1)]
for hpp in genHiggsChannels:
    for hmm in genHiggsChannels:
        genChannelsPP += [hpp+hmm]
    for hm in genHiggsChannels2:
        genChannelsAP += [hpp+hm]

hpp3l_pp_selections = {}
hpp3l_ap_selections = {}
sels = selectionParams['Hpp3l'].keys()
for sel in sels:
    for chan in genChannelsPP:
        directory = '{0}/gen_{1}'.format(selectionParams['Hpp3l'][sel]['kwargs']['directory'],chan)
        name = '{0}_gen_{1}'.format(sel,chan)
        hpp3l_pp_selections[name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = hpp3l_pp_selections[name]['args']
        hpp3l_pp_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp3l_pp_selections[name]['kwargs']['directory'] = directory
        hpp3l_pp_selections[name]['kwargs']['countOnly'] = True
    for chan in genChannelsAP:
        directory = '{0}/gen_{1}'.format(selectionParams['Hpp3l'][sel]['kwargs']['directory'],chan)
        name = '{0}_gen_{1}'.format(sel,chan)
        hpp3l_ap_selections[name] = deepcopy(selectionParams['Hpp3l'][sel])
        args = hpp3l_ap_selections[name]['args']
        hpp3l_ap_selections[name]['args'][0] = args[0] + ' && ' + 'genChannel=="{0}"'.format(chan)
        hpp3l_ap_selections[name]['kwargs']['directory'] = directory
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
    if analysis in params: histParams.update(params2D[analysis])
    return histParams

def getHistSelections(analysis,sample):
    params = {}
    if analysis in selectionParams:
        params.update(selectionParams[analysis])
    if analysis in sampleSelectionParams:
        if sample in sampleSelectionParams[analysis]:
            params.update(sampleSelectionParams[analysis][sample])
    return params
