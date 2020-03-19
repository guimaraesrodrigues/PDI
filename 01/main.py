# ===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
# -------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
# ===============================================================================

import sys
import timeit
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = 'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.7
ALTURA_MIN = 22
LARGURA_MIN = 31
N_PIXELS_MIN = 400


# ===============================================================================

def binariza(img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.

Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > threshold:
                img[i][j] = 1.0
            else:
                img[i][j] = 0

    return img

# -------------------------------------------------------------------------------


def rotula(img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

    label = 2

    components_list = []

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 1.0:
                floodfill(label, img, i, j)
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


def floodfill(label, img, x0, y0):

    if x0 < 0 or y0 < 0:
        return

    if x0 >= img.shape[0]-1 or y0 >= img.shape[1]-1:
        return

    if img[x0][y0] == label:
        return

    if img[x0][y0] == 0:
        return

    img[x0][y0] = label

    floodfill(label, img, x0 + 1, y0)
    floodfill(label, img, x0 - 1, y0)
    floodfill(label, img, x0, y0 + 1)
    floodfill(label, img, x0, y0 - 1)

    return

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
    cv2.imshow('01 - binarizada', img)
    cv2.imwrite('01 - binarizada.png', img * 255)

    start_time = timeit.default_timer()
    componentes = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len(componentes)
    print('Tempo: %f' % (timeit.default_timer() - start_time))
    print('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle(img_out, (c['L'], c['T']), (c['R'], c['B']), (0, 0, 1))

    cv2.imshow('02 - out', img_out)
    cv2.imwrite('02 - out.png', img_out * 255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

# ===============================================================================