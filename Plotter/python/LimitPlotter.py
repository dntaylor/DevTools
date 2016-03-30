import os
import sys
import logging
import math
from array import array
from collections import OrderedDict

import ROOT

from DevTools.Plotter.utilities import python_mkdir, getLumi
from DevTools.Plotter.style import getStyle
import DevTools.Plotter.CMS_lumi as CMS_lumi
import DevTools.Plotter.tdrstyle as tdrstyle

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPalette(1)

class LimitPlotter(object):
    '''Basic limit plotter utilities'''

    def __init__(self,**kwargs):
        '''Initialize the plotter'''
        # plot directory
        self.outputDirectory = kwargs.pop('outputDirectory','plots/Hpp4l')
        # initialize stuff

    def __readLimit(self,filename):
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

    def __readLimits(self,xvals,filenames):
        limits = {}
        if len(xvals)!=len(filenames):
            logging.error('Mismatch betwen length of xvals ({0}) and length of filenames ({1}).'.format(len(xvals),len(filenames)))
            return limits
        for x,filename in zip(xvals,filenames):
            limits[x] = self.__readLimit(filename)
        return limits

    def __getLegend(self,**kwargs):
        '''Get the legend'''
        entryArgs = kwargs.pop('entries',[])
        position = kwargs.pop('position',33)
        numcol = kwargs.pop('numcol',1)
        # programatically decide position
        # ----------------
        # | 14 | 24 | 34 |
        # ----------------
        # | 13 | 23 | 33 |
        # ----------------
        # | 12 | 22 | 32 |
        # ----------------
        # | 11 | 21 | 31 |
        # ----------------
        width = 0.15*numcol+0.1
        numentries = len(entryArgs)
        height = math.ceil(float(numentries)/numcol)*0.06+0.02
        if position % 10 == 1:   # bottom
            ystart = 0.16
            yend = ystart+height
        elif position % 10 == 2: # middle
            yend = 0.54+height/2
            ystart = 0.54-height/2
        elif position % 10 == 3: # top
            yend = 0.84
            ystart = yend-height
        else:                    # verytop
            yend = 0.92
            ystart = yend-height
        if position / 10 == 1:   # left
            xstart = 0.19
            xend = xstart+width
        elif position / 10 == 2: # middle
            xstart = 0.57-width/2
            xend = 0.57+width/2
        else:                    # right
            xend = 0.95
            xstart = xend-width
        legend = ROOT.TLegend(xstart,ystart,xend,yend,'','NDC')
        if numcol>1: legend.SetNColumns(int(numcol))
        legend.SetTextFont(42)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        for entryArg in entryArgs:
            legend.AddEntry(*entryArg)
        return legend

    def __setStyle(self,pad,position=11,preliminary=True):
        '''Set style for plots based on the CMS TDR style guidelines.
           https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines#Figures_and_tables
           https://ghm.web.cern.ch/ghm/plots/'''
        # set period (used in CMS_lumi)
        # period : sqrts
        # 1 : 7, 2 : 8, 3 : 7+8, 4 : 13, ... 7 : 7+8+13
        period_int = 4
        # set position
        # 11: upper left, 33 upper right
        CMS_lumi.wrtieExtraText = preliminary
        CMS_lumi.extraText = "Preliminary"
        CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (float(getLumi())/1000.)
        if getLumi < 1000:
            CMS_lumi.lumi_13TeV = "%0.1f pb^{-1}" % (float(getLumi))
        CMS_lumi.CMS_lumi(pad,period_int,position)

    def __save(self, canvas, savename):
        '''Save the canvas in multiple formats.'''
        canvas.SetName(savename)
        for type in ['pdf','root','png']:
            name = '{0}/{1}/{2}.{1}'.format(self.outputDirectory, type, savename)
            python_mkdir(os.path.dirname(name))
            canvas.Print(name)

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

        limits = self.__readLimits(xvals,filenames)
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
        legend = self.__getLegend(entries=entries,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        self.__setStyle(canvas,position=lumipos,preliminary=isprelim)

        self.__save(canvas,savename)
