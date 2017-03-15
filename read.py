#coding=utf-8

import os, sys
from PIL import Image, ImageFilter
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

    def binaryzation(self, value=80):
        '''
        set image to two value, 0 black, 255 white
        :return:None
        '''

        self.load()
        self.im = self.im.point(lambda i: 0 if (i < value) else 255)

    def denoising(self):
        '''
        remove noise dot.
        :return:
        '''

        self.load()
        px = self.im.load()

        # for i in range(self.size[0]):
        #     for j in range(self.size[1]):
        #         print(px[i, j])

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
    im = open('sample/qiangzhi/MZWW7PC4JI')
    im_obj = Pure(im)
    # im_obj.show() # original picture in 'L' mode
    im_obj.crop((5, 5, 65, 22))
    # im_obj.show() # crop characters region
    im_obj.binaryzation(100)
    # im_obj.show() # set to 2 value
    im_obj.denoising()
