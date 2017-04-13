import os
import sys
from multiprocessing import Pool

from DevTools.MVATrainer.Hpp4lTrainer import Hpp4lTrainer



def train(mass,nTaus):
    trainer = Hpp4lTrainer(
        mass=mass,
        nTaus=nTaus,
        outputFileName='mvaTraining.{0}GeV.{1}Taus.root'.format(mass,nTaus),
        jobName='training.{0}GeV.{1}Taus'.format(mass,nTaus),
    )
    trainer.train()
    

train(500,0)

#pool = Pool(16)
#masses = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
#
#try:
#    pool.map_async(train, masses).get(999999)
#except KeyboardInterrupt:
#    pool.terminate()
#    print 'training cancelled'
#    sys.exit(1)
