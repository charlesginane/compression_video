import glob
import os
import shutil
import sys

class Decompress:
    def __init__(self, video_file, tmp_dir, override_path_mpeg2dec=None):
        self.video_file = video_file
        self.tmp_dir = tmp_dir
        self.override_path_mpeg2dec = override_path_mpeg2dec
        self.list_frame = []

    def run(self):
        if not self.override_path_mpeg2dec:
            code = os.system('(../../tools/mpeg2dec/src/mpeg2dec -v -o pgm %s > log.txt) 2> /dev/null' % (self.video_file))
        else:
            code = os.system('%s -v -o pgm %s > log.txt' % (self.override_path_mpeg2dec, self.video_file))

        if code != 0:
            sys.stderr.write("Error during decompression, mpeg2dec returns a non 0 value (%d)" % (code >> 8))
            return 2

        list_pgm = glob.glob("*.pgm")
        for pgm in list_pgm:
            self.list_frame.append(int(pgm.split('.')[0]))
            shutil.move('%s' % pgm, '%s' % self.tmp_dir)
        sys.stdout.write("Decompression: All frames will be generated at %s directory\n" % (self.tmp_dir))
        self.list_frame.sort()
        return 0


    def get_list_of_frame(self):
        return self.list_frame
