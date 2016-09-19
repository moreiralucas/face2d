import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import degrees, pi
import sys
import cv2
import os
# import xmltodict
import itertools

if __name__=='__main__':
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    individuals = []
    X = np.zeros((len(onlyfiles),200*100),dtype=np.float32)
    fli = 0
    for fl in onlyfiles:
        individuals.append(os.path.splitext(fl)[0])
        Img = cv2.imread(join(sys.argv[1], f), 0)
        Reshape_Img = Img.reshape((1,200*100))
        X[fli,:] = Reshape_Img
        fli += 1
    covar,mean = cv2.calcCovarMatrix(X,cv2.COVAR_SCRAMBLED + cv2.COVAR_COLS)
    print covar.shape
    #cv2.eigen(X,)



        #
        # for (eye1, eye2) in pairEyes:
        #     Bak_Img = Img.copy()
        #     center = np.divide((np.array(eye1) + np.array(eye2)), 2)
        #     M = cv2.getRotationMatrix2D((center[0], center[1]), degrees(angle(eye1, eye2)), 1)
        #     dst = cv2.warpAffine(Bak_Img, M, (Bak_Img.shape[1], Bak_Img.shape[0]))
        #     eye1 = np.array(list(eye1) + [0]).reshape((1, 3))
        #     e1p = eye1 * M
        #     eye2 = np.array(list(eye2) + [0]).reshape((1, 3))
        #     e2p = eye2 * M
        #     step = int(np.linalg.norm(e1p - e2p) / 2)
        #     minX, maxX, minY, maxY = int(min(e1p[0, 0], e2p[0, 0])), int(max(e1p[0, 0], e2p[0, 0])), int(
        #         min(e1p[1, 1], e2p[1, 1])), int(max(e1p[1, 1], e2p[1, 1]))
        #     crop = dst[minY - step:maxY + step, minX - step:maxX + step]
        #     cv2.rectangle(Bak_Img, (minX - step, minY - step), (maxX + step, maxY + step), (0, 0, 255), 3)
        #     cv2.imshow('crop', crop)
        #     cv2.waitKey(1)
        #     cv2.imwrite((os.path.splitext(join(sys.argv[3], fl))[0]) + '_' + str(i) + '.jpg', crop)
        #     i += 1

            # for p in eyes:
            #     drawAnchorPoint(Img, p, 10, (0, 255, 0))
            # for p in noses:
            #     drawAnchorPoint(Img, p, 10, (255, 0, 0))
            # for p in mouthes:
            #     drawAnchorPoint(Img, p, 10, (255, 255, 0))

            # cv2.imshow('teste', Img)
            # cv2.imwrite((os.path.splitext(join(sys.argv[3], fl))[0]) + '_' + str(thresh) + '.jpg', Img)
            # cv2.waitKey(500)