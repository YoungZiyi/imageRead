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

    if not is_file_exists((fp)):
        raise IOError("%r file path not found" % fp)

    return Image.open(fp)


class Pure:
    '''
    Purify picture, remove noise dot.
    '''

    def __init__(self, im):
        '''
        Init
        :param im: image file object (Image object).
        '''

        self.im = im.convert('L')
        self.load()

    def load(self):
        '''
        update current image size

        :return:None
        '''
        self.size = self.im.size

    def crop(self, box=None):
        '''
        Crop image
        :param length:int
        :param width: int
        :return:
        '''

        if box == None:
            return self.im.copy()

        self.im = self.im.crop(box)
        return self.im.crop(box)

    def set_2_value(self):
        '''
        set image to two value, 0 black, 255 white
        :return:None
        '''

        self.load()
        self.im = self.im.point(lambda i: 0 if (i < 80) else 255)
        # for x in range(1, self.size[0] - 1):
        #     for y in range(1, self.size[1] - 1):
        #         print(x, y)

    def show(self):
        self.im.show()

    def test(self):
        # Image.blend
        pass



class Cut:
    pass

class Read:
    pass


if __name__ == '__main__':
    im = open('0AFO9PP5Q1 ')
    im_obj = Pure(im)
    im_obj.crop((5, 5, 60, 22))
    im_obj.show()
    im_obj.set_2_value()
    im_obj.show()
