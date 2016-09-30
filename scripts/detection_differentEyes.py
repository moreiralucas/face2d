import numpy as np
import cv2
from os import listdir
from os.path import isfile, join, splitext, basename
from math import atan2, degrees, pi
import sys
import xmltodict

def detect(Img):
    eyeL = cv2.CascadeClassifier('cascades/ojoI.xml')
    eyeR = cv2.CascadeClassifier('cascades/ojoD.xml')
    nose = cv2.CascadeClassifier('cascades/Nariz.xml')

    eyesL = eyeL.detectMultiScale(Img, scaleFactor=1.1, minNeighbors=3, minSize=(24,24), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    eyesR = eyeR.detectMultiScale(Img, scaleFactor=1.1, minNeighbors=3, minSize=(24,24), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    noses = nose.detectMultiScale(Img, scaleFactor=1.1, minNeighbors=3, minSize=(24,24), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

    pEyesL = [(int((x+x+w)/2.0),int((y+y+h)/2.0)) for (x,y,w,h) in eyesL]
    pEyesR = [(int((x+x+w)/2.0),int((y+y+h)/2.0)) for (x,y,w,h) in eyesR]
    pNoses = [(int((x+x+w)/2.0),int(y+h)) for (x,y,w,h) in noses]

    return [pEyesL, pEyesR, pNoses];

if __name__=="__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    for fl in onlyfiles:
        Img = cv2.imread(join(sys.argv[1], fl),1)
        if Img!=None:
            [pEyesL, pEyesR, pNoses] = detect(Img)
            print 'Working on',fl,'file'
            with open(join(sys.argv[2], splitext(basename(fl))[0]+'.txt'),'w') as pureout:
                [pureout.write('eyesL:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pEyesL]
                [pureout.write('eyesR:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pEyesR]
                [pureout.write('noses:\n')]
                [pureout.write(str(x)+' '+str(y)+'\n') for (x,y) in pNoses]
