# 15112 Project 
Age Prophet

## Pre-requisites
* Python 3.7 or 3.6.7
* Scipy 1.2.0
* kivy 1.10.1
* keras 2.2.4
* TensorFlow 1.10.0
* opencv 3.4.1
* dlib 19.4
* numpy 1.15.4
* pillow 5.2.0


## Trainning 
* Trainning has been done for you
* Please download pre-trained model at https://drive.google.com/open?id=1e-ViGd__dkAwvzf4RVv9uE-4_pq2KmrK unzip and put two models into the same directory.

## Running the App
* Once the trainned models have been downloaded, and the working environment has been setted up,  you could start running your kivyMain.py to try.  

## Project Description
* This is a course project for 15112. Age Prophet is an app that will take a picture of you and tell what you look like right now. You can also know what you look like in to next 4 years, 8 years, 12 years and 16 years. In addition, you can invite your friend to see how old they look and what they will look like in the future. 

## Files
* kivyMain.py is the main file for the app, it would call other files such as ageEstimation.py, ageProgression.py. All the images are saved in the images folder including cropped image for age progression.
* imageScale.txt is used to store the face position and used for replace face during age-progression
* all .ttf files are used for font


## Citations
[1]:[Zhifei Zhang](http://web.eecs.utk.edu/~zzhang61/), [Yang Song](http://web.eecs.utk.edu/~ysong18/), and [Hairong Qi](https://www.eecs.utk.edu/people/faculty/hqi/). "Age Progression/Regression by Conditional Adversarial Autoencoder." *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2017.

[2]:[Face Aging with Identity-Preserved Conditional Generative Adversarial Networks, CVPR 2018](http://openaccess.thecvf.com/content_cvpr_2018/papers/Wang_Face_Aging_With_CVPR_2018_paper.pdf) by Zongwei Wang, Xu Tang, Weixin Luo and Shenghua Gao. 

[3]:Face Age Progression Source:(https://github.com/dawei6875797/Face-Aging-with-Identity-Preserved-Conditional-Generative-Adversarial-Networks.git)

[4]: Face Age and Detection Source:(https://github.com/yu4u/age-gender-estimation.git)

[5]: Image Data Generator Source: (https://github.com/joelthchao/tensorflow-finetune-flickr-style.git)

[6]: Kivy API: (https://kivy.org/doc/stable/api-index.html)

[7]: ops.py Code modification of (http://stackoverflow.com/a/33950177)

