import logging
import os
import sys
import glob

import ROOT

from DevTools.Plotter.FlattenTree import FlattenTree

class WZFlatten(FlattenTree):
    '''Produces flat histograms'''

    def __init__(self,**kwargs):
        ntupleDirectory = kwargs.pop('ntupleDirectory','ntuples/WZ')
        treeName = kwargs.pop('treeName','WZTree')
        super(WZFlatten,self).__init__(treeName=treeName,ntupleDirectory=ntupleDirectory)
        # add variables
        self.histParameters = {
            'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
            'zLeadingLeptonPt'    : {'variable': 'z1_pt',   'binning': [50, 0, 500]},
            'zSubLeadingLeptonPt' : {'variable': 'z2_pt',   'binning': [50, 0, 500]},
            'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
            'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
            'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
        }

