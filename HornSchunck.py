#!/usr/bin/env python
from __future__ import division
from pyOpticalFlow import Path
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import convolve as filter2
from scipy.ndimage import imread

FILTER = 7

def HS(im1, im2, alpha, Niter):
    """
    im1: image at t=0
    im2: image at t=1
    alpha: regularization constant
    Niter: number of iteration
    """

	#set up initial velocities
    uInitial = np.zeros([im1.shape[0],im1.shape[1]])
    vInitial = np.zeros([im1.shape[0],im1.shape[1]])

	# Set initial value for the flow vectors
    u = uInitial
    v = vInitial

	# Estimate derivatives
    [fx, fy, ft] = computeDerivatives(im1, im2)

    fg,ax = plt.subplots(1,3,figsize=(18,5))
    for f,a,t in zip((fx,fy,ft),ax,('$f_x$','$f_y$','$f_t$')):
        h=a.imshow(f,cmap='bwr')
        a.set_title(t)
        fg.colorbar(h,ax=a)

	# Averaging kernel
    kernel=np.array([[1/12., 1/6, 1/12],
                      [1/6,    0, 1/6],
                      [1/12, 1/6, 1/12]])

    print(fx[100,100],fy[100,100],ft[100,100])

	# Iteration to reduce error
    for i in range(Niter):
#%% Compute local averages of the flow vectors
        uAvg = filter2(u,kernel)
        vAvg = filter2(v,kernel)
#%% common part of update step
        der = (fx*uAvg + fy*vAvg + ft) / (alpha**2 + fx**2 + fy**2)
#%% iterative step
        u = uAvg - fx * der
        v = vAvg - fy * der

    return u,v

def computeDerivatives(im1, im2):
#%% build kernels for calculating derivatives
    kernelX = np.array([[-1, 1],
                         [-1, 1]]) * .25 #kernel for computing dx
    kernelY = np.array([[-1,-1],
                         [ 1, 1]]) * .25 #kernel for computing dy
    kernelT = np.ones((2,2))*.25

	#apply the filter to every pixel using OpenCV's convolution function
#	fx = cv2.filter2D(im1,-1,kernelX) + cv2.filter2D(im2,-1,kernelX)
#	fy = cv2.filter2D(im1,-1,kernelY) + cv2.filter2D(im2,-1,kernelY)

    fx = filter2(im1,kernelX) + filter2(im2,kernelX)
    fy = filter2(im1,kernelY) + filter2(im2,kernelY)

     #ft = im2 - im1
 	#ft = cv2.filter2D(im2,-1,kernelT) + cv2.filter2D(im1,-1,-kernelT)
    ft = filter2(im2,kernelT) + filter2(im1,-kernelT)
    return (fx,fy,ft)

def compareGraphs():
    """
    makes quiver
    """
    ax = plt.figure().gca()
    ax.imshow(imgNew,cmap = 'gray')
    # plt.scatter(POI[:,0,1],POI[:,0,0])
    for i in range(len(u)):
        if i%5 ==0:
            for j in range(len(u)):
                if j%5 == 0:
                    ax.arrow(j,i,v[i,j]*5e-4,u[i,j]*5e-4, color = 'red')

    print('done')
		# print i
	# plt.arrow(POI[:,0,0],POI[:,0,1],0,-5)

def demo(stem):
    for i in range(1):
        #upload images#
        directory = 'box/box.'
        # directory = 'office/office.'
        # directory = 'rubic/rubic.'
        # directory = 'sphere/sphere.'
        fileName = directory + str(i) + '.bmp'
        imgOld = imread(fileName).astype(float)
        # imgOld = cv2.GaussianBlur(imgOld,(FILTER,FILTER),1)
        imgOld = gaussian_filter(imgOld,3)

        i += 1
        fileName = directory + str(i) + '.bmp'
        imgNew = imread(fileName).astype(float)
        # imgNew = cv2.GaussianBlur(imgNew,(FILTER,FILTER),1)
        imgNew = gaussian_filter(imgNew,3)
        #plt.imshow(imgNew)
        #plt.title('new image')

        [u,v] = HS(imgOld, imgNew, 1, 100)
        compareGraphs()


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Pure Python Horn Schunck Optical Flow')
    p.add_argument('stem',help='path/stem of files to analyze')
    p = p.parse_args()

    demo(p.stem)

    plt.show()