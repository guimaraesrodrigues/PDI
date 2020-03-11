import cv2 as cv
import sys
import numpy as np

threshold = 0.7


def main():
    sys.setrecursionlimit(650000)

    img = cv.imread('arroz.bmp', cv.IMREAD_GRAYSCALE)

    # oldColor = 1;
    #
    # newColor = oldColor ? 0: 1;

    # rotula(2, img, 0, 0)

    img_out = img

    img_bin = binariza(img, img_out, threshold)

    # for i in range(img_out.shape[0]):
    #     for j in range(img_out.shape[1]):
    #         if img_bin[i][j] != 0.0:
    #             print(img_bin[i][j])

    # show_img("Binarizada", img_bin)

    print("Quantidade de arroz: ", rotula(img_bin, 20, 30, 60))


def show_img(title, img):
    cv.imshow(title, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def binariza(img_in, img_out, threshold):
    if img_in.shape != img_out.shape:
        print("ERRO: binariza: as imagens precisam ter o mesmo tamanho e numero de canais.")
    else:
        img_out = cv.normalize(img_in.astype('float'), None, 0.0, 1.0, cv.NORM_MINMAX)

        for i in range(img_out.shape[0]):
            for j in range(img_out.shape[1]):
                if img_out[i][j] > threshold:
                    img_out[i][j] = -1.0
                else:
                    img_out[i][j] = 0

        return img_out


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


def defineComponents(img, component, x0, y0):
    if x0 < 0 or y0 < 0:
        return

    if x0 >= img.shape[0]-1 or y0 >= img.shape[1]-1:
        return

    if img[x0][y0] == 0:
        return

    if x0 > component['x0']:
        component['x'] = x0

    if x0 > component['y0']:
        component['y'] = y0

    component['qtd_pixels'] += 1

    defineComponents(img, component, x0 + 1, y0)
    defineComponents(img, component, x0 - 1, y0)
    defineComponents(img, component, x0, y0 + 1)
    defineComponents(img, component, x0, y0 - 1)

    return component


def rotula(img, largura_min, altura_min, n_pixels_min):

    label = 1

    componentsList = []

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == -1.0:
                floodfill(label, img, i, j)
                label += 1

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >= 1:
                new_component = {'label': img[i][j], 'x0': i, 'y0': j, 'x': i, 'y': j, 'qtd_pixels': 0}

                new_component = defineComponents(img, new_component, i, j)

                componentsList.append(new_component)

    for component in componentsList:
        if (component['x'] - component['x0']) < altura_min:
            componentsList.remove(component)
            continue

        if (component['y'] - component['y0']) < largura_min:
            componentsList.remove(component)
            continue

        if component['qtd_pixels'] < n_pixels_min:
            componentsList.remove(component)
            continue

    return len(componentsList)


if __name__ == '__main__': main()
