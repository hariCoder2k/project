"""
The code will split the training set into k-fold for cross-validation
"""

import os
from sklearn.model_selection import StratifiedKFold, KFold
import numpy as np

root = '/content/drive/MyDrive/data/BraTS_2018/Train'
valid_txt_dir = './content/drive/MyDrive/data/BraTS_2018/Valid'
valid_data_dir = '/content/drive/MyDrive/data/BraTS_2018/Valid'


def write(data, fname, root=root):
    fname = os.path.join(root, fname)
    with open(fname, 'w') as f:
        f.write('\n'.join(data))
  

hgg = os.listdir(os.path.join(root, 'HGG'))
hgg = [os.path.join('HGG', f) for f in hgg]
lgg = os.listdir(os.path.join(root, 'LGG'))
lgg = [os.path.join('LGG', f) for f in lgg]

X = hgg + lgg
Y = [1]*len(hgg) + [0]*len(lgg)

write(X, 'all.txt')

X, Y = np.array(X), np.array(Y)

kf = KFold(n_splits=5, shuffle=True, random_state=2020)


for k, (train_index, valid_index) in enumerate(kf.split(X, Y)):
    train_list = list(X[train_index])
    valid_list = list(X[valid_index])

    write(train_list, 'train_{}.txt'.format(k), root)
    write(valid_list, 'valid_{}.txt'.format(k), root)


