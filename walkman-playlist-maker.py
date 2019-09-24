# A script to convert playlists output by a program such as Lollypop into a
# playlist that will work on Sony Walkman devices (with relative filepaths)
from argparse import ArgumentParser
import re
import os

parser = ArgumentParser()
parser.add_argument('-f', '--file', dest='filename')

args = parser.parse_args()

if args.filename:
    playlist = args.filename
    if playlist[-4:] != '.m3u':
        raise EnvironmentError("This playlist format is not supported, use m3u.")

    print("Opening ", playlist)
    f = open(playlist)
    w = open(playlist[:-4]+" 2.m3u", 'a')
    for line in f:
        try:
            if re.search('#EXTM3U', line):
                continue
            remove_start = re.sub('.+?(?:Music\/)', '', line)
            replace_20_spaces = re.sub('%20', ' ', remove_start)
            w.write(replace_20_spaces)
        except:
            raise

    w.close()
    f.close()
    os.rename(playlist, playlist[:-4]+" Original.m3u")
    os.rename(playlist[:-4]+" 2.m3u", playlist)
