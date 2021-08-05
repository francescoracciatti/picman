"""
Picman is a tool to rapidly create large training and validation sets.

Usage:
 python3 picman.py [-d basename for root folder]
                   [-n basename for images]
                   [-r training set size ratio over entire dataset]
                   [-t training set folder name]
                   [-v validation set folder name]
                   [-i index of camera device]

args:
 -d basename to the destination root folder, will contain training and validation datasets,
     "dataset" by default,
     the current date and time will be appended

 -n basename for images,
     "img" by default,
     an incremental counter will be appended

 -r the ratio of the training set over the whole dataset, in percentage,
     0.9 by default

 -t name of the folder for the training set,
     "train" by default

 -v name of the folder for the validation set,
     "test" by default

 -i index of the camera device,
     0 by default (i.e. webcam)
"""
import argparse
import logging
import sys
from datetime import datetime
from os import path
from pathlib import Path

from src.video.video import VideoHandler

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)

# Default ratio for the size of the training set over the whole dataset
_DEFAULT_TRAINING_RATIO = 0.9

# Default name of the folder for training dataset
_DEFAULT_FOLDER_TRAINING = 'train'

# Default name of the folder for the test/validation dataset
_DEFAULT_FOLDER_TEST = 'test'

# Default name of the folder that will contain images
_DEFAULT_FOLDER_DATASET = 'dataset'

# Default name for images
_DEFAULT_NAME_IMAGE = 'img'

# The default index of the video device
_DEFAULT_INDEX_CAMERA = 0

if __name__ == '__main__':
    """
    Picman entry point.
    """
    logging.info("Hi, I'm Picman, I'm running")

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dst', default=_DEFAULT_FOLDER_DATASET,
                        help=f"dataset root folder, '{_DEFAULT_FOLDER_DATASET}' by default")
    parser.add_argument('-n', '--name', default=_DEFAULT_NAME_IMAGE,
                        help=f"base name for images, '{_DEFAULT_NAME_IMAGE}' by default")
    parser.add_argument('-r', '--ratio', default=_DEFAULT_TRAINING_RATIO,
                        help="the ratio of the training dataset over the entire dataset in decimal number, "
                             f"{_DEFAULT_TRAINING_RATIO} by default")
    parser.add_argument('-t', '--train', default=_DEFAULT_FOLDER_TRAINING,
                        help=f"folder name for the training set, {_DEFAULT_FOLDER_TRAINING} by default")
    parser.add_argument('-v', '--validation', default=_DEFAULT_FOLDER_TEST,
                        help=f"folder name for the validation/test set, {_DEFAULT_FOLDER_TEST} by default")
    parser.add_argument('-i', '--index', default=_DEFAULT_INDEX_CAMERA,
                        help=f"the index of the video device, {_DEFAULT_INDEX_CAMERA} by default")
    args = parser.parse_args()

    logging.info(f"argument -d dst: {args.dst}")
    logging.info(f"argument -n name: {args.name}")
    logging.info(f"argument -r ratio: {args.ratio}")
    logging.info(f"argument -t train: {args.train}")
    logging.info(f"argument -v test/validation: {args.validation}")
    logging.info(f"argument -i index: {args.index}")

    # Appends date and time to dataset folder
    now = datetime.now()
    time_mark = now.strftime("%Y-%m-%d_%H-%M-%S")
    dataset_folder = f"{args.dst}-{time_mark}"

    # Checks if the destination folder already exists
    if path.exists(dataset_folder):
        logging.critical(f"destination folder {dataset_folder} already exist, will not overwrite nor remove, exiting")
        sys.exit()

    # Makes folders
    Path(dataset_folder).mkdir(parents=True, exist_ok=False)
    Path(f'{dataset_folder}/{args.train}').mkdir(parents=True, exist_ok=False)
    Path(f'{dataset_folder}/{args.validation}').mkdir(parents=True, exist_ok=False)

    dst_path_training = f'{dataset_folder}/{args.train}'
    dst_path_validation = f'{dataset_folder}/{args.validation}'

    video = VideoHandler(dst_path_training, dst_path_validation, args.name, float(args.ratio), int(args.index))

    logging.info("Start capturing images")
    video.run()
    logging.info("Done")
