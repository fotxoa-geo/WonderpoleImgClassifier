import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import tkinter as tk
from tkinter import ttk, filedialog
import csv

from matplotlib import colors  # This is now safe to keep
from matplotlib.widgets import Button
import os

# Set the number of points to classify
n = 30  # Number of random points

# Define classification options
classification_options = ["GV", "NPV", "Soil"]

# Color mapping for each class
color_map = {"GV": "red", "NPV": "green", "Soil": "blue"}

# Function to save points to CSV
def save_to_csv(event=None):
    file_path = os.path.join(os.getcwd(), f"{image_file}_classified.csv")  # Save per image

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y', 'Class', 'R', 'G', 'B'])  # Including RGB headers

        for (x, y), (r, g, b) in points.items():
            label = point_labels.get((x, y), "Unclassified")
            writer.writerow([x, y, label, r, g, b])

    print(f"CSV file saved as: {file_path}")

# Function to classify a point
def classify_point(closest_point, point_colors):
    def on_select():
        selected_class = combo.get()
        point_labels[closest_point] = selected_class

        # Update color list
        idx = list(points.keys()).index(closest_point)
        point_colors[idx] = color_map[selected_class]
        scatter_plot.set_color(point_colors)  # Update scatter plot colors

        # Update or create annotation
        if closest_point in annotations:
            annotations[closest_point].set_text(selected_class)
        else:
            annotations[closest_point] = ax.annotate(selected_class, closest_point,
                                                     textcoords="offset points",
                                                     xytext=(0, 5), ha='center',
                                                     color=color_map[selected_class])

        plt.draw()  # Refresh the plot
        root.destroy()

    # Create Tkinter window
    root = tk.Tk()
    root.geometry("200x100+200+200")

    label = tk.Label(root, text=f"Classify point {closest_point}:")
    label.pack()

    combo = ttk.Combobox(root, values=classification_options)
    combo.pack()

    # Pre-select current classification
    current_label = point_labels.get(closest_point)
    combo.set(current_label if current_label else classification_options[0])

    # Add button to confirm classification
    btn = tk.Button(root, text="OK", command=on_select)
    btn.pack()

    root.mainloop()

# Click event handler
def on_click(event):
    if event.inaxes != ax:
        return

    if event.xdata and event.ydata:
        x, y = int(event.xdata), int(event.ydata)
        closest_point = min(points, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        classify_point(closest_point, point_colors)

# Folder containing images
folder_path = r"C:\Users\mmgia\OneDrive\Documents\Geog199SS\images"  # Change to your folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Process each image
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    image = Image.open(image_path)

    # Reset classification data for each image
    width, height = image.size
    points = {}
    for _ in range(n):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        rgb = image.getpixel((x, y))[:3]  # Just R, G, B
        points[(x, y)] = rgb

    point_labels = {pt: None for pt in points}
    point_colors = ["black"] * len(points)

    # Create figure and display image
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    ax.imshow(image)

    # Plot initial points
    scatter_plot = ax.scatter(*zip(*points.keys()), c=point_colors, s=20)
    annotations = {}

    # Add save button
    ax_button = plt.axes([0.75, 0.05, 0.15, 0.075])
    button = Button(ax_button, 'Save to CSV')
    button.on_clicked(save_to_csv)

    # Connect click event
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Show the plot and classify points
    plt.show()

    # Save classified points for this image
    save_to_csv()
