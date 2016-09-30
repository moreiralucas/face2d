import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import atan2, degrees, pi
import sys
import xmltodict

if __name__=="__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()

    for fl in onlyfiles:
        with open(join(sys.argv[1], fl)) as ts:
            with open(join(sys.argv[2], fl)) as gt:
                contentTruth = gt.readlines()
                split = contentTruth[0].split(' ')
                gtEyeL = (int(split[0]), int(split[1]))
                split = contentTruth[1].split(' ')
                gtEyeR = (int(split[0]), int(split[1]))
                split = contentTruth[2].split(' ')
                gtNose = (int(split[0]), int(split[1]))

                print gtEyeL

                contentTest = ts.readlines()
                eyesL = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('eyesL:\n')+1:contentTest.index('eyesR:\n')]]]
                eyesR = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('eyesL:\n')+1:contentTest.index('eyesR:\n')]]]
                noses = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('eyesL:\n')+1:contentTest.index('eyesR:\n')]]]

                dEyesL = [np.linalg.norm(np.array(eyeL)-np.array(gtEyeL)) for eyeL in eyesL]
                dEyesR = [np.linalg.norm(np.array(eyeR)-np.array(gtEyeR)) for eyeR in eyesR]
                dNose = [np.linalg.norm(np.array(nose)-np.array(gtNose)) for nose in noses]

                print dEyesL
                raw_input('digite algo\n')
