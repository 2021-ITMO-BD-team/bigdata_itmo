#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 12:25:11 2021
@author: chaitanya
"""

import cv2
import pafy
import os
from datetime import datetime
import sys
import glob
# directory = '/home/Documents/python/frames_from_liveVideo/images'


class frames:
    def __init__(self, source_url, quality = False, channelName='channel'):
        self.source_url = source_url
        self.vPafy = pafy.new(self.source_url)
        self.channelName = channelName
        if quality:
            self.play = self.vPafy.getbest(preftype="mp4")
        else:
            self.play = self.vPafy.streams[0]

        self.url = self.play.url

    def saveFrames(self, n=5):
        vid = cv2.VideoCapture(self.url)
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        frame_number = 0
        img_count = 1
        print(fps)
        while True:
            # frame_number += n * fps
            # vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            check, frame = vid.read()
            if check:
                time = str(datetime.now())
                name = self.channelName + '_' + time + '_' + str(img_count) + '.jpg'
                print('Creating...' + name)
                # os.chdir(directory)
                cv2.imwrite(name, frame)
                img_count += 1
        vid.release()
        cv2.destroyAllWindows()

    def saveVideo(self):
        img_array = []
        dir = os.getcwd()
        # os.chdir(directory)
        for filename in sorted(glob.glob(dir+'/*.jpg')):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        out = cv2.VideoWriter(self.channelName+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        
    
    
if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=UUxkVYP36gA&ab_channel=AajTak'
    video = frames(url, channelName='aaj')
    key = int(input('Enter 0 for saving images \nEnter 1 for creating vid: '))
    if key == 0:
        try:
            video.saveFrames()
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
    else:
        video.saveVideo()
