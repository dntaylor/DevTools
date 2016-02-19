# CutTree.py
# Hold the pass fail decision of events
import logging
import ROOT
from array import array

class CutTree(object):
    '''
    Stores pass-fail decisions of events
    '''
    def __init__(self):
        self.labels = []
        self.selections = {}
        self.results = {}
        self.tree = ROOT.TTree("CutTree","CutTree")
        self.results['run'] = array('i',[0])
        self.results['lumi'] = array('i',[0])
        self.results['event'] = array('L',[0])
        self.tree.Branch('run',self.results['run'],'run/I')
        self.tree.Branch('lumi',self.results['lumi'],'lumi/I')
        self.tree.Branch('event',self.results['event'],'event/l')
        self.filled = set()

    def add(self, fun, label):
        if label not in self.results:
            self.labels += [label]
            self.selections[label] = fun
            self.results[label] = array('i',[0])
            self.tree.Branch(label,self.results[label],'{0}/I'.format(label))
        else:
            logging.warning("{0} already in CutTree.".format(label))

    def getLabels(self):
        return self.labels

    def evaluate(self,rtrow,cands):
        eventkey = '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
        if eventkey in self.filled:
            logging.warning("Event {0} already filled.".format(eventkey))
            return False
        else:
            self.results['run'][0] = int(rtrow.run)
            self.results['lumi'][0] = int(rtrow.lumi)
            self.results['event'][0] = long(rtrow.event)
            passAll = True
            # verify each cut
            for label in self.selections:
                cut = self.selections[label]
                self.results[label][0] = int(cut(rtrow,cands))
                if not self.results[label][0]: passAll = False
            self.tree.Fill()
            self.filled.add(eventkey)
            # verify we have a candidate
            if passAll:
                for cname,cand in cands.iteritems():
                    if not cand:
                        passAll = False
            return passAll

    def getResults(self):
        return self.results
