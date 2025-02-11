from exports.flat.iflat_export import IFlatExport
from utils.VariableClass import VariableClass
from os.path import (
    join as pjoin,
    dirname as pdirname,
    abspath as pabspath,
)
import os
import time


class FlatExport(IFlatExport):
    """
    Base Export class that implements functions for
    initializing and saving frame under specific format.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        self.name = name
        self._var = VariableClass()
        _cur_dir = pdirname(pabspath(__file__))
        self.proj_dir = pjoin(_cur_dir, f'../../data/{name}')
        self.proj_dir = pabspath(self.proj_dir)  # normalise the link
        self.result_dir_path = None
        self.result_labeled_dir_path = None

    def initialize_save_dir(self):
        """
        See iflat_export.py

        Returns:
            success True or False
        """
        self.result_dir_path = pjoin(self.proj_dir, f'{self._var.DATASET_FORMAT}-v{self._var.DATASET_VERSION}')
        os.makedirs(self.result_dir_path, exist_ok=True)

        self.result_labeled_dir_path = pjoin(self.proj_dir,
                                             f'{self._var.DATASET_FORMAT}-v{self._var.DATASET_VERSION}-labeled')

        if os.path.exists(self.result_dir_path):
            print('Successfully initialize save directory!')
            return True
        else:
            print('Something wrong happened!')
            return False

    def save_frame(self, frame, predicted_frames, cv2, labels_and_boxes, labeled_frame=None):
        """
        See iflat_export.py

        Returns:
            Predicted frame counter.
        """
        print(f'5.1. Condition met, processing valid frame: {predicted_frames}')
        # Save original frame
        unix_time = int(time.time())
        print("5.2. Saving frame, labels and boxes")
        cv2.imwrite(
            f'{self.result_dir_path}/{unix_time}.png',
            frame)

        if labeled_frame is not None:
            os.makedirs(self.result_labeled_dir_path, exist_ok=True)

            cv2.imwrite(
                f'{self.result_labeled_dir_path}/{unix_time}.png',
                labeled_frame)
        # Save labels and boxes
        with open(f'{self.result_dir_path}/{unix_time}.txt',
                  'w') as my_file:
            my_file.write(labels_and_boxes)

        # Increase the frame_number and predicted_frames by one.
        return predicted_frames + 1
