import os
import sys
import glob
import logging
from multiprocessing import Pool


from DevTools.Utilities.MultiProgress import MultiProgress
from DevTools.Plotter.FlattenTree import FlattenTree

try:
    from progressbar import ProgressBar, ETA, Percentage, Bar, SimpleProgress
    hasProgress = True
except:
    hasProgress = False

logger = logging.getLogger("ElectronFlatten")
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

sourceDirectory = '/hdfs/store/user/dntaylor/2016-03-10_ElectronAnalysis_v1/'


histParams = {
    'pt'               : {'variable': 'e_pt',            'binning': [200,0,1000]},
    'eta'              : {'variable': 'e_eta',           'binning': [60,-3.,3.]},
    'dz'               : {'variable': 'e_dz',            'binning': [50,0,0.5]},
    'dxy'              : {'variable': 'e_dxy',           'binning': [50,0,0.3]},
    'mvaTrig'          : {'variable': 'e_mvaTrigValues', 'binning': [100,-1.,1.]},
}
histParams2D = {
    'pt_v_dz' : {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dz)',  'xBinning': [50,0,500], 'yBinning': [50,0,0.5]},
    'pt_v_dxy': {'xVariable': 'e_pt', 'yVariable': 'fabs(e_dxy)', 'xBinning': [50,0,500], 'yBinning': [50,0,0.3]},
}


def flatten(directory,**kwargs):
    sample = directory.split('/')[-1]
    if hasProgress:
        pbar = kwargs.pop('progressbar',ProgressBar(widgets=['{0}: '.format(sample),' ',SimpleProgress(),' histograms ',Percentage(),' ',Bar(),' ',ETA()]))
    else:
        pbar = None
    eFlatten = FlattenTree(
        ntupleDirectory=sourceDirectory,
        treeName='ETree',
    )
    eFlatten.initializeSample(sample,'flat/Electron/{0}.root'.format(sample))

    for histName, params in histParams.iteritems():
        eFlatten.addHistogram(histName,**params)
    
    promptCut = 'e_genMatch==1 && e_genIsPrompt==1'
    fakeCut = '(e_genMatch==0 || (e_genMatch==1 && e_genIsFromHadron))'
    barrelCut = 'fabs(e_eta)<1.479'
    endcapCut = 'fabs(e_eta)>1.479'
    lowpt = 'e_pt<50'
    highpt = 'e_pt>100'

    eFlatten.addSelection(promptCut)
    eFlatten.addSelection(fakeCut,postfix='fake')
    eFlatten.addSelection(' && '.join([promptCut,barrelCut]),postfix='barrel')
    eFlatten.addSelection(' && '.join([fakeCut,barrelCut]),postfix='barrel_fake')
    eFlatten.addSelection(' && '.join([promptCut,endcapCut]),postfix='endcap')
    eFlatten.addSelection(' && '.join([fakeCut,endcapCut]),postfix='endcap_fake')
    eFlatten.addSelection(' && '.join([promptCut,lowpt]),postfix='lowpt')
    eFlatten.addSelection(' && '.join([fakeCut,lowpt]),postfix='lowpt_fake')
    eFlatten.addSelection(' && '.join([promptCut,highpt]),postfix='highpt')
    eFlatten.addSelection(' && '.join([fakeCut,highpt]),postfix='highpt_fake')

    eFlatten.flattenAll(progressbar=pbar)

multi = MultiProgress(16)

for directory in glob.glob('{0}/*'.format(sourceDirectory)):
    sample = directory.split('/')[-1]
    multi.addJob(sample,flatten,args=(directory,))
    #flatten(directory)
multi.retrieve()

