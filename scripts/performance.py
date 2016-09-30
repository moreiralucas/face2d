import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import atan2, degrees, pi
import sys
import cv2
import os
#import xmltodict
import itertools

def angle(p1, p2):
    angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    print p1, p2, angle
    return angle

def drawGroundTruthPoint(Img,(x,y),radius):
    cv2.circle(Img,(x,y),radius,(0,0,255))
    cv2.circle(Img,(x,y),1,(255,0,0))
    return Img

def drawAnchorPoint(Img,(x,y),radius,color):
    cv2.line(Img,(x,y-radius/2),(x,y+radius/2),color)
    cv2.line(Img,(x-radius/2,y),(x+radius/2,y),color)
    return Img

if __name__=="__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    for thresh in range(1,76,2):
        EYE_POSITIVE = 0
        EYE_TOTAL = 0
        EYE_IND = 0
        EYE_IND_TOTAL = 0
        NOSE_POSITIVE = 0
        NOSE_TOTAL = 0
        NOSE_IND = 0
        NOSE_IND_TOTAL = 0
        MOUTH_POSITIVE = 0
        MOUTH_TOTAL = 0
        MOUTH_IND = 0
        MOUTH_IND_TOTAL = 0
        EYE_NOSE_OR_MOUTH_IND = 0
        EYE_NOSE_OR_MOUTH_IND_TOTAL = 0
        for fl in onlyfiles:
            with open(join(sys.argv[2], fl)) as ts:
                with open(join(sys.argv[1], fl)) as gt:
                    contentTruth = gt.readlines()
                    split = contentTruth[0].split(' ')
                    gtEyeL = (int(split[0]), int(split[1]))
                    split = contentTruth[1].split(' ')
                    gtEyeR = (int(split[0]), int(split[1]))
                    split = contentTruth[2].split(' ')
                    gtNose = (int(split[0]), int(split[1]))

                    contentTest = ts.readlines()
                    eyes = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('eyes:\n')+1:contentTest.index('noses:\n')]]]
                    noses = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('noses:\n')+1:contentTest.index('mouthes:\n')]]]
                    mouthes = [(int(x),int(y)) for (x,y) in [x.split(' ') for x in contentTest[contentTest.index('mouthes:\n')+1:]]]

                    dEyes = [min(np.linalg.norm(np.array(eye)-np.array(gtEyeL)),np.linalg.norm(np.array(eye)-np.array(gtEyeR))) for eye in eyes]
                    dEyesLeft = [np.linalg.norm(np.array(eye)-np.array(gtEyeL)) for eye in eyes]
                    dEyesRight = [np.linalg.norm(np.array(eye)-np.array(gtEyeR)) for eye in eyes]
                    dNose = [np.linalg.norm(np.array(nose)-np.array(gtNose)) for nose in noses]
                    dMouth = [np.linalg.norm(np.array(nose)-np.array(gtNose)) for nose in mouthes]

                    EYE_POSITIVE += len(filter(lambda dist : dist <= thresh, dEyes))
                    EYE_TOTAL += len(dEyes)
                    EYE_IND += ((len(filter(lambda dist: dist <= thresh, dEyesRight)) == 0 or len(filter(lambda dist : dist <= thresh, dEyesLeft)) == 0) and 1 ) or 0
                    EYE_IND_TOTAL += 1

                    NOSE_POSITIVE += len(filter(lambda dist : dist <= thresh, dNose))
                    NOSE_TOTAL += len(dNose)
                    NOSE_IND += (len(filter(lambda dist : dist <= thresh, dNose)) == 0 and 1 ) or 0
                    NOSE_IND_TOTAL += 1

                    MOUTH_POSITIVE += len(filter(lambda dist : dist <= thresh, dMouth))
                    MOUTH_TOTAL += len(dMouth)
                    MOUTH_IND += (len(filter(lambda dist: dist <= thresh, dMouth)) == 0 and 1 ) or 0
                    MOUTH_IND_TOTAL += 1

                    EYE_NOSE_OR_MOUTH_IND += (len(filter(lambda dist : dist <= thresh, dEyesRight)) == 0 or len(filter(lambda dist : dist <= thresh, dEyesLeft)) == 0 or (len(filter(lambda dist : dist <= thresh, dNose)) == 0 and len(filter(lambda dist : dist <= thresh, dMouth)) == 0) and 1 ) or 0
                    EYE_NOSE_OR_MOUTH_IND_TOTAL += 1
                    Img = cv2.imread(os.path.splitext(join(sys.argv[3], fl))[0]+'.bmp',1)

                    for p in eyes:
                        drawAnchorPoint(Img,p,10,(0,255,0))
                    for p in noses:
                        drawAnchorPoint(Img,p,10,(255,0,0))
                    for p in mouthes:
                        drawAnchorPoint(Img,p,10,(255,255,0))
                    drawGroundTruthPoint(Img,gtEyeL,thresh)
                    drawGroundTruthPoint(Img,gtEyeR,thresh)
                    drawGroundTruthPoint(Img,gtNose,thresh)

                    cv2.imwrite((os.path.splitext(join(sys.argv[4], fl))[0])+'_'+str(thresh)+'.jpg',Img)
                    #cv2.imshow("Teste",Img)
                    #cv2.waitKey(3)
        #print "%d %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % (thresh, 100*(EYE_POSITIVE/float(EYE_TOTAL)), 100*(EYE_IND/float(EYE_IND_TOTAL)), 100*(NOSE_POSITIVE/float(NOSE_TOTAL)), 100*(NOSE_IND/float(NOSE_IND_TOTAL)), 100*(MOUTH_POSITIVE/float(MOUTH_TOTAL)), 100*(MOUTH_IND/float(MOUTH_IND_TOTAL)), 100*(EYE_NOSE_OR_MOUTH_IND/float(EYE_NOSE_OR_MOUTH_IND_TOTAL)))

        #print "(%d,%.2f)" % (thresh, 100*(EYE_POSITIVE/float(EYE_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(NOSE_POSITIVE/float(NOSE_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(MOUTH_POSITIVE/float(MOUTH_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(EYE_IND/float(EYE_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(NOSE_IND/float(NOSE_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(MOUTH_IND/float(MOUTH_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(EYE_NOSE_OR_MOUTH_IND/float(EYE_NOSE_OR_MOUTH_IND_TOTAL))),