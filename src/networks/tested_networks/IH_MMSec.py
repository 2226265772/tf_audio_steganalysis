#!/usr/bin/env python3
# -*- coding: utf-8 -*-33

"""
Created on 2018.09.25
Finished on 2018.09.25
Modified on

@author: Wang Yuntao
"""

from layer import *
from filters import *

"""
    function:
        all versions are modified on the basis of wasdn
        
        wasdn1_1: Remove the BN layer
        wasdn1_2: Average pooling layer is used for subsampling
        wasdn1_3: Convolutional layer with stride 2 is used for subsampling
        wasdn1_4: Replace the convolutional kernel with 5x5 kernel
        wasdn1_5: ReLu is used as the activation function
        wasdn1_6: Leaky-ReLu is used as the activation function
        wasdn1_7: Deepen the network to block convolutional layers
        wasdn1_8: Remove the 1x1 convolutional layers
        wasdn1_9: Remove the HPF layer
        wasdn2_1: Remove the first BN layer in the first group
        wasdn2_2: Remove the first BN layers in the first two groups
        wasdn2_3: Remove the first BN layers in the first four groups
"""


def wasdn1_1(input_data, class_num=2, is_bn=False, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    remove the batch normalization
    """
    print("WASDN1_1: Remove the BN layer")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=is_bn)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=is_bn)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=is_bn)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_2(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=False):
    """
    Average pooling layer is used for subsampling
    """
    print("WASDN1_2: replace the max pooling layer with the average pooling layer")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_3(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=False):
    """
    Convolutional layer with stride 2 is used for subsampling
    """
    print("WASDN1_3: replace the max pooling layer with the convolutional pooling layer")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    conv1_4 = conv_layer(bn1_3, 3, 3, 2, 2, 16, name="conv1_4", activation_method="None", padding="VALID")

    # Group2
    conv2_1 = conv_layer(conv1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    conv2_4 = conv_layer(bn2_3, 3, 3, 2, 2, 64, name="conv2_4", activation_method="None", padding="VALID")

    # Group3
    conv3_1 = conv_layer(conv2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, "conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    conv3_3 = conv_layer(bn3_3, 3, 3, 2, 2, 128, name="conv3_4", activation_method="None", padding="VALID")

    # Group4
    conv4_1 = conv_layer(conv3_3, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method="tanh", is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method="tanh", is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_4(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Replace the convolutional kernel with 5x5 kernel
    """
    print("WASDN1_4: replace the 3 x 3 kernel with the 5 x 5 kernel")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 5, 5, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 5, 5, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 5, 5, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 5, 5, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 5, 5, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 5, 5, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc11", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN12", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc13", activation_method=None)

    return logits


def wasdn1_5(input_data, class_num=2, is_bn=True, activation_method="relu", padding="SAME", is_max_pool=True):
    """
    ReLu is used as the activation function
    """
    print("WASDN1_5: use relu as the activation function")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_6(input_data, class_num=2, is_bn=True, activation_method="leakrelu", padding="SAME", is_max_pool=True):
    """
    Leaky-ReLu is used as the activation function
    """
    print("WASDN1_6: use leakrelu as the activation function")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_7(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Deepen the network to block convolutional layers
    """
    print("WASDN1_7: Deepen the network to 7 groups.")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Group7
    conv7_1 = conv_layer(pool6_4, 3, 3, 1, 1, 1024, name="conv7_1", activation_method=activation_method, padding=padding)
    conv7_2 = conv_layer(conv7_1, 1, 1, 1, 1, 2048, name="conv7_2", activation_method=None, padding=padding)
    bn7_3 = batch_normalization(conv7_2, name="BN7_3", activation_method=activation_method, is_train=is_bn)
    pool7_4 = pool_layer(bn7_3, 2, 2, 2, 2, name="pool7_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc8 = fc_layer(pool7_4, 4096, name="fc8", activation_method=None)
    bn9 = batch_normalization(fc8, name="BN9", activation_method=activation_method, is_train=is_bn)
    fc10 = fc_layer(bn9, 512, name="fc10", activation_method=None)
    bn11 = batch_normalization(fc10, name="BN11", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn11, class_num, name="fc12", activation_method=None)

    return logits


def network1_8(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Remove the 1x1 convolutional layers
    """
    print("WASDN1_8: Remove the 1x1 conv layers.")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    bn1_2 = batch_normalization(conv1_1, name="BN1_2", activation_method=activation_method, is_train=False)
    pool1_3 = pool_layer(bn1_2, 2, 2, 2, 2, name="pool1_3", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_3, 3, 3, 1, 1, 32, name="conv2_1", activation_method=None, padding=padding)
    bn2_2 = batch_normalization(conv2_1, name="BN2_2", activation_method=activation_method, is_train=False)
    pool2_3 = pool_layer(bn2_2, 2, 2, 2, 2, name="pool2_3", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_3, 3, 3, 1, 1, 64, name="conv3_1", activation_method=None, padding=padding)
    bn3_2 = batch_normalization(conv3_1, name="BN3_2", activation_method=activation_method, is_train=False)
    pool3_3 = pool_layer(bn3_2, 2, 2, 2, 2, name="pool3_3", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_3, 3, 3, 1, 1, 128, name="conv4_1", activation_method=None, padding=padding)
    bn4_2 = batch_normalization(conv4_1, name="BN4_2", activation_method=activation_method, is_train=is_bn)
    pool4_3 = pool_layer(bn4_2, 2, 2, 2, 2, name="pool4_3", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_3, 3, 3, 1, 1, 256, name="conv5_1", activation_method=None, padding=padding)
    bn5_2 = batch_normalization(conv5_1, name="BN5_2", activation_method=activation_method, is_train=is_bn)
    pool5_3 = pool_layer(bn5_2, 2, 2, 2, 2, name="pool5_3", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_3, 3, 3, 1, 1, 512, name="conv6_1", activation_method=None, padding=padding)
    bn6_2 = batch_normalization(conv6_1, name="BN6_2", activation_method=activation_method, is_train=is_bn)
    pool6_3 = pool_layer(bn6_2, 2, 2, 2, 2, name="pool6_3", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_3, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method="tanh", is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method="tanh", is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn1_9(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Remove the HPF layer
    """
    print("WASDN1_9: Replace the max pooling layer with the average pooling layer")
    print("Network Structure: ")

    # Group1
    conv1_1 = conv_layer(input_data, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method=activation_method, is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method=activation_method, is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn2_1(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Remove the BN layer in the first group
    """
    print("WASDN2_1: Remove the BN layer in the first group")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=is_bn)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=is_bn)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method="tanh", is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method="tanh", is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn2_2(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Remove the BN layer in the first two groups
    """
    print("WASDN2_2: Remove the BN layers in the first  groups")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=is_bn)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=is_bn)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method="tanh", is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method="tanh", is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits


def wasdn2_3(input_data, class_num=2, is_bn=True, activation_method="tanh", padding="SAME", is_max_pool=True):
    """
    Remove the BN layer in the first four groups
    """
    print("WASDN2_3: Remove the BN layers in the first four groups")
    print("Network Structure: ")

    # preprocessing
    data_diff = diff_layer(input_data, is_diff=True, is_diff_abs=False, is_abs_diff=False, order=2, direction="inter", name="difference")

    # Group1
    conv1_1 = conv_layer(data_diff, 3, 3, 1, 1, 16, name="conv1_1", activation_method=activation_method, padding=padding)
    conv1_2 = conv_layer(conv1_1, 1, 1, 1, 1, 32, name="conv1_2", activation_method=None, padding=padding)
    bn1_3 = batch_normalization(conv1_2, name="BN1_3", activation_method=activation_method, is_train=False)
    pool1_4 = pool_layer(bn1_3, 2, 2, 2, 2, name="pool1_4", is_max_pool=is_max_pool)

    # Group2
    conv2_1 = conv_layer(pool1_4, 3, 3, 1, 1, 32, name="conv2_1", activation_method=activation_method, padding=padding)
    conv2_2 = conv_layer(conv2_1, 1, 1, 1, 1, 64, name="conv2_2", activation_method=None, padding=padding)
    bn2_3 = batch_normalization(conv2_2, name="BN2_3", activation_method=activation_method, is_train=False)
    pool2_4 = pool_layer(bn2_3, 2, 2, 2, 2, name="pool2_4", is_max_pool=is_max_pool)

    # Group3
    conv3_1 = conv_layer(pool2_4, 3, 3, 1, 1, 64, name="conv3_1", activation_method=activation_method, padding=padding)
    conv3_2 = conv_layer(conv3_1, 1, 1, 1, 1, 128, name="conv3_2", activation_method=None, padding=padding)
    bn3_3 = batch_normalization(conv3_2, name="BN3_3", activation_method=activation_method, is_train=False)
    pool3_4 = pool_layer(bn3_3, 2, 2, 2, 2, name="pool3_4", is_max_pool=is_max_pool)

    # Group4
    conv4_1 = conv_layer(pool3_4, 3, 3, 1, 1, 128, name="conv4_1", activation_method=activation_method, padding=padding)
    conv4_2 = conv_layer(conv4_1, 1, 1, 1, 1, 256, name="conv4_2", activation_method=None, padding=padding)
    bn4_3 = batch_normalization(conv4_2, name="BN4_3", activation_method=activation_method, is_train=False)
    pool4_4 = pool_layer(bn4_3, 2, 2, 2, 2, name="pool4_4", is_max_pool=is_max_pool)

    # Group5
    conv5_1 = conv_layer(pool4_4, 3, 3, 1, 1, 256, name="conv5_1", activation_method=activation_method, padding=padding)
    conv5_2 = conv_layer(conv5_1, 1, 1, 1, 1, 512, name="conv5_2", activation_method=None, padding=padding)
    bn5_3 = batch_normalization(conv5_2, name="BN5_3", activation_method=activation_method, is_train=is_bn)
    pool5_4 = pool_layer(bn5_3, 2, 2, 2, 2, name="pool5_4", is_max_pool=is_max_pool)

    # Group6
    conv6_1 = conv_layer(pool5_4, 3, 3, 1, 1, 512, name="conv6_1", activation_method=activation_method, padding=padding)
    conv6_2 = conv_layer(conv6_1, 1, 1, 1, 1, 1024, name="conv6_2", activation_method=None, padding=padding)
    bn6_3 = batch_normalization(conv6_2, name="BN6_3", activation_method=activation_method, is_train=is_bn)
    pool6_4 = pool_layer(bn6_3, 2, 2, 2, 2, name="pool6_4", is_max_pool=is_max_pool)

    # Fully connected layer
    fc7 = fc_layer(pool6_4, 4096, name="fc7", activation_method=None)
    bn8 = batch_normalization(fc7, name="BN8", activation_method="tanh", is_train=is_bn)
    fc9 = fc_layer(bn8, 512, name="fc9", activation_method=None)
    bn10 = batch_normalization(fc9, name="BN10", activation_method="tanh", is_train=is_bn)

    logits = fc_layer(bn10, class_num, name="fc11", activation_method=None)

    return logits
