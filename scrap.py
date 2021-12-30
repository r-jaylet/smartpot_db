import bs4
import requests
import string
import pandas as pd
import sqlite3


"""
Create DB from scrapping data of a website
"""


def getWebPages():
    """
        return list with all the URL accessible with names of plant : link to all the plant seach pages
    """
    base = "https://jardinage.ooreka.fr/plante/rechercheAlpha/"
    alpha = list(string.ascii_lowercase)
    L = []
    for i in range(len(alpha)):
        token = base+alpha[i]
        L.append(token)
        for i in range(2,30):
            j = token + "/" +str(i)
            r = str(requests.get(j))
            if(r != "<Response [404]>"):
                L.append(j)
            else:
                break
    return L



def getNames(L):
    """
        returns list with all the URLs of all the elements in a web page : link to all the plant pages
    """
    res=[]
    for link in L:
        requete = requests.get(link)
        page = requete.content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        for name in soup.find_all("a", {"class":"titre_liste_plante"}):
            res.append("https://jardinage.ooreka.fr" + name.get("href"))
    return res





def getMaxCount(txt,list):
    """
        return the most recurent in word in the str txt from the list of word list
    """
    L=[]
    for i in range(len(list)):
        L.append(txt.count(list[i]))
    m = max(L)
    a = L.index(max(L))
    if m > 1 :
        return list[a]
    else :
        return 'None'


def getMaxCount2(txt,list):
    """
        return the most recurent in word in the str txt from the list of word list
    """
    L=[]
    for i in range(len(list)):
        L.append(txt.count(list[i]))
    m = max(L)
    a = L.index(max(L))
    if m >= 1 :
        return list[a]
    else :
        return 'None'



"""
listeURL = lyste.split(", '")
for i in range(len(listeURL)):
    listeURL[i] = listeURL[i].replace('\n', '')
    listeURL[i] = listeURL[i][0:-2]
"""



lst = ['Nom(s) commun(s)', 'Nom(s) latin(s)', 'Famille', 'Type(s) de plante','Couleur des fleurs', 'Végétation', 'Entretien', 'Besoin en eau', 'Croissance', 'Résistance au froid', 'Type de sol', 'Exposition']

def getCharacteristicsPage(L):
    res=[]
    for link in L:
        plant = ['None']*12
        requete = requests.get(link)
        page = requete.content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        for points in soup.find_all("li", {"class":"clearfix"}):
            point = points.text
            point = point.replace('\n','')
            point = point.replace('\t','')
            for i in range(len(lst)):
                if point[0:len(lst[i])] == lst[i]:
                    plant[i]=point
        plant[0] = plant[0].replace('Nom(s) commun(s)', '')
        plant[1] = plant[1].replace('Nom(s) latin(s)', '')
        plant[2] = plant[2].replace('Famille', '')
        plant[3] = getMaxCount2(plant[3],["Arbre", "Arbuste", "Plante comestible", "Plante ornementale"])
        plant[4] = plant[4].replace('Couleur des fleurs', '')
        plant[4] = plant[4].replace('Fleurs', '')
        plant[4] = plant[4].strip()
        plant[5] = getMaxCount(plant[5],["Vivace", "Bisannuelle", "Annuelle"])
        plant[6] = getMaxCount(plant[6],["Facile", "Modéré", "Difficile"])
        plant[7] = getMaxCount(plant[7],["Faible", "Moyen", "Important"])
        plant[8] = getMaxCount(plant[8],["Lente", "Normale", "Rapide"])
        plant[9] = getMaxCount(plant[9],["À protéger", "À rentrer", "Résistante"])
        plant[10] = getMaxCount(plant[10],["Sol argileux", "Sol calcaire", "Sol sableux", "Sol caillouteux", "Humifère", "Terre de bruyère", "Terreau"])
        plant[11] = getMaxCount(plant[11],["Soleil", "Mi-ombre", "Ombre" ])
        ima = soup.find("a", {"class":"_lightbox-photos presentation_img_intro"})
        if ima == None:
            plant = plant +['None']
        else :
            plant = plant + [ima.get("href")]
        desc = soup.find("p", {"class":"intro_courte_plantes"})
        if desc == None:
            plant = plant +['None']
        else :
            plant = plant + [desc.get_text()]
        periode = soup.find_all("td", {"class":"_selected1 selectionne"})
        if periode == []:
            plant = plant +['None']
        else :
            plant = plant + [periode[0].get_text()+' - '+periode[-1].get_text()]
        res.append(plant)
    return res



"""
connection = sqlite3.connect("smart.db")
cursor = connection.cursor()
for p in getCharacteristicsPage(listeURL):
    cursor.execute("INSERT INTO plants VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", p)
connection.commit()
connection.close()
"""