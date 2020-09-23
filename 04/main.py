# ===============================================================================
# Trabalho 04
# -------------------------------------------------------------------------------
# Autor: Rodrigo Guimarães
# Universidade Tecnológica Federal do Paraná
# ===============================================================================
import sys
from statistics import pstdev

import numpy as np
import cv2
import matplotlib.pyplot as plt

# ===============================================================================
from matplotlib.ticker import PercentFormatter

INPUT_IMAGE = '60.bmp'
NEGATIVO = False


def main():
    # Abre a imagem em escala de cinza.
    img = open_img(INPUT_IMAGE)

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Remove ruídos e binariza
    img_bin = pre_process(img)

    # Rotula componentes
    img = labeling(img_bin)

    # Identifica tamanho dos blobs
    blobs = identify_blobs(img)

    # Desenha um retangulo em volta de cada blob
    draw_rectangles(img_out, blobs)

    # Conta quantos grãos de arroz existem na imagem
    print(count_blobs(blobs))

    # Exibe imagem com os blobs identificados
    show_img(img_out)


def pre_process(img):
    img_blurred = cv2.blur(img, (59, 59))

    img = cv2.subtract(img, img_blurred)

    img = cv2.threshold(img, 0.16, 1, cv2.THRESH_BINARY)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)

    return img


def labeling(img):
    label = 2

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 1.0:
                cv2.floodFill(img, None, (j, i), label)
                label += 1

    return img


def identify_blobs(img):

    blobs_dict = {}

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >= 2:
                key = str(img[i][j])
                component = {'label': key, 'n_pixels': 1, 'T': i, 'L': j, 'B': i, 'R': j}

                if blobs_dict.get(key):

                    blobs_dict[key]['n_pixels'] = blobs_dict[key]['n_pixels'] + 1

                    if blobs_dict[key]['T'] < i:
                        blobs_dict[key]['T'] = i

                    if blobs_dict[key]['L'] > j:
                        blobs_dict[key]['L'] = j

                    if blobs_dict[key]['B'] > i:
                        blobs_dict[key]['B'] = i

                    if blobs_dict[key]['R'] < j:
                        blobs_dict[key]['R'] = j

                else:
                    blobs_dict[key] = component

    return blobs_dict


def calc_blob_size_avg(blobs_dict):

    blobs_sorted = sorted(blobs_dict.items(), key=lambda x: x[1]['n_pixels'])

    blob_sorted_size = len(blobs_sorted)
    blob_sum = 0

    for elem in blobs_sorted[round(blob_sorted_size/20):-round(blob_sorted_size/3)]:
        blob_sum += elem[1]['n_pixels']

    return round(blob_sum / len(blobs_sorted[round(blob_sorted_size/20):-round(blob_sorted_size/3)]))


def count_blobs(blobs):
    blob_avg_size = calc_blob_size_avg(blobs)

    n_blobs = 0
    for key in blobs:
        blob_quantity = blobs[key]['n_pixels'] / blob_avg_size
        if blob_quantity < 1:
            n_blobs += 1
        else:
            n_blobs += round(blob_quantity)

    return n_blobs


def open_img(file_name):
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    # img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img

    return img


def show_img(img):
    cv2.imshow('img', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def draw_rectangles(img_out, blobs_dict):
    for b in blobs_dict.values():
        cv2.rectangle(img_out, (b['L'], b['T']), (b['R'], b['B']), (0, 0, 1))


if __name__ == '__main__':
    main()

# ===============================================================================