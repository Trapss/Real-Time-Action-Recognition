import numpy as np

# clip length
L = 15
# winWidth = 1280
winWidth = 640
# winHeight = 720
winHeight = 480
move_status = ['unrecognized', 'stand', 'sit', 'walk', 'walk close', 'walk away', 'sit down', 'stand up', 'lying']

c = np.random.rand(32, 3) * 255
sort_max_age = 100
sort_min_hit = 1
