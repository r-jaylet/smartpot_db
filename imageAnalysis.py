#!/usr/bin/env python3
# coding:utf-8

import cv2
import os
import time
from time import sleep

"""ici on trouvera toutes les fonctions en rapport avec le traitement d'image """


def NDVI_local(image, x, y):
    """methode permettant de calculer le NDVI du pixel (x,y). Je considère que l'on obtient une image à 4 canaux mais il faudra probablement transformer deux images (une RGB et un IR) en une image à 4 canaux (ordre des canaux R,G,B,IR)"""
    img = cv2.imread(image)
    pixel = img[x, y]
    return ((pixel[3] - pixel[0]) / (pixel[3] + pixel[0]))


def NDVI_global(image):
    """cette méthode renvoie un tableau contenant la liste des NDVI pixels par pixels"""
    res = []
    img = cv2.imread(image)
    height, length = img.shape()
    for x in range(height):
        l = []
        for y in range(length):
            l.append(NDVI_local(image, x, y))
        res.append(l)
    return (res)


def detect_leaves(image, name):
    """Cette fonction met à 0 tout les pixels dont le NDVI est inférieur à 0.1
    Name est le nom de la nouvelle image"""
    NDVI = NDVI_global(image)
    img = cv2.imread(image)
    height, length = img.shape()
    for x in range(height):
        for y in range(length):
            if NDVI[x][y] < 0.1:
                img[x, y] = (0, 0, 0)
    cv2.imwrite(name, img)


def get_image():
    """Prend une image et la retourne. Je ne sais pas s'il faut automatiser la fonction"""
    while (True):
        if (time.ctime()[11:16] == '12:00'):
            camera = PiCamera()
            camera.start_preview()
            sleep(2)
            camera.capture('/home/pi/Desktop/image.jpg')
            camera.stop_preview()

            img = Image.open('/home/pi/Desktop/image.jpg')

            return img


def simple_disease_detection(image):
    """Prend en entrée une image de feuille et verifie si la plante est malade. On convertit d'abord l'image en niveaux de gris puis on fait un seuillage pour binariser l'image enfin on utilise findContours (s'il n'y a pas de contours on considère qu'il n'y a pas de tâche). On renvoie 0 si la plante est en bonne santé et 1 sinon """
    if not (os.path.isfile(image)):
        raise Exception("image is not file")

    img1 = cv2.imread(image)
    img = img1.copy()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imggray, 127, 255, 0)
    img2, contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return (0)
    else:
        return (1)


HEALTHY = 0
ILL = 1


def multiple_disease_detection(image: str) -> int:
    """
       image: lien vers l'image.
       Prend en entrée une image de plante avec plusieurs feuilles et
       verifie si la plante est malade. On convertit d'abord l'image
       en niveaux de gris puis on fait un seuillage pour binariser
       l'image enfin on utilise findContours Les contours les plus à
       l'exterieurs dans la hiérarchie sont les feuilles et si les
       feuilles ont un contour fils alors c'est une tâche et la plante
       est malade.
    """
    if not (os.path.isfile(image)):
        raise Exception("image is not file")

    img1 = cv2.imread(image)
    img = img1.copy()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imggray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return HEALTHY
    else:
        for i in range(len(hierarchy[0])):
            if hierarchy[0][i][2] != -1:
                return ILL
        return HEALTHY


if __name__ == '__main__':
    link = "./imagesTest/feuille_saine.jpg"
    print("saine: ", multiple_disease_detection(link))
    link = "./imagesTest/feuille_malade.jpg"
    print("malade: ", multiple_disease_detection(link))
