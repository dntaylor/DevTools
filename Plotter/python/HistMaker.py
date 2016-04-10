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

class HistMaker(PlotterBase):
    '''Basic histogram making utilities'''

    def __init__(self,**kwargs):
        '''Initialize the plotter'''
        super(HistMaker, self).__init__(**kwargs)
        # initialize stuff
        self.outputFileName = kwargs.pop('outputFileName','root/file.root')

    def _write(self,hist,directory=''):
        basedir = os.path.dirname(self.outputFileName)
        python_mkdir(basedir)
        outfile = ROOT.TFile(self.outputFileName,'update')
        if not outfile.GetDirectory(directory): outfile.mkdir(directory)
        outfile.cd('{0}:/{1}'.format(self.outputFileName,directory))
        hist.Write('',ROOT.TObject.kOverwrite)
        outfile.Close()


    def make2D(self,savename,values,errors,xBinning,yBinning,**kwargs):
        '''
        Make a 2D histogram with values/errors
        values/errors must be of the form:
            {
                (x,y): val/err
            }
        '''
        savedir = kwargs.pop('savedir','')
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Variable')
        # the histogram
        hist = ROOT.TH2F(savename,savename,len(xBinning)-1,array('d',xBinning),len(yBinning)-1,array('d',yBinning))
        for pos,val in values.iteritems():
            hist.SetBinContent(hist.FindBin(*pos),val)
        for pos,err in errors.iteritems():
            hist.SetBinError(hist.FindBin(*pos),err)
        hist.GetXaxis().SetTitle(xaxis)
        hist.GetYaxis().SetTitle(yaxis)
        self._write(hist,directory=savedir)
