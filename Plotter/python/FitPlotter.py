import os
import sys
import logging
import math
from array import array
from collections import OrderedDict

import ROOT

from DevTools.Plotter.PlotterBase import PlotterBase
from DevTools.Plotter.utilities import python_mkdir, getLumi
from DevTools.Plotter.style import getStyle
import DevTools.Plotter.CMS_lumi as CMS_lumi
import DevTools.Plotter.tdrstyle as tdrstyle

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPalette(1)

class FitPlotter(PlotterBase):
    '''Basic fit plotter utilities'''

    def __init__(self,**kwargs):
        '''Initialize the plotter'''
        super(LimitPlotter, self).__init__(**kwargs)
        # initialize stuff

    def plotFit(self,xvals,yvals,savename,**kwargs):
        '''Plot fit'''
        xaxis = kwargs.pop('xaxis','')
        yaxis = kwargs.pop('yaxis','Events')
        lumipos = kwargs.pop('lumipos',11)
        isprelim = kwargs.pop('isprelim',True)
        legendpos = kwargs.pop('legendpos',31)
        numcol = kwargs.pop('numcol',1)

        logging.info('Plotting {0}'.format(savename))

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

        # get legend
        entries = []
        legend = self._getLegend(entries=entries,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        self._setStyle(canvas,position=lumipos,preliminary=isprelim)

        self._save(canvas,savename)
