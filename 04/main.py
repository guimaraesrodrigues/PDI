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

# TODO: ajuste estes parâmetros!
NEGATIVO = False


# ===============================================================================

def main():
    # Abre a imagem em escala de cinza.
    img = open_img(INPUT_IMAGE)

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img

    # cv2.imwrite('01 - binarizada.png', img * 255)
    img = pre_process(img)

    show_img(img)
    # cv2.imshow('img', img)
    # cv2.imwrite('02 - out.png', img_out * 255)


def pre_process(img):
    img_blurred = cv2.blur(img, (105, 105))

    img = cv2.subtract(img, img_blurred)

    img = cv2.threshold(img, 0.2, 1, cv2.THRESH_BINARY)[1]

    kernel = np.ones((5, 5), np.uint8)

    erosion = cv2.erode(img, kernel, iterations=1)

    return cv2.dilate(erosion, kernel, iterations=1)


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