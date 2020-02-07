import sys
import numpy as np
import skimage.io
import skimage.color
from skimage.transform import resize
import PIL.Image
import matplotlib.pyplot as plt
import cv2

class Image:
    def __init__(self, path_image, first=0):
        self.path = path_image
        self.pgm = np.array(PIL.Image.open(path_image))
        self.rows = (self.pgm.shape[0] * 2) // 3
        self.cols =  self.pgm.shape[1] // 2
        self.frame_1 = None
        self.frame_2 = None
        self.ppm = None
        self.first = first


    def getUV(self, image):
        # Resize U and V channel
        U_1 = image[self.rows:image.shape[0],0:self.cols]
        U = np.zeros((self.rows, image.shape[1]))
        U[::2,::2] = U_1[:,:]
        U[1::2,::2] = U_1[:,:]
        U[::2,1::2] = U_1[:,:]
        U[1::2,1::2] = U_1[:,:]

        V_1 = image[self.rows:image.shape[0],self.cols:image.shape[1]]
        V = np.zeros((self.rows, image.shape[1]))
        V[::2,::2] = V_1[:,:]
        V[1::2,::2] = V_1[:,:]
        V[::2,1::2] = V_1[:,:]
        V[1::2,1::2] = V_1[:,:]
        return U, V

    def mean_frame(self):
        # Apply the desentrelacer
        for i in range(0, self.frame_1.shape[0]):
            if i % 2 == 0:
                if i == 0:
                    continue
                self.frame_2[i] = (self.frame_2[i - 1] + self.frame_2[i + 1]) // 2
            else:
                if i + 1 == self.frame_1.shape[0]:
                    continue
                self.frame_1[i] = (self.frame_1[i - 1] + self.frame_1[i + 1]) // 2

    def convert(self):
        U, V = self.getUV(self.pgm)
        self.frame_1 = np.zeros((self.rows, self.pgm.shape[1], 3))
        self.frame_2 = np.zeros((self.rows, self.pgm.shape[1], 3))
        if self.first:
            # Frame need to be desentrelacer
            self.frame_1[::2,:,0] =  self.pgm[:self.rows:2,::]
            self.frame_2[1::2,:,0] =  self.pgm[1:self.rows:2,::]
            self.frame_1[::2,:,1] =  U[::2,::]
            self.frame_2[1::2,:,1] =  U[1::2,::]
            self.frame_1[::2,:,2] =  V[::2,::]
            self.frame_2[1::2,:,2] =  V[1::2,::]

            self.mean_frame()

        else:
            self.frame_1 = np.zeros((self.rows, self.pgm.shape[1], 3))
            for j in range(self.pgm.shape[1]):
                for i in range(0, self.rows):
                    self.frame_1[i, j, 0] = self.pgm[i, j]
                    self.frame_1[i, j, 1] = U[i, j]
                    self.frame_1[i, j, 2] = V[i, j]
        self.frame_1 = cv2.cvtColor(self.frame_1.astype(np.uint8), cv2.COLOR_YUV2RGB)
        self.frame_2 = cv2.cvtColor(self.frame_2.astype(np.uint8), cv2.COLOR_YUV2RGB)


        # Adding a black line on top of the seconde frame
        for i in range(self.frame_2.shape[1]):
             self.frame_2[0,i] = 0
             self.frame_2[self.frame_2.shape[0] - 1,i] = 0
             self.frame_1[self.frame_2.shape[0] - 1,i] = 0
