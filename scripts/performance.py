import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import atan2, degrees, pi
import sys
import cv2
import os
#import xmltodict
import itertools
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save
from sklearn.metrics import roc_curve, auc

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return itertools.izip(a, a)

def angle(p1, p2):
    angle = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
    #print p1, p2, angle
    return angle

def drawGroundTruthPoint(Img,(x,y),radius):
    cv2.circle(Img,(x,y),radius,(0,0,255))
    cv2.circle(Img,(x,y),1,(255,0,0))
    return Img

def drawAnchorPoint(Img,(x,y),radius,color):
    cv2.line(Img,(x,y-radius/2),(x,y+radius/2),color)
    cv2.line(Img,(x-radius/2,y),(x+radius/2,y),color)
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
                    summ[i] = np.add(summ[i],eye)
                    count[i] += 1
                    means[i] = summ[i] / count[i]
    p = list(filter(lambda (p1, p2): (-0.25 <= angle(p1, p2) <= 0.25) and np.linalg.norm(np.array(p1)-np.array(p2)) > (thresh*1.5), list(itertools.permutations(means, 2))))
    return p

if __name__=="__main__":
    print "Running"
    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    onlyfiles.sort()
    tpr_eyevalid = np.empty((0, 2))
    fpr_eyevalid = np.empty((0, 2))
    tpr_nose = np.empty((0, 2))
    fpr_nose = np.empty((0, 2))
    tpr_mouth = np.empty((0, 2))
    fpr_mouth = np.empty((0, 2))
    max_thresh = 51
    for thresh in range(max_thresh):
        tpm_eyevalid, fpm_eyevalid, fnm_eyevalid, tnm_eyevalid = 0, 0, 0, 0
        tpm_nose, fpm_nose, fnm_nose, tnm_nose = 0, 0, 0, 0
        tpm_mouth, fpm_mouth, fnm_mouth, tnm_mouth = 0, 0, 0, 0
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
                    neyes = validEyes(eyes,10)

                    dEyes = [min(np.linalg.norm(np.array(eye)-np.array(gtEyeL)),np.linalg.norm(np.array(eye)-np.array(gtEyeR))) for eye in eyes]
                    dEyesLeft = [np.linalg.norm(np.array(eye)-np.array(gtEyeL)) for eye in eyes]
                    dEyesRight = [np.linalg.norm(np.array(eye)-np.array(gtEyeR)) for eye in eyes]
                    dnEyes = np.array([(np.linalg.norm(np.array(eye1) - np.array(gtEyeL)),(np.linalg.norm(np.array(eye2) - np.array(gtEyeR)))) for (eye1,eye2) in neyes])
                    dNose = np.array([np.linalg.norm(np.array(nose)-np.array(gtNose)) for nose in noses])
                    dMouth = np.array([np.linalg.norm(np.array(nose)-np.array(gtNose)) for nose in mouthes])

                    if dnEyes.shape[0] > 0:
                        aux = np.sum(np.all(dnEyes <= thresh, axis=1))
                        (tp_eyevalid, fp_eyevalid) = (aux > 1 and (1, aux - 1)) or (aux == 1 and (1, 0) or (0, 0))
                        aux = np.sum(np.logical_not(np.all(dnEyes <= thresh, axis=1)))
                        (tn_eyevalid, fn_eyevalid) = (aux >= 1 and ((tp_eyevalid == 1 and (aux, 0)) or (aux - 1, 1))) or (0, 0)
                        #print thresh,tp,fp,fn,tn
                    else:
                        tp_eyevalid, fp_eyevalid, tn_eyevalid, fn_eyevalid = 0, 0, 0, 1

                    if dNose.shape[0] > 0:
                        aux = np.sum(np.all(dNose <= thresh))
                        (tp_nose, fp_nose) = (aux > 1 and (1, aux - 1)) or (aux == 1 and (1, 0) or (0, 0))
                        aux = np.sum(np.logical_not(np.all(dNose <= thresh)))
                        (tn_nose, fn_nose) = (aux >= 1 and ((tp_nose == 1 and (aux, 0)) or (aux - 1, 1))) or (0, 0)
                        # print thresh,tp,fp,fn,tn
                    else:
                        tp_nose, fp_nose, tn_nose, fn_nose = 0, 0, 0, 1

                    if dMouth.shape[0] > 0:
                        aux = np.sum(np.all(dMouth <= thresh))
                        (tp_mouth, fp_mouth) = (aux > 1 and (1, aux - 1)) or (aux == 1 and (1, 0) or (0, 0))
                        aux = np.sum(np.logical_not(np.all(dMouth <= thresh)))
                        (tn_mouth, fn_mouth) = (aux >= 1 and ((tp_mouth == 1 and (aux, 0)) or (aux - 1, 1))) or (0, 0)
                        # print thresh,tp,fp,fn,tn
                    else:
                        tp_mouth, fp_mouth, tn_mouth, fn_mouth = 0, 0, 0, 1

                    tpm_eyevalid += tp_eyevalid
                    fpm_eyevalid += fp_eyevalid
                    fnm_eyevalid += fn_eyevalid
                    tnm_eyevalid += tn_eyevalid
                    tpm_nose += tp_nose
                    fpm_nose += fp_nose
                    fnm_nose += fn_nose
                    tnm_nose += tn_nose
                    tpm_mouth += tp_mouth
                    fpm_mouth += fp_mouth
                    fnm_mouth += fn_mouth
                    tnm_mouth += tn_mouth
        #print tpr.shape,fpr.shape
        #print 'tpm\t', 'fpm\t', 'fnm\t', 'tnm\t'
        #print '%d\t%d\t%d\t%d\t%d\t%d\t' % (tpm_nose, fpm_nose, fnm_nose, tnm_nose, float(tpm_nose + fnm_nose), float(fpm_nose + tnm_nose))
        tpr_eyevalid = np.vstack((tpr_eyevalid, np.array((thresh, (tpm_eyevalid / float(tpm_eyevalid + fnm_eyevalid))))))
        fpr_eyevalid = np.vstack((fpr_eyevalid, np.array((thresh, (fpm_eyevalid / float(fpm_eyevalid + tnm_eyevalid))))))
        tpr_nose = np.vstack((tpr_nose, np.array((thresh, (tpm_nose / float(tpm_nose + fnm_nose))))))
        if (tnm_nose > 0):
            fpr_nose = np.vstack((fpr_nose, np.array((thresh, (fpm_nose / float(fpm_nose + tnm_nose))))))

        tpr_mouth = np.vstack((tpr_mouth, np.array((thresh, (tpm_mouth / float(tpm_mouth + fnm_mouth))))))
        if (tnm_mouth > 0):
            fpr_mouth = np.vstack((fpr_mouth, np.array((thresh, (fpm_mouth / float(fpm_mouth + tnm_mouth))))))

    plt.plot(tpr_eyevalid[:, 0], tpr_eyevalid[:, 1], color='g',
             label='TPR\'s eye')
    plt.plot(fpr_eyevalid[:, 0], fpr_eyevalid[:, 1], color='r',
             label='FPR\'s eye')
    # plt.plot(tpr_nose[:, 0], tpr_nose[:, 1], color='g', linestyle='--',
    #          label='TPR\'s nose')
    # plt.plot(fpr_nose[:, 0], fpr_nose[:, 1], color='r', linestyle='--',
    #          label='FPR\'s nose')
    # plt.plot(tpr_mouth[:, 0], tpr_mouth[:, 1], color='g', linestyle='-.',
    #          label='TPR\'s mouth')
    # plt.plot(fpr_mouth[:, 0], fpr_mouth[:, 1], color='r', linestyle='-.',
    #          label='FPR\'s mouth')

    tpr_eyevalid = np.vstack((tpr_eyevalid, np.array((max_thresh, 1.0))))
    fpr_eyevalid = np.vstack((fpr_eyevalid, np.array((max_thresh, 1.0))))
    tpr_nose = np.vstack((tpr_nose, np.array((max_thresh, 1.0))))
    fpr_mouth = np.vstack((fpr_mouth, np.array((max_thresh, 1.0))))
    tpr_mouth = np.vstack((tpr_mouth, np.array((max_thresh, 1.0))))
    fpr_mouth = np.vstack((fpr_mouth, np.array((max_thresh, 1.0))))
    
    plt.xlim([-0.05, max_thresh])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Threshold')
    plt.ylabel('Rate')
    plt.title('TPR and FPR by Thresholds')
    plt.legend(loc="lower right")
    tikz_save('ratedetection.tex')
    plt.show()
    plt.figure()
    mean_auc = auc(fpr_eyevalid[:, 1], tpr_eyevalid[:, 1])
    plt.plot(fpr_eyevalid[:, 1], tpr_eyevalid[:, 1], color='b',
             label='Mean ROC (area = %0.2f)' % mean_auc)
    # mean_auc = auc(fpr_eyevalid[:, 1], tpr_eyevalid[:, 1])
    # plt.plot(fpr_nose[:, 1], tpr_nose[:, 1], color='r',
    #          label='Mean ROC (area = %0.2f)' % mean_auc)
    # mean_auc = auc(fpr_eyevalid[:, 1], tpr_eyevalid[:, 1])
    # plt.plot(fpr_mouth[:, 1], tpr_mouth[:, 1], color='g',
    #          label='Mean ROC (area = %0.2f)' % mean_auc)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    tikz_save('rocdetection.tex')
    plt.show()
    print zip(fpr_eyevalid[:, 1], tpr_eyevalid[:, 1])
        #Img = cv2.imread(os.path.splitext(join(sys.argv[3], fl))[0]+'.bmp',1)
                #for p in eyes:
                #    drawAnchorPoint(Img,p,10,(0,255,0))
                #for p in noses:
                #    drawAnchorPoint(Img,p,10,(255,0,0))
                #for p in mouthes:
                #    drawAnchorPoint(Img,p,10,(255,255,0))
                #drawGroundTruthPoint(Img,gtEyeL,thresh)
                #drawGroundTruthPoint(Img,gtEyeR,thresh)
                #drawGroundTruthPoint(Img,gtNose,thresh)

                #print 'terminou', thresh

                #cv2.imwrite((os.path.splitext(join(sys.argv[4], fl))[0])+'_'+str(thresh)+'.jpg',Img)
                #cv2.imshow("Teste",Img)
                #cv2.waitKey(3)
        #print 'fim'
    #print "%d %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % (thresh, 100*(EYE_POSITIVE/float(EYE_TOTAL)), 100*(EYE_IND/float(EYE_IND_TOTAL)), 100*(NOSE_POSITIVE/float(NOSE_TOTAL)), 100*(NOSE_IND/float(NOSE_IND_TOTAL)), 100*(MOUTH_POSITIVE/float(MOUTH_TOTAL)), 100*(MOUTH_IND/float(MOUTH_IND_TOTAL)), 100*(EYE_NOSE_OR_MOUTH_IND/float(EYE_NOSE_OR_MOUTH_IND_TOTAL)))

        #print "(%d,%.2f)" % (thresh, 100*(EYE_POSITIVE/float(EYE_TOTAL))),

        #print "(%d,%.2f)" % (thresh, 100*(NEYE_POSITIVE/float(NEYE_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(NOSE_POSITIVE/float(NOSE_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(MOUTH_POSITIVE/float(MOUTH_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(EYE_IND/float(EYE_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(NOSE_IND/float(NOSE_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(MOUTH_IND/float(MOUTH_IND_TOTAL))),
        #print "(%d,%.2f)" % (thresh, 100*(EYE_NOSE_OR_MOUTH_IND/float(EYE_NOSE_OR_MOUTH_IND_TOTAL))),