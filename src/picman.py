"""
This module provides Picman, that is a Python based tool
to create large datasets of raw images with ease.

Picman will take a bulk of images from your WebCam
and choose where to store each of them between two main folders: 'train' and 'test'.

Usage:
 python3 picman.py -d path_to_destination
                   [-n name_images]
                   [-r ratio_training_set]
                   [-t name_train_set]
                   [-v name_validation_set]
                   [-i video_device_index]

args:
 -d the path to the destination base folder,
     e.g. 'dataset'

 -n the base name of captured images, "img" by default,
     e.g. 'img' (images' names will be img-1, img-2, and so on)

 -r the ratio of the training set over the whole dataset, 0.9 by default,
     e.g. 0.9 (in a dataset made up by 100 images, about 90 will be stored in the training folder)

 -t name of the folder to store the training set, "train" by default
    e.g. 'train' (the training set images will be stored in ./dataset/train/images)

 -v name of the folder to store the validation set, "test" by default
    e.g. 'test' (the validation set images will be stored in ./dataset/test/images)

 -i index of the video device, 0 (webcam) by default
"""

import argparse
import logging
import sys
from os import path
from pathlib import Path

from src.video.video import VideoHandler

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)

# Default ratio for the size of the training dataset over the dataset
_RATIO = 0.9

# Default name of the folder that will contain training images
_TRAIN = 'train'

# Default name of the folder that will contain test images
_TEST = 'test'

# Default name of the folder that will contain images
_IMAGES = 'images'

# The default index of the video device
_INDEX_VIDEO = 0

if __name__ == '__main__':
    """
    Picman entry point.
    """
    logging.info("Hi, I'm Picman, I'm running")

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dst',
                        help="destination folder", required=True)
    parser.add_argument('-n', '--name', default='img',
                        help="base name for images, 'img' by default")
    parser.add_argument('-r', '--ratio', default=_RATIO,
                        help="the ratio of the training dataset over the entire dataset in decimal number, "
                             f"{_RATIO} by default")
    parser.add_argument('-t', '--train', default=_TRAIN,
                        help=f"the name of the training set, {_TRAIN} by default")
    parser.add_argument('-v', '--validation', default=_TEST,
                        help=f"the name of the test set, {_TEST} by default")
    parser.add_argument('-i', '--index', default=_INDEX_VIDEO,
                        help=f"the index of the video device, {_INDEX_VIDEO} by default")
    args = parser.parse_args()

    logging.info(f"argument -d dst: {args.dst}")
    logging.info(f"argument -n name: {args.name}")
    logging.info(f"argument -r ratio: {args.ratio}")
    logging.info(f"argument -t train: {args.train}")
    logging.info(f"argument -v validation: {args.validation}")
    logging.info(f"argument -i index: {args.index}")

    # Checks if the destination folder already exists
    if path.exists(args.dst):
        logging.warning(f"destination folder {args.dst} already exist, will not overwrite nor remove, exiting")
        sys.exit()

    # Creates folders
    Path(args.dst).mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{args.train}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{args.train}/{_IMAGES}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{args.validation}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{args.validation}/{_IMAGES}').mkdir(parents=True, exist_ok=False)

    dst_path_training = f'{args.dst}/{args.train}/{_IMAGES}'
    dst_path_validation = f'{args.dst}/{args.validation}/{_IMAGES}'

    video = VideoHandler(dst_path_training, dst_path_validation, args.name, args.ratio, args.index)

    logging.info("Start capturing raw images")
    video.run()
    logging.info("Done")
