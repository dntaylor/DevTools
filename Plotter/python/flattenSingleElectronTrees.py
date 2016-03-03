import os
import sys
import glob
import logging

from DevTools.Plotter.FlattenTree import FlattenTree

logger = logging.getLogger("SingleElectronFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

myCut = 'l1_genMatch==1'
sourceDirectory = '/hdfs/store/user/dntaylor/2016-03-02_SingleElectronAnalysis_v1/'

eFlatten = FlattenTree(
    ntupleDirectory=sourceDirectory,
    treeName='ETree',
)

histParams = {
    'pt_v_dz' : {'xVariable': 'l1_pt', 'yVariable': 'fabs(l1_dz)',  'xBinning': [50,0,500], 'yBinning': [50,0,0.5]},
    'pt_v_dxy': {'xVariable': 'l1_pt', 'yVariable': 'fabs(l1_dxy)', 'xBinning': [50,0,500], 'yBinning': [50,0,0.3]},
}

for histName, params in histParams.iteritems():
    eFlatten.add2DHistogram(histName,**params)

for sDir in glob.glob('{0}/*'.format(sourceDirectory)):
    sample = sDir.split('/')[-1]
    eFlatten.flatten2D(sample,'flat/SingleElectron/{0}.root'.format(sample),myCut)
