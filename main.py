import argparse
from log import logger
import os
from core import convert_and_merge, multiprocess


def start(args):
    if not os.path.exists(args.srcdir):
        logger.critical(f'src dir "{args.srcdir}" does not exist.')
        return
    if not os.path.exists(args.destdir):
        os.makedirs(args.destdir)
    if args.batch:
        multiprocess(args.srcdir, args.destdir)
    else:
        convert_and_merge(args.srcdir, args.destdir)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert and merge bilibili m4s files to mp4 file.')
    parser.add_argument('srcdir', type=str, help='downloaded from bilibili client (like "1550141198" or its parent dir).')
    parser.add_argument('destdir', type=str, help="the mp4 ouput dir you want.")
    parser.add_argument('-b', '--batch', action='store_true', help='batch processing.')

    args = parser.parse_args()
    start(args)
    # print()
    