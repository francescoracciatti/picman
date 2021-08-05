"""
This module provides the class for storing images taken from the camera device.
"""

import logging
import os
import sys
from enum import Enum, unique

import cv2 as cv
import numpy as np


class VideoHandler(object):
    """
    Handles the video capturing process.
    """

    _KEY_ESC = 27
    _KEY_SPACE = 32

    @unique
    class RGBColor(Enum):
        GREEN = (0, 255, 0)

    def __init__(self, dst_path_training: str, dst_path_validation: str, image_basename: str, ratio: float, index: int) -> None:
        """

        :param dst_path_training: the path to the training set
        :param dst_path_validation: the path to the validation
        :param image_basename: the base-name for images, for example 'img'
        :param ratio: the ratio of the training set over the entire data set
        :param index: the index of the camera device
        """
        self.dst_path_training = dst_path_training
        self.dst_path_validation = dst_path_validation
        self.image_basename = image_basename
        self.ratio = ratio
        self.index = index

        if ratio < 0.0 or ratio > 1.0:
            raise ValueError("ratio of training set must be in range [0.0, 1.0]")

    def run(self) -> None:
        """
        Start capturing the video.
        """
        # Reads video
        video = cv.VideoCapture(self.index)
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

        # Exits if video not open
        if not video.isOpened():
            logging.critical("Cannot open video")
            sys.exit()

        # Counts images
        count_total = 0
        count_training = 0
        count_validation = 0

        run = True
        while run:
            # Capture the current frame
            run, frame = video.read()

            if not run:
                logging.critical("Cannot capture frames")
                sys.exit()

            # Makes a copy of the original frame
            annotated = frame.copy()

            # Writes the ESC command on the annotated frame
            msg = "ESC to exit"
            cv.putText(annotated, msg, (int(0.05 * width), int(0.05 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            # Writes the SPACE command on the annotated frame
            msg = "SPACE to take the image"
            msg_size = cv.getTextSize(msg, cv.FONT_HERSHEY_SIMPLEX, 0.75, 2)
            msg_width = msg_size[0][0]
            cv.putText(annotated, msg, (int(0.5 * width - msg_width / 2), int(0.95 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            # Writes the img counter on the annotated frame
            msg = f"Training set: {count_training}"
            cv.putText(annotated, msg, (int(0.800 * width), int(0.875 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)
            msg = f"Validation set: {count_validation}"
            cv.putText(annotated, msg, (int(0.800 * width), int(0.925 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)
            msg = f"TOTAL: {count_total}"
            cv.putText(annotated, msg, (int(0.800 * width), int(0.975 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            cv.imshow("Picman", annotated)

            # Streams until esc is pressed
            k = cv.waitKey(1) & 0xff

            # Esc, stops running
            if k == self._KEY_ESC:
                logging.info("Got ESC command")
                run = False

            # Space, takes the current image
            if k == self._KEY_SPACE:
                filename = f"{self.image_basename}-{count_total}"
                logging.info(f"Got SPACE command, storing image {filename}")

                # Chooses where to store the image
                r = np.random.random_sample()
                if r < self.ratio:
                    dst = self.dst_path_training
                    count_training += 1
                else:
                    dst = self.dst_path_validation
                    count_validation += 1

                # Stores the image (no critical time constraints)
                cv.imwrite(os.path.join(dst, f"{filename}.jpeg"), frame)
                count_total += 1

        logging.info(f"Got {count_total} images (training {count_training}, validation {count_validation})")
