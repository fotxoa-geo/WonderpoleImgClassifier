import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import tkinter as tk
from tkinter import ttk, filedialog
import csv
from matplotlib.widgets import Button
import os

# Load the image
image_path = r"test.jpeg"  # Replace with your image path
image = Image.open(image_path)
width, height = image.size

# Set the number of points to classify
n = 3  # Change this as needed

# Define classification options
classification_options = ["Class A", "Class B", "Class C"]

# Generate random points
points = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(n)]
point_labels = {point: None for point in points}  # Initialize with no classification

# Color mapping for each class
color_map = {"Class A": "red", "Class B": "green", "Class C": "blue"}

# Initialize colors (default to black for unclassified points)
colors = ["black"] * len(points)

# Create figure and display image
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.imshow(image)

# Plot initial points
scatter_plot = ax.scatter(*zip(*points), c=colors, s=20)

# Store text annotations
annotations = {}

# Function to save points to CSV
def save_to_csv(event=None):
    root = tk.Tk()
    root.withdraw()

    file_path = os.path.join(os.getcwd(), "test.csv")  # Save in current working directory

    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Class']) # class headers
            for point in points:
                print(point)
                writer.writerow([point[0], point[1], point_labels.get(point, "Unclassified")])
        print(f"CSV file saved as: {file_path}")

# Function to classify a point
def classify_point(closest_point):
    def on_select():
        selected_class = combo.get()
        point_labels[closest_point] = selected_class

        # Update color list
        idx = points.index(closest_point)
        colors[idx] = color_map[selected_class]  # Assign new color
        scatter_plot.set_color(colors)  # Update scatter plot colors

        # Update or create annotation
        if closest_point in annotations:
            annotations[closest_point].set_text(selected_class)
        else:
            annotations[closest_point] = ax.annotate(selected_class, closest_point,
                                                     textcoords="offset points",
                                                     xytext=(0, 5), ha='center',
                                                     color=color_map[selected_class])

        plt.draw()
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
        classify_point(closest_point)

# Add save button
ax_button = plt.axes([0.75, 0.05, 0.15, 0.075])
button = Button(ax_button, 'Save to CSV')
button.on_clicked(save_to_csv)

# Connect click event
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
