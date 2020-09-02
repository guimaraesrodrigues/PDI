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

INPUT_IMAGE = 'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
N_PIXELS_MIN = 400

# -------------------------------------------------------------------------------


def rotula(img, largura_min, altura_min, n_pixels_min):

    label = 2

    components_list = []

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 1.0:
                # floodfill(label, img, i, j)
                label += 1

    components_list = define_components(img, components_list)

    return components_list


def define_components(img, components_list):

    components_dict = {}

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >= 2:

                key = str(img[i][j][0])
                component = {'label': key, 'n_pixels': 1, 'T': i, 'L': j, 'B': i, 'R': j}

                if components_dict.get(key):

                    components_dict[key]['n_pixels'] = components_dict[key]['n_pixels'] + 1

                    if components_dict[key]['T'] < i:
                        components_dict[key]['T'] = i

                    if components_dict[key]['L'] > j:
                        components_dict[key]['L'] = j

                    if components_dict[key]['B'] > i:
                        components_dict[key]['B'] = i

                    if components_dict[key]['R'] < j:
                        components_dict[key]['R'] = j

                else:
                    components_dict[key] = component

    for key in components_dict:
        if components_dict[key]['n_pixels'] > N_PIXELS_MIN:
            components_list.append(components_dict[key])

    return components_list

# ===============================================================================

def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza(img, THRESHOLD)
    # cv2.imshow('01 - binarizada', img)
    # cv2.imwrite('01 - binarizada.png', img * 255)

    componentes = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len(componentes)

    print('%d componentes detectados.' % n_componentes)

    # cv2.imshow('02 - out', img_out)
    # cv2.imwrite('02 - out.png', img_out * 255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

# ===============================================================================