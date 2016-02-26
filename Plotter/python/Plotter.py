import os
import sys
import logging

import ROOT

from DevTools.Plotter.utilities import python_mkdir, getLumi
from DevTools.Plotter.style import getStyle
import DevTools.Plotter.CMS_lumi as CMS_lumi
import DevTools.Plotter.tdrstyle as tdrstyle

ROOT.gROOT.SetBatch(ROOT.kTRUE)
tdrstyle.setTDRStyle()

class Plotter(object):
    '''Basic plotter utilities'''

    def __init__(self,**kwargs):
        '''Initialize the plotter'''
        # histogram directory
        self.inputDirectory = kwargs.pop('inputDirectory','flat/WZ')

        # plot directory
        self.outputDirectory = kwargs.pop('outputDirectory','plots/WZ')

        # file to hold all plots
        saveFileName = kwargs.pop('saveFileName','plots.root')
        fullSaveFileName = '{0}/{1}'.format(self.outputDirectory,saveFileName)
        python_mkdir(os.path.dirname(fullSaveFileName))
        self.saveFile = ROOT.TFile(fullSaveFileName,"recreate")

        # empty initialization
        self.histDict = {}
        self.stackOrder = []
        self.histOrder = []
        self.sampleFiles = {}

    def __exit__(self, type, value, traceback):
        self.finish()

    def __del__(self):
        self.finish()

    def finish(self):
        '''Cleanup stuff'''
        logging.info('Finished plotting')
        self.saveFile.Close()

    def __openFile(self,sampleName):
        '''Verify and open a sample'''
        fname = '{0}/{1}.root'.format(self.inputDirectory,sampleName)
        if os.path.isfile(fname):
            if sampleName not in self.sampleFiles:
                self.sampleFiles[sampleName] = ROOT.TFile.Open(fname)
            else:
                logging.error('Sample {0} already added to plot.'.format(sampleName))
        else:
            logging.error('{0} does not exist.'.format(fname))

    def addHistogramToStack(self,histName,histConstituents):
        '''
        Add a histogram to the stack. histConstituents is a list.
        '''
        for sampleName in histConstituents:
            self.__openFile(sampleName)
        self.histDict[histName] = histConstituents
        self.stackOrder += [histName]

    def addHistogram(self,histName,histConstituents):
        '''
        Add histogram to plot. histConstituents is a list.
        '''
        for sampleName in histConstituents:
            self.__openFile(sampleName)
        self.histDict[histName] = histConstituents
        self.histOrder += [histName]

    def __readSampleVariable(self,sampleName,variable):
        '''Read the histogram from file'''
        if self.sampleFiles[sampleName].GetListOfKeys().Contains(variable):
            hist = self.sampleFiles[sampleName].Get(variable)
            return hist
        else:
            logging.error('Variable {0} does not exist for {1}'.format(variable,sampleName))
            return 0

    def __getHistogram(self,histName,variable):
        '''Get a styled histogram'''
        if histName in self.histDict:
            hists = ROOT.TList()
            for sampleName in self.histDict[histName]:
                hist = self.__readSampleVariable(sampleName,variable)
                if hist: hists.Add(hist)
            if hists.IsEmpty(): return 0
            hist = hists[0].Clone('{0}_{1}'.format(histName,variable))
            hist.Reset()
            hist.Merge(hists)
            style = getStyle(histName)
            hist.SetTitle(style['name'])
            if 'fillstyle' in style: hist.SetFillStyle(style['fillstyle'])
            if 'linecolor' in style: hist.SetLineColor(style['linecolor'])
            if 'fillcolor' in style: hist.SetFillColor(style['fillcolor'])
            return hist
        else:
            logging.error('{0} not defined.'.format(histName))
            return 0

    def __getStack(self,variable):
        '''Get a stack of histograms'''
        stack = ROOT.THStack('stack_{0}'.format(variable),'stack_{0}'.format(variable))
        for histName in self.stackOrder:
            hist = self.__getHistogram(histName,variable)
            if hist: stack.Add(hist)
        return stack

    def __getLegend(self,**kwargs):
        '''Get the legend'''
        stack = kwargs.pop('stack',ROOT.THStack())
        hists = kwargs.pop('hists',[])
        # TODO, programatically decide
        xstart = 0.76
        ystart = 0.6
        xend = 0.92
        yend = 0.90
        legend = ROOT.TLegend(xstart,ystart,xend,yend,'','NDC')
        legend.SetTextFont(42)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        if stack:
            for hist,name in zip(reversed(stack.GetHists()),reversed(self.stackOrder)):
                style = getStyle(name)
                legend.AddEntry(hist,style['name'],style['legendstyle'])
        if hists:
            for hist,name in zip(hists,self.histOrder):
                style = getStyle(name)
                legend.AddEntry(hist,style['name'],style['legendstyle'])
        return legend

    def __setStyle(self,pad,preliminary=True):
        '''Set style for plots based on the CMS TDR style guidelines.
           https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines#Figures_and_tables
           https://ghm.web.cern.ch/ghm/plots/'''
        # set period (used in CMS_lumi)
        # period : sqrts
        # 1 : 7, 2 : 8, 3 : 7+8, 4 : 13, ... 7 : 7+8+13
        period_int = 4
        # set position
        # 11: upper left, 33 upper right
        position = 11
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
        self.saveFile.WriteTObject(canvas)

    def plot(self,variable,savename,**kwargs):
        '''Plot a variable and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

        # TODO: add ratio
        stack = ROOT.THStack()
        if self.stackOrder:
            stack = self.__getStack(variable)
            stack.Draw("hist")
            stack.GetXaxis().SetTitle(xaxis)
            stack.GetYaxis().SetTitle(yaxis)

        hists = []
        for histName in self.histOrder:
            # TODO: poisson errors for data
            hist = self.__getHistogram(histName,variable)
            style = getStyle(histName)
            hist.Draw(style['drawstyle']+' same')
            hists += [hist]

        legend = self.__getLegend(stack=stack,hists=hists)
        legend.Draw()

        self.__setStyle(canvas)

        self.__save(canvas,savename)