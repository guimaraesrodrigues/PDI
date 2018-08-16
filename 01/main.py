import cv2 as cv
import numpy as np

threshold = 210


def main():
    img = cv.imread('arroz.bmp', cv.IMREAD_GRAYSCALE)

    img_bin = img

    binariza(img, img_bin, threshold)

    #print(img_bin.shape)

    # cv.imshow('ola', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    #cv.imwrite('arrozb.bmp', img)
    # cv.imshow('ola', img_out)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


def binariza(img_in, img_out, threshold):
    if img_in.shape != img_out.shape:
        print("ERRO: binariza: as imagens precisam ter o mesmo tamanho e numero de canais.")
    else:
        img_out = cv.normalize(img_in.astype('float'), None, 0.0, 1.0, cv.NORM_MINMAX)
        cv.imwrite('binarizada.bmp', img_out.convertTo(img_out, cv.CV_8UC3, 255.0))
        for i in range(len(img_out)):
            for j in range(len(img_out[i])):
                if img_out[i][j] > threshold:
                    img_out[i][j] = 255
                else:
                    img_out[i][j] = 0



        # roi = img_in[280:340, 330:390]
        # img_out[280:340, 330:390] = roi
        # cv.imwrite('teste.bmp', img_out)


def rotula(img, componentes, largura_min, altura_min, n_pixels_min):
    pass


if  __name__ =='__main__':main()