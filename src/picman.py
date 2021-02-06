"""
This module provides Picman, that is a Python based tool
to create large datasets of raw images with ease.

Picman will take a bulk of images from your WebCam
and choose where to store each of them between two main folders: 'training' and 'validation'.

Usage:
 python3 picman.py -d path_to_destination -n img_basename -s size_trainingset

args:
 -d the path to the destination base folder,
     e.g. 'dataset'

 -n the base name for each images,
     e.g. 'img' (images' names will be img-1, img-2, and so on)

 -s the size of the training set over the whole dataset,
     e.g. 0.7 (in a dataset made up by 100 images, about 70 will be stored in the training folder)
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

# Name of the folder that will contain training images
_TRAINING = 'training'

# Name of the folder that will contain validation images
_VALIDATION = 'validation'

# Name of the folder that will contain images
_IMAGES = 'images'

# Name of the folder that will contain annotations (left empty)
_ANNOTATIONS = 'annotations'

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
    parser.add_argument('-s', '--size', default=0.7,
                        help="the size of the training over the entire dataset in decimal number, 0.7 by default")
    args = parser.parse_args()

    logging.info(f"argument dst: {args.dst}")
    logging.info(f"argument name: {args.name}")
    logging.info(f"argument name: {args.size}")

    # Checks if the destination folder already exists
    if path.exists(args.dst):
        logging.warning(f"destination folder {args.dst} already exist, will not overwrite nor remove, exiting")
        sys.exit()

    # Creates folders
    Path(args.dst).mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_TRAINING}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_TRAINING}/{_IMAGES}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_TRAINING}/{_ANNOTATIONS}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_VALIDATION}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_VALIDATION}/{_IMAGES}').mkdir(parents=True, exist_ok=False)
    Path(f'{args.dst}/{_VALIDATION}/{_ANNOTATIONS}').mkdir(parents=True, exist_ok=False)

    dst_path_training = f'{args.dst}/{_TRAINING}/{_IMAGES}'
    dst_path_validation = f'{args.dst}/{_VALIDATION}/{_IMAGES}'

    video = VideoHandler(dst_path_training, dst_path_validation, args.name, args.size)

    logging.info("Start capturing raw images")
    video.run()
    logging.info("Done")
