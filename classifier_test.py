image_path = r"C:\Users\spect\Desktop\EMIT STM Meeting\R1.jpg"  # Replace with your image path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import tkinter as tk
from tkinter import ttk

# Load the image
image = Image.open(image_path)
width, height = image.size

# Set the number of points to classify
n = 10  # Number of points (change as needed)

# Generate random points on the image
points = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(n)]
point_labels = {}

# Define classification options
classification_options = ["Class A", "Class B", "Class C"]  # Modify as needed

# Display the image and plot points
fig, ax = plt.subplots()
ax.imshow(image)
x, y = zip(*points)
scatter_plot = ax.scatter(x, y, color='blue', s=20)  # Initial random points in blue
annotations = {}


# Function to update point classification
def classify_point(closest_point):
    def on_select(event):
        selected_class = combo.get()
        point_labels[closest_point] = selected_class

        # Update point color to red and add annotation
        idx = points.index(closest_point)
        scatter_plot.get_offsets()[idx] = closest_point  # Update point position
        scatter_plot.set_facecolor(['blue' if pt not in point_labels else 'red' for pt in points])

        # Update or create annotation
        if closest_point in annotations:
            annotations[closest_point].set_text(selected_class)
        else:
            annotation = ax.annotate(selected_class, closest_point, textcoords="offset points",
                                     xytext=(0, 5), ha='center', color='red')
            annotations[closest_point] = annotation

        plt.draw()
        root.destroy()

    # Create a Tkinter window for dropdown
    root = tk.Tk()
    root.geometry("200x100+200+200")  # Position window in the center of the screen

    # Dropdown setup
    label = tk.Label(root, text=f"Classify point {closest_point}:")
    label.pack()
    combo = ttk.Combobox(root, values=classification_options)
    combo.pack()

    # Pre-select the current classification if it exists
    if closest_point in point_labels:
        combo.set(point_labels[closest_point])

    combo.bind("<<ComboboxSelected>>", on_select)
    root.mainloop()


# Event handler to detect clicks and open classification dropdown
def on_click(event):
    if event.xdata and event.ydata:
        x, y = int(event.xdata), int(event.ydata)
        closest_point = min(points, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        classify_point(closest_point)


# Connect the event to the classification function
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
