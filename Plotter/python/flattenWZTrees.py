import os
import sys
import glob
import logging

from DevTools.Plotter.WZFlatten import WZFlatten

logger = logging.getLogger("WZFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

myCut = "z1_passMedium==1 && z2_passMedium==1 && w1_passTight==1 && z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100"

sourceDirectory = '/hdfs/store/user/dntaylor/2016-02-28_WZAnalysis_v1/'

wzFlatten = WZFlatten(ntupleDirectory=sourceDirectory)
for sDir in glob.glob('{0}/*'.format(sourceDirectory)):
    sample = sDir.split('/')[-1]
    wzFlatten.flatten(sample,'flat/WZ/{0}.root'.format(sample),myCut)
