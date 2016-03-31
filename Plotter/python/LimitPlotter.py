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

class LimitPlotter(PlotterBase):
    '''Basic limit plotter utilities'''

    def __init__(self,**kwargs):
        '''Initialize the plotter'''
        super(LimitPlotter, self).__init__(**kwargs)
        # initialize stuff

    def _readLimit(self,filename):
        '''Read limits from file, must be one line of the form:
               "exp0.025 exp0.16 exp0.5 exp0.84 exp0.975 obs"'''
        with open(filename) as f:
           content = f.readlines()
        limitString = content[0].rstrip()
        limvals = [float(x) for x in limitString.split()]
        if len(limvals)!=6:
            logging.warning('No limit found in {0}'.format(filename))
            limvals = [0.]*6
        return limvals

    def _readLimits(self,xvals,filenames):
        limits = {}
        if len(xvals)!=len(filenames):
            logging.error('Mismatch betwen length of xvals ({0}) and length of filenames ({1}).'.format(len(xvals),len(filenames)))
            return limits
        for x,filename in zip(xvals,filenames):
            limits[x] = self._readLimit(filename)
        return limits

    def plotLimit(self,xvals,filenames,savename,**kwargs):
        '''Plot limits'''
        xaxis = kwargs.pop('xaxis','#Phi^{++} Mass (GeV)')
        yaxis = kwargs.pop('yaxis','95% CLs Upper Limit on #sigma/#sigma_{model}')
        blind = kwargs.pop('blind',True)
        lumipos = kwargs.pop('lumipos',11)
        isprelim = kwargs.pop('isprelim',True)
        legendpos = kwargs.pop('legendpos',31)
        numcol = kwargs.pop('numcol',1)

        logging.info('Plotting {0}'.format(savename))

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(1)

        limits = self._readLimits(xvals,filenames)
        if not limits: return

        n = len(xvals)
        twoSigma = ROOT.TGraph(2*n)
        oneSigma = ROOT.TGraph(2*n)
        expected = ROOT.TGraph(n)
        observed = ROOT.TGraph(n)

        for i in range(len(xvals)):
            twoSigma.SetPoint(i,   xvals[i],     limits[xvals[i]][0]) # 0.025
            oneSigma.SetPoint(i,   xvals[i],     limits[xvals[i]][1]) # 0.16
            expected.SetPoint(i,   xvals[i],     limits[xvals[i]][2]) # 0.5
            oneSigma.SetPoint(n+i, xvals[n-i-1], limits[xvals[n-i-1]][3]) # 0.84
            twoSigma.SetPoint(n+i, xvals[n-i-1], limits[xvals[n-i-1]][4]) # 0.975
            observed.SetPoint(i,   xvals[i],     limits[xvals[i]][5]) # obs

        twoSigma.SetFillColor(ROOT.kYellow)
        twoSigma.SetLineColor(ROOT.kYellow)
        twoSigma.SetMarkerStyle(0)
        oneSigma.SetFillColor(ROOT.kSpring)
        oneSigma.SetLineColor(ROOT.kSpring)
        oneSigma.SetMarkerStyle(0)
        expected.SetLineStyle(7)
        expected.SetMarkerStyle(0)
        expected.SetFillStyle(0)
        observed.SetMarkerStyle(0)
        observed.SetFillStyle(0)

        expected.GetXaxis().SetLimits(xvals[0],xvals[-1])
        expected.GetXaxis().SetTitle(xaxis)
        expected.GetYaxis().SetTitle(yaxis)

        expected.Draw()
        twoSigma.Draw('f')
        oneSigma.Draw('f')
        expected.Draw('same')
        ROOT.gPad.RedrawAxis()
        if not blind: observed.Draw('same')

        ratiounity = ROOT.TLine(expected.GetXaxis().GetXmin(),1,expected.GetXaxis().GetXmax(),1)
        ratiounity.Draw()

        # get the legend
        entries = [
            [expected,'Expected','l'],
            [twoSigma,'Expected 2#sigma','F'],
            [oneSigma,'Expected 1#sigma','F'],
        ]
        if not blind: entries = [[observed,'Observed','l']] + entries
        legend = self._getLegend(entries=entries,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        self._setStyle(canvas,position=lumipos,preliminary=isprelim)

        self._save(canvas,savename)
