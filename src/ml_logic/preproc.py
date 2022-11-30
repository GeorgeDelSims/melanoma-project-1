
import os
import shutil
from pathlib import Path

import albumentations as A
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
from imblearn.over_sampling import SMOTE
from PIL import Image
from tensorflow.keras.utils import image_dataset_from_directory, to_categorical

from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

def move_images():
    '''
    Moves images from training set into 9 different folders, named according to the target category of each image.
    Args: None
    Returns: None
    '''
    df = pd.read_csv(os.environ.get('TARGET_CSV_PATH'))
    df.set_index('image')
    for source in df.index:
        for column in df.columns:
            if df.loc[source][column] == 1:
                source_path = os.environ.get('ORIGINAL_IMAGE_PATH')
                destination_path = os.environ.get('IMAGE_DATA_PATH')
                shutil.move(source_path, destination_path)


def load_images():
    '''
    Loads images from various categorical folders
    Transforms them into Numpy arrays and then dataframes
    Adds "image_name" as X feature and origin folder as y feature.

    Args: None

    Returns: Dataframe

    '''
    classes = {'MEL':0, 'NV':1,
                'BCC':2, 'AK' : 3,
                'BKL' : 4, 'DF' : 5,
                'VASC' : 6, 'SCC' : 7,
                'UNK' : 8}
    data_path = os.environ.get('DATA_PATH')


    for (cl, i) in classes.items():
        break
    pass


def augmentation_pipeline(img):

    '''
    Augments image data by random cropping, horizontal flipping and changing the brightness contrast.

    Args: img (numpy array)

    returns: image (numpy array)
    '''

    img = A.Compose([
    A.RandomCrop(width=256, height=256),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),])
    return img['image']


def normalise(img):
    '''
    Normalises images to values between 0 and 1.

    Args: img (numpy array)

    returns: img (numpy array)
    '''

    norm_img = np.zeros((256,256))
    normalised_img = cv.normalize(img,  norm_img, 0.00, 1.00)
    return normalised_img


def balance_data(X):
    '''
    Function that balances the dataset by adding weights to the under-represented classes.

    '''
    sampling_amount = 4522

    X_balanced = SMOTE(X, sampling_strategy={'MEL':sampling_amount,
                                'NV':sampling_amount,
                                'BCC':sampling_amount,
                                'AK' : sampling_amount,
                                'BKL' : sampling_amount,
                                'DF' : sampling_amount,
                                'VASC' : sampling_amount,
                                'SCC' : sampling_amount,
                                'UNK' : sampling_amount},
                                k_neighborsint=5,
                                n_jobs=-1)
    return X_balanced




def image_preprocessing_pipeline():
    '''

    '''



def images_to_dataset():
    '''
    Function that sort and transform images into a tensorflow dataset according to their classes

    Returns: Tensor (but should return Numpy or Dataframe)
    '''
    directory = os.environ.get('IMAGE_DATA_PATH')
    dataset = image_dataset_from_directory(
                                    directory,
                                    labels='inferred',
                                    label_mode='int',
                                    class_names=None,
                                    color_mode='rgb',
                                    batch_size=32,
                                    image_size=(256, 256),
                                    shuffle=True,
                                    seed=None,
                                    validation_split=None,
                                    subset=None,
                                    follow_links=False,
                                    crop_to_aspect_ratio=False,
                                )
    return dataset


def preprocessing_tabulaire():

    """
     Cette function fait preprocessing des données tabulaires

    """
    df = pd.read_csv(Path('..', 'data', 'archive', 'ISIC_2019_Training_Metadata.csv'))
    df = df.dropna(axis=0, how='all', subset=['age_approx', 'anatom_site_general', 'sex'])
    df = df.drop(['lesion_id'], axis=1)
    df.sex.replace(np.nan, "Delete", inplace=True)
    df.anatom_site_general.replace(np.nan, "Delete1", inplace=True)
    imputer = SimpleImputer(strategy="mean")
    imputer.fit(df[['age_approx']])
    df['age_approx'] = imputer.transform(df[['age_approx']])
    df.sex.unique()
    ohe = OneHotEncoder(sparse = False, handle_unknown='ignore')
    ohe.fit(df[['sex']])
    sex_encoded = ohe.transform(df[['sex']])
    df[ohe.categories_[0]] = sex_encoded
    df.anatom_site_general.unique()
    ohe2 = OneHotEncoder(sparse = False, handle_unknown='ignore')
    ohe2.fit(df[['anatom_site_general']])
    anatom_site_general_encoded = ohe2.transform(df[['anatom_site_general']])
    df[ohe2.categories_[0]] = anatom_site_general_encoded
    df = df.drop(columns=['anatom_site_general', 'sex', 'Delete', 'Delete1'])
    y_df = pd.read_csv(Path('..', 'data', 'archive', 'ISIC_2019_Training_GroundTruth.csv'))
    y_df = y_df.set_index('image')
    y_df = y_df.idxmax(axis='columns')
    y_df = y_df.reset_index()
    y_df.columns = ['image', 'target']
    df = df.merge(y_df, how='left', on='image')
    df.set_index('image', inplace = True)

    return df


def get_X_y(df):
    X = df.drop(['target'], axis=1)
    y = df[['target']]
    return X, y
