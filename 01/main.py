import cv2 as cv
import numpy as np

threshold = 0.7


def main():
    img = cv.imread('arroz.bmp', cv.IMREAD_GRAYSCALE)

    # oldColor = 1;
    #
    # newColor = oldColor ? 0: 1;

    # rotula(2, img, 0, 0)

    img_out = img

    img_bin = binariza(img, img_out, threshold)

    show_img("Binarizada", img_bin)

    # print("Quantidade de arroz: ", rotula(img_bin, 0, 0, 0.1))


def show_img(title, img):
    cv.imshow(title, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def binariza (img_in, img_out, threshold):
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


# def floodFill(i, j):
#
#     if ( 0 <= i and i < height and   0 <= j and j < width and  bitmap[i][j] == oldColor )
#     {
#         bitmap[i][j] = newColor;
#         floodFill(i-1,j);
#         floodFill(i+1,j);
#         floodFill(i,j-1);
#         floodFill(i,j+1);
#     }
# }

def floodfill (label, img, x0, y0):

    if (img[x0][y0] == 1) or (x0 < 0 and y0 < 0):
        return

    img[x0:y0] = label

    floodfill(label, img, x0 + 1, y0)
    floodfill(label, img, x0 - 1, y0)
    floodfill(label, img, x0, y0 + 1)
    floodfill(label, img, x0, y0 - 1)

    return img


def rotula (img, componentes, largura_min, altura_min, n_pixels_min):
    pass

if __name__ == '__main__': main()