#!/usr/bin/python
import os
import sys
import src.tool
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
        # Create the workspace
        os.system("rm -rf workspace")
        os.system("mkdir workspace")
        os.system("mkdir workspace/res")
        os.system("mkdir workspace/tmp")

        file_video = sys.argv[sys.argv.index('--decompress') + 1]
        sys.argv.remove('--decompress')
        sys.argv.remove(file_video)

        # Call to the Decompression class
        print("Decompressing file %s" % (file_video))
        tmp_dir = 'workspace/tmp/'
        print("All PGM images will be saved into workspace/tmp/")
        dec = src.lib.Decompress(file_video, tmp_dir, pid=pid)

        # Little check for the wrapper
        if (dec.run()):
            exit(2)

        # Get the list of decoded frames
        list_frame = dec.get_list_of_frame()

        # Convert frames and display them (or save them)
        list_im, fps = src.tool.convert_frame(list_frame, tmp_dir=tmp_dir, fps=fps, change_fps=change_fps)
        src.tool.animate(list_im, fps=fps, save=save)
        exit(0)


__main__()
