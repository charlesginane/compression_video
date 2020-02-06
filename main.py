#!/usr/bin/python
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


def usage():
    print('./main.py -s -p pid --fps <Number of FPS> --pgm <PGM image> --decompress <Video file>')
    print()
    print('-s: Save mode')
    print('   Save the video in a file')
    print('-p: Pid of video')
    print('   Specify a pid for a video')
    print('--fps: frame sequence')
    print('   Specify the frame sequence of the video which will be generated')
    print('--decompress: the video')
    print('   Specify the video which will be decomrpessed')

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


def read_log(log_file):
    lines = []
    with open(log_file, 'r+') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines


def __main__():
    save = False
    image_file = None
    log_file = "log.txt"
    fps = 25
    pid = ""
    change_fps = False

    if '-s' in sys.argv:
        save = True
        print("Save mode enable")
        sys.argv.remove('-s')

    if '--fps' in sys.argv:
        fps = int(sys.argv[sys.argv.index('--fps') + 1])
        print("Changin FPS to %d" % (fps))
        sys.argv.remove('--fps')
        sys.argv.remove(str(fps))
        change_fps = True

    if '--pid' in sys.argv:
        pid = sys.argv[sys.argv.index('--pid') + 1]
        sys.argv.remove('--pid')
        sys.argv.remove(pid)

    if '--usage' in sys.argv:
        usage()
        exit(0)

    if '--help' in sys.argv:
        usage()
        exit(0)

    if len(sys.argv) < 2:
        usage()
        exit(1)

    if '--decompress' in sys.argv:
        os.system("rm -rf workspace")
        os.system("mkdir workspace")
        os.system("mkdir workspace/res")
        os.system("mkdir workspace/tmp")
        file_video = sys.argv[sys.argv.index('--decompress') + 1]
        sys.argv.remove('--decompress')
        sys.argv.remove(file_video)
        print("Decompressing file %s" % (file_video))
        tmp_dir = 'workspace/tmp/'
        print("All PGM images will be saved into workspace/tmp/")
        dec = src.lib.Decompress(file_video, tmp_dir, pid=pid)
        if (dec.run()):
            exit(2)

        list_frame = dec.get_list_of_frame()
        print('got %d frames' % (len(list_frame)))
        lines = read_log(log_file)
        line = 0
        index_im = 0
        f = True
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

        animate(index_im, fps=fps, save=save)
        exit(0)

    if '--pgm' in sys.argv:
        image_file = sys.argv[sys.argv.index('--pgm') + 1]
        sys.argv.remove('--pgm')
        sys.argv.remove(image_file)
        im = lib.Image(image_file)
        im.convert()
        skimage.io.imsave("save.ppm", im.ppm)


__main__()
