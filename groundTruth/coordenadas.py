import numpy as np

if __name__=='__main__':
    N = 25#50
    M = 3#5
    arr = np.zeros([N, M, 5, 2, 3])
    for n in range(1,N+1):
        for m in range(1,M+1):
            arr[n-1, m-1, :, :, 0] = np.loadtxt('groundTruth/alvaro_groundTruth/' + str(n) + '_' + str(m) + '.txt')
            arr[n-1, m-1, :, :, 1] = np.loadtxt('groundTruth/lucas_groundTruth/' + str(n) + '_' + str(m) + '.txt')
            arr[n-1, m-1, :, :, 2] = np.loadtxt('groundTruth/kalyf_groundTruth/' + str(n) + '_' + str(m) + '.txt')
    olhoEsqX = np.int(np.mean(np.mean(arr[:,:,0:2,0,:],axis=3),axis=2))
    olhoEsqY = np.int(np.mean(np.mean(arr[:,:,0:2,1,:],axis=3),axis=2))
    olhoDirX = np.int(np.mean(np.mean(arr[:,:,2:4,0,:],axis=3),axis=2))
    olhoDirY = np.int(np.mean(np.mean(arr[:,:,2:4,1,:],axis=3),axis=2))
    inferiorX = np.int(np.mean(arr[:,:,4,0,:],axis=2))
    inferiorY = np.int(np.mean(arr[:,:,4,1,:],axis=2))

    for n in range(1,N+1):
        for m in range(1,M+1):
            with open('groundTruth/coordenadas_groundTruth/' + str(n) + '_' + str(m) + '.txt') as fp:
                fp.write(str(olhoEsqX[n,m])+' '+str(olhoEsqY[n,m])+'\n')
                fp.write(str(olhoDirX[n,m])+' '+str(olhoDirY[n,m])+'\n')
                fp.write(str(inferiorX[n,m])+' '+str(inferiorY[n,m])+'\n')
                fp.close()
