#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 2018.08.21
Finished on 2018.08.21
@author: Wang Yuntao
"""

"""
    This script is used for the test of funtion
"""

from audio_preprocess import *

audio_file_path = "E:/Myself/2.database/3.cover/cover_10s/128/wav10s_00001.mp3"

audio = audio_read(audio_file_path)

print(audio)
