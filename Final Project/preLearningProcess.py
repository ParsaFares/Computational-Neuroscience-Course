import Converter
import Scaler
import Gabor
import SigmaAI
import MaxPool
import Intensity2Latency
import STDP
# import MakeSquare # It was a beautiful mistake!!!
import os
import math
import matplotlib.pyplot as plt
import numpy as np

# ----------------------Making Dir Structure--------------------
os.mkdir("grayscaled")
os.mkdir("scales")
os.mkdir("S1")
os.mkdir("timed S1")
os.mkdir("C1")
os.mkdir("features")

scales = [0.7, 0.6, 0.5, 0.4]
for d in ["scales", "S1", "timed S1", "C1"]:
    for s in scales:
        os.mkdir(d+"/"+str(s))

print("Directories created!")
# --------------------------------------------------------------

# ------------------PreProcessing Images--------------------
# Converting images to grayscale
Converter.convert_all_in_dir("images/", "grayscaled/")

print("All images were converted!")

# Scaling images to 1, 0.8, 0.65, 0.5, 0.3 times it's size
Scaler.scale_all_dir("grayscaled/", "scales/", scales)

print("All images were scaled!")
# ----------------------------------------------------------

# -----------------------------Making S1-------------------------------
entries = os.listdir("scales/")
try:
    entries.remove(".DS_Store")
except:
    pass

n = 5
cost_func = SigmaAI.summation(n)
kernel = []
for i in range(4):
    data = [5, i*math.pi/4, 2, 5]
    data = SigmaAI.my_ai_min(cost_func, data)
    gabor_func = Gabor.make_gabor_func(*data)
    kernel.append(Gabor.make_gabor_filter(n, gabor_func))

# Applying gabor filter on images
for d in entries:
    Gabor.apply_gabor_on_dir("scales/"+d+"/", "S1/"+d+"/", kernel)

print("Gabor filter applied to all images!")
# ---------------------------------------------------------------------

# -----------------------Encoding Intensity-to-Latency----------------------
entries = os.listdir("S1/")
try:
    entries.remove(".DS_Store")
except:
    pass

# Encoding imgages with law of intensity-to-latency
k = 64
for d in entries:
    Intensity2Latency.encode_all_in_dir("S1/"+d+"/", "timed S1/"+d+"/", k)

print("Images were encoded!")
# ---------------------------------------------------------------------------

# ------------------------------Making C1---------------------------------
entries = os.listdir("S1/")
try:
    entries.remove(".DS_Store")
except:
    pass

# Applying max-pool on images
n = 4
stride = n//2
for d in entries:
    MaxPool.maxpool_on_all_dir("timed S1/"+d+"/", "C1/"+d+"/", n, stride)

print("Max pooling applied to all images!")
# -------------------------------------------------------------------------


# ------------------------STDP Learning-------------------------
entries = os.listdir("C1/")
entries.sort()
try:
    entries.remove(".DS_Store")
except:
    pass

f_count = 50
homo_neuron_data = [-75, -55, 5, 3]
features_mats = STDP.make_all_features(f_count, 25, 30)
C2 = []
for d in entries:
    print(d)
    features_mats, c2 = STDP.core(
        "C1/"+d+"/", homo_neuron_data, features_mats)
    C2.append(c2)

for f in range(len(features_mats)):
    for i in range(4):
        plt.imshow(np.array(features_mats[f][i]), cmap='gray')
        plt.imsave("features/"+str(f)+"_"+str(i)+".png",
                   np.array(features_mats[f][i]), cmap="gray")

f = open("C2.txt", "a")
f.write(str(C2))
print(C2)

print("Model trained!")
# --------------------------------------------------------------
