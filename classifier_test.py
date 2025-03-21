import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import os
from matplotlib.widgets import Button
from PIL import Image

# Load the image
image_path = r"C:\Users\Marcu\OneDrive\Desktop\Wonderpole Images\Northern Quadrants\Northwest.JPG"
image = Image.open(image_path)
width, height = image.size

# Set the number of points to classify initially (30 points)
n = 30  # Change this to 30

# Define classification options
classification_options = ["GV", "NPV", "Soil"]

# Generate random points (30 points)
points = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(n)]
point_labels = {point: None for point in points}  # Initialize with no classification

# Updated color mapping for each class
color_map = {"GV": "green", "NPV": "red", "Soil": "blue"}

# Default color for unclassified points
default_color = "white"

# Initialize colors (default to white for unclassified points)
colors = [default_color] * len(points)

# Create figure and display image
fig, ax = plt.subplots(figsize=(10, 8))  # Adjust size of the figure for more space
plt.subplots_adjust(bottom=0.25)  # Adjust bottom space to allow for buttons
ax.imshow(image)

# Store original axis limits for later use
original_xlim = ax.get_xlim()
original_ylim = ax.get_ylim()

# Plot initial points
scatter_plot = ax.scatter(*zip(*points), c=colors, s=20)

# Store text annotations
annotations = {}

# Function to save points to CSV
def save_to_csv(event=None):
    # Ask for the file name
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to choose the save location and file name
    file_name = filedialog.asksaveasfilename(
        initialdir=os.path.expanduser("~") + "/Downloads",  # Default to Downloads folder
        title="Save CSV as...",
        filetypes=[("CSV Files", "*.csv")],  # Filter for CSV files
        defaultextension=".csv"
    )

    # If the user selected a file (didn't cancel the dialog)
    if file_name:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Class', 'Color'])  # Added 'Color' header
            for point in points:
                # Write data for all points, whether classified or not
                classification = point_labels.get(point, "Unclassified")  # Default to "Unclassified" if not classified
                color = colors[points.index(point)]  # Get color (default "white" for unclassified)
                writer.writerow([point[0], point[1], classification, color])  # Added color
        print(f"CSV file saved as: {file_name}")

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

# Function to handle clicks on existing points and classify them
def on_click(event):
    if event.inaxes != ax:
        return

    if event.xdata and event.ydata:
        x, y = int(event.xdata), int(event.ydata)

        # Find the closest point that was clicked on
        closest_point = min(points, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
        classify_point(closest_point)

# Function for zooming using mouse scroll
def zoom(event):
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    # Get the current axis limits
    x_center, y_center = (event.xdata, event.ydata)

    # Zoom in or out based on scroll direction
    if event.button == 'up':  # Zoom in
        factor = 0.8
    elif event.button == 'down':  # Zoom out
        factor = 1.2
    else:
        return

    # Calculate new axis limits
    new_xlim = [x_center - (x_center - xlim[0]) * factor, x_center + (xlim[1] - x_center) * factor]
    new_ylim = [y_center - (y_center - ylim[0]) * factor, y_center + (ylim[1] - y_center) * factor]

    # Apply the new zoom limits
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    # Scale point sizes proportionally with zoom level (opposite direction)
    zoom_level = (xlim[1] - xlim[0]) / (original_xlim[1] - original_xlim[0])

    # Adjust the point size, making them grow with zoom-in
    scatter_plot.set_sizes([20 * (1 / zoom_level)] * len(points))  # Adjust size to grow with zoom level

    plt.draw()

# Function to reset to the original view
def reset_view(event=None):
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)
    scatter_plot.set_sizes([20] * len(points))  # Reset to default point size
    plt.draw()

# Add save button
ax_button = plt.axes([0.75, 0.05, 0.15, 0.075])  # Position for save button
button = Button(ax_button, 'Save to CSV')
button.on_clicked(save_to_csv)

# Add reset view button (Further moved down to avoid overlap)
reset_button_ax = plt.axes([0.75, 0.15, 0.15, 0.075])  # Adjusted position (further down)
reset_button = Button(reset_button_ax, 'Reset View')
reset_button.on_clicked(reset_view)

# Connect the click event to the function
fig.canvas.mpl_connect('button_press_event', on_click)

# Connect the zoom event (scrolling)
fig.canvas.mpl_connect('scroll_event', zoom)

# Set the figure to full screen mode
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')  # This maximizes the figure window

plt.show()




