import os
import sys
import logging

import ROOT

class Limits(object):
    '''
    Limits

    A class to encapsulate an analysis selection and produce 
    a datacard that can be read by the Higgs Combine tool.
    '''

    def __init__(self):
        self.eras = []        # 7, 8, 13 TeV
        self.analyses = []    # analysis name
        self.channels = []    # analysis channel
        self.observed = {}    # there is one observable per era/analysis/channel combination
        self.processes = {}   # background and signal processes
        self.signals = []
        self.backgrounds = []
        self.expected = {}    # expected yield, one per process/era/analysis/chanel combination
        self.masses = []      # masses
        self.systematics = {} # systematic uncertainties

    def __check(self,test,stored,name='Object'):
        goodToAdd = True
        if 'all' in test: return goodToAdd
        for t in test:
            if t not in stored:
                logging.warning('{0} {1} not recognized.'.format(name,t))
                goodToAdd = False
        return goodToAdd

    def __checkEras(self,eras):
        return self.__check(eras,self.eras,name='Era')

    def __checkAnalyses(self,analyses):
        return self.__check(analyses,self.analyses,name='Analysis')

    def __checkChannels(self,channels):
        return self.__check(channels,self.channels,name='Channel')

    def __checkProcesses(self,processes):
        return self.__check(processes,self.processes,name='Process')

    def addEra(self,era):
        '''Add era to analysis (i.e., 7TeV, 8TeV, 13TeV).'''
        if era in self.eras:
            logging.warning('Era {0} already added.'.format(era))
        else:
            self.eras += [era]

    def addAnalysis(self,analysis):
        '''Add analysis.'''
        if analysis in self.analyses:
            logging.warning('Analysis {0} already added.'.format(analysis))
        else:
            self.analyses += [analysis]

    def addChannel(self,channel):
        '''Add channel to analysis.'''
        if channel in self.channels:
            logging.warning('Channel {0} already added.'.format(channel))
        else:
            self.channels += [channel]

    def addProcess(self,proc,signal=False):
        '''
        Add a process to the datacard.
            parameters:
                signal   - bool            - Declares process to be a signal, default False
        '''
        if proc in self.processes:
            logging.warning('Process {0} already added.'.format(proc))
        else:
            self.processes[proc] = {
                'signal'  : signal,
            }
            if signal:
                self.signals += [proc]
            else:
                self.backgrounds += [proc]

    def addSystematic(self,systname,mode,systematics={}):
        '''
        Add a systematic uncertainty. The name can include the following string
        formatting replacements to set uncorrelated:
            {process}  : uncorrelate process
            {era}      : uncorrelate era
            {analysis} : uncorrelate analysis
            {channel}  : uncorrelate channel
        The supported modes are:
            'lnN' : log normal uncertainty shape
        The values are set with the 'systematics' arguments. They are dictionaries with the form:
            systematics = {
               (processes,eras,analyses,channels) : value,
            }
        where the key is a tuple of process, era, analysis, and channel the systematic covers, each
        of which is another tuple of the components this sytematic covers.
        '''
        if systname in self.systematics:
            logging.warning('Systematic {0} already added.'.format(syst))
        else:
            goodToAdd = True
            for syst in systematics:
                processes,eras,analyses,channels = syst
                goodToAdd = goodToAdd and self.__checkProcesses(processes)
                goodToAdd = goodToAdd and self.__checkEras(eras)
                goodToAdd = goodToAdd and self.__checkAnalyses(analyses)
                goodToAdd = goodToAdd and self.__checkChannels(channels)
            if goodToAdd:
                self.systematics[systname] = {
                    'mode'  : mode,
                    'values': systematics,
                }

    def getSystematic(self,systname,process,era,analysis,channel):
        '''Return the systematic value for a given systematic/process/era/analysis/channel combination.'''
        # make sure it exists:
        for syst in self.systematics:
            fullSystName = syst.format(process=process,era=era,analysis=analysis,channel=channel)
            if fullSystName != systname: continue
            # check if there is a systematic value for this combination
            for syst_vals in self.systematics[syst]['values']:
                s_processes, s_eras, s_analyses, s_channels = syst_vals
                if process not in s_processes and 'all' not in s_processes: continue
                if era not in s_eras and 'all' not in s_eras: continue
                if analysis not in s_analyses and 'all' not in s_analyses: continue
                if channel not in s_channels and 'all' not in s_channels: continue
                # return the value
                return self.systematics[syst]['values'][syst_vals]
        return 1.

    def __getSystematicRows(self,syst,processes,era,analysis,channel):
        '''
        Return a dictionary of the systematic values of the form:
            systs = {
                systname : {
                    'mode' : 'lnN',
                    'systs': {
                        (era,analysis,channel,'proc_1'): 1.,
                        ...
                    },
                },
            }
        '''
        systs = {}
        for process in processes:
            systname = syst.format(process=process,era=era,analysis=analysis,channel=channel)
            if systname not in systs:
                systs[systname] = {
                    'mode' : self.systematics[syst]['mode'], 
                    'systs': {},
                }
            systs[systname]['systs'][(era,analysis,channel,process)] = self.getSystematic(systname,process,era,analysis,channel)
        return systs

    def __combineSystematics(self,*systs):
        '''Combine systematics of the form output by __getSystematicRows.'''
        combinedSyst = {}
        for syst in systs:
            for systname in syst:
                if systname not in combinedSyst:
                    combinedSyst[systname] = {
                        'mode' : syst[systname]['mode'],
                        'systs': {},
                    }
                combinedSyst[systname]['systs'].update(syst[systname]['systs'])
        return combinedSyst

    def setObserved(self,era,analysis,channel,value):
        '''Set the observed value for a given era,analysis,channel.'''
        goodToAdd = True
        goodToAdd = goodToAdd and self.__checkEras([era])
        goodToAdd = goodToAdd and self.__checkAnalyses([analysis])
        goodToAdd = goodToAdd and self.__checkChannels([channel])
        if goodToAdd:
            self.observed[(era,analysis,channel)] = value

    def getObserved(self,era,analysis,channel,blind=True):
        '''Get the observed value. If blinded returns the sum of the expected background.'''
        if blind:
            return sum([self.getExpected(process,era,analysis,channel) for process in self.backgrounds])
        else:
            key = (era,analysis,channel)
            return self.observed[key] if key in self.observed else 0.

    def setExpected(self,process,era,analysis,channel,value):
        '''Set the expected value for a given process,era,analysis,channel.'''
        goodToAdd = True
        goodToAdd = goodToAdd and self.__checkProcesses([process])
        goodToAdd = goodToAdd and self.__checkEras([era])
        goodToAdd = goodToAdd and self.__checkAnalyses([analysis])
        goodToAdd = goodToAdd and self.__checkChannels([channel])
        if goodToAdd:
            self.expected[(process,era,analysis,channel)] = value

    def getExpected(self,process,era,analysis,channel):
        '''Get the expected value.'''
        key = (process,era,analysis,channel)
        val = self.expected[key] if key in self.expected else 0.
        return val if val else 1.0e-10

    def printCard(self,filename,eras=['all'],analyses=['all'],channels=['all'],blind=True):
        '''
        Print a datacard to file.
        Select the eras, analyses, channels you want to include.
        Each will correspond to one bin in the datacard.
        '''
        goodToPrint = True
        goodToPrint = goodToPrint and self.__checkEras(eras)
        goodToPrint = goodToPrint and self.__checkAnalyses(analyses)
        goodToPrint = goodToPrint and self.__checkChannels(channels)
        if not goodToPrint: return

        if eras==['all']: eras = self.eras
        if analyses==['all']: analyses = self.analyses
        if channels==['all']: channels = self.channels
        processes = self.processes.keys()


        # setup bins
        bins = ['bin']
        observations = ['observation']
        binName = '{era}_{analysis}_{channel}'
        for era in eras:
            for analysis in analyses:
                for channel in channels:
                    bins += [binName.format(era=era,analysis=analysis,channel=channel)]
                    observations += ['{0}'.format(self.getObserved(era,analysis,channel,blind=blind))]
        imax = len(bins)-1

        # setup processes
        jmax = len(self.processes)-1

        totalColumns = len(eras)*len(analyses)*len(channels)*len(processes)
        processesOrdered = self.signals + self.backgrounds
        binsForRates = ['bin','']+['']*totalColumns
        processNames = ['process','']+['']*totalColumns
        processNumbers = ['process','']+['']*totalColumns
        rates = ['rate','']+['']*totalColumns
        colpos = 1
        for era in eras:
            for analysis in analyses:
                for channel in channels:
                    for process in processesOrdered:
                        colpos += 1
                        binsForRates[colpos] = '{era}_{analysis}_{channel}'.format(era=era,analysis=analysis,channel=channel)
                        processNames[colpos] = process
                        processNumbers[colpos] = '{0:<10}'.format(processesOrdered.index(process)-len(self.signals)+1)
                        rates[colpos] = '{0:<10.4g}'.format(self.getExpected(process,era,analysis,channel))

        # setup nuissances
        systs = {}
        keys = []
        for era in eras:
            for analysis in analyses:
                for channel in channels:
                    key = (era,analysis,channel)
                    keys += [key]
                    systs[key] = {}
                    for syst in self.systematics:
                        systs[key].update(self.__getSystematicRows(syst,processes,era,analysis,channel))

        combinedSysts = self.__combineSystematics(*[systs[key] for key in systs])
        systRows = []
        for syst in sorted(combinedSysts.keys()):
            thisRow = [syst,combinedSysts[syst]['mode']]
            for era in eras:
                for analysis in analyses:
                    for channel in channels:
                        for process in processesOrdered:
                            key = (era,analysis,channel,process)
                            thisRow += ['{0:<10.4g}'.format(combinedSysts[syst]['systs'][key]) if key in combinedSysts[syst]['systs'] else '-']
            systRows += [thisRow]

        kmax = len(systRows)

        # now write to file
        with open(filename,'w') as f:
            lineWidth = 80
            firstWidth = 30
            restWidth = 20
            def getline(row):
                return '{0} {1}\n'.format(row[0][:firstWidth]+' '*max(0,firstWidth-len(row[0])), ''.join([r[:restWidth]+' '*max(0,restWidth-len(r)) for r in row[1:]]))

            # header
            f.write('imax {0} number of bins\n'.format(imax))
            f.write('jmax {0} number of processes\n'.format(jmax))
            f.write('kmax * number of nuissances\n')
            f.write('-'*lineWidth+'\n')

            # shape information
            
            # observation
            f.write(getline(bins))
            f.write(getline(observations))
            f.write('-'*lineWidth+'\n')

            # process definition
            f.write(getline(binsForRates))
            f.write(getline(processNames))
            f.write(getline(processNumbers))
            f.write(getline(rates))
            f.write('-'*lineWidth+'\n')

            # nuissances
            for systRow in systRows:
                f.write(getline(systRow))
            f.write('-'*lineWidth+'\n')



