import time
import pandas as pd
import os
import numpy as np
from p_tqdm import p_map
from PIL import Image
from functools import partial

#from setuptools.package_index import unique_values


def linear_distance(row, df):
    # Extract RGB training data and labels from the dataframe
    df= df.dropna()
    df= df.reset_index(drop= True)
    X = df[['R', 'G', 'B']].to_numpy()
    labels = df['Class'].to_numpy()

    row_labels = []
    for rgb in row:
        distances = np.linalg.norm(X - rgb, axis=1)
        min_index = np.argmin(distances)
        row_labels.append(labels[min_index])  # Append nearest label

    return row_labels

def main():
    # === Input paths ===
    image_path = r"C:\Users\mmgia\OneDrive\Documents\Geog199SS\images\DSC00482.JPG"
    csv_path = r"C:\Users\mmgia\PycharmProjects\WonderpoleImgClassifier\DSC00482.JPG_classified.csv"

    # === Load image and training data ===
    df_class = pd.read_csv(csv_path)
    image = Image.open(image_path)
    img_data = np.array(image)

    refpoints = df_class[['X', 'Y']]
    print(refpoints)

    # === Classify all pixels using parallel processing ===
    results = p_map(partial(linear_distance, df=df_class), img_data)

    # === Build a color image based on classification ===
    class_to_color = {
        "GV": 1,   # Green
        "NPV": 2,  # Red
        "Soil": 3  # Blue
    }

    color_to_class = {
        1:"GV",
        2:"NPV",
        3:"Soil"
    }


    height, width = len(results), len(results[0])
    classified_image = np.zeros((height, width))

    for y, row in enumerate(results):
        for x, label in enumerate(row):
             classified_image[y, x] = class_to_color[label]

    refpoints = df_class[['X', 'Y']].to_numpy()
    print(refpoints.shape)

    for _row, row in enumerate(refpoints):
        classified_image[int(row[1]), int(row[0])] = np.nan

    # get frac cover inf0
    unique_vals, counts = np.unique(classified_image, return_counts=True)

    for val, count in zip(unique_vals, counts):
        print(f"{color_to_class[int(val)]}  appears {count}. fraction = {count/(height * width)}" )
    # Display and save the result ===
   # classified_img = Image.fromarray(classified_image)
    #classified_img.show()  # View the image
    #output_path = os.path.splitext(image_path)[0] + "_classifiedimg.png"
    #classified_img.save(output_path)
    #print(f"Classified image saved to: {output_path}")

if __name__ == '__main__':
    main()

