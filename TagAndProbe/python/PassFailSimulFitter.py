#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import re

def rooIter(coll) :
    # PyROOT hasn't iterator-ized the RooFit collections
    if not coll.InheritsFrom(ROOT.RooAbsCollection.Class()) :
        raise Exception("Object is not iterable:\n"+repr(coll))
    i = coll.iterator()
    obj = i.Next()
    while obj :
        yield obj
        obj = i.Next()

class PassFailSimulFitter :
    _bkgPassRE = re.compile('background.*Pass.*')
    _bkgFailRE = re.compile('background.*Fail.*')

    def _wsimport(self, *args) :
        # getattr since import is special in python
        # NB RooWorkspace clones object
        if len(args) < 2 :
            # Useless RooCmdArg: https://sft.its.cern.ch/jira/browse/ROOT-6785
            args += (ROOT.RooCmdArg(),)
        return getattr(self.workspace, 'import')(*args)

    def __init__(self, name, fitVariable) :
        self.workspace = ROOT.RooWorkspace(name)
        self._wsimport(fitVariable)
        self._fitVar = self.workspace.var(fitVariable.GetName())
        self.workspace.factory("decision[Passed,Failed]")

    def setPdf(self, pdfDefinition) :
        for line in pdfDefinition :
            self.workspace.factory(line)
        self.workspace.saveSnapshot('setPdfParameters', self.workspace.components())

    def setData(self, name, passed, failed, separate = False) :
        # TODO: check passing failing hists for consistency
        nPass = passed.Integral()
        nFail = failed.Integral()
        if nPass == 0 or nFail == 0 :
            print 'WARNING: No passing or failing data!'
        if separate :
            dataPass = ROOT.RooDataHist(name+'Pass', name+' Passing bin', ROOT.RooArgList(self._fitVar), passed)
            self._wsimport(dataPass)
            dataFail = ROOT.RooDataHist(name+'Fail', name+' Failing bin', ROOT.RooArgList(self._fitVar), failed)
            self._wsimport(dataFail)
        else :
            m = ROOT.std.map('string, TH1*')()
            # const string: https://root.cern.ch/phpBB3/viewtopic.php?f=15&t=16882&start=15#p86985
            m.insert(ROOT.std.pair('const string, TH1*')('Passed', passed))
            m.insert(ROOT.std.pair('const string, TH1*')('Failed', failed))
            data = ROOT.RooDataHist(name, name, ROOT.RooArgList(self._fitVar), self.workspace.cat('decision'), m)
            self._wsimport(data)

    def addDataFromTree(self, tree, dataName, allProbeCondition, passingProbeCondition, **kwargs) :
        weightVariable = kwargs.pop('weightVariable', 'totWeight')
        separatePassFail = kwargs.pop('separatePassFail', False)
        varMin = self._fitVar.getMin()
        varMax = self._fitVar.getMax()
        varBins = self._fitVar.getBins()
        hpass = ROOT.TH1F(dataName+'_passed_probes', '', varBins, varMin, varMax)
        hfail = hpass.Clone(dataName+'_failed_probes')
        if type(allProbeCondition) is list :
            allProbeCondition = '&&'.join(allProbeCondition)
        tree.Draw('mass >> %s_passed_probes' % dataName, '%s*(%s)*(%s)' % (weightVariable, allProbeCondition, passingProbeCondition), 'goff')
        tree.Draw('mass >> %s_failed_probes' % dataName, '%s*(%s)*!(%s)' % (weightVariable, allProbeCondition, passingProbeCondition), 'goff')
        self.setData(dataName, hpass, hfail, separatePassFail)

    def fit(self, pdfName, dataName, reInitializeParameters = True) :
        w = self.workspace
        rf = ROOT.RooFit
        pdf = w.pdf(pdfName)
        data = w.data(dataName)

        #if reInitializeParameters :
        #    w.loadSnapshot('setPdfParameters')

        # Initialize some parameters
        nPass = data.sumEntries('decision==decision::Passed')
        nFail = data.sumEntries('decision==decision::Failed')
        # Crude estimate of passing signal purity
        # TODO: relies on fitVar being Z mass
        nPassCenter = data.sumEntries('decision==decision::Passed && mass>80 && mass<100')
        nPassSides   = data.sumEntries('decision==decision::Passed && mass<80 && mass>100')
        signalFractionPassing = (nPassCenter-nPassSides/2)/nPass

        initialEff = w.var('efficiency').getVal()
        nSignal = min(nPass*signalFractionPassing/initialEff, nPass+nFail)
        w.var('numSignalAll').setVal(nSignal)
        # Signal cannot be more than total data entries
        # but we leave wiggle room so that the uncertainty on low-background fits is still ok
        w.var('numSignalAll').setMax(nPass+nFail+math.sqrt(nPass+nFail))
        if w.var('numBackgroundPass') :
            # Similarly, background cannot be more than total pass/fail
            w.var('numBackgroundPass').setVal(nPass-nSignal*initialEff)
            w.var('numBackgroundPass').setMax(nPass+math.sqrt(nPass))
            w.var('numBackgroundFail').setVal(nFail-min(nSignal*(1-initialEff), nFail))
            w.var('numBackgroundFail').setMax(nFail+math.sqrt(nFail))

        minosVars = ROOT.RooArgSet(w.var('efficiency'))
        args = [
            rf.Save(True),
            rf.Minos(minosVars),
            rf.Verbose(False),
            rf.PrintLevel(0),
            rf.Minimizer("Minuit2","Migrad"),
        ]
        result = pdf.fitTo(data, *args)
        # Make title more computer-friendly
        result.SetTitle('%s;%s' % (pdfName, dataName))
        return result

    def drawFitCanvas(self, result) :
        w = self.workspace
        fitVar = self._fitVar
        rf = ROOT.RooFit

        passFrame = fitVar.frame(rf.Name("Passing"), rf.Title('Passing Probes'))
        failFrame = fitVar.frame(rf.Name('Failing'), rf.Title('Failing Probes'))
        allFrame  = fitVar.frame(rf.Name('All'),     rf.Title('All Probes'))

        for p in rooIter(result.floatParsFinal()) :
            w.var(p.GetName()).setVal(p.getVal())

        (pdfName, dataName) = result.GetTitle().split(';')
        pdf = w.pdf(pdfName)
        pdfComponents = [c.GetName() for c in rooIter(pdf.getComponents())]
        bkgPassComponent = filter(self._bkgPassRE.match, pdfComponents).pop(0)
        bkgFailComponent = filter(self._bkgFailRE.match, pdfComponents).pop(0)
        bkgComponents = bkgPassComponent+','+bkgFailComponent
        data = w.data(dataName)
        datapass = data.reduce(rf.Cut('decision==decision::Passed'))
        datafail = data.reduce(rf.Cut('decision==decision::Failed'))

        datapass.plotOn(passFrame)
        pdf.plotOn(passFrame, rf.Slice(w.cat('decision'), 'Passed'), rf.ProjWData(datapass), rf.LineColor(ROOT.kGreen))
        if w.pdf('backgroundPass') :
            pdf.plotOn(passFrame, rf.Slice(w.cat('decision'), 'Passed'), rf.ProjWData(datapass), rf.LineColor(ROOT.kGreen), rf.Components(bkgPassComponent), rf.LineStyle(ROOT.kDashed))

        datafail.plotOn(failFrame)
        pdf.plotOn(failFrame, rf.Slice(w.cat('decision'), 'Failed'), rf.ProjWData(datafail), rf.LineColor(ROOT.kRed))
        if w.pdf('backgroundFail') :
            pdf.plotOn(failFrame, rf.Slice(w.cat('decision'), 'Failed'), rf.ProjWData(datafail), rf.LineColor(ROOT.kRed), rf.Components(bkgFailComponent), rf.LineStyle(ROOT.kDashed))

        data.plotOn(allFrame)
        pdf.plotOn(allFrame, rf.ProjWData(data))
        if w.pdf('backgroundPass') :
            pdf.plotOn(allFrame, rf.ProjWData(data), rf.LineColor(ROOT.kBlue), rf.Components(bkgComponents), rf.LineStyle(ROOT.kDashed))

        # infoFrame is a placeholder
        infoFrame = fitVar.frame(rf.Name("Fit Results"), rf.Title("Fit Results"))
        dispParams = pdf.getParameters(data)
        pdf.paramOn(infoFrame, rf.Format('NE'), rf.Layout(0.15, 0.95, 0.95), rf.Parameters(dispParams))
        paramBox = infoFrame.findObject('%s_paramBox'%pdf.GetName())

        c = ROOT.TCanvas('fit_canvas', 'Fit Canvas', 700, 500)
        c.Divide(2,2)
        c.cd(1)
        passFrame.Draw()
        c.cd(2)
        failFrame.Draw()
        c.cd(3)
        allFrame.Draw()
        c.cd(4)
        paramBox.Draw()
        for obj in [passFrame, failFrame, allFrame, infoFrame] :
            ROOT.SetOwnership(obj, False)
        c.GetListOfPrimitives().SetOwner(True)
        return c


