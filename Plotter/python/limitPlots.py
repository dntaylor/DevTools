import os
import sys
import logging
from itertools import product, combinations_with_replacement

from DevTools.Plotter.LimitPlotter import LimitPlotter
from copy import deepcopy
import ROOT

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

blind = True

limitPlotter = LimitPlotter('Limits')

masses = [200,300,400,500,600,700,800,900,1000]
modes = ['ee100','em100','et100','mm100','mt100','tt100','BP1','BP2','BP3','BP4']

for mode in modes:
    filenames = ['asymptotic/Hpp4l/{0}/{1}/limits.txt'.format(mode,mass) for mass in masses]
    kwargs = {
        'xaxis': '#Phi^{++} Mass (GeV)',
        'yaxis': '95% CLs Upper Limit on #sigma/#sigma_{model}',
    }
    limitPlotter.plotLimit(masses,filenames,'Hpp4l/{0}'.format(mode),**kwargs)


