#coding=utf-8

import os, sys

from PIL import Image

import logging

logger = logging.getLogger(__name__)


def is_file_exists(fp):
    '''
    Check whether image file exists
    :param fp: image file path (string)
    :return: bool
    '''

    if os.path.exists(fp):
        return True
    else:
        return False

def open(fp):
    '''
    Open an image file
    :param fp: image file path (string).
    :return: return a file object.
    '''

    if not is_file_exists((fg)):
        raise IOError("%r file path not found" % fp)

    return Image.open(fg)


class Pure:
    '''
    Purify picture, remove noise dot.
    '''

    def __init__(self, im):
        '''
        Init
        :param im: image file object (Image object).
        '''

        self.im = im

    def check(self):
        self.im.show()

    def test(self):
        # Image.blend
        pass



class Cut:
    pass

class Read:
    pass


if __name__ == '__main__':

    pass