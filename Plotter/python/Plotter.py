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
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPalette(1)

# set a custom style, copied from 6.04, just directly when CMSSW has 6.04
stops = array('d', [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000])
# rust
red   = array('d', [  0./255., 30./255., 63./255., 101./255., 143./255., 152./255., 169./255., 187./255., 230./255.])
green = array('d', [  0./255., 14./255., 28./255.,  42./255.,  58./255.,  61./255.,  67./255.,  74./255.,  91./255.])
blue  = array('d', [ 39./255., 26./255., 21./255.,  18./255.,  15./255.,  14./255.,  14./255.,  13./255.,  13./255.])
# solar
#red   = array('d', [ 99./255., 116./255., 154./255., 174./255., 200./255., 196./255., 201./255., 201./255., 230./255.])
#green = array('d', [  0./255.,   0./255.,   8./255.,  32./255.,  58./255.,  83./255., 119./255., 136./255., 173./255.])
#blue  = array('d', [  5./255.,   6./255.,   7./255.,   9./255.,   9./255.,  14./255.,  17./255.,  19./255.,  24./255.])
Idx = ROOT.TColor.CreateGradientColorTable(9, stops, red, green, blue, 255);
ROOT.gStyle.SetNumberContours(255)


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
        self.styles = {}
        self.signals = []

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
                logging.warning('Sample {0} already added to plot.'.format(sampleName))
        else:
            logging.error('{0} does not exist.'.format(fname))

    def addHistogramToStack(self,histName,histConstituents,style={}):
        '''
        Add a histogram to the stack. histConstituents is a list.
        '''
        for sampleName in histConstituents:
            self.__openFile(sampleName)
        self.histDict[histName] = histConstituents
        self.stackOrder += [histName]
        self.styles[histName] = getStyle(histName)
        self.styles[histName].update(style)

    def addHistogram(self,histName,histConstituents,style={},signal=False):
        '''
        Add histogram to plot. histConstituents is a list.
        Style is a custom styling.
        '''
        for sampleName in histConstituents:
            self.__openFile(sampleName)
        self.histDict[histName] = histConstituents
        self.histOrder += [histName]
        self.styles[histName] = getStyle(histName)
        self.styles[histName].update(style)
        if signal: self.signals += [histName]

    def clearHistograms(self):
        samples = self.sampleFiles.keys()
        for sampleName in samples:
            tfile = self.sampleFiles.pop(sampleName)
            tfile.Close()
        self.sampleFiles = {}
        self.histDict = {}
        self.histOrder = []
        self.stackOrder = []
        self.styles = {}
        self.signals = []

    def __readSampleVariable(self,sampleName,variable):
        '''Read the histogram from file'''
        if self.sampleFiles[sampleName].GetListOfKeys().Contains(variable):
            hist = self.sampleFiles[sampleName].Get(variable)
            #hist.Sumw2()
            return hist
        else:
            logging.error('Variable {0} does not exist for {1}'.format(variable,sampleName))
            return 0

    def __getHistogram(self,histName,variable,**kwargs):
        '''Get a styled histogram'''
        rebin = kwargs.pop('rebin',0)
        # check if it is a variable map
        varName = variable if isinstance(variable,basestring) else variable[histName]
        nofill = kwargs.pop('nofill',False)
        if histName in self.histDict:
            hists = ROOT.TList()
            for sampleName in self.histDict[histName]:
                hist = self.__readSampleVariable(sampleName,varName)
                if hist: hists.Add(hist)
            if hists.IsEmpty(): return 0
            hist = hists[0].Clone('{0}_{1}'.format(histName,varName))
            hist.Reset()
            hist.Merge(hists)
            if rebin: hist = hist.Rebin(rebin)
            style = self.styles[histName]
            hist.SetTitle(style['name'])
            if 'linecolor' in style:
                hist.SetLineColor(style['linecolor'])
                hist.SetMarkerColor(style['linecolor'])
            if not nofill:
                if 'fillstyle' in style: hist.SetFillStyle(style['fillstyle'])
                if 'fillcolor' in style: hist.SetFillColor(style['fillcolor'])
            return hist
        else:
            logging.error('{0} not defined.'.format(histName))
            return 0

    def __get2DHistogram(self,histName,variable,**kwargs):
        '''Get a styled histogram'''
        rebinx = kwargs.pop('rebinx',0)
        rebiny = kwargs.pop('rebiny',0)
        # check if it is a variable map
        varName = variable if isinstance(variable,basestring) else variable[histName]
        if histName in self.histDict:
            hists = ROOT.TList()
            for sampleName in self.histDict[histName]:
                hist = self.__readSampleVariable(sampleName,varName)
                if hist: hists.Add(hist)
            if hists.IsEmpty(): return 0
            hist = hists[0].Clone('{0}_{1}'.format(histName,varName))
            hist.Reset()
            hist.Merge(hists)
            if rebinx: hist = hist.RebinX(rebinx)
            if rebiny: hist = hist.RebinY(rebiny)
            style = self.styles[histName]
            hist.SetTitle(style['name'])
            return hist
        else:
            logging.error('{0} not defined.'.format(histName))
            return 0

    def __getStack(self,variable,**kwargs):
        '''Get a stack of histograms'''
        stack = ROOT.THStack('stack_{0}'.format(variable),'stack_{0}'.format(variable))
        for histName in self.stackOrder:
            hist = self.__getHistogram(histName,variable,**kwargs)
            if hist: stack.Add(hist)
        return stack

    def __get_ratio_stat_err(self, hist, **kwargs):
        '''Return a statistical error bars for a ratio plot'''
        ratiomin = kwargs.pop('ratiomin',0.5)
        ratiomax = kwargs.pop('ratiomax',1.5)
        ratiostaterr = hist.Clone("ratiostaterr")
        #ratiostaterr.Sumw2()
        ratiostaterr.SetStats(0)
        ratiostaterr.SetTitle("")
        ratiostaterr.GetYaxis().SetTitle("Data/MC")
        ratiostaterr.SetMaximum(ratiomax)
        ratiostaterr.SetMinimum(ratiomin)
        ratiostaterr.SetMarkerSize(0)
        ratiostaterr.SetFillColor(ROOT.kGray+3)
        ratiostaterr.SetFillStyle(3013)
        ratiostaterr.GetXaxis().SetLabelSize(0.19)
        ratiostaterr.GetXaxis().SetTitleSize(0.21)
        ratiostaterr.GetXaxis().SetTitleOffset(1.0)
        ratiostaterr.GetYaxis().SetLabelSize(0.19)
        ratiostaterr.GetYaxis().SetTitleSize(0.21)
        ratiostaterr.GetYaxis().SetTitleOffset(0.27)
        ratiostaterr.GetYaxis().SetNdivisions(503)

        # bin by bin errors
        for i in range(hist.GetNbinsX()+2):
            ratiostaterr.SetBinContent(i, 1.0)
            if hist.GetBinContent(i)>1e-6:  # not empty
                binerror = hist.GetBinError(i) / hist.GetBinContent(i)
                ratiostaterr.SetBinError(i, binerror)
            else:
                ratiostaterr.SetBinError(i, 999.)

        return ratiostaterr


    def __getLegend(self,**kwargs):
        '''Get the legend'''
        stack = kwargs.pop('stack',None)
        hists = kwargs.pop('hists',{})
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
        numentries = len(hists.keys())
        if stack: numentries += len(stack.GetHists())
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
        if stack:
            for hist,name in zip(reversed(stack.GetHists()),reversed(self.stackOrder)):
                style = self.styles[name]
                legend.AddEntry(hist,hist.GetTitle(),style['legendstyle'])
        if hists:
            for name,hist in hists.iteritems():
                style = self.styles[name]
                legend.AddEntry(hist,hist.GetTitle(),style['legendstyle'])
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
        self.saveFile.WriteTObject(canvas)

    def plot(self,variable,savename,**kwargs):
        '''Plot a variable and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymax',None)
        ymax = kwargs.pop('ymax',None)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        lumipos = kwargs.pop('lumipos',11)
        isprelim = kwargs.pop('preliminary',True)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        plotratio = kwargs.pop('plotratio',True)
        blinder = kwargs.pop('blinder',[])

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

        # ratio plot
        if plotratio:
            plotpad = ROOT.TPad("plotpad", "top pad", 0.0, 0.21, 1.0, 1.0)
            plotpad.SetBottomMargin(0.04)
            plotpad.Draw()
            plotpad.SetLogy(logy)
            plotpad.SetLogx(logx)
            ratiopad = ROOT.TPad("ratiopad", "bottom pad", 0.0, 0.0, 1.0, 0.21)
            ratiopad.SetTopMargin(0.06)
            ratiopad.SetBottomMargin(0.5)
            ratiopad.SetTickx(1)
            ratiopad.SetTicky(1)
            ratiopad.Draw()
            ratiopad.SetLogx(logx)
            if plotpad != ROOT.TVirtualPad.Pad(): plotpad.cd()
        else:
            canvas.SetLogy(logy)
            canvas.SetLogx(logx)


        highestMax = -9999999.

        # stack
        stack = ROOT.THStack()
        if self.stackOrder:
            stack = self.__getStack(variable,**kwargs)
            highestMax = max(highestMax,stack.GetMaximum())

        # overlay histograms
        hists = OrderedDict()
        for histName in self.histOrder:
            hist = self.__getHistogram(histName,variable,nofill=True,**kwargs)
            if histName=='data':
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(1.)
                hist.SetLineColor(ROOT.kBlack)
                if len(blinder)==2:
                    lowbin = hist.FindBin(blinder[0])
                    highbin = hist.FindBin(blinder[1])
                    for b in range(highbin-lowbin+1):
                        hist.SetBinContent(b+lowbin,0.)
                hist.SetBinErrorOption(ROOT.TH1.kPoisson)
            highestMax = max(highestMax,hist.GetMaximum())
            hists[histName] = hist

        # now draw them
        if self.stackOrder:
            stack.Draw("hist")
            stack.GetXaxis().SetTitle(xaxis)
            stack.GetYaxis().SetTitle(yaxis)
            stack.SetMaximum(1.2*highestMax)
            if ymax!=None: stack.SetMaximum(ymax)
            if ymin!=None: stack.SetMinimum(ymin)
            if plotratio: stack.GetHistogram().GetXaxis().SetLabelOffset(999)
        for histName,hist in hists.iteritems():
            style = self.styles[histName]
            hist.Draw(style['drawstyle']+' same')

        # get the legend
        legend = self.__getLegend(stack=stack,hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        pad = plotpad if plotratio else canvas
        if pad != ROOT.TVirtualPad.Pad(): pad.cd()
        self.__setStyle(pad,position=lumipos,preliminary=isprelim)

        # the ratio portion
        if plotratio:
            denom = stack.GetStack().Last().Clone('stack_{0}_ratio'.format(variable))
            ratiostaterr = self.__get_ratio_stat_err(denom)
            ratiostaterr.SetXTitle(xaxis)
            ratiounity = ROOT.TLine(stack.GetXaxis().GetXmin(),1,stack.GetXaxis().GetXmax(),1)
            ratiounity.SetLineStyle(2)
            ratios = OrderedDict()
            for histName, hist in hists.iteritems():
                if histName in self.signals:
                    hists = ROOT.TList()
                    hists.Add(hist)
                    hists.Add(denom)
                    num = hists[0].Clone('{0}_{1}_ratio'.format(histName,variable))
                    num.Reset()
                    num.Merge(hists)
                else:
                    num = hist.Clone('{0}_{1}_ratio'.format(histName,variable))
                if histName=='data':
                    num.SetBinErrorOption(ROOT.TH1.kPoisson)
                    num.Divide(denom)
                    #nbins = num.GetNbinsX()
                    #errs = ROOT.TGraphAsymmErrors(nbins)
                    #errs.Divide(num,denom,'pois')
                    #num = errs
                else:
                    num.Divide(denom)
                ratios[histName] = num

            # and draw
            if ratiopad != ROOT.TVirtualPad.Pad(): ratiopad.cd()
            ratiostaterr.Draw("e2")
            ratiounity.Draw('same')
            for histName, hist in ratios.iteritems():
                if histName=='data':
                    hist.Draw('e0 same')
                    #hist.Draw('0P same')
                else:
                    hist.Draw('hist same')

        # save
        if canvas != ROOT.TVirtualPad.Pad(): canvas.cd()
        self.__save(canvas,savename)

    def plotRatio(self,numerator,denominator,savename,**kwargs):
        '''Plot a ratio of two variables and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymin',None)
        ymax = kwargs.pop('ymax',None)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        customOrder = kwargs.pop('customOrder',[])

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        highestMax = 0.

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        for i,histName in enumerate(histOrder):
            num = self.__getHistogram(histName,numerator,nofill=True,**kwargs)
            denom = self.__getHistogram(histName,denominator,nofill=True,**kwargs)
            num.Sumw2()
            denom.Sumw2()
            num.Divide(denom)
            num.SetLineWidth(3)
            style = self.styles[histName]
            if i==0:
                num.Draw('e0')
                num.GetXaxis().SetTitle(xaxis)
                num.GetYaxis().SetTitle(yaxis)
                num.GetYaxis().SetTitleOffset(1.5)
                if ymax!=None: num.SetMaximum(ymax)
                if ymin!=None: num.SetMinimum(ymin)
            else:
                num.Draw('e0 same')
            highestMax = max(highestMax,num.GetMaximum())
            if ymax==None: num.SetMaximum(1.2*highestMax)
            hists[histName] = num

        legend = self.__getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self.__setStyle(canvas)

        self.__save(canvas,savename)

    def plotROC(self,signalVariable,backgroundVariable,savename,**kwargs):
        '''Plot ROC curve'''
        xaxis = kwargs.pop('xaxis', 'Signal Efficiency')
        yaxis = kwargs.pop('yaxis', 'Background Rejection')
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        customOrder = kwargs.pop('customOrder',[])
        invert = kwargs.pop('invert',False)
        ymin = kwargs.pop('ymin',0)
        ymax = kwargs.pop('ymax',1.2)

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        for i,histName in enumerate(histOrder):
            sig = self.__getHistogram(histName,signalVariable,nofill=True,**kwargs)
            bg = self.__getHistogram(histName,backgroundVariable,nofill=True,**kwargs)
            numBins = sig.GetNbinsX()
            sigEff = [0]*numBins
            bgEff = [0]*numBins
            totSig = sig.Integral()
            totBg = bg.Integral()
            for b in range(numBins):
                sigEff[b] = sig.Integral(1,b+1)/totSig if invert else sig.Integral(b+1,numBins)/totSig
                bgEff[b] = (totBg-bg.Integral(1,b+1))/totBg if invert else (totBg-bg.Integral(b+1,numBins))/totBg
            roc = ROOT.TGraph(numBins,array('f',sigEff),array('f',bgEff))
            style = self.styles[histName]
            roc.SetLineWidth(2)
            roc.SetLineColor(style['linecolor'])
            roc.SetMarkerColor(style['linecolor'])
            roc.SetFillColor(0)
            if i==0:
                roc.Draw('AL')
                roc.GetXaxis().SetTitle(xaxis)
                roc.GetYaxis().SetTitle(yaxis)
                roc.GetYaxis().SetTitleOffset(1.2)
                roc.SetMaximum(ymax)
                roc.SetMinimum(ymin)
            else:
                roc.Draw('L same')
            roc.SetTitle(style['name'])
            hists[histName] = roc

        legend = self.__getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self.__setStyle(canvas)

        self.__save(canvas,savename)

    def plotNormalized(self,variable,savename,**kwargs):
        '''Plot a ratio of two variables and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymin',None)
        ymax = kwargs.pop('ymax',None)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        customOrder = kwargs.pop('customOrder',[])

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        highestMax = 0.

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        for i,histName in enumerate(histOrder):
            hist = self.__getHistogram(histName,variable,nofill=True,**kwargs)
            hist.Scale(1./hist.Integral())
            hist.SetLineWidth(3)
            style = self.styles[histName]
            if i==0:
                hist.Draw(style['drawstyle'])
                hist.GetXaxis().SetTitle(xaxis)
                hist.GetYaxis().SetTitle(yaxis)
                hist.GetYaxis().SetTitleOffset(1.5)
                if ymax!=None: hist.SetMaximum(ymax)
                if ymin!=None: hist.SetMinimum(ymin)
            else:
                hist.Draw(style['drawstyle']+' same')
            highestMax = max(highestMax,hist.GetMaximum())
            if ymax==None: hist.SetMaximum(1.2*highestMax)
            hists[histName] = hist

        legend = self.__getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self.__setStyle(canvas)

        self.__save(canvas,savename)

    def plot2D(self,variable,savename,**kwargs):
        '''Plot a variable and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymax',None)
        ymax = kwargs.pop('ymax',None)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        logz = kwargs.pop('logz',False)

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)
        canvas.SetLogz(logz)
        canvas.SetRightMargin(0.14) # for Z axis


        highestMax = 0.

        hists = OrderedDict()
        for i,histName in enumerate(self.histOrder):
            hist = self.__get2DHistogram(histName,variable,**kwargs)
            hist.Draw('colz')
            if i==0:
                hist.GetXaxis().SetTitle(xaxis)
                hist.GetYaxis().SetTitle(yaxis)
                hist.GetYaxis().SetTitleOffset(1.5)
            hists[histName] = hist

        #legend = self.__getLegend(stack=stack,hists=hists,numcol=numcol,position=legendpos)
        #legend.Draw()

        self.__setStyle(canvas,position=0)

        self.__save(canvas,savename)
