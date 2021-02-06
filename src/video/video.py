"""
This module provides the class for storing images taken from the video capturing device.
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

    def __init__(self, dst_path_training: str, dst_path_validation: str, name: str, size_training: float) -> None:
        """

        :param dst_path_training: the path to the training set
        :param dst_path_validation: the path to the validation
        :param name: the base-name for images, for example 'img'
        :param size_training: the size of the training set over the entire data set
        """
        self.dst_path_training = dst_path_training
        self.dst_path_validation = dst_path_validation
        self.name = name
        self.size_training = size_training

        if size_training < 0.0 or size_training > 1.0:
            raise ValueError("size of training set must be in range [0.0, 1.0]")

    def run(self) -> None:
        """
        Start capturing the video.
        """
        # Reads video
        video = cv.VideoCapture(0)  # WebCam
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

            # Writes the Esc command on the annotated frame
            msg = "Esc to exit"
            cv.putText(annotated, msg, (int(0.05 * width), int(0.05 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            # Writes the Space command on the annotated frame
            msg = "Space to take the image"
            msg_size = cv.getTextSize(msg, cv.FONT_HERSHEY_SIMPLEX, 0.75, 2)
            msg_width = msg_size[0][0]
            cv.putText(annotated, msg, (int(0.5 * width - msg_width / 2), int(0.95 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            # Writes the img counter on the annotated frame
            msg = f"Stored: {count_total}"
            cv.putText(annotated, msg, (int(0.825 * width), int(0.875 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)
            msg = f"Training: {count_training}"
            cv.putText(annotated, msg, (int(0.825 * width), int(0.925 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)
            msg = f"Validation: {count_validation}"
            cv.putText(annotated, msg, (int(0.825 * width), int(0.975 * height)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, self.RGBColor.GREEN.value, 2)

            cv.imshow("Picman", annotated)

            # Streams until esc is pressed
            k = cv.waitKey(1) & 0xff

            # Esc, stops running
            if k == self._KEY_ESC:
                logging.info("Got esc command")
                run = False

            # Space, takes the current image
            if k == self._KEY_SPACE:
                filename = f"{self.name}-{count_total}"
                logging.info(f"Got space command, storing image {filename}")

                # Chooses where to store the image
                dst = ''
                r = np.random.random_sample()
                if r < self.size_training:
                    dst = self.dst_path_training
                    count_training += 1
                else:
                    dst = self.dst_path_validation
                    count_validation += 1

                # Stores the image (no critical time constraints)
                cv.imwrite(os.path.join(dst, f"{filename}.jpeg"), frame)
                count_total += 1

        logging.info(f"stored {count_total} images (training {count_training}, validation {count_validation})")
