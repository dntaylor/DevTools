import os
import sys
import glob
import logging
from multiprocessing import Pool

from DevTools.Plotter.FlattenTree import FlattenTree
from DevTools.Plotter.utilities import isData

logger = logging.getLogger("WZFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

baseCut = "z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100"

sourceDirectory = '/hdfs/store/user/dntaylor/2016-03-07_WZAnalysis_v1/'

tightVar = {
    0: 'z1_passMedium',
    1: 'z2_passMedium',
    2: 'w1_passTight',
}

tightScale = {
    0: 'z1_mediumScale',
    1: 'z2_mediumScale',
    2: 'w1_tightScale',
}

looseScale = {
    0: 'z1_looseScale',
    1: 'z2_looseScale',
    2: 'w1_looseScale',
}

scaleMap = {
    'P': tightScale,
    'F': looseScale,
}

histParameters = {
    'zMass'               : {'variable': 'z_mass',  'binning': [60, 60, 120]},
    'zLeadingLeptonPt'    : {'variable': 'z1_pt',   'binning': [50, 0, 500]},
    'zSubLeadingLeptonPt' : {'variable': 'z2_pt',   'binning': [50, 0, 500]},
    'wLeptonPt'           : {'variable': 'w1_pt',   'binning': [50, 0, 500]},
    'met'                 : {'variable': 'met_pt',  'binning': [50, 0, 500]},
    'mass'                : {'variable': '3l_mass', 'binning': [50, 0, 500]},
}

def flatten(directory):
    wzFlatten = FlattenTree(
        ntupleDirectory = sourceDirectory,
        treeName = 'WZTree',
    )
    for histName, params in histParameters.iteritems():
        wzFlatten.addHistogram(histName,**params)
    
    sample = directory.split('/')[-1]

    nl = 3
    for region in ['PPP','PPF','PFP','FPP','PFF','FPF','FFP','FFF']:
        scalefactor = '*'.join([scaleMap[region[x]][x] for x in range(3)]+['genWeight'])
        if isData(sample): scalefactor = '1'

        cut = ' && '.join(['{0}=={1}'.format(tightVar[x],1 if region[x]=='P' else 0) for x in range(3)]+[baseCut])

        postfix = '' if region=='PPP' else region
        wzFlatten.flatten(sample,'flat/WZ/{0}.root'.format(sample),cut,scalefactor=scalefactor,postfix=postfix)

pool = Pool(16)

try:
    pool.map_async(flatten,glob.glob('{0}/*'.format(sourceDirectory))).get(99999999)
    logging.info('Finished flattening WZ.')
except:
    pool.terminate()
    logging.info('Cancelled WZ flatten.')
    sys.exit(1)


