import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import degrees, pi
import sys
import cv2
import os
# import xmltodict
import itertools


def angle(p1, p2):
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    # print p1, p2, angle
    return angle


def drawGroundTruthPoint(Img, (x, y), radius):
    cv2.circle(Img, (x, y), radius, (0, 0, 255))
    cv2.circle(Img, (x, y), 1, (255, 0, 0))
    return Img


def drawAnchorPoint(Img, (x, y), radius, color):
    cv2.line(Img, (x, y - radius / 2), (x, y + radius / 2), color)
    cv2.line(Img, (x - radius / 2, y), (x + radius / 2, y), color)
    return Img


def validEyes(eyes, thresh):
    means = []
    summ = []
    count = []
    for eye in eyes:
        ct = filter(lambda (x, y): np.linalg.norm(np.array((x, y)) - np.array(eye)) <= thresh, means)
        if len(means) == 0 or len(ct) == 0:
            means.append(eye)
            summ.append(eye)
            count.append(1)
        else:
            for i in range(0, len(means)):
                if np.linalg.norm(np.array(means[i]) - np.array(eye)) <= thresh:
                    summ[i] += eye
                    count[i] += 1
                    means[i] = np.array(summ[i]) / count[i]
    p = list(filter(lambda (p1, p2): (-0.25 <= angle(p1, p2) <= 0.25) and np.linalg.norm(np.array(p1)-np.array(p2)) > (thresh*1.5), list(itertools.permutations(means, 2))))
    return p

def normalizeLight(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    img = cv2.cvtColor(limg,cv2.COLOR_LAB2BGR)
    return img


if __name__ == "__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    thresh = 15
    for fl in onlyfiles:
        with open(join(sys.argv[1], fl)) as ts:
            contentTest = ts.readlines()
            try:
                eyes = [(int(x), int(y)) for (x, y) in [x.split(' ') for x in contentTest[contentTest.index(
                    'eyes:\n') + 1:contentTest.index('noses:\n')]]]
                noses = [(int(x), int(y)) for (x, y) in [x.split(' ') for x in contentTest[contentTest.index(
                    'noses:\n') + 1:contentTest.index('mouthes:\n')]]]
                mouthes = [(int(x), int(y)) for (x, y) in
                           [x.split(' ') for x in contentTest[contentTest.index('mouthes:\n') + 1:]]]

                pairEyes = validEyes(eyes, 10)

                Img = cv2.imread(os.path.splitext(join(sys.argv[2], fl))[0] + '.bmp', 1)
                Img = normalizeLight(Img)
                i=1
                for (eye1, eye2) in pairEyes:
                    Bak_Img = Img.copy()
                    center = np.divide((np.array(eye1)+np.array(eye2)),2)
                    M = cv2.getRotationMatrix2D((center[0],center[1]), degrees(angle(eye1,eye2)), 1)
                    dst = cv2.warpAffine(Bak_Img, M, (Bak_Img.shape[1],Bak_Img.shape[0]))
                    eye1 = np.array(list(eye1)+[0]).reshape((1, 3))
                    e1p = eye1 * M
                    eye2 = np.array(list(eye2)+[0]).reshape((1, 3))
                    e2p = eye2 * M
                    step = int(np.linalg.norm(e1p-e2p)/2)
                    minX,maxX,minY,maxY = int(min(e1p[0, 0], e2p[0, 0])), int(max(e1p[0,0],e2p[0,0])), int(min(e1p[1, 1], e2p[1, 1])), int(max(e1p[1,1],e2p[1,1]))
                    crop = dst[minY-step:maxY+step,minX-step:maxX+step]
                    cv2.rectangle(Bak_Img,(minX-step,minY-step),(maxX+step,maxY+step),(0,0,255),3)
                    cv2.imshow('crop',crop)
                    cv2.waitKey(1)

                    cv2.imwrite((os.path.splitext(join(sys.argv[3], fl))[0]) + '_' + str(i) + '.jpg', crop)
                    i += 1
            except ValueError:
                print '*'

    onlyfiles = [f for f in listdir(sys.argv[3]) if isfile(join(sys.argv[3], f))]
    onlyfiles.sort()
    for fl in onlyfiles:
        cmd = 'convert '+join(sys.argv[3], fl)+' -resize 100x50! '+join(sys.argv[4], fl)
        print cmd
        os.system(cmd)


            # for p in eyes:
            #     drawAnchorPoint(Img, p, 10, (0, 255, 0))
            # for p in noses:
            #     drawAnchorPoint(Img, p, 10, (255, 0, 0))
            # for p in mouthes:
            #     drawAnchorPoint(Img, p, 10, (255, 255, 0))

            #cv2.imshow('teste', Img)
            # cv2.imwrite((os.path.splitext(join(sys.argv[3], fl))[0]) + '_' + str(thresh) + '.jpg', Img)
            #cv2.waitKey(500)