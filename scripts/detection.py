import numpy as np
import cv2
from os import listdir
from os.path import isfile, join, splitext, basename
from math import atan2, degrees, pi
import sys
import itertools

def angle(p1, p2):
    angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    print p1, p2, angle
    return angle

def detectEyes(Img):
    eyeC = cv2.CascadeClassifier('cascades/eye.xml')
    eyes = eyeC.detectMultiScale(Img, scaleFactor=1.05, minNeighbors=5, minSize=(24,24), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    pEyes = [(int((x+x+w)/2.0),int((y+y+h)/2.0)) for (x,y,w,h) in eyes]
    return pEyes

def detectNoses(Img):
    noseC = cv2.CascadeClassifier('cascades/Nariz.xml')
    noses = noseC.detectMultiScale(Img, scaleFactor=1.05, minNeighbors=5, minSize=(24,24), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    pNoses = [(int((x+x+w)/2.0),int(y+h)) for (x,y,w,h) in noses]
    return pNoses

def detectMouthes(Img):
    mouthC = cv2.CascadeClassifier('cascades/Mouth.xml')
    mouthes = mouthC.detectMultiScale(Img, scaleFactor=1.05, minNeighbors=5, minSize=(24, 24),
                                   flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    pMouthes = [(int((x + x + w) / 2.0), int(y)) for (x, y, w, h) in mouthes]
    return pMouthes


if __name__=="__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    for fl in onlyfiles:
        print fl
        Img = cv2.imread(join(sys.argv[1], fl),1)
        #equalized = np.zeros(Img.shape,dtype=np.uint8)
        if Img!=None:

            pEyes = detectEyes(Img)
            pNoses = detectNoses(Img)
            pMouthes = detectMouthes(Img)

            print 'Working on',fl,'file'
            with open(join(sys.argv[2], splitext(basename(fl))[0]+'.txt'),'w') as pureout:
                [pureout.write('eyes:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pEyes]

            with open(join(sys.argv[2], splitext(basename(fl))[0]+'.txt'),'a') as pureout:
                [pureout.write('noses:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pNoses]

            with open(join(sys.argv[2], splitext(basename(fl))[0]+'.txt'),'a') as pureout:
                [pureout.write('mouthes:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pMouthes]
