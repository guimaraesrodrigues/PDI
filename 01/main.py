import cv2 as cv
import numpy as np

threshold = 0.7
componentes = 0


def main():
    img = cv.imread('arroz.bmp', cv.IMREAD_GRAYSCALE)

    img_bin = img

    show_img("Binarizada", binariza(img, img_bin, threshold))

    print("Quantidade de arroz: ", rotula(img_bin, 0, 0, 0.1))


def show_img(title, img):
    cv.imshow(title, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def binariza(img_in, img_out, threshold):
    if img_in.shape != img_out.shape:
        print("ERRO: binariza: as imagens precisam ter o mesmo tamanho e numero de canais.")
    else:
        img_out = cv.normalize(img_in.astype('float'), None, 0.0, 1.0, cv.NORM_MINMAX)

        for i in range(len(img_out)):
            for j in range(len(img_out[i])):
                if img_out[i][j] > threshold:
                    img_out[i][j] = 1.0
                else:
                    img_out[i][j] = 0

        img_out = img_out * 255

        cv.imwrite('binarizada.bmp', img_out)

        return img_out


def rotula(img, x, y, label):
    
    if img[x][y] == 1.0:
        componentes += 1
        img[x][y] = label
        label += 0.2

        if x > 0:
            rotula(img, x - 1, y, label)
        if x < len(img[y]) - 1:
            rotula(img, x + 1, y, label)
        if y > 0:
            rotula(img, x, y - 1, label)
        if y < len(img) - 1:
            rotula(img, x, y + 1, label)
    
    return componentes


if __name__ == '__main__': main()