"""
Load the 'nii' file and save as pkl file.
Carefully check your path please.
"""

import pickle
import os
import numpy as np
import nibabel as nib
from utils import Parser
import glob

args = Parser()
modalities = ('flair', 't1ce', 't1', 't2')


train_set = {
        'root': './data2/BraTS_2018/train/LGG',
        'flist': 'all2.txt',
        }

valid_set = {
        'root': "./data2/BraTS_2018/BraTS_2018/valid",
        'flist': 'valid.txt',
        }

test_set = {
        'root': "./data2/BraTS_2018/MICCAI_BraTS2018_TestingData_gz/",
        'flist': 'test.txt',
        }

pkl_save_path = './data2/BraTS_2018/pkg'


def nib_load(file_name):
    if not os.path.exists(file_name):
        return np.array([1])

    proxy = nib.load(file_name)
    data = proxy.get_fdata()
    proxy.uncache()
    return data


def normalize(image, mask=None):
    assert len(image.shape) == 3 # shape is [H,W,D]
    assert image[0,0,0] == 0 # check the background is zero
    if mask is not None:
        mask = (image>0) # The bg is zero

    mean = image[mask].mean()
    std = image[mask].std()
    image = image.astype(dtype=np.float32)
    image[mask] = (image[mask] - mean) / std
    return image


def savepkl(data,path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def process_f32(path):
    """ Set all Voxels that are outside of the brain mask to 0"""
    label = np.array(nib_load(path + '_' + 'seg.nii.gz'), dtype='uint8', order='C')
    images = np.stack([
        np.array(nib_load(path + '_' + modal + '.nii.gz'), dtype='float32', order='C')
        for modal in modalities], -1)
    # print ([(path + '_' + modal + '.nii.gz') for modal in modalities])

    mask = images.sum(-1) > 0
    for k in range(4):
        x = images[..., k] #
        y = x[mask] #
        
        lower = np.percentile(y, 0.2)
        upper = np.percentile(y, 99.8)
        
        x[mask & (x < lower)] = lower
        x[mask & (x > upper)] = upper

        y = x[mask]

        x -= y.mean()
        x /= y.std()

        images[..., k] = x

    output = pkl_save_path + '/' + path.split('/')[-1] + '_data_f32.pkl'
    print("saving:",output)
    savepkl(data=(images, label),path=output)


def doit(dset):
    root = dset['root']
    paths = glob.glob(os.path.join(root, "Brats18*"))
    for path in paths:
        print(path+'/'+(path.split('/')[-1]))
        break
        # process_f32(path+'/'+(path.split('/')[-1]))
        #process_f32(root + path.split('/')[-1] + '/' + path.split('/')[-1])
        

doit(train_set)
# doit(valid_set)
# doit(test_set)



