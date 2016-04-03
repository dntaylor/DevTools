import os
import sys
import logging

import ROOT

import operator


class TriggerPrescales(object):
    '''Class to access the trigger prescales for a given trigger.'''

    def __init__(self):
        self.prescales = {}
        self.prescales['2015D'] = {
            # HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v*
            'Ele17_Ele12Leg2': 2263.552/4.174,
            # HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v*
            'Ele17_Ele12Leg1': 2263.552/45.941,
            # HLT_Mu8_TrkIsoVVL_v*
            'Mu17_Mu8Leg2': 2263.552/1.330,
            # HLT_Mu17_TrkIsoVVL_v*
            'Mu17_Mu8Leg1': 2263.552/197.362,
        }

    def getPrescale(self,trigger):
        if trigger in self.prescales['2015D']:
            return self.prescales['2015D'][trigger]
        else:
            return 1.
