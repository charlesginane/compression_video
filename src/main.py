#!/usr/bin/python
import sys
import lib
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re


def usage():
    print('./main.py -s --fps <Number of FPS> --pgm <PGM image> --decompress <Video file>')

def animate(list_images, fps=25, save=False):
    fig = plt.figure() # initialise la figure
    images_plot = []
    for im in list_images:
        images_plot.append([plt.imshow(im, animated=True)])

    ani = animation.ArtistAnimation(fig, images_plot, blit=True, interval=fps, repeat_delay=1000)
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
    if '-s' in sys.argv:
        save = True
        print("Save mode enable")
        sys.argv.remove('-s')

    if '--fps' in sys.argv:
        fps = int(sys.argv[sys.argv.index('--fps') + 1])
        print("Changin FPS to %d" % (fps))
        sys.argv.remove('--fps')
        sys.argv.remove(str(fps))

    if len(sys.argv) < 2:
        exit(1)

    if '--decompress' in sys.argv:
        file_video = sys.argv[sys.argv.index('--decompress') + 1]
        sys.argv.remove('--decompress')
        sys.argv.remove(file_video)
        print("Decompressing file %s" % (file_video))
        tmp_dir = tempfile.mkdtemp()
        print("All file will be saved into /tmp/")
        dec = lib.Decompress(file_video, tmp_dir)
        if (dec.run()):
            exit(2)

        list_frame = dec.get_list_of_frame()
        print('got %d frames' % (len(list_frame)))
        lines = read_log(log_file)
        line = 0
        list_image = []
        if re.match('Frame period:*', lines[0]):
            fps = int(float(lines[0].split(':')[-1]))
            print('new :', fps)
            line += 1

        for frame in list_frame:
            first = 0
            if re.match('Frame period:*', lines[line]):
                line += 1
            if lines[line] == "PIC_FLAG_TOP_FIELD_FIRST":
                first = 1
                line += 1
            elif lines[line] == "PIC_FLAG_REPEAT_FIRST_FIELD":
                first = 2
                line += 1
            elif lines[line] == "PIC_FLAG_PROGRESSIVE_FRAME":
                line += 1

            im = lib.Image('%s/%d.pgm' % (tmp_dir, frame), first=first)
            im.convert()
            list_image.append(im.ppm)
        print(len(list_image))

        animate(list_image, fps=fps, save=save)
        exit(0)



    if '--pgm' in sys.argv:
        image_file = sys.argv[sys.argv.index('--pgm') + 1]
        sys.argv.remove('--pgm')
        sys.argv.remove(image_file)



    # im = lib.Image(image_file, log_file)
    # im.convert()
    #
    #
    # if save:
    #     im.save()
    #
    # else:
    #     im.plot()
    #     input("test")


__main__()
