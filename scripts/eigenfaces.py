import numpy as np
from os import listdir
from os.path import isfile, join, splitext, basename
from math import degrees, pi
import sys
import cv2
import os
# import xmltodict
import itertools
from skimage import feature
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.cross_validation import *

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def match(trainX,trainY,testX):
    distances = []
    for x in trainX:
        distances.append(cv2.compareHist(x, testX, cv2.cv.CV_COMP_CHISQR))
    sorted = np.argsort(distances)
    return trainY[sorted]

def lbp(numPoints, radius, image, eps=1e-7):
    lbp = feature.local_binary_pattern(image, numPoints,
                                       radius, method="uniform")
    (hist, _) = np.histogram(lbp.ravel(),  bins=np.arange(0, numPoints + 3), range=(0, numPoints + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + eps)
    return hist

def loadDataset(path,descriptor,args):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles.sort()
    individuals = []
    X = np.zeros((len(onlyfiles), 26), dtype=np.float32)
    fli = 0
    for fl in onlyfiles:
        individuals.append(int(os.path.splitext(fl)[0].split('_')[0]))
        Img = cv2.imread(join(sys.argv[1], fl), 0)
        desc = descriptor(*(args+[Img]))
        X[fli, :] = desc
        fli += 1
    return [X,np.array(individuals)]

if __name__=='__main__':
    print 'Loading Dataset...'
    X,Y = loadDataset(sys.argv[1],lbp,[24,8])
    # X_train = X[3:,:]
    # y_train = Y[3:]
    # X_test = X[:3]
    # y_test = Y[:3]
    labels = np.ones(Y.shape)*-1
    indexs = filter(lambda indexs : indexs.shape[0]  > 1, [np.where(Y == label)[0] for label in np.unique(Y)])
    cycle = itertools.cycle(range(0,min([i.shape[0] for i in indexs])))
    for x in indexs:
        cycle_bak = cycle
        labels[x] = [next(cycle_bak) for y in x]
    #print labels
    skf = PredefinedSplit(labels)
    for n_faces in range(1,51):
        accs = []
        for train_index, test_index in skf:
             X_train, X_test = X[train_index], X[test_index]
             y_train, y_test = Y[train_index], Y[test_index]
             acerto = 0
             erro = 0
             for t_idx in range(len(y_test)):
                 predicted = match(X_train,y_train,X_test[t_idx])
                 #print predicted[:3]
                 predicted_bak = predicted
                 _,sort = np.unique(predicted_bak.copy(), return_index=True)

                 predicted = predicted[np.sort(sort)]
                 #print sort

                 #raw_input('ok')
                 if np.any(predicted[:n_faces] == y_test[t_idx]):
                     acerto += 1
                 else:
                     erro += 1
             acc = acerto / float(acerto + erro)
             #print acerto, erro, acc
             accs.append(acc)
        #print accs
        accuracy = np.mean(np.array(accs))
        print (n_faces,accuracy),

    #plt.figure()
    #for train_index, test_index in skf:
    #     X_train, X_test = X[train_index], X[test_index]
    #     y_train, y_test = Y[train_index], Y[test_index]
    #     print X_train.shape, y_train.shape
    #
    #     classifier = SVMLearning(X=X_train, Y=y_train)
    #     predicted = classifier.guess(X_test)
    #     cm = confusion_matrix(y_test, predicted)
    #     np.set_printoptions(precision=2)
    #     print('Confusion matrix, without normalization')
    #     print(cm)
    #     #plot_confusion_matrix(cm)
    #     #plt.show()


    #print eigenValues.shape, eigenVectors.shape

    #cv2.eigen(X,)
