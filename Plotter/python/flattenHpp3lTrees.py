import os
import sys
import glob
import logging

from DevTools.Plotter.FlattenTree import FlattenTree

logger = logging.getLogger("Hpp3lFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

myCut = "hpp1_passTight==1 && hpp2_passTight==1 && hm1_passTight==1"

sourceDirectory = '/hdfs/store/user/dntaylor/2016-02-28_Hpp3lAnalysis_v1/'

hpp3lFlatten = FlattenTree(
    ntupleDirectory=sourceDirectory,
    treeName='Hpp3lTree',
)
for sDir in glob.glob('{0}/*'.format(sourceDirectory)):
    sample = sDir.split('/')[-1]
    hpp3lFlatten.flatten(sample,'flat/Hpp3l/{0}.root'.format(sample),myCut)
