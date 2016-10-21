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
from sklearn.metrics import roc_curve, auc
from scipy import interp
from matplotlib2tikz import save as tikz_save
from sklearn.model_selection import PredefinedSplit


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

def calcDistances(trainX,testX):
    distances = []
    for x in trainX:
        distances.append(cv2.compareHist(x, testX, cv2.cv.CV_COMP_CHISQR))
    return distances

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

def loadDatasetNonSplit(path,descriptor,args):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles.sort()
    individuals = []
    X = np.zeros((len(onlyfiles), 26), dtype=np.float32)
    fli = 0
    for fl in onlyfiles:
        individuals.append(os.path.splitext(fl)[0])
        Img = cv2.imread(join(sys.argv[1], fl), 0)
        desc = descriptor(*(args+[Img]))
        X[fli, :] = desc
        fli += 1
    return [X,np.array(individuals)]

def statsByNFace(X,Y):
    skf = StratifiedKFold(y, n_folds=3)
    stats = []
    for n_faces in range(0, 51):
        accs = []
        for train_index, test_index in skf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = Y[train_index], Y[test_index]
            acerto = 0
            erro = 0
            for t_idx in range(len(y_test)):
                predicted = match(X_train, y_train, X_test[t_idx])
                # print predicted[:3]
                predicted_bak = predicted
                _, sort = np.unique(predicted_bak.copy(), return_index=True)

                predicted = predicted[np.sort(sort)]
                # print sort

                # raw_input('ok')
                if np.any(predicted[:n_faces] == y_test[t_idx]):
                    acerto += 1
                else:
                    erro += 1
            acc = acerto / float(acerto + erro)
            # print acerto, erro, acc
            accs.append(acc)
        # print accs
        accuracy = np.mean(np.array(accs))
        print (n_faces, accuracy),
        stats.append((n_faces,accuracy))
    points = np.array(stats)
    plt.plot(points[:,0], points[:,1], color='b',
             )
    plt.xlim([-0.05, 50.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Threshold')
    plt.ylabel('Accuracy')
    plt.title('Rank Top N')
    plt.legend(loc="lower right")
    tikz_save('ranktopn.tex')
    plt.show()

def ROCAllClasses(X,y):
    print 'Testing faces'
    # Run classifier with cross-validation and plot ROC curves
    cv = StratifiedKFold(y, n_folds=3)
    #cv = KFold(y.shape[0])
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)

    colors = itertools.cycle(['cyan', 'indigo', 'seagreen', 'yellow', 'blue', 'darkorange'])
    lw = 2

    count = 0
    y_labels = None
    y_probas = None
    for (train, test), color in zip(cv, colors):
        # for (train, test), color in zip(cv.split(X), colors):
        # for train, test in cv:
        y_scores = np.zeros((y[test].shape[0], np.unique(y).shape[0]))
        for t_idx in range(len(X[test])):
            predicted = calcDistances(X[train], X[test][t_idx])
            pred_scores = np.array(zip(predicted, y[train]))
            distances = np.array([np.min(pred_scores[pred_scores[:, 1] == i], axis=0) for i in range(1, np.unique(y).shape[0] + 1)])
            y_scores[t_idx,:] = (1/distances[:,0])/np.sum(1/distances[:,0])
            #y_scores[t_idx, :] = distances[:, 0]
            # _, sort = np.unique(predicted.copy(), return_index=True)
            # predicted = predicted[np.sort(sort)]
        y_labels = np.array(
            [map(lambda bl: bl == True and 1 or -1, y[test] == x) for x in range(1, np.unique(y).shape[0] + 1)]).ravel()
        y_probas = y_scores.transpose().ravel()
        # y_labels = np.array(map(lambda bl: bl == True and 1 or -1, y[test] == 1))
        # y_probas = y_scores[:,1]
        # raw_input('parou\n')
        fpr, tpr, thresholds = roc_curve(y_labels, y_probas)
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=lw, color=color,
                 label='ROC fold %d (area = %0.2f)' % (count, roc_auc))
        count += 1
    plt.plot([0, 1], [0, 1], linestyle='--', lw=lw, color='k',
             label='Luck')

    mean_tpr /= count
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, color='g', linestyle='--',
             label='Mean ROC (area = %0.2f)' % mean_auc, lw=lw)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    tikz_save('rocall.tex')
    plt.show()

