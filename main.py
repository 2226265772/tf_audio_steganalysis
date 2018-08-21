#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017.11.16
Finished on 2017.12.19
@author: Wang Yuntao
"""

import os
from run import *
from manager import *
import tensorflow as tf
from config import command_parse


def main():
    # command parsing
    arguments = command_parse()

    if arguments.gpu_selection == "auto":
        gm = GPUManager()
        gpu_index = gm.auto_choice()
        if not gpu_index == -1:
            os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = arguments.gpu

    run_mode(arguments)


if __name__ == "__main__":
    main()
