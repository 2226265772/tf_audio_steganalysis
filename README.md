# Audio Steganalysis with CNN
@ author: Wang Yuntao <br>
## Necessary Package
tensorflow-gpu==1.3 or 1.4, numpy, matplotlib

## CNN Architecture (To be perfected)

## Steganographic Algorithm
HCM(Huffman Code Mapping) and EECS(Equal Length Entropy Codes Substitution)

## dataset
The dataset url is https://pan.baidu.com/s/1ZRkfQTBXg4qMrASR_-ZBSQ <br>
the *extraction password* is "**1fzi**"


## file description
ID      |   File                    |   Function
:-      |   :-                      |    :-
1       |   audio_preprocess.py     |   include some pre-process methods for **audio**
2       |   text_preprocess.py      |   include some pre-process methods for **test**
3       |   image_preocess.py       |   include some pre-process methods for **image** 
4       |   file_preprocess.py      |   get the name, size and type of the **file**
5       |   pre_process.py          |   some pre-processing method such as **truncation**, **down_sampling**
6       |   classifier.py           |   machine learning classifiers such as **SVM**, **KNN**, and **model selection**, **ROC** plot, etc.
7       |   config.py               |   **command parser** and some package management
8       |   filters.py              |   some **filters** used for pre-processing such as kv kernel or other **rich model**
9       |   main.py                 |   the main program
10      |   manager.py              |   **GPU** management (free GPU selection **automatically**)
11      |   layer.py                |   basic unit in CNN such as **conv layer**, **pooling layer**, **BN layer** and so on
12      |   network.py              |   various networks including **VGG19**, **LeNet** and **ourselves' network**
13      |   run.py                  |   the **train** and **test** of the network
14      |   utils.py                |   some useful tools such as **minibatch**, **get_model_info**, **get_weights**, **get_biases** and so on
15      |   TODO                    |   to do list
16      |   model                   |   model files Folder
17      |   label.txt               |   label file if batch test


## Run
* install **python3.x** and add the path into environment variable
* GPU run enviroment configure if train the network (optional)
* pip install **tensorflow==1.3 or later, numpy, scikit-image, pydub** (depend on FFmpeg, optional)
* run the code as the example as follows

## Command Parser
Command: python3 main.py --argument 1 --argument 2 ... --argument N <br>


## The description of each network
*  **network for audio steganalysis**

        network1  : The proposed network (最终选定的网络)
        network1_1: Remove all BN layers (去掉所有BN层)
        network1_2: Average pooling layer is used for subsampling (将所有的降采样方式改为平均池化方式)
        network1_3: Convolutional layer with stride 2 is used for subsampling (将所有的降采样方式改为卷积池化方式)
        network1_4: Replace the convolutional kernel with 5x5 kernel (将卷积核尺寸由3 x 3改为5 x 5)
        network1_5: ReLu is used as the activation function (将激活函数由Tanh改为ReLu)
        network1_6: Leaky-ReLu is used as the activation function (将激活函数由tanh改为Leaky-ReLu)
        network1_7: Deepen the network to block convolution layers (加深网络)
        network1_8: Design a network to steganalyze audios of arbitrary size (解决可变尺寸输入数据的训练问题)
        network1__1: Remove the BN layer in the first group (去除第一个卷积块中的BN层)
        network1__2: Remove the BN layers in the first two groups (去除前两个卷积块中的BN层)
        network1__4: Remove the BN layers in the first four groups (去除前四个卷积块中的BN层)

        Note: HPF and ABS is applied at the pre-processing
    
* network for image steganalysis
    
        stegshi   : Xu-Net

    
## The method of pre-processing
    
There are positive and negative values in QMDCT coefficients matrix. The values in interval **[-15, 15]** is modified.
The ratio of values in [-15, 15] is more than **99\%**, as the figure shown.
* Abs
* Truncation
* Down-sampling

## Reference
    [1] Yanzhen Ren, Qiaochu Xiong, and Lina Wang. 2017. A Steganalysis Scheme for AAC Audio Based on MDCT Difference Between Intra and Inter Frame. In Digital Forensics and Watermarking - 16th International Workshop, IWDW 2017, Magdeburg, Germany, August 23-25, 2017, Proceedings. 217–231.
    [2] Chao Jin, Rangding Wang, and Diqun Yan. 2017. Steganalysis of MP3Stego with low embedding-rate using Markov feature. Multimedia Tools and Applications 76, 5 (2017), 6143–6158.