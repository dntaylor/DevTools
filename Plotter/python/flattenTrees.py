import glob

from DevTools.Plotter.FlattenTree import FlattenTree

myCut = "z1_passMedium==1 && z2_passMedium==1 && w1_passTight==1 && z1_pt>20 && z2_pt>10 && w1_pt>20 && met_pt>30 && numBjetsTight30==0 && fabs(z_mass-91.1876)<15 && 3l_mass>100"

flattenTree = FlattenTree()
for sDir in glob.glob('ntuples/WZ/*'):
    sample = sDir.split('/')[-1]
    flattenTree.flatten(sample,'flat/WZ/{0}.root'.format(sample),myCut)
