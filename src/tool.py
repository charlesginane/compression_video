import os
import sys
import src.lib
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
import skimage
import time
from tqdm import tqdm

def read_log(log_file):
    lines = []
    with open(log_file, 'r+') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines


def animate(len_image, fps=1, save=False):
    fig = plt.figure()
    im = plt.imshow((skimage.io.imread('workspace/res/frame_0.ppm')), animated=True)

    def update(frame):
        im.set_array((skimage.io.imread('workspace/res/frame_%d.ppm' % frame)))
        return im,

    ani = animation.FuncAnimation(fig, update, frames=len_image - 1, blit=True, interval=fps, repeat=False)
    if save:
        sys.stdout.write("Save the video at out.mp4\n")
        ani.save("out.mp4")
    else:
        plt.show()


def convert_frame(list_frame, tmp_dir, fps, change_fps=False, log_file="log.txt"):
    print('got %d frames' % (len(list_frame)))
    lines = read_log(log_file)
    line = 0
    index_im = 0
    f = True

    # Checking for frame_period flag
    if  line < len(lines) and re.match('Frame period:*', lines[0]) and change_fps == False:
        fps = int(float(lines[0].split(':')[-1]))
        print('new fps:', fps)
        line += 1

    for frame in tqdm(list_frame):
        first = 0
        if line < len(lines) and re.match('Frame period:*', lines[line]):
            line += 1
        if  line < len(lines) and lines[line] == "PIC_FLAG_REPEAT_FIRST_FIELD":
            first = 2
            line += 1
        if  line < len(lines) and lines[line] == "PIC_FLAG_TOP_FIELD_FIRST":
            first = 1
            line += 1
        elif  line < len(lines) and lines[line] == "PIC_FLAG_PROGRESSIVE_FRAME":
            line += 1
            first = 0

        im = src.lib.Image('%s/%d.pgm' % (tmp_dir, frame), first=first)
        im.convert()

        skimage.io.imsave("workspace/res/frame_%d.ppm" % (index_im), im.frame_1)
        if first:
            skimage.io.imsave("workspace/res/frame_%d.ppm" % (index_im + 1), im.frame_2)
            index_im += 1
        index_im += 1
    return index_im, fps
