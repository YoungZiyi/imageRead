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

        self.ch_list = []
        self.ch_list = self.remove_white_in_y(ch_list)

        n = len(self.ch_list)
        if n < 4:
            self.ch_list = self.separate(n)
        elif n > 4:
            raise Exception('more than 4 characters, must be wrong')
        for u in self.ch_list:
            u.show()

    def remove_white_in_y(self, ch_list):
        '''
        remove the blank row in y direction
        :param ch_list: a list of characters image
        :return: c_list
        '''

        c_list = []
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
            c_list.append(ch.crop((0, x, l, y)))
        return c_list

    def separate(self, n):
        '''
        n is the number of pictures in self.ch_lsit
        :param n:
        :return: the character image list
        '''
        c_list = []
        for i in range(n):
            size = self.ch_list[i].size
            c = int(size[0] / 10)
            if c == 0: c = 1
            sx = int(size[0] / c)
            n = 1
            while(c >= 1):
                if c == 1:
                    c_im = self.ch_list[i].crop(  (  (n - 1) * sx, 0, size[0], size[1]  )  )
                else:
                    c_im = self.ch_list[i].crop( ((n - 1) * sx, 0, n * sx + 1, size[1])  )
                c_list.append(c_im)
                n = n + 1
                c = c - 1

        if len(c_list) == 4:
            c_list = self.remove_white_in_y(c_list)
            if len(c_list) == 4:
                return c_list
        return []

    def show(self):
        self.im.show()


if __name__ == '__main__':
    im = open('sample/qiangzhi/S18C0HOMEW')
    im_obj = Read(im)
    # im_obj.show() # original picture in 'L' mode
    im_obj.crop((5, 5, 65, 22))
    # im_obj.show() # crop characters region
    im_obj.binaryzation(100)
    # im_obj.show() # set to 2 value
    im_obj.denoising()
    # im_obj.show() # after denoiseing
    im_obj.cut()
