# MultiProgress.py
import signal
import sys
import time
import logging
import logging.handlers
import math
from multiprocessing import Pool, current_process, Process, Queue
from blessings import Terminal
from progressbar import ProgressBar, Bar, ETA, Percentage, SimpleProgress

term = Terminal()

class Writer(object):
    '''
    A writer object that prints strings to a line of a terminal.
    '''
    def __init__(self,location):
        self.location = location

    def write(self,string):
        with term.location(*self.location):
            print(string)

def func_wrapper(jobnum, name, func, func_args, func_kwargs):
    proc_num = current_process()._identity
    location = (0,proc_num[0]-1)
    writer = Writer(location)
    width = int(math.floor(term.width/3))
    writer.write('{0:3} {1}: Queued'.format(proc_num[0],name[:width]+' '*max(0,width-len(name))))
    pbar = ProgressBar(widgets=['{0:3} {1}: '.format(proc_num[0],name[:width]+' '*max(0,width-len(name))),' ',SimpleProgress(),' ',Percentage(),' ',Bar(),' ',ETA()],fd=writer,term_width=term.width)
    return func(*func_args,progressbar=pbar,**func_kwargs)


class MultiProgress(object):
    '''
    A class to print multiple progress bars from a pool.
    '''
    def __init__(self,numCores,**kwargs):
        self.numCores = numCores
        self.orig_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.pool = Pool(self.numCores)
        signal.signal(signal.SIGINT, self.orig_sigint_handler)
        self.total = 0
        self.results = []
        print term.enter_fullscreen

    def addJob(self,name,func,args=[],kwargs={}):
        '''
        Add a job to the parallel running.
            name  : name of job
            func  : function to map in pool
            args  : arguments for function
            kwargs: kwargs for function
        '''
        self.total += 1
        jobnum = self.total
        self.results += [self.pool.apply_async(func_wrapper,args=(jobnum,name,func,args,kwargs))]

    def jobsRemaining(self):
        numleft = [r.ready() for r in self.results].count(False)
        return numleft

    def retrieve(self):
        '''
        Execute the jobs
        '''
        numleft = self.total
        writer = Writer((0,self.numCores))
        width = int(math.floor(term.width/3))
        name = 'Total'
        writer.write('{0:3} {1}: Queued'.format('',name[:width]+' '*max(0,width-len(name))))
        pbar = ProgressBar(widgets=['{0:3} {1}: '.format('',name[:width]+' '*max(0,width-len(name))),' ',SimpleProgress(),' ',Percentage(),' ',Bar(),' ',ETA()],fd=writer,term_width=term.width, maxval=self.total).start()
        try:
            while True:
               numleft_new = self.jobsRemaining()
               if numleft_new < numleft:
                   pbar.update(self.total-numleft_new)
               numleft = numleft_new
               if numleft==0: break
               time.sleep(0.1)
            theResult = [r.get(9999999999) for r in self.results]
        except:
            e = sys.exc_info()[0]
            self.pool.terminate()
            print term.exit_fullscreen
            print e
            theResult = []
        else:
            print term.exit_fullscreen
            self.pool.close()
        self.pool.join()
        return theResult
