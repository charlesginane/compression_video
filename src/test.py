import numpy as np
import skimage.io
import skimage.color
from skimage.transform import resize
import PIL.Image
import matplotlib.pyplot as plt
import cv2


image = np.array(PIL.Image.open('1335.pgm'))
rows = (image.shape[0] * 2) // 3
cols =  image.shape[1] // 2

print(image.shape)
print(rows, cols)

im_1 = np.zeros((rows // 2, image.shape[1], 3))
im_2 = np.zeros((rows // 2, image.shape[1], 3))

U_1 = image[rows:image.shape[0],0:cols]
U = np.zeros((rows, image.shape[1]))
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



V_1 = image[rows:image.shape[0],cols:image.shape[1]]
V = np.zeros((rows, image.shape[1]))

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


for j in range(image.shape[1]):
    n_1 = 0
    n_2 = 0
    for i in range(0, rows):
        if i % 2 == 0:
            im_1[n_1, j, 0] = image[i, j]
            im_1[n_1, j, 1] = U[i, j]
            im_1[n_1, j, 2] = V[i, j]
            n_1 += 1
        else:
            im_2[n_2, j, 0] = image[i, j]
            im_2[n_2, j, 1] = U[i, j]
            im_2[n_2, j, 2] = V[i, j]
            n_2 += 1


t = cv2.cvtColor(im_1.astype(np.uint8), cv2.COLOR_YUV2RGB)
plt.imshow(t)
plt.show()
