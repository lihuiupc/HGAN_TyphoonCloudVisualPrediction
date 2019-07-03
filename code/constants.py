import numpy as np
import os
from glob import glob
import shutil
from datetime import datetime
from scipy.ndimage import imread
from skimage.transform import resize
##
# Data
##

def get_date_str():
    """
    @return: A string representing the current date/time that can be used as a directory name.
    """
    return str(datetime.now()).replace(' ', '_').replace(':', '.')[:-10]

def get_dir(directory):
    """
    Creates the given directory if it does not exist.

    @param directory: The path to the directory.
    @return: The path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clear_dir(directory):
    """
    Removes all files in the given directory.

    @param directory: The path to the directory.
    """
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        try:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(e)


def get_test_frame_dims():
    img_path = glob(os.path.join(TEST_DIR, '*/*'))[0]
    img = imread(img_path, mode='RGB')
    #shapeh = int(img.shape[0]/8)
    #shapew = int(img.shape[1]/8)
    #img = resize(img,[shapeh,shapew,3])
    shape = np.shape(img)

    return shape[0], shape[1]


def get_train_frame_dims():
    img_path = glob(os.path.join(TRAIN_DIR, '*/*'))[0]
    img = imread(img_path, mode='RGB')
    shape = np.shape(img)

    return shape[0], shape[1]


def set_test_dir(directory):
    """
    Edits all constants dependent on TEST_DIR.

    @param directory: The new test directory.
    """
    global TEST_DIR, FULL_HEIGHT, FULL_WIDTH

    TEST_DIR = directory
    FULL_HEIGHT, FULL_WIDTH = get_test_frame_dims()

# root directory for all data
DATA_DIR = get_dir('../Data/')
# directory of unprocessed training frames
TRAIN_DIR = os.path.join(DATA_DIR, 'Train/')
# directory of unprocessed test frames
TEST_DIR = os.path.join(DATA_DIR, 'Test/')



# the height and width of the full frames to test on. 
FULL_HEIGHT = 334
FULL_WIDTH = 334
# the height and width of the patches to train on
TRAIN_HEIGHT = 222
TRAIN_WIDTH = 390

##
# Output
##

def set_save_name(name):
    """
    Edits all constants dependent on SAVE_NAME.

    @param name: The new save name.
    """
    global SAVE_NAME, MODEL_SAVE_DIR, SUMMARY_SAVE_DIR, IMG_SAVE_DIR

    SAVE_NAME = name
    MODEL_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Models/', SAVE_NAME))
    SUMMARY_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Summaries/', SAVE_NAME))
    IMG_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Images/', SAVE_NAME))

def clear_save_name():
    """
    Clears all saved content for SAVE_NAME.
    """
    clear_dir(MODEL_SAVE_DIR)
    clear_dir(SUMMARY_SAVE_DIR)
    clear_dir(IMG_SAVE_DIR)


# root directory for all saved content
SAVE_DIR = get_dir('../Save/')

# inner directory to differentiate between runs
SAVE_NAME = 'Default/'
# directory for saved models
MODEL_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Models/', SAVE_NAME))
# directory for saved TensorBoard summaries
SUMMARY_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Summaries/', SAVE_NAME))
# directory for saved images
IMG_SAVE_DIR = get_dir(os.path.join(SAVE_DIR, 'Images/', SAVE_NAME))


STATS_FREQ      = 500    # how often to print loss/train error stats, in # steps
SUMMARY_FREQ    = 500    # how often to save the summaries, in # steps
IMG_SAVE_FREQ   = 500   # how often to save generated images, in # steps
TEST_FREQ       = 500   # how often to test the model on test data, in # steps
MODEL_SAVE_FREQ = 500   # how often to save the model, in # steps

##
# General training
##

# whether to use adversarial training vs. basic training of the generator
ADVERSARIAL = True
# the training minibatch size
BATCH_SIZE = 4
TEST_BATCH_SIZE = 1  
# the number of history frames to give as input to the network
HIST_LEN = 10

##
# Loss parameters
##

# for lp loss. e.g, 1 or 2 for l1 and l2 loss, respectively)
L_NUM = 1
# the power to which each gradient term is raised in GDL loss
ALPHA_NUM = 1

# the percentage of the adversarial loss to use in the combined loss
LAM_ADV = 20
# the percentage of the lp loss to use in the combined loss
LAM_LP = 0.05
# the percentage of the GDL loss to use in the combined loss
LAM_GDL = 0.001
#the percentage of the tv loss to use in the combined loss 
LAM_TV = 0.001

##
# Generator model
##

# learning rate for the generator model
LRATE_G = 5e-5  # Value in paper is 0.04
# padding for convolutions in the generator model
PADDING_G = 'SAME'
# feature maps for each convolution of each scale network in the generator model
# e.g SCALE_FMS_G[1][2] is the input of the 3rd convolution in the 2nd scale network.
SCALE_FMS_G = [[3 * HIST_LEN, 128, 256, 128, 3],
               [3 * (HIST_LEN + 1), 128, 256, 128, 3],
               [3 * (HIST_LEN + 1), 128, 256, 512, 256, 128, 3],
               [3 * (HIST_LEN + 1), 128, 256, 512, 256, 128, 3]]
# kernel sizes for each convolution of each scale network in the generator model
SCALE_KERNEL_SIZES_G = [[3, 3, 3, 3],
                        [5, 3, 3, 15],
                        [5, 3, 3, 3, 3, 5],
                        [7, 5, 5, 5, 5, 7]]


##
# Discriminator model
##

# learning rate for the discriminator model
LRATE_D = 5e-5
# padding for convolutions in the discriminator model
PADDING_D = 'VALID'
# feature maps for each convolution of each scale network in the discriminator model
SCALE_CONV_FMS_D = [[3, 64],
                    [3, 64, 128],#[3, 64, 128, 128],
                    [3, 128, 256, 256],
                    [3, 128, 256, 512, 128]]
# kernel sizes for each convolution of each scale network in the discriminator model
#SCALE_KERNEL_SIZES_D = [[3],
#                        [3, 3, 3],
#                        [5, 5, 5],
#                        [7, 7, 5, 5]]
SCALE_KERNEL_SIZES_D = [[3],
                        [3, 3],
                        [5, 5, 5],
                        [7, 7, 5, 5]]
# layer sizes for each fully-connected layer of each scale network in the discriminator model
# layer connecting conv to fully-connected is dynamically generated when creating the model
SCALE_FC_LAYER_SIZES_D = [[256, 128, 1],
                          [256, 128, 1],
                          [256, 128, 1],
                          [256, 128, 1]]
