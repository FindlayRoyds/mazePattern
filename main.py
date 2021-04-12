import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import os
import ctypes
import pathlib
from PIL import Image
import threading
import time

os.chdir(__file__[:__file__.rfind("\\")])

kwargs = {
    "linewidth": 20,
    #"solid_capstyle": 'round',
    "color": '#f48c06'
}
grid_size = 20
width = int(1366 / grid_size)
height = int(768 / grid_size)
quality = 2
history = {}
lines = {}
use_threads = False
join_lines = False
start_time = time.time()

plt.figure(figsize=(width, height), dpi=grid_size * 1.296 * quality)
ax = plt.axes()
plt.gca().set_xlim(0, width)
plt.gca().set_ylim(0, height)
plt.axis("off")
plt.margins(0, 0)

ax.add_patch(Rectangle((0, 0), width, height, facecolor = '#000814'))
total_lines = 0

def create_line(y):
    history[y] = {}
    for x in range(width):
        selected = random.getrandbits(1) == 1
        if y > 0 and x > 0:
           if history[y-1][x-1] and not history[y][x-1] and not history[y-1][x]:
               selected = False
        if selected:
            if join_lines:
                lines[(x, y, 1)] = (((x, y+0.5), (x+0.5, y)))
                lines[(x, y, 2)] = ((x+0.5, y+1), (x+1, y+0.5))
            else:
                plt.plot((x, x+0.5), (y+0.5, y), **kwargs)
                plt.plot((x+0.5, x+1), (y+1, y+0.5), **kwargs)
        else:
            if join_lines:
                lines[(x, y, 1)] = ((x, y+0.5), (x+0.5, y+1))
                lines[(x, y, 2)] = ((x+0.5, y), (x+1, y+0.5))
            else:
                plt.plot((x, x+0.5), (y+0.5, y+1), **kwargs)
                plt.plot((x+0.5, x+1), (y+0, y+0.5), **kwargs)
        history[y][x] = selected
    print(int(y / height * 100))

for y in range(height):
    if use_threads:
        x = threading.Thread(target=create_line, args=(y,))
        x.start()
    else:
        create_line(y)

if join_lines:
    while len(lines) != 0:
        for begin_pos in lines:
            pos = begin_pos
            line_begin = begin_pos
            first_pos = None
            current_direction = None
            while True:
                endline = False
                endtrail = False
                data = lines[pos]
                start_pos = data[0]
                end_pos = data[1]
                if first_pos == None:
                    first_pos = start_pos
                if current_direction == None:
                    current_direction = pos[2]
                offsetx = 0
                offsety = 0
                if end_pos[0] == pos[0] + 1:
                    offsetx = 1
                else:
                    offsety = 1
                next_pos = None
                lines.pop(pos)
                plt.plot((start_pos[0], end_pos[0]), (start_pos[1], end_pos[1]), **kwargs)
                if (pos[0] + offsetx, pos[1] + offsety, 1) in lines:
                    if lines[(pos[0] + offsetx, pos[1] + offsety, 1)][0] == end_pos:
                        next_pos = (pos[0] + offsetx, pos[1] + offsety, 1)#lines[(pos[0] + offsetx, pos[1] + offsety, 1)]
                        endline = current_direction == 2
                    else:
                        next_pos = (pos[0] + offsetx, pos[1] + offsety, 2)#lines[(pos[0] + offsetx, pos[1] + offsety, 2)]
                        endline = current_direction == 1
                else:
                    endline = True
                    endtrail = True
                
                if next_pos == begin_pos:
                    endtrail = True
                
                if endline:
                    plt.plot((first_pos[0], first_pos[0]), (first_pos[1], first_pos[1]), **kwargs)
                    total_lines += 1
                    first_pos = end_pos
                if endtrail:
                    break

                pos = next_pos
            break

plt.savefig("yeah", dpi=None, facecolor='w', edgecolor='w',
        orientation='landscape', format=None,
        transparent=False, pad_inches=0,
        frameon=None, metadata=None, bbox_inches='tight')

with Image.open("yeah.png") as im:
    im_crop = im.crop((0, 0, 1366 * quality, 768 * quality))
    #im_crop.save("yeah.png")

ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\Findlay\\Documents\\Python Projects\\MazePattern\\yeah.png", 0)
print(time.time() - start_time)
print(total_lines)