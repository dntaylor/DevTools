import os
import sys
import logging
import math

import ROOT

import operator

def product(iterable):
    if not iterable: return 0. # case of empty list
    return reduce(operator.mul, iterable, 1)

class TriggerScales(object):
    '''Class to access the trigger scales for a given trigger configuration.'''

    def __init__(self):
        ####################
        ### POG APPROVED ###
        ####################
        # single muon
        # https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2
        singleMu_path = '{0}/src/DevTools/Analyzer/data/SingleMuonTrigger_Z_RunCD_Reco76X_Feb15.root'.format(os.environ['CMSSW_BASE'])
        self.singleMu_rootfile = ROOT.TFile(singleMu_path)
        self.singleMu_efficiencies = {}
        for name in ['runC_IsoMu20_OR_IsoTkMu20', 'runC_Mu45_eta2p1', 'runC_Mu50',
                     'runD_IsoMu20_OR_IsoTkMu20_HLTv4p2', 'runD_IsoMu20_OR_IsoTkMu20_HLTv4p3',
                     'runD_Mu45_eta2p1', 'runD_Mu50']:
                directory = '{0}_PtEtaBins'.format(name)
                self.singleMu_efficiencies[name] = {
                    'MC'   : self.singleMu_rootfile.Get('{0}/efficienciesMC/pt_abseta_MC'.format(directory)),
                    'DATA' : self.singleMu_rootfile.Get('{0}/efficienciesDATA/pt_abseta_DATA'.format(directory)),
                }

        # double tau fits
        self.doubleTau_efficiencies = {
            'MC': {
                'val'    : {'m0' : 3.60274e01, 'sigma' : 5.89434e00, 'alpha' : 5.82870e00, 'n' : 1.83737e00, 'norm' : 9.58000e-01,},
                'errUp'  : {'m0' : 3.56012e01, 'sigma' : 5.97209e00, 'alpha' : 6.09604e00, 'n' : 1.68740e00, 'norm' : 9.87653e-01,},
                'errDown': {'m0' : 3.62436e01, 'sigma' : 5.58461e00, 'alpha' : 5.12924e00, 'n' : 2.05921e00, 'norm' : 9.32305e-01,},
            },
            'DATA': {
                'val'    : {'m0' : 3.45412e01, 'sigma' : 5.63353e00, 'alpha' : 2.49242e00, 'n' : 3.35896e00, 'norm' : 1.00000e00,},
                'errUp'  : {'m0' : 3.31713e01, 'sigma' : 5.66551e00, 'alpha' : 1.87175e00, 'n' : 8.07790e00, 'norm' : 1.00000e00,},
                'errDown': {'m0' : 3.56264e01, 'sigma' : 5.30711e00, 'alpha' : 2.81591e00, 'n' : 2.40649e00, 'norm' : 9.99958e-01,},
            },
        }

        ##############
        ### OTHERS ###
        ##############
        # HWW measurements: single mu, single e, double mu per leg, double e per leg
        # https://twiki.cern.ch/twiki/bin/view/CMS/HWW2015TriggerResults
        singleMu_path     = '{0}/src/DevTools/Analyzer/data/HWW_HLT_IsoMu20orIsoTkMu20_76X.txt'.format(os.environ['CMSSW_BASE'])
        doubleMuLeg1_path = '{0}/src/DevTools/Analyzer/data/HWW_HLT_Mu17_Mu8Leg1_76X.txt'.format(os.environ['CMSSW_BASE'])
        doubleMuLeg2_path = '{0}/src/DevTools/Analyzer/data/HWW_HLT_Mu17_Mu8Leg2_76X.txt'.format(os.environ['CMSSW_BASE'])
        singleE_path      = '{0}/src/DevTools/Analyzer/data/HWW_HLT_Ele23_WPLoose_76X.txt'.format(os.environ['CMSSW_BASE'])
        doubleELeg1_path  = '{0}/src/DevTools/Analyzer/data/HWW_HLT_Ele17_Ele12Leg1_76X.txt'.format(os.environ['CMSSW_BASE'])
        doubleELeg2_path  = '{0}/src/DevTools/Analyzer/data/HWW_HLT_Ele17_Ele12Leg2_76X.txt'.format(os.environ['CMSSW_BASE'])
        self.hww_singleMu_efficiencies     = self.__parse_hww(singleMu_path,'muons')
        self.hww_doubleMuLeg1_efficiencies = self.__parse_hww(doubleMuLeg1_path,'muons')
        self.hww_doubleMuLeg2_efficiencies = self.__parse_hww(doubleMuLeg2_path,'muons')
        self.hww_singleE_efficiencies      = self.__parse_hww(singleE_path,'electrons')
        self.hww_doubleELeg1_efficiencies  = self.__parse_hww(doubleELeg1_path,'electrons')
        self.hww_doubleELeg2_efficiencies  = self.__parse_hww(doubleELeg2_path,'electrons')
        
        # define supported triggers
        self.singleTriggers = {
            'muons'    : ['IsoMu20_OR_IsoTkMu20', 'Mu45_eta2p1', 'Mu50', 'Mu17_Mu8Leg1', 'Mu17_Mu8Leg2'],
            'electrons': ['Ele23_WPLoose', 'Ele17_Ele12Leg1', 'Ele17_Ele12Leg2'],
            'taus'     : ['PFTau35'],
        }
        self.doubleTriggers = {
            'muons'    : ['Mu17_Mu8'],
            'electrons': ['Ele17_Ele12'],
            'taus'     : ['DoublePFTau35'],
        }

    def __parse_hww(self,filename,fileType):
        '''Parse text file of trigger efficiencies
           Format:
               muons:     etamin etamax ptmin ptmax eff errup errdown
               electrons: etamin etamax ptmin ptmax eff err
        '''
        scales = []
        with open(filename) as f:
            for line in f.readlines():
                if fileType=='muons':
                    etamin, etamax, ptmin, ptmax, eff, errup, errdown = line.split()
                elif fileType=='electrons':
                    etamin, etamax, ptmin, ptmax, eff, err = line.split()
                    errup = err
                    errdown = err
                else:
                    logging.error('Unrecognized HWW scale fileType: {0}'.format(fileType))
                    return []
                scales += [{
                    'etamin' : float(etamin), 
                    'etamax' : float(etamax), 
                    'ptmin'  : float(ptmin), 
                    'ptmax'  : float(ptmax), 
                    'eff'    : float(eff), 
                    'errup'  : float(errup), 
                    'errdown': float(errdown),
                }]
        return scales

    def __doubleTau35_fit(self,pt,mode):
        m0    = self.doubleTau_efficiencies[mode]['val']['m0']
        sigma = self.doubleTau_efficiencies[mode]['val']['sigma']
        alpha = self.doubleTau_efficiencies[mode]['val']['alpha']
        n     = self.doubleTau_efficiencies[mode]['val']['n']
        norm  = self.doubleTau_efficiencies[mode]['val']['norm']
        x = pt
        # recreate the fit
        sqrtPiOver2 = math.sqrt(ROOT.TMath.PiOver2())
        sqrt2 = math.sqrt(2.)
        sig = abs(sigma)
        t = (x-m0)/sig * alpha/abs(alpha)
        absAlpha = abs(alpha/sig)
        a =  ROOT.TMath.Power(n/absAlpha,n) * ROOT.TMath.Exp(-0.5*absAlpha*absAlpha)
        b = absAlpha - n/absAlpha
        arg = absAlpha/sqrt2
        if arg>5.: ApproxErf = 1.
        elif arg<-5.: ApproxErf = -1.
        else: ApproxErf = ROOT.TMath.Erf(arg)
        leftArea = (1.+ApproxErf)*sqrtPiOver2
        rightArea = (a*1./ROOT.TMath.Power(absAlpha-b,n-1))/(n-1)
        area = leftArea+rightArea
        if t<= absAlpha:
            arg = t/sqrt2
            if arg>5.: ApproxErf = 1.
            elif arg<-5.: ApproxErf = -1.
            else: ApproxErf = ROOT.TMath.Erf(arg)
            return norm * (1.+ApproxErf)*sqrtPiOver2/area
        else:
            return norm * (leftArea + a * (1./ROOT.TMath.Power(t-b,n-1) - 1./ROOT.TMath.Power(absAlpha-b,n-1))/(1-n))/area

    def __exit__(self, type, value, traceback):
        self.__finish()

    def __del__(self):
        self.__finish()

    def __finish(self):
        self.singleMu_rootfile.Close()

    def __triggerWarning(self,triggers):
        logging.warning('Unmatched triggers: {0}'.format(' '.join(triggers)))
        return 0.

    def __getEfficiency(self,rtrow,rootName,mode,cand,pt,eta):
        if cand[0]=='muons':
            # Muon POG
            # ignore Run2015C, reweight isomu via hlt trigger
            if rootName == 'IsoMu20_OR_IsoTkMu20':
                if pt>120: pt = 119
                name0 = 'runD_{0}_HLTv4p2'.format(rootName)
                name1 = 'runD_{0}_HLTv4p3'.format(rootName)
                hist0 = self.singleMu_efficiencies[name0][mode]
                hist1 = self.singleMu_efficiencies[name1][mode]
                val0 = hist0.GetBinContent(hist0.FindBin(pt,abs(eta)))
                val1 = hist0.GetBinContent(hist1.FindBin(pt,abs(eta)))
                return (0.401*val0+1.899*val1)/2.3
            elif rootName in ['Mu50', 'Mu45_eta2p1']:
                if pt>120: pt = 119
                hist = self.singleMu_efficiencies['runD_{0}'.format(rootName)][mode]
                return hist.GetBinContent(hist.FindBin(pt,abs(eta)))
            # HWW
            elif rootName=='Mu17_Mu8Leg1':
                if pt>200: pt = 199
                for row in self.hww_doubleMuLeg1_efficiencies:
                   if (eta>=row['etamin'] 
                       and eta<=row['etamax']
                       and pt>=row['ptmin']
                       and pt<=row['ptmax']):
                       return row['eff']
            elif rootName=='Mu17_Mu8Leg2':
                if pt>200: pt = 199
                for row in self.hww_doubleMuLeg2_efficiencies:
                   if (eta>=row['etamin'] 
                       and eta<=row['etamax']
                       and pt>=row['ptmin']
                       and pt<=row['ptmax']):
                       return row['eff']
        elif cand[0]=='electrons':
            # HWW
            if rootName=='Ele23_WPLoose':
                if pt>100: pt = 99
                for row in self.hww_singleE_efficiencies:
                   if (eta>=row['etamin'] 
                       and eta<=row['etamax']
                       and pt>=row['ptmin']
                       and pt<=row['ptmax']):
                       return row['eff']
            elif rootName=='Ele17_Ele12Leg1':
                if pt>100: pt = 99
                for row in self.hww_doubleELeg1_efficiencies:
                   if (eta>=row['etamin'] 
                       and eta<=row['etamax']
                       and pt>=row['ptmin']
                       and pt<=row['ptmax']):
                       return row['eff']
            elif rootName=='Ele17_Ele12Leg2':
                if pt>100: pt = 99
                for row in self.hww_doubleELeg2_efficiencies:
                   if (eta>=row['etamin'] 
                       and eta<=row['etamax']
                       and pt>=row['ptmin']
                       and pt<=row['ptmax']):
                       return row['eff']
        elif cand[0]=='taus':
            if rootName=='PFTau35':
                return self.__doubleTau35_fit(pt,mode)
        return 0.

    def __getLeadEfficiency(self,rtrow,rootNames,mode,cand,pt,eta):
        if cand[0]=='electrons':
            if 'Ele17_Ele12' in rootNames:
                return self.__getEfficiency(rtrow,'Ele17_Ele12Leg1',mode,cand,pt,eta)
        elif cand[0]=='muons':
            if 'Mu17_Mu8' in rootNames:
                return self.__getEfficiency(rtrow,'Mu17_Mu8Leg1',mode,cand,pt,eta)
        elif cand[0]=='taus':
            if 'DoublePFTau35' in rootNames:
                return self.__getEfficiency(rtrow,'PFTau35',mode,cand,pt,eta)
        return 0.

    def __getTrailEfficiency(self,rtrow,rootNames,mode,cand,pt,eta):
        if cand[0]=='electrons':
            if 'Ele17_Ele12' in rootNames:
                return self.__getEfficiency(rtrow,'Ele17_Ele12Leg2',mode,cand,pt,eta)
        elif cand[0]=='muons':
            if 'Mu17_Mu8' in rootNames:
                return self.__getEfficiency(rtrow,'Mu17_Mu8Leg2',mode,cand,pt,eta)
        elif cand[0]=='taus':
            if 'DoublePFTau35' in rootNames:
                return self.__getEfficiency(rtrow,'PFTau35',mode,cand,pt,eta)
        return 0.

    def __getSingleEfficiency(self,rtrow,rootNames,mode,cand,pt,eta):
        if cand[0]=='electrons':
            if 'Ele23_WPLoose' in rootNames:
                return self.__getEfficiency(rtrow,'Ele23_WPLoose',mode,cand,pt,eta)
            elif 'Ele17_Ele12Leg1' in rootNames:
                return self.__getEfficiency(rtrow,'Ele17_Ele12Leg1',mode,cand,pt,eta)
            elif 'Ele17_Ele12Leg2' in rootNames:
                return self.__getEfficiency(rtrow,'Ele17_Ele12Leg2',mode,cand,pt,eta)
        elif cand[0]=='muons':
            if 'IsoMu20_OR_IsoTkMu20' in rootNames:
                return self.__getEfficiency(rtrow,'IsoMu20_OR_IsoTkMu20',mode,cand,pt,eta)
            elif 'Mu45_eta2p1' in rootNames:
                return self.__getEfficiency(rtrow,'Mu45_eta2p1',mode,cand,pt,eta)
            elif 'Mu50' in rootNames:
                return self.__getEfficiency(rtrow,'Mu50',mode,cand,pt,eta)
            elif 'Mu17_Mu8Leg1' in rootNames:
                return self.__getEfficiency(rtrow,'Mu17_Mu8Leg1',mode,cand,pt,eta)
            elif 'Mu17_Mu8Leg2' in rootNames:
                return self.__getEfficiency(rtrow,'Mu17_Mu8Leg2',mode,cand,pt,eta)
        elif cand[0]=='taus':
            if 'PFTau35' in rootNames:
                return self.__getEfficiency(rtrow,'PFTau35',mode,cand,pt,eta)
        return 0.

    def __hasSingle(self,triggers,triggerType):
        for trigger in triggers:
            if trigger in self.singleTriggers[triggerType]: return True
        return False

    def __hasDouble(self,triggers,triggerType):
        for trigger in triggers:
            if trigger in self.doubleTriggers[triggerType]: return True
        return False


    def __getTriggerEfficiency(self,rtrow,triggers,cands,mode):
        '''Get an efficiency'''

        pts = {}
        etas = {}
        for cand in cands:
            pts[cand]  = getattr(rtrow,'{0}_rochesterPt'.format(cand[0]))[cand[1]] if cand[0]=='muons' else getattr(rtrow,'{0}_pt'.format(cand[0]))[cand[1]]
            etas[cand] = getattr(rtrow,'{0}_rochesterEta'.format(cand[0]))[cand[1]] if cand[0]=='muons' else getattr(rtrow,'{0}_eta'.format(cand[0]))[cand[1]]

        #######################
        ### Single triggers ###
        #######################
        if ((len(triggers)==1 and (self.__hasSingle(triggers,'electrons') or self.__hasSingle(triggers,'muons'))) or
            (len(triggers)==2 and (self.__hasSingle(triggers,'electrons') and self.__hasSingle(triggers,'muons')))):
            val = 1-product([1-self.__getSingleEfficiency(rtrow,triggers,mode,cand,pts[cand],etas[cand]) for cand in cands])
        

        #######################
        ### Double triggers ###
        #######################
        elif ((len(triggers)==1 and (self.__hasDouble(triggers,'electrons') or self.__hasDouble(triggers,'muons') or   # ee, mm, tt
                  self.__hasDouble(triggers,'taus'))) or
              (len(triggers)==2 and (self.__hasDouble(triggers,'electrons') and self.__hasDouble(triggers,'muons')))): # ee/mm
            val = 1-(
                # none pass lead
                product([1-self.__getLeadEfficiency(rtrow,triggers,mode,cand,pts[cand],etas[cand]) for cand in cands])
                # one pass lead, none pass trail
                +sum([self.__getLeadEfficiency(rtrow,triggers,mode,lead,pts[lead],etas[lead])
                      *product([1-self.__getTrailEfficiency(rtrow,triggers,mode,trail,pts[trail],etas[trail]) if trail!=lead else 1. for trail in cands if trail[0]==lead[0]]) for lead in cands])
                # TODO: DZ not included ???
                # one pass lead, one pass trail, fail dz
                # one pass lead, two pass trail, both fail dz
            )

        ################################
        ### single + double triggers ###
        ################################
        elif ((len(triggers)==2 and ((self.__hasSingle(triggers,'electrons') and self.__hasDouble(triggers,'electrons')) or # e/ee
                                     (self.__hasSingle(triggers,'muons') and self.__hasDouble(triggers,'muons')))) or       # m/mm
              (len(triggers)==3 and ((self.__hasSingle(triggers,'electrons') and self.__hasSingle(triggers,'muons')         # e/m/tt
                                     and self.__hasDouble(triggers,'taus')))) or
              (len(triggers)==4 and (self.__hasSingle(triggers,'electrons') and self.__hasDouble(triggers,'electrons') and  # e/m/ee/mm (e/m/ee/em/mm)
                                     self.__hasSingle(triggers,'muons') and self.__hasDouble(triggers,'muons'))) or
              (len(triggers)==5 and (self.__hasSingle(triggers,'electrons') and self.__hasDouble(triggers,'electrons') and  # e/m/ee/mm/tt (e/m/ee/em/mm/tt)
                                     self.__hasSingle(triggers,'muons') and self.__hasDouble(triggers,'muons') and
                                     self.__hasDouble(triggers,'taus')))):
            val = 1-(
                # none pass single
                product([1-self.__getSingleEfficiency(rtrow,triggers,mode,cand,pts[cand],etas[cand]) for cand in cands if cand[0] in ['electrons','muons']]) # only electron/muon single triggers
            )*(
                # none pass lead
                product([1-self.__getLeadEfficiency(rtrow,triggers,mode,cand,pts[cand],etas[cand]) for cand in cands])
                # one pass lead, none pass trail
                +sum([self.__getLeadEfficiency(rtrow,triggers,mode,lead,pts[lead],etas[lead])
                      *product([1-self.__getTrailEfficiency(rtrow,triggers,mode,trail,pts[trail],etas[trail]) if trail!=lead else 1. for trail in cands if (
                                       (trail[0]=='taus' and lead[0]=='taus') or                                # no cross trigger with taus
                                       (trail[0] in ['electrons','muons'] and lead[0] in ['electrons','muons']) # allow cross triggers with e/m
                                   )
                               ]) for lead in cands])
                # TODO: DZ not included ???
                # one pass lead, one pass trail, fail dz
                # one pass lead, two pass trail, both fail dz
            )

        else:
            val = 1

        return val

    def getMCEfficiency(self,rtrow,triggers,cands):
        '''Get the efficiency for a set of triggers for a list of candidates in MC'''
        return self.__getTriggerEfficiency(rtrow,triggers,cands,'MC')

    def getDataEfficiency(self,rtrow,triggers,cands):
        '''Get the efficiency for a set of triggers for a list of candidates in DATA'''
        return self.__getTriggerEfficiency(rtrow,triggers,cands,'DATA')

    def getRatio(self,rtrow,triggers,cands):
        '''Get the scale to apply to MC (eff_data/eff_mc)'''
        eff_data = self.getDataEfficiency(rtrow,triggers,cands)
        eff_mc = self.getMCEfficiency(rtrow,triggers,cands)
        if eff_mc: return eff_data/eff_mc
        return 1.
