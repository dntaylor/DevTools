import logging
import os
import sys
import glob

import ROOT

from DevTools.Plotter.FlattenTree import FlattenTree

class Hpp3lFlatten(FlattenTree):
    '''Produces flat histograms'''

    def __init__(self,**kwargs):
        ntupleDirectory = kwargs.pop('ntupleDirectory','ntuples/Hpp3l')
        treeName = kwargs.pop('treeName','Hpp3lTree')
        super(Hpp3lFlatten,self).__init__(treeName=treeName,ntupleDirectory=ntupleDirectory)
        # add variables
        self.histParameters = {
            'hppMass'             : {'variable': 'hpp_mass','binning': [100, 0, 1000]},
            'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
            'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
            'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
            'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
        }

