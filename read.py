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


class Read:
    '''
    Purify picture, remove noise dot.
    '''

    def __init__(self, im):
        '''
        Init
        :param im: image file object (Image object).
        '''

        self.im = im.convert('L')
        self.size = self.im.size
        self.ch_list = [] # character image

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

        self.size = self.im.size
        self.im = self.im.point(lambda i: 0 if (i < value) else 255)

    def denoising(self):
        '''
        remove noise dot.
        :return:
        '''

        self.size = self.im.size

        # remove the noise in the frame of image
        for i in range(self.size[0]):
            self.im.putpixel((i, 0), 255)
            self.im.putpixel((i, self.size[1]-1), 255)
        for j in range(self.size[1]):
            self.im.putpixel((0, j), 255)
            self.im.putpixel((self.size[0]-1, j), 255)

        # remove single noise
        px = self.im.load()
        for i in range(1, self.size[0]-1):
            for j in range(1, self.size[1]-1):
                if px[i,j] == 0:
                    if px[i, j-1] == 255 and \
                       px[i, j+1] == 255 and \
                       px[i-1, j] == 255 and \
                       px[i+1, j] ==255:
                        self.im.putpixel((i, j), 255)
                    elif px[i + 1, j] == 0 and \
                          px[i + 2, j] == 255 and \
                          px[i + 1, j + 1] == 255 and \
                          px[i + 1, j - 1] == 255 and \
                          px[i, j + 1] == 255 and \
                          px[i, j - 1] == 255 and \
                          px[i - 1, j] == 255:
                        self.im.putpixel((i, j), 255)
                        self.im.putpixel((i + 1, j), 255)
                    elif px[i, j + 1] == 0 and \
                          px[i, j + 2] == 255 and \
                          px[i + 1, j + 1] == 255 and \
                          px[i - 1, j + 1] == 255 and \
                          px[i + 1, j] == 255 and \
                          px[i - 1, j] == 255 and \
                          px[i, j - 1] == 255:
                        self.im.putpixel((i, j), 255)
                        self.im.putpixel((i, j + 1), 255)

    def cut(self):
        '''
        sperate each character
        :return:
        '''

        px = self.im.load()

        # get character 'x' coordinate
        x_list = []
        for i in range(1, self.size[0]-1):
            for j in range(1, self.size[1]-1):
                if px[i,j] == 0:
                    x_list.append(i)
                    break

        if len(x_list) < 10:
            raise Exception('no character detected')

        c = []
        c.append(x_list[0])
        for k in range(1,len(x_list)-1):
            if x_list[k - 1] + 1 != x_list[k]:
                c.append(x_list[k - 1])
                c.append(x_list[k])
        c.append(x_list[-1])

        if len(c) % 2 != 0:
            raise Exception('bad image')

        w = self.size[1]
        ch_list = []
        for h in range(0, len(c), 2):
            x = c[h]
            y = c[h + 1]+1
            ch_list.append(self.im.crop((x, 0, y, w)))

        for ch in ch_list:
            ch_px = ch.load()
            ch_size = ch.size
            l = ch_size[0]
            y_list = []
            for j in range(ch_size[1]):
                for i in range(ch_size[0]):
                    if ch_px[i, j] == 0:
                        y_list.append(j)
                        break
            x = y_list[0]
            y = y_list[-1]+1
            self.ch_list.append(ch.crop((0, x, l, y)))

        n = len(self.ch_list)
        if n < 4:
            self.separate(n)
        elif n > 4:
            raise Exception('more than 4 characters, must be wrong')

    def separate(self, n):
        for i in range(n):
            size = self.ch_list[i].size
            int(size[0] / 10)
        pass

    def show(self):
        self.im.show()


if __name__ == '__main__':
    im = open('sample/qiangzhi/ZRQBPXOGRQ')
    im_obj = Read(im)
    # im_obj.show() # original picture in 'L' mode
    im_obj.crop((5, 5, 65, 22))
    # im_obj.show() # crop characters region
    im_obj.binaryzation(100)
    # im_obj.show() # set to 2 value
    im_obj.denoising()
    # im_obj.show() # after denoiseing
    im_obj.cut()
