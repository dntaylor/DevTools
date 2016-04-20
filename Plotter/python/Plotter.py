import os
import sys
import logging
import math
from array import array
from collections import OrderedDict

import ROOT

from DevTools.Plotter.PlotterBase import PlotterBase
from DevTools.Plotter.NtupleWrapper import NtupleWrapper
from DevTools.Plotter.utilities import python_mkdir, getLumi
from DevTools.Plotter.style import getStyle
import DevTools.Plotter.CMS_lumi as CMS_lumi
import DevTools.Plotter.tdrstyle as tdrstyle

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
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


class Plotter(PlotterBase):
    '''Basic plotter utilities'''

    def __init__(self,analysis,**kwargs):
        '''Initialize the plotter'''
        super(Plotter, self).__init__(analysis,**kwargs)

        # empty initialization
        self.histDict = {}
        self.analysisDict = {}
        self.stackOrder = []
        self.histOrder = []
        self.sampleFiles = {}
        self.styles = {}
        self.signals = []
        self.histScales = {}
        self.j = 0

    def __exit__(self, type, value, traceback):
        self.finish()

    def __del__(self):
        self.finish()

    def finish(self):
        '''Cleanup stuff'''
        logging.info('Finished plotting')
        #self.saveFile.Close()

    def _openFile(self,sampleName,**kwargs):
        '''Verify and open a sample'''
        analysis = kwargs.pop('analysis',self.analysis)
        if analysis not in self.sampleFiles: self.sampleFiles[analysis] = {}
        if sampleName not in self.sampleFiles:
            self.sampleFiles[analysis][sampleName] = NtupleWrapper(analysis,sampleName,**kwargs)
            ROOT.gROOT.cd()
        else:
            logging.warning('Sample {0} for analysis {1} already added to plot.'.format(sampleName,analysis))

    def addHistogramToStack(self,histName,histConstituents,style={},**kwargs):
        '''
        Add a histogram to the stack. histConstituents is a list.
        '''
        analysis = kwargs.pop('analysis',self.analysis)
        for sampleName in histConstituents:
            self._openFile(sampleName,analysis=analysis,**kwargs)
        self.analysisDict[histName] = analysis
        self.histDict[histName] = histConstituents
        self.stackOrder += [histName]
        self.styles[histName] = getStyle(histName)
        self.styles[histName].update(style)

    def addHistogram(self,histName,histConstituents,style={},signal=False,scale=1,**kwargs):
        '''
        Add histogram to plot. histConstituents is a list.
        Style is a custom styling.
        '''
        analysis = kwargs.pop('analysis',self.analysis)
        for sampleName in histConstituents:
            self._openFile(sampleName,analysis=analysis,**kwargs)
        self.analysisDict[histName] = analysis
        self.histDict[histName] = histConstituents
        self.histOrder += [histName]
        self.styles[histName] = getStyle(histName)
        self.styles[histName].update(style)
        if signal: self.signals += [histName]
        if scale!=1: self.histScales[histName] = scale

    def clearHistograms(self):
        self.sampleFiles = {}
        self.analysisDict = {}
        self.histDict = {}
        self.histOrder = []
        self.stackOrder = []
        self.styles = {}
        self.signals = []
        self.histScales = {}

    def _readSampleVariable(self,sampleName,variable,**kwargs):
        '''Read the histogram from file'''
        analysis = kwargs.pop('analysis',self.analysis)
        hist = self.sampleFiles[analysis][sampleName].getHist(variable)
        return hist

    def _getHistogram(self,histName,variable,**kwargs):
        '''Get a styled histogram'''
        rebin = kwargs.pop('rebin',0)
        nofill = kwargs.pop('nofill',False)
        analysis = self.analysisDict[histName]
        # check if it is a variable map, variable list, or single variable
        if isinstance(variable,dict):       # its a map
            variable = variable[histName]
        if isinstance(variable,basestring): # its a single variable
            variable = [variable]
        # it is now a list
        if histName in self.histDict:
            hists = ROOT.TList()
            for varName in variable:
                for sampleName in self.histDict[histName]:
                    hist = self._readSampleVariable(sampleName,varName,analysis=analysis)
                    if hist: hists.Add(hist)
            if hists.IsEmpty(): return 0
            hist = hists[0].Clone('h_{0}_{1}'.format(histName,varName.replace('/','_')))
            hist.Reset()
            hist.Merge(hists)
            if rebin:
                if type(rebin) in [list,tuple]:
                    hist = hist.Rebin(len(rebin)-1,'',array('d',rebin))
                else:
                    hist = hist.Rebin(rebin)
            style = self.styles[histName]
            hist.SetTitle(style['name'])
            if 'linecolor' in style:
                hist.SetLineColor(style['linecolor'])
                hist.SetMarkerColor(style['linecolor'])
            if 'linestyle' in style:
                hist.SetLineStyle(style['linestyle'])
            if not nofill:
                if 'fillstyle' in style: hist.SetFillStyle(style['fillstyle'])
                if 'fillcolor' in style: hist.SetFillColor(style['fillcolor'])
            return hist
        else:
            logging.error('{0} not defined.'.format(histName))
            return 0

    def _getHistogramCounts(self,histName,variables,**kwargs):
        '''Get the integral of each given histogram'''
        savename = kwargs.pop('savename','')
        nofill = kwargs.pop('nofill',False)
        analysis = self.analysisDict[histName]
        numBins = len(variables)
        histTitle = 'h_{0}_{1}'.format(savename.replace('/','_'),histName)
        hist = ROOT.TH1F(histTitle,histTitle,numBins,0,numBins)
        for b,variable in enumerate(variables):
            varHist = self._getHistogram(histName,variable,analysis=analysis)
            if not varHist:
               hist.SetBinContent(b+1,0)
               hist.SetBinError(b+1,0)
            else:
               integral = varHist.Integral()
               err2 = 0.
               for hb in range(varHist.GetNbinsX()):
                   err2 += varHist.GetBinError(hb+1)**2
               hist.SetBinContent(b+1,integral)
               hist.SetBinError(b+1,err2**0.5)
        style = self.styles[histName]
        hist.SetTitle(style['name'])
        if 'linecolor' in style:
            hist.SetLineColor(style['linecolor'])
            hist.SetMarkerColor(style['linecolor'])
        if 'linestyle' in style:
            hist.SetLineStyle(style['linestyle'])
        if not nofill:
            if 'fillstyle' in style: hist.SetFillStyle(style['fillstyle'])
            if 'fillcolor' in style: hist.SetFillColor(style['fillcolor'])
        return hist


    def _get2DHistogram(self,histName,variable,**kwargs):
        '''Get a styled histogram'''
        rebinx = kwargs.pop('rebinx',0)
        rebiny = kwargs.pop('rebiny',0)
        analysis = self.analysisDict[histName]
        # check if it is a variable map
        varName = variable if isinstance(variable,basestring) else variable[histName]
        if histName in self.histDict:
            hists = ROOT.TList()
            for sampleName in self.histDict[histName]:
                hist = self._readSampleVariable(sampleName,varName,analysis=analysis)
                if hist: hists.Add(hist)
            if hists.IsEmpty(): return 0
            hist = hists[0].Clone('h_{0}_{1}'.format(histName,varName.replace('/','_')))
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

    def _getStack(self,variable,**kwargs):
        '''Get a stack of histograms'''
        stackname = 'h_stack_{0}'.format(self.j)
        self.j += 1
        stack = ROOT.THStack(stackname,stackname)
        for histName in self.stackOrder:
            hist = self._getHistogram(histName,variable,**kwargs)
            if hist: stack.Add(hist)
        return stack

    def _getStackCounts(self,variables,**kwargs):
        '''Get a stack of histograms'''
        savename = kwargs.pop('savename','')
        stackname = 'h_stack_{0}'.format(self.j)
        self.j += 1
        stack = ROOT.THStack(stackname,stackname)
        for histName in self.stackOrder:
            hist = self._getHistogramCounts(histName,variables,savename=savename,**kwargs)
            if hist: stack.Add(hist)
        return stack

    def _get_ratio_stat_err(self, hist, **kwargs):
        '''Return a statistical error bars for a ratio plot'''
        ratiomin = kwargs.pop('ratiomin',0.5)
        ratiomax = kwargs.pop('ratiomax',1.5)
        ratiostaterr = hist.Clone("{0}_ratiostaterr".format(hist.GetName))
        #ratiostaterr.Sumw2()
        ratiostaterr.SetStats(0)
        ratiostaterr.SetTitle("")
        ratiostaterr.GetYaxis().SetTitle("Data / MC")
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


    def _getLegend(self,**kwargs):
        '''Get the legend'''
        stack = kwargs.pop('stack',None)
        hists = kwargs.pop('hists',{})
        entries = []
        if stack:
            for hist,name in zip(reversed(stack.GetHists()),reversed(self.stackOrder)):
                style = self.styles[name]
                entries += [[hist,hist.GetTitle(),style['legendstyle']]]
        if hists:
            for name,hist in hists.iteritems():
                style = self.styles[name]
                entries += [[hist,hist.GetTitle(),style['legendstyle']]]
        return super(Plotter,self)._getLegend(entries=entries,**kwargs)

    def plot(self,variable,savename,**kwargs):
        '''Plot a variable and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymax',None)
        ymax = kwargs.pop('ymin',None)
        yscale = kwargs.pop('yscale',1.2)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        lumipos = kwargs.pop('lumipos',11)
        isprelim = kwargs.pop('preliminary',True)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        plotratio = kwargs.pop('plotratio',True)
        blinder = kwargs.pop('blinder',[])
        rangex = kwargs.pop('rangex',[])
        save = kwargs.pop('save',True)

        logging.info('Plotting {0}'.format(savename))

        ROOT.gDirectory.Delete('h_*')

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

        # ratio plot
        if plotratio:
            plotpad = ROOT.TPad("plotpad", "top pad", 0.0, 0.21, 1.0, 1.0)
            ROOT.SetOwnership(plotpad,False)
            plotpad.SetBottomMargin(0.04)
            plotpad.Draw()
            plotpad.SetLogy(logy)
            plotpad.SetLogx(logx)
            ratiopad = ROOT.TPad("ratiopad", "bottom pad", 0.0, 0.0, 1.0, 0.21)
            ROOT.SetOwnership(ratiopad,False)
            ratiopad.SetTopMargin(0.06)
            ratiopad.SetBottomMargin(0.5)
            ratiopad.SetTickx(1)
            ratiopad.SetTicky(1)
            ratiopad.Draw()
            ratiopad.SetLogx(logx)
            #if plotpad != ROOT.TVirtualPad.Pad(): plotpad.cd()
            plotpad.cd()
        else:
            canvas.SetLogy(logy)
            canvas.SetLogx(logx)


        highestMax = -9999999.

        # stack
        stack = 0
        if self.stackOrder:
            stack = self._getStack(variable,**kwargs)
            highestMax = max(highestMax,stack.GetMaximum())

        # overlay histograms
        hists = OrderedDict()
        for histName in self.histOrder:
            hist = self._getHistogram(histName,variable,nofill=True,**kwargs)
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
            else:
                hist.SetLineWidth(3)
            if histName in self.histScales:
                hist.Scale(self.histScales[histName])
                name = hist.GetTitle()
                name += ' (x{0})'.format(self.histScales[histName])
                hist.SetTitle(name)
            highestMax = max(highestMax,hist.GetMaximum())
            hists[histName] = hist

        # now draw them
        if self.stackOrder:
            stack.Draw("hist")
            stack.GetXaxis().SetTitle(xaxis)
            stack.GetYaxis().SetTitle(yaxis)
            stack.SetMaximum(yscale*highestMax)
            if len(rangex)==2: stack.GetXaxis().SetRangeUser(*rangex)
            if ymax!=None: stack.SetMaximum(ymax)
            if ymin!=None: stack.SetMinimum(ymin)
            if plotratio: stack.GetHistogram().GetXaxis().SetLabelOffset(999)
        for histName,hist in hists.iteritems():
            style = self.styles[histName]
            hist.Draw(style['drawstyle']+' same')

        # get the legend
        legend = self._getLegend(stack=stack,hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        pad = plotpad if plotratio else canvas
        #if pad != ROOT.TVirtualPad.Pad(): pad.cd()
        self._setStyle(pad,position=lumipos,preliminary=isprelim)

        # the ratio portion
        if plotratio:
            stackname = 'h_stack_{0}_ratio'.format(self.j)
            self.j += 1
            denom = stack.GetStack().Last().Clone(stackname)
            ratiostaterr = self._get_ratio_stat_err(denom)
            ratiostaterr.SetXTitle(xaxis)
            unityargs = [rangex[0],1,rangex[1],1] if len(rangex)==2 else [stack.GetXaxis().GetXmin(),1,stack.GetXaxis().GetXmax(),1]
            ratiounity = ROOT.TLine(*unityargs)
            ratiounity.SetLineStyle(2)
            ratios = OrderedDict()
            for histName, hist in hists.iteritems():
                numname = 'h_{0}_{1}_ratio'.format(histName,self.j)
                self.j += 1
                if histName in self.signals:
                    sighists = ROOT.TList()
                    sighists.Add(hist)
                    sighists.Add(denom)
                    num = sighists[0].Clone(numname)
                    num.Reset()
                    num.Merge(sighists)
                else:
                    num = hist.Clone(numname)
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
            #if ratiopad != ROOT.TVirtualPad.Pad(): ratiopad.cd()
            ratiopad.cd()
            ratiostaterr.Draw("e2")
            if len(rangex)==2: ratiostaterr.GetXaxis().SetRangeUser(*rangex)
            ratiounity.Draw('same')
            for histName, hist in ratios.iteritems():
                if histName=='data':
                    hist.Draw('e0 same')
                    #hist.Draw('0P same')
                else:
                    hist.SetLineWidth(3)
                    hist.Draw('hist same')
            #if canvas != ROOT.TVirtualPad.Pad(): canvas.cd()
            canvas.cd()

        # save
        if save: self._save(canvas,savename)

    def plotCounts(self,bins,labels,savename,**kwargs):
        '''Plot a histogram of counts for each bin and save'''
        xaxis = kwargs.pop('xaxis', '')
        yaxis = kwargs.pop('yaxis', 'Events')
        ymin = kwargs.pop('ymin',None)
        ymax = kwargs.pop('ymax',None)
        yscale = kwargs.pop('yscale',1.2)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',33)
        lumipos = kwargs.pop('lumipos',11)
        isprelim = kwargs.pop('preliminary',True)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        plotratio = kwargs.pop('plotratio',True)
        save = kwargs.pop('save',True)

        logging.info('Plotting {0}'.format(savename))
        ROOT.gDirectory.Delete('h_*')

        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)

        # ratio plot
        if plotratio:
            plotpad = ROOT.TPad("plotpad", "top pad", 0.0, 0.21, 1.0, 1.0)
            ROOT.SetOwnership(plotpad,False)
            plotpad.SetBottomMargin(0.04)
            plotpad.Draw()
            plotpad.SetLogy(logy)
            plotpad.SetLogx(logx)
            ratiopad = ROOT.TPad("ratiopad", "bottom pad", 0.0, 0.0, 1.0, 0.21)
            ROOT.SetOwnership(ratiopad,False)
            ratiopad.SetTopMargin(0.06)
            ratiopad.SetBottomMargin(0.5)
            ratiopad.SetTickx(1)
            ratiopad.SetTicky(1)
            ratiopad.Draw()
            ratiopad.SetLogx(logx)
            #if plotpad != ROOT.TVirtualPad.Pad(): plotpad.cd()
            plotpad.cd()
        else:
            canvas.SetLogy(logy)
            canvas.SetLogx(logx)

        highestMax = -9999999.

        # stack
        stack = ROOT.THStack()
        if self.stackOrder:
            stack = self._getStackCounts(bins,savename=savename,**kwargs)
            highestMax = max(highestMax,stack.GetMaximum())

        # overlay histograms
        hists = OrderedDict()
        for histName in self.histOrder:
            hist = self._getHistogramCounts(histName,bins,nofill=True,**kwargs)
            if histName=='data':
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(1.)
                hist.SetLineColor(ROOT.kBlack)
                hist.SetBinErrorOption(ROOT.TH1.kPoisson)
            else:
                hist.SetLineWidth(3)
            if histName in self.histScales:
                hist.Scale(self.histScales[histName])
                name = hist.GetTitle()
                name += ' (x{0})'.format(self.histScales[histName])
                hist.SetTitle(name)
            highestMax = max(highestMax,hist.GetMaximum())
            hists[histName] = hist

        # now draw them
        if self.stackOrder:
            stack.Draw("hist")
            stack.GetXaxis().SetTitle(xaxis)
            stack.GetYaxis().SetTitle(yaxis)
            stack.SetMaximum(yscale*highestMax)
            for b,label in enumerate(labels):
                stack.GetHistogram().GetXaxis().SetBinLabel(b+1,label)
            if ymax!=None: stack.SetMaximum(ymax)
            if ymin!=None: stack.SetMinimum(ymin)
            if plotratio: stack.GetHistogram().GetXaxis().SetLabelOffset(999)
        for histName,hist in hists.iteritems():
            style = self.styles[histName]
            hist.Draw(style['drawstyle']+' same')

        # get the legend
        legend = self._getLegend(stack=stack,hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        # cms lumi styling
        pad = plotpad if plotratio else canvas
        #if pad != ROOT.TVirtualPad.Pad(): pad.cd()
        self._setStyle(pad,position=lumipos,preliminary=isprelim)

        # cms lumi styling
        pad = plotpad if plotratio else canvas
        #if pad != ROOT.TVirtualPad.Pad(): pad.cd()
        self._setStyle(pad,position=lumipos,preliminary=isprelim)

        # the ratio portion
        if plotratio:
            denom = stack.GetStack().Last().Clone('h_stack_{0}_ratio'.format(savename.replace('/','_')))
            ratiostaterr = self._get_ratio_stat_err(denom)
            ratiostaterr.SetXTitle(xaxis)
            for b,label in enumerate(labels):
                ratiostaterr.GetXaxis().SetBinLabel(b+1,label)
            unityargs = [stack.GetXaxis().GetXmin(),1,stack.GetXaxis().GetXmax(),1]
            ratiounity = ROOT.TLine(*unityargs)
            ratiounity.SetLineStyle(2)
            ratios = OrderedDict()
            for histName, hist in hists.iteritems():
                if histName in self.signals:
                    sighists = ROOT.TList()
                    sighists.Add(hist)
                    sighists.Add(denom)
                    num = sighists[0].Clone('h_{0}_{1}_ratio'.format(histName,savename.replace('/','_')))
                    num.Reset()
                    num.Merge(sighists)
                else:
                    num = hist.Clone('h_{0}_{1}_ratio'.format(histName,savename.replace('/','_')))
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
            #if ratiopad != ROOT.TVirtualPad.Pad(): ratiopad.cd()
            ratiopad.cd()
            ratiostaterr.Draw("e2")
            ratiounity.Draw('same')
            for histName, hist in ratios.iteritems():
                if histName=='data':
                    hist.Draw('e0 same')
                    #hist.Draw('0P same')
                else:
                    hist.SetLineWidth(3)
                    hist.Draw('hist same')
            #if canvas != ROOT.TVirtualPad.Pad(): canvas.cd()
            canvas.cd()

        # save
        if save: self._save(canvas,savename)


    def plotRatio(self,numerator,denominator,savename,**kwargs):
        '''Plot a ratio of two variables and save'''
        xaxis = kwargs.pop('xaxis', 'Variable')
        yaxis = kwargs.pop('yaxis', 'Efficiency')
        ymin = kwargs.pop('ymin',None)
        ymax = kwargs.pop('ymax',None)
        yscale = kwargs.pop('yscale',1.2)
        numcol = kwargs.pop('numcol',1)
        legendpos = kwargs.pop('legendpos',34)
        logy = kwargs.pop('logy',False)
        logx = kwargs.pop('logx',False)
        customOrder = kwargs.pop('customOrder',[])
        subtractMap = kwargs.pop('subtractMap',{})
        getHists = kwargs.pop('getHists', False)

        logging.info('Plotting {0}'.format(savename))
        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        highestMax = 0.

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        
        for i,histName in enumerate(histOrder):
            num = self._getHistogram(histName,numerator,nofill=True,**kwargs)
            denom = self._getHistogram(histName,denominator,nofill=True,**kwargs)
            if histName in subtractMap:
                for subName in subtractMap[histName]:
                    numsub = self._getHistogram(subName,numerator,nofill=True,**kwargs)
                    num.Add(numsub,-1)
                    denomsub = self._getHistogram(subName,denominator,nofill=True,**kwargs)
                    denom.Add(denomsub,-1)
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
                num.SetMinimum(0.)
                if ymax!=None: num.SetMaximum(ymax)
                if ymin!=None: num.SetMinimum(ymin)
            else:
                num.Draw('e0 same')
            highestMax = max(highestMax,num.GetMaximum())
            if ymax==None: num.SetMaximum(yscale*highestMax)
            hists[histName] = num

        if getHists: return hists

        legend = self._getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self._setStyle(canvas)

        self._save(canvas,savename)

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

        logging.info('Plotting {0}'.format(savename))
        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        for i,histName in enumerate(histOrder):
            sig = self._getHistogram(histName,signalVariable,nofill=True,**kwargs)
            bg = self._getHistogram(histName,backgroundVariable,nofill=True,**kwargs)
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

        legend = self._getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self._setStyle(canvas)

        self._save(canvas,savename)

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
        rangex = kwargs.pop('rangex',[])
        customOrder = kwargs.pop('customOrder',[])
        subtractMap = kwargs.pop('subtractMap',{})

        logging.info('Plotting {0}'.format(savename))
        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)

        highestMax = 0.

        hists = OrderedDict()
        histOrder = customOrder if customOrder else self.histOrder
        for i,histName in enumerate(histOrder):
            hist = self._getHistogram(histName,variable,nofill=True,**kwargs)
            if histName in subtractMap:
                for subName in subtractMap[histName]:
                    histsub = self._getHistogram(subName,variable,nofill=True,**kwargs)
                    hist.Add(histsub,-1)
            if hist.Integral(): hist.Scale(1./hist.Integral())
            hist.SetLineWidth(3)
            highestMax = max(highestMax,hist.GetMaximum())
            if ymax==None: hist.SetMaximum(1.2*highestMax)
            hists[histName] = hist

        for i,histName in enumerate(histOrder):
            hist = hists[histName]
            style = self.styles[histName]
            if i==0:
                hist.Draw(style['drawstyle'])
                hist.GetXaxis().SetTitle(xaxis)
                hist.GetYaxis().SetTitle(yaxis)
                hist.GetYaxis().SetTitleOffset(1.5)
                if len(rangex)==2: hist.GetXaxis().SetRangeUser(*rangex)
                if ymax!=None: hist.SetMaximum(ymax)
                if ymin!=None: hist.SetMinimum(ymin)
                if ymax==None: hist.SetMaximum(1.2*highestMax)
            else:
                hist.Draw(style['drawstyle']+' same')

        legend = self._getLegend(hists=hists,numcol=numcol,position=legendpos)
        legend.Draw()

        self._setStyle(canvas)

        self._save(canvas,savename)

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

        logging.info('Plotting {0}'.format(savename))
        canvas = ROOT.TCanvas(savename,savename,50,50,600,600)
        canvas.SetLogy(logy)
        canvas.SetLogx(logx)
        canvas.SetLogz(logz)
        canvas.SetRightMargin(0.14) # for Z axis


        highestMax = 0.

        hists = OrderedDict()
        for i,histName in enumerate(self.histOrder):
            hist = self._get2DHistogram(histName,variable,**kwargs)
            hist.Draw('colz')
            if i==0:
                hist.GetXaxis().SetTitle(xaxis)
                hist.GetYaxis().SetTitle(yaxis)
                hist.GetYaxis().SetTitleOffset(1.5)
            hists[histName] = hist

        #legend = self._getLegend(stack=stack,hists=hists,numcol=numcol,position=legendpos)
        #legend.Draw()

        self._setStyle(canvas,position=0)

        self._save(canvas,savename)
