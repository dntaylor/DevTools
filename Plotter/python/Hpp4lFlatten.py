import logging
import os
import sys
import glob

import ROOT

from DevTools.Plotter.FlattenTree import FlattenTree

class Hpp4lFlatten(FlattenTree):
    '''Produces flat histograms'''

    def __init__(self,**kwargs):
        ntupleDirectory = kwargs.pop('ntupleDirectory','ntuples/Hpp4l')
        treeName = kwargs.pop('treeName','Hpp4lTree')
        super(Hpp4lFlatten,self).__init__(treeName=treeName,ntupleDirectory=ntupleDirectory)
        # add variables
        self.histParameters = {
            'hppMass'             : {'variable': 'hpp_mass','binning': [100, 0, 1000]},
            'hmmMass'             : {'variable': 'hmm_mass','binning': [100, 0, 1000]},
            'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
            'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
            'mass'                : {'variable': '4l_mass', 'binning': [50, 0, 500]},
        }

