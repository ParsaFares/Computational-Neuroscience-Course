import random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os


def dot_product_3d(m1, m2):
    s = 0
    for d in range(4):
        for i in range(len(m1[d])):
            for j in range(len(m1[d])):
                if m2[d][i][j] != 0:
                    s += m1[d][i][j][0]

    return s


def input_current_calc(images, feature, size):
    s = len(feature[0])
    mat = [[0]*size[1] for _ in range(size[0])]
    for i in range(size[0]):
        for j in range(size[1]):
            m1 = []
            for d in range(4):
                m1.append([[images[d][r][c] for c in range(j, j+s)]
                           for r in range(i, i+s)])
            mat[i][j] = dot_product_3d(m1, feature)

    return mat


def u_calc(current_mat, img, u_mat, spike_mat, neuron_data_mat, feature_mat):
    row_size = len(u_mat)
    col_size = len(u_mat[0])
    for i in range(row_size):
        for j in range(col_size):
            if spike_mat[i][j] <= 0:
                tau = neuron_data_mat[i][j][2]*neuron_data_mat[i][j][3]
                u_mat[i][j] = u_mat[i][j] - (1/(tau*100)) * (
                    u_mat[i][j] - neuron_data_mat[i][j][0] - neuron_data_mat[i][j][2] * current_mat[i][j])
                if spike_mat[i][j] < 0:
                    spike_mat[i][j] += 1

            if spike_mat[i][j] == 1:
                spike_mat[i][j] = 2
                feature_mat = flat_stdp(i, j, feature_mat, img, -1)

            if spike_mat[i][j] == 0 and u_mat[i][j] > neuron_data_mat[i][j][1]:
                spike_mat[i][j] = 1
                feature_mat = flat_stdp(i, j, feature_mat, img, 1)

    return u_mat, spike_mat, feature_mat


def flat_stdp(i, j, f_mat, img, delta_t):
    for d in range(4):
        for r in range(len(f_mat[d])):
            for c in range(len(f_mat[d])):
                if i+r < len(img[d]) and j+c < len(img[d][0]) and i+r >= 0 and j+c >= 0:
                    if img[d][i+r][j+c][0] != 0:
                        f_mat[d][r][c] += 10 * delta_t

    return f_mat


def winner_take_all(spike_mats, feature_mats, f_num):
    s = len(spike_mats[f_num])
    for f in range(len(feature_mats)):
        if len(spike_mats[f]) == len(spike_mats[f_num]) and feature_mats[f] != feature_mats[f_num]:
            for r in range(len(spike_mats[f_num])):
                for c in range(len(spike_mats[f_num])):
                    if spike_mats[f_num][r][c] == 1:
                        for i in range(max(0, r-s//2), min(s, r+s//2)):
                            for j in range(max(0, c-s//2), min(s, c+s//2)):
                                if spike_mats[f][i][j] == 0:
                                    spike_mats[f][i][j] = -2

    return spike_mats


def make_feature(s):
    return [[[5]*s for _ in range(s)] for _ in range(4)]


def make_all_features(n, min, max):
    features = []
    for _ in range(n):
        s = int(random.uniform(min, max))
        features.append(make_feature(s))

    return features


def do_cycle(images, features, u_mats, spike_mats, neurons_data_mat, sizes):
    for f in range(len(features)):
        current_mat = input_current_calc(images, features[f], sizes[f])
        u_mats[f], spike_mats[f], features[f] = u_calc(
            current_mat, images, u_mats[f], spike_mats[f], neurons_data_mat[f], features[f])
        spike_mats = winner_take_all(spike_mats, features, f)

    return features, u_mats, spike_mats


def set_mats(homo_neuron_data, sizes, f_mats):
    neurons_data_mat = []
    spike_mats = []
    u_mats = []
    out_sizes = []
    for s in range(len(f_mats)):
        size = len(f_mats[s][0])
        rows = sizes[0] - size + 1
        cols = sizes[1] - size + 1
        out_sizes.append([rows, cols])

        # u_rest, u_threshold, R, C
        neurons_data_mat.append([[[
            random.uniform(homo_neuron_data[0]-5, homo_neuron_data[0]+5),
            random.uniform(homo_neuron_data[1]-5, homo_neuron_data[1]+5),
            random.uniform(
                max(homo_neuron_data[2]-3, 0), homo_neuron_data[2]+3),
            random.uniform(
                max(homo_neuron_data[3]-3, 0), homo_neuron_data[3]+3),
        ] for _ in range(cols)] for _ in range(rows)])
        spike_mats.append([[0]*cols for _ in range(rows)])
        u_mats.append([[0]*cols for _ in range(rows)])

        for i in range(rows):
            for j in range(cols):
                u_mats[-1][i][j] = neurons_data_mat[-1][i][j][0]

    return spike_mats, u_mats, neurons_data_mat, out_sizes


def core(source_dir, homo_neuron_data, features_mats):
    folders = os.listdir(source_dir)
    folders.sort()
    try:
        folders.remove(".DS_Store")
    except:
        pass

    C2 = []
    for folder in folders:
        files = os.listdir(source_dir+folder+"/")
        try:
            files.remove(".DS_Store")
        except:
            pass

        img = mpimg.imread(source_dir+folder+"/"+files[0])
        spike_mats, u_mats, neurons_data_mat, sizes = set_mats(
            homo_neuron_data, [len(img), len(img[0])], features_mats)

        files.sort(reverse=True)
        for i in range(0, len(files), 4):
            print(files[i:i+4])
            images = []
            for j in range(4):
                images += [mpimg.imread(source_dir+folder+"/"+files[i+j])]

            features_mats, u_mats, spike_mats = do_cycle(images, features_mats, u_mats,
                                                         spike_mats, neurons_data_mat, sizes)

        c2 = []
        for s in range(len(spike_mats)):
            spikes = 0
            for i in range(len(spike_mats[s])):
                for j in range(len(spike_mats[s])):
                    if spike_mats[s][i][j] > 0:
                        spikes += 1

            c2.append(spikes)

        C2.append(c2)

    return features_mats, C2
