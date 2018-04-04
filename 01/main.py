import cv2 as cv

def main():
    img = cv.imread('arroz.bmp', )
    print(img)


    cv.imshow('ola', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #cv.imwrite('arrozb.bmp', img)


def binariza(img_in, img_out, threshold):
    pass


def rotula(img, componentes, largura_min, altura_min, n_pixels_min):
    pass


if  __name__ =='__main__':main()