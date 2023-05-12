# load all the gestures saved in ./guestures

import os
from typing import Dict, List

import numpy as np

from grid import Point
from save_load_points import load_points

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use the 'Agg' backend

from PIL import Image

def plot_prediction_percentages(pred_perct: Dict[str, np.ndarray]) -> None:
    """ Plots the prediction percentages """
    gesture_labels = list(pred_perct.keys())
    prediction_percentages: list[float] = list(pred_perct.values())
    # start the axis at min + 0.1 

    plt.bar(gesture_labels, prediction_percentages)
    plt.ylim( min(prediction_percentages) - 0.1 )
    plt.xlabel('Gesture')
    plt.ylabel('Prediction Percentage')

    # This is used so that the matplot lib doesn't shrink the pygame window
    plt.savefig('temp_prediction_percentages.png')
    # show the image using python default library 
    img = Image.open('temp_prediction_percentages.png')
    img.show()


def load_all_gestures() -> Dict[ str, List[Point]]:
    """ Loads all the gestures saved in ./guestures """
    guestures = {}
    for file_name in os.listdir('./guestures'):
        if file_name.endswith('.txt'):
            file_name_without_extension = file_name[:-4]
            guestures[file_name_without_extension] = load_points(file_name_without_extension)
    return guestures

# create a ml model to predict the gesture 
def predict(gesture: List[Point]) -> str:
    """ Predicts the gesture from the gesture points """
    guestures = load_all_gestures()
    score_dict = {}
    for name, points in guestures.items():
        score_dict[name] = score(points, gesture)

    plot_prediction_percentages(score_dict)
    return max(score_dict, key= lambda key: score_dict[key] )

def score(p1: List[Point], p2: List[Point]) -> float:
    """ Scores the similarity between two gestures """

    # pad the vectors to be the same length
    if len(p1) > len(p2):
        p2 += [(0, 0)] * (len(p1) - len(p2))
    elif len(p2) > len(p1):
        p1 += [(0, 0)] * (len(p2) - len(p1))

    # calculate the score using dot product
    # score = 0
    # for i in range(len(p1)):
    #     score += p1[i][0] * p2[i][0] + p1[i][1] * p2[i][1]
    # return score

    A = np.array(p1).reshape(1, -1)
    B = np.array(p2).reshape(1, -1)

    # cosine similarity
    return (np.dot(A, B.T) / (np.linalg.norm(A) * np.linalg.norm(B)))[0][0] # unpacking to make it a float