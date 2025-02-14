import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import tkinter as tk
from tkinter import ttk, filedialog
import csv
from matplotlib.widgets import Button

# Load the image
image_path = r"C:\Users\Marcu\OneDrive\Pictures\Rocca Calascio.jpg"  # Replace with your image path
image = Image.open(image_path)
width, height = image.size

# Set the number of points to classify
n = 1  # Number of points (change as needed)

# Define classification options
classification_options = ["Class A", "Class B", "Class C"]  # Modify as needed

# Generate random points on the image and randomly classify them
points = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(n)]
point_labels = {point: random.choice(classification_options) for point in points}  # Assign random classes

# Display the image and plot points
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Adjust layout to fit button
ax.imshow(image)

# Color mapping for each class
color_map = {"Class A": "red", "Class B": "green", "Class C": "blue"}
point_colors = [color_map[point_labels[point]] for point in points]

scatter_plot = ax.scatter(*zip(*points), c=point_colors, s=20)  # Set initial point colors
annotations = {point: ax.annotate(point_labels[point], point, textcoords="offset points",
                                  xytext=(0, 5), ha='center', color=color_map[point_labels[point]])
               for point in points}

# Function to save points and their classifications to a user-selected CSV file
def save_to_csv(event=None):
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Save CSV File")
    if file_path:  # Check if the user selected a file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Class'])  # Column headers
            for point in points:
                writer.writerow([point[0], point[1], point_labels[point]])

        print(f"CSV file saved as: {file_path}")

# Function to update point classification
def classify_point(closest_point):
    def on_select(event):
        selected_class = combo.get()
        point_labels[closest_point] = selected_class

        # Update point color and annotation
        idx = points.index(closest_point)
        scatter_plot.get_facecolors()[idx] = color_map[selected_class]
        annotations[closest_point].set_text(selected_class)
        annotations[closest_point].set_color(color_map[selected_class])

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

    # Pre-select the current classification
    combo.set(point_labels[closest_point])
    combo.bind("<<ComboboxSelected>>", on_select)
    root.mainloop()

# Event handler to detect clicks and open classification dropdown
def on_click(event):
    if event.xdata and event.ydata:
        x, y = int(event.xdata), int(event.ydata)
        closest_point = min(points, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        classify_point(closest_point)

# Add a "Save to CSV" button to the figure
ax_button = plt.axes([0.75, 0.05, 0.15, 0.075])  # Position for button
button = Button(ax_button, 'Save to CSV')
button.on_clicked(save_to_csv)

# Connect the click event to the image
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()

