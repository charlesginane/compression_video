import sys
import numpy as np
import skimage.io
import skimage.color
from skimage.transform import resize
import PIL.Image
import matplotlib.pyplot as plt
import cv2

class Image:
    def __init__(self, path_image, log_file = None):
        self.path = path_image
        self.pgm = np.array(PIL.Image.open(path_image))
        self.log_file = log_file
        if not self.log_file:
            sys.stdout.write("WARNING: No log file found, apply default pattern (TOP_FIRST)\n")
        self.rows = (self.pgm.shape[0] * 2) // 3
        self.cols =  self.pgm.shape[1] // 2
        self.frame_1 = None
        self.frame_2 = None
        self.ppm = None


    def getUV(self, image):
        U_1 = image[self.rows:image.shape[0],0:self.cols]
        U = np.zeros((self.rows, image.shape[1]))
        l = 0
        for j in range(U_1.shape[0]):
            c = 0
            for i in range(U_1.shape[1]):
                U[l, c] = U_1[j, i]
                c += 1
                U[l, c] = U_1[j, i]
                c += 1
            for i in range(image.shape[1]):
                U[l+1, i] = U[l, i]
            l += 2

        V_1 = image[self.rows:image.shape[0],self.cols:image.shape[1]]
        V = np.zeros((self.rows, image.shape[1]))
        l = 0
        for j in range(V_1.shape[0]):
            c = 0
            for i in range(V_1.shape[1]):
                V[l, c] = V_1[j, i]
                c += 1
                V[l, c] = V_1[j, i]
                c += 1
            for i in range(image.shape[1]):
                V[l+1, i] = V[l, i]
            l += 2
        return U, V


    def convert(self):
        U, V = self.getUV(self.pgm)
        self.frame_1 = np.zeros((self.rows // 2, self.pgm.shape[1], 3))
        self.frame_2 = np.zeros((self.rows // 2, self.pgm.shape[1], 3))
        for j in range(self.pgm.shape[1]):
            n_1 = 0
            n_2 = 0
            for i in range(0, self.rows):
                if i % 2 == 0:
                    self.frame_1[n_1, j, 0] = self.pgm[i, j]
                    self.frame_1[n_1, j, 1] = U[i, j]
                    self.frame_1[n_1, j, 2] = V[i, j]
                    n_1 += 1
                else:
                    self.frame_2[n_2, j, 0] = self.pgm[i, j]
                    self.frame_2[n_2, j, 1] = U[i, j]
                    self.frame_2[n_2, j, 2] = V[i, j]
                    n_2 += 1
        self.ppm = cv2.cvtColor(self.frame_1.astype(np.uint8), cv2.COLOR_YUV2RGB)


    def plot(self):
        plt.imshow(self.ppm)
        plt.show(block=False)
        print("sncf")

    def save(self, name_file='out.ppm'):
        self.ppm.save(name_file)