def ROC(X,y):
    print 'Testing faces'
    # Run classifier with cross-validation and plot ROC curves
    cv = StratifiedKFold(y, n_folds=3)
    #cv = KFold(y.shape[0])
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)

    colors = itertools.cycle(['cyan', 'indigo', 'seagreen', 'yellow', 'blue', 'darkorange'])
    lw = 2

    count = 0
    y_labels = None
    y_probas = None
    for (train, test), color in zip(cv, colors):
        plt.figure()
        count = 0
        y_scores = np.zeros((y[test].shape[0], np.unique(y).shape[0]))
        for t_idx in range(len(X[test])):
            predicted = calcDistances(X[train], X[test][t_idx])
            pred_scores = np.array(zip(predicted, y[train]))
            distances = np.array([np.min(pred_scores[pred_scores[:, 1] == i], axis=0) for i in range(1, np.unique(y).shape[0] + 1)])
            y_scores[t_idx,:] = (1/distances[:,0])/np.sum(1/distances[:,0])
            for x in range(1, np.unique(y).shape[0] + 1):
                y_labels = map(lambda bl: bl == True and 1 or -1, y[test] == x)
                fpr, tpr, thresholds = roc_curve(y_labels, y_scores[:, x-1])
                mean_tpr += interp(mean_fpr, fpr, tpr)
                mean_tpr[0] = 0.0
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, lw=lw, color=color,
                         label='ROC fold %d (area = %0.2f)' % (count, roc_auc))
                count += 1
        plt.plot([0, 1], [0, 1], linestyle='--', lw=lw, color='k',
                 label='Luck')

        mean_tpr /= count
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        plt.plot(mean_fpr, mean_tpr, color='g', linestyle='--',
                 label='Mean ROC (area = %0.2f)' % mean_auc, lw=lw)

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.show()

def matchWithValidation(X,Y):
    labels = np.ones(Y.shape) * -1
    indexs = filter(lambda indexs: indexs.shape[0] > 1, [np.where(Y == label)[0] for label in np.unique(Y)])
    cycle = itertools.cycle(range(0, min([i.shape[0] for i in indexs])))
    for x in indexs:
        cycle_bak = cycle
        labels[x] = [next(cycle_bak) for y in x]
    # print labels
    skf = PredefinedSplit(labels)
    preds = []
    reals = []
    for train_index, test_index in skf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]
        pred = []
        real = []
        for t_idx in range(len(y_test)):
            predicted = match(X_train, y_train, X_test[t_idx])
            # print predicted[:3]
            predicted_bak = predicted
            _, sort = np.unique(predicted_bak.copy(), return_index=True)
            predicted = predicted[np.sort(sort)]
            pred.append(predicted[0])
            real.append(y_test[t_idx])
        preds.append(pred)
        reals.append(real)
    return np.array(preds),np.array(reals)

def generateStats(X,y):

    y_individuals = map(lambda yi: int(yi.split('_')[0]), y)
    idx = np.argsort(y_individuals)
    X,y = X[idx],y[idx]

    for i in range(len(y)):
        idx_train = range(0, i)+range(i+1,len(y))
        X_train,y_train = X[idx_train],y[idx_train]
        X_test,y_test = X[i],y[i]
        predicted = calcDistances(X_train, X_test)
        y_train_individuals = map(lambda y: int(y.split('_')[0]), y_train)
        pred_scores = np.array(zip(predicted, y_train_individuals))
        distances = np.array(
            [np.min(pred_scores[pred_scores[:, 1] == i], axis=0) for i in range(
                1, np.unique(y_individuals).shape[0] + 1)])
        y_scores = (1 / distances[:,0]) / np.sum(1 / distances[:,0])
        print y_test,
        for score in y_scores:
            print score,
        print ''




if __name__=='__main__':
    print 'Loading Dataset...'
    #X,y = loadDataset(sys.argv[1],lbp,[24,8])
    X, y = loadDatasetNonSplit(sys.argv[1], lbp, [24, 8])
    idx = np.argsort(y)
    X,y = X[idx],y[idx]
    #print X.shape
    #statsByNFace(X,y)
    #ROCAllClasses(X,y)
    #ROC(X,y)
    # print 'Stats by Face'
    #print y
    generateStats(X,y)