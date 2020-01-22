#!/usr/bin/python
import sys
import lib


def usage():
    pass

save = False

if '-s' in sys.argv:
    save = True
    print("Save mode")
    sys.argv.remove('-s')

if len(sys.argv) < 2:
    exit(1)


im = lib.Image(sys.argv[1])
im.convert()

if save:
    im.save()

else:
    im.plot()
    input("test")
