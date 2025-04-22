import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import os
from matplotlib.widgets import Button
from PIL import Image
from matplotlib.patheffects import withStroke  # For halo effect around text

# ================= CONFIGURATION =================
random.seed(13)

image_path = r"C:\Users\Marcu\OneDrive\Desktop\Wonderpole Images\Northern Quadrants\Northeast.JPG"
image = Image.open(image_path)
width, height = image.size
n = 30

classification_options = ["GV", "NPV", "Soil"]
color_map = {"GV": "green", "NPV": "red", "Soil": "blue"}
default_color = "white"

frame_width = 90
frame_height = 60
current_point_index = 0

# ================= POINT GENERATION =================
points = []
point_rgbs = {}
for _ in range(n):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    rgb = image.getpixel((x, y))[:3]
    points.append((x, y))
    point_rgbs[(x, y)] = rgb

point_labels = {point: None for point in points}
colors = [default_color] * len(points)

# ================= FIGURE SETUP =================
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.3)
ax.imshow(image)

original_xlim = ax.get_xlim()
original_ylim = ax.get_ylim()

halo_points = ax.scatter(*zip(*points), c="white", s=90, edgecolors="white", alpha=0.5)
scatter_plot = ax.scatter(*zip(*points), c=colors, s=30)
annotations = {}

# Create a text box for point index display
index_text_ax = plt.axes([0.45, 0.05, 0.1, 0.075])
index_text_ax.axis('off')  # Hide box and ticks
index_display = index_text_ax.text(0.5, 0.5, "", ha='center', va='center', fontsize=12, fontweight='bold')

def update_index_display():
    index_display.set_text(f"Point {current_point_index + 1} of {n}")
    fig.canvas.draw_idle()

# ================= FUNCTIONALITY =================
def save_to_csv(event=None):
    root = tk.Tk()
    root.withdraw()
    file_name = filedialog.asksaveasfilename(
        initialdir=os.path.expanduser("~") + "/Downloads",
        title="Save CSV as...",
        filetypes=[("CSV Files", "*.csv")],
        defaultextension=".csv"
    )
    if file_name:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Class', 'R', 'G', 'B'])
            for point in points:
                label = point_labels.get(point, "Unclassified")
                r, g, b = point_rgbs[point]
                writer.writerow([point[0], point[1], label, r, g, b])
        print(f"CSV file saved as: {file_name}")

def classify_point(closest_point):
    def on_select():
        selected_class = combo.get()
        point_labels[closest_point] = selected_class
        idx = points.index(closest_point)
        colors[idx] = color_map[selected_class]
        scatter_plot.set_color(colors)

        if closest_point in annotations:
            annotations[closest_point].set_text(selected_class)
        else:
            border = withStroke(linewidth=3, foreground="white")
            annotations[closest_point] = ax.annotate(
                selected_class, closest_point,
                textcoords="offset points", xytext=(0, 5),
                ha='center', color=color_map[selected_class],
                fontsize=12, fontweight='bold',
                path_effects=[border]
            )
        plt.draw()
        root.destroy()

    root = tk.Tk()
    root.geometry("200x100+200+200")
    tk.Label(root, text=f"Classify point {closest_point}:").pack()
    combo = ttk.Combobox(root, values=classification_options)
    current_label = point_labels.get(closest_point)
    combo.set(current_label if current_label else classification_options[0])
    combo.pack()
    tk.Button(root, text="OK", command=on_select).pack()
    root.mainloop()

def on_click(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return
    x, y = int(event.xdata), int(event.ydata)
    closest_point = min(points, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
    classify_point(closest_point)

def zoom(event):
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    x_center, y_center = event.xdata, event.ydata
    if event.button == 'up':
        factor = 0.8
    elif event.button == 'down':
        factor = 1.2
    else:
        return
    new_xlim = [x_center - (x_center - xlim[0]) * factor, x_center + (xlim[1] - x_center) * factor]
    new_ylim = [y_center - (y_center - ylim[0]) * factor, y_center + (ylim[1] - y_center) * factor]
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)

    zoom_level = (xlim[1] - xlim[0]) / (original_xlim[1] - original_xlim[0])
    scatter_plot.set_sizes([30 * (1 / zoom_level)] * len(points))
    halo_points.set_sizes([90 * (1 / zoom_level)] * len(points))
    plt.draw()

def reset_view(event=None):
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)
    scatter_plot.set_sizes([30] * len(points))
    halo_points.set_sizes([90] * len(points))
    plt.draw()

def focus_on_point(index):
    global current_point_index
    current_point_index = index % len(points)
    x, y = points[current_point_index]
    ax.set_xlim(x - frame_width // 2, x + frame_width // 2)
    ax.set_ylim(y + frame_height // 2, y - frame_height // 2)
    update_index_display()

def next_point(event=None):  # ⬆ Go forward
    focus_on_point(current_point_index + 1)

def prev_point(event=None):  # ⬇ Go back
    focus_on_point(current_point_index - 1)

def on_key(event):
    if event.key == 'up':      # ⬆ = Next
        next_point()
    elif event.key == 'down':  # ⬇ = Previous
        prev_point()

# ================= UI ELEMENTS =================
ax_button = plt.axes([0.75, 0.05, 0.15, 0.075])
button = Button(ax_button, 'Save to CSV')
button.on_clicked(save_to_csv)

reset_button_ax = plt.axes([0.75, 0.15, 0.15, 0.075])
reset_button = Button(reset_button_ax, 'Reset View')
reset_button.on_clicked(reset_view)

# Inverted button layout
prev_button_ax = plt.axes([0.05, 0.05, 0.15, 0.075])
prev_button = Button(prev_button_ax, '⬇ Prev Point')
prev_button.on_clicked(prev_point)

next_button_ax = plt.axes([0.25, 0.05, 0.15, 0.075])
next_button = Button(next_button_ax, '⬆ Next Point')
next_button.on_clicked(next_point)

# ================= INIT + EVENTS =================
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('scroll_event', zoom)
fig.canvas.mpl_connect('key_press_event', on_key)

manager = plt.get_current_fig_manager()
manager.window.state('zoomed')

# Full image view on load
update_index_display()
plt.show()

