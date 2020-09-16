# ===============================================================================
# Trabalho 04
# -------------------------------------------------------------------------------
# Autor: Rodrigo Guimarães
# Universidade Tecnológica Federal do Paraná
# ===============================================================================
import sys
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = '150.bmp'
NEGATIVO = False


def main():
    # Abre a imagem em escala de cinza.
    img = open_img(INPUT_IMAGE)

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img

    img = pre_process(img)

    # show_img(img)

    img = labeling(img)

    blobs = identify_blobs(img)

    calc_blob_size_avg(blobs)


def pre_process(img):
    img_blurred = cv2.blur(img, (59, 59))

    img = cv2.subtract(img, img_blurred)

    img = cv2.threshold(img, 0.2, 1, cv2.THRESH_BINARY)[1]

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
    # blob_max_size = next(iter(blobs_dict.values()))['n_pixels']
    # blob_min_size = next(iter(blobs_dict.values()))['n_pixels']

    blobs_sorted = sorted(blobs_dict.items(), key=lambda x: x[1]['n_pixels'])
    blob_sum = 0
    for elem in blobs_sorted[5:-5]:
        blob_sum += elem[1]['n_pixels']

    return round(blob_sum / len(blobs_sorted[5:-5]))


    # blob_sum = 0
    # for key in blobs_dict:
    #     blob_size = blobs_dict[key]['n_pixels']
    #     blob_sum += blobs_dict[key]['n_pixels']
    #
    #     if blob_size > blob_max_size:
    #         blob_max_size = blob_size
    #     elif blob_size < blob_min_size:
    #         blob_min_size = blob_size
    #
    # print(blob_max_size)
    # print(blob_min_size)
    # print(blob_sum / len(blobs_dict.keys()))


def open_img(file_name):
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    return img


def show_img(img):
    cv2.imshow('img', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

# ===============================================================================