import os
import sys
import glob
import logging

from DevTools.Plotter.Hpp4lFlatten import Hpp4lFlatten

logger = logging.getLogger("Hpp4lFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

myCut = "hpp1_passTight==1 && hpp2_passTight==1 && hmm1_passTight==1 && hmm2_passTight==1"

sourceDirectory = '/hdfs/store/user/dntaylor/2016-02-28_Hpp4lAnalysis_v1/'

hpp4lFlatten = Hpp4lFlatten(ntupleDirectory=sourceDirectory)
for sDir in glob.glob('{0}/*'.format(sourceDirectory)):
    sample = sDir.split('/')[-1]
    hpp4lFlatten.flatten(sample,'flat/Hpp4l/{0}.root'.format(sample),myCut)
