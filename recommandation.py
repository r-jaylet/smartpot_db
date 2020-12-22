import sqlite3
from random import *
from typing import List

"""Dans ce fichier on définira les fonctions implémentants les deux algorithmes de recommandation"""


#def nearest_neighbors(k):
    #k est le nombre de plantes que l'on veut recommander
    #name,temp,lum,hum=read_file("bdd_smart_pot.csv")
    #temp=transform_temp(temp)
    #lum=transform_lum(lum)
    #hum=transform_hum(hum)
    #param=zip(temp,lum,hum)

def createBase():
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    plantL = []
    for row in cursor.execute('SELECT common_name, type, color, care, growth, plantation, hardiness, lighting FROM plants'):
        plantL.append(row)
    return plantL
    connection.close()


def score_type(type,criteria):
    """"Donne le score pour le type de plante. type est une string donnant le type de la plante dont on veut le score. criteria est une string donnant le type voulu par l'utilisateur"""
    if (criteria.lower()=="pas de préférences"):
        return(0.3)
    if (type.lower()=='none'):
        return(0)
    elif(type.lower()==criteria.lower()):
        return(0.3)
    else:
        return(0)

def score_month(month,criteria):
    """Donne un score selon le mois durant lequel l'utilisateur préfére planter sa plante. La string month est le meilleur mois pour planter une certaine plante (les mois de la bdd sont de la forme janvier,février...décembre. La string criteria est le critère de notation (mois choisi par l'utilisateur au format numérique soit 1,2,3,4...12. Les éléments month de la bdd prennent souvent la forme "Avril-Mai"."""
    if (criteria.lower()=="pas de préférences"):
        return(0.2)
    months=[]
    k=0
    for i in range(len(month)):
        if month[i]=="-":
            months.append(month[k:i-1])
            k=i+2
    months.append((month[k:]))

    for i in range(len(months)):
        if months[i]=='JANVIER':
            months[i]=1
        if months[i]=='FÉVRIER':
            months[i]=2
        if months[i]=='MARS':
            months[i]=3
        if months[i]=='AVRIL':
            months[i]=4
        if months[i]=='MAI':
            months[i]=5
        if months[i]=='JUIN':
            months[i]=6
        if months[i]=='JUILLET':
            months[i]=7
        if months[i]=='AOÛT':
            months[i]=8
        if months[i]=='SEPT.':
            months[i]=9
        if months[i]=='OCT.':
            months[i]=10
        if months[i]=='NOV.':
            months[i]=11
        if months[i]=='DÉC.':
            months[i]=12
    for i in range(len(months)-1):
        if(months[i]<= int(criteria) and months[i+1]>= int(criteria) ):
            return(0.2)
    return(0)

def score_flower_color(color,criteria):
    """Donne un score pour la couleur des fleurs. La string color est la couleur de la plante que l'on veut noter. La string criteria est la couleur choisie par l'utilisateur."""
    if criteria=="pas de préférences":
        return 0.2
    k=0
    colors=[]
    for i in range(len(color)):
        if (color[i]=="-"):
            colors.append(color[k:i])
            k=i+1
    colors.append(color[k::])
    for i in range(len(colors)):
        if (colors[i].lower()==criteria.lower()):
            return(0.2)
    return 0


def score_growth(speed,criteria):
    """Donne un score pour la vitesse de croissance d'une plante. La string speed est la vitesse de croissance de la plante à noter. La string criteria la vitesse voulue par l'utilisateur"""
    if criteria.lower()=="pas de préférences":
        return 0.1
    criteria=criteria.lower().replace("court","1")
    criteria=criteria.lower().replace("moyen","2")
    criteria=criteria.lower().replace("long","3")
    if int(speed)==int(criteria):
        return(0.1)
    else:
        return 0

def score_care(care,criteria):
    """Donne un score pour la difficulté d'entretien de la plante. La string care est la difficulté d'entretien de la plante à noter. La string criteria est le critère de difficulté choisi par l'utilisateur"""
    if (criteria.lower()=="pas de préférences"):
        return 0.1
    criteria=criteria.lower().replace("facile",'1')
    criteria=criteria.lower().replace("moyen",'2')
    criteria=criteria.lower().replace("difficile",'3')
    if int(care)==int(criteria):
        return 0.1
    else:
        return 0

def score_location(cold,light,criteria):
    """Donne un score pour l'endroit où l'on veut placer la plante. La string criteria est l'endroit choisi par l'utilisateur pour placer la plante (intérieur ou extérieur). Le positionnement idéal de la plante est calculé à partir des string cold et light (résistance au froid et exposition)"""
    if criteria.lower()=="pas de préférences":
        return(0.1)
    else:
        if (float(cold)<=1.5 and float(light<=1.5)):
            if criteria.lower()=="interieur":
                return(0.1)
            else:
                return(0)
        else:
            if criteria.lower()=="exterieur":
                return(0.1)
            else:
                return 0


def grading_individual(plant,criterions):
    """cette fonction attribue une note de recommandation à une plante à partir des critères: elle renvoie le nom de la plante et son score
    plant est de la forme [name,type,flower_color,care,growth,month,cold,light]
    criterions)=[type,flower_color,care,growth,month,place] dont les descriptions sont en-dessous
    -type est un string qui prend comme valeurs: "Arbre","Arbuste","Plante ornementale","plante comestible","fleur","pas de préférences"
    -flower_color est un string
    -care est un string qui prend pour valeurs "facile","moyen","difficile",'pas de préférences'
    -growth est un string qui prend pour valeurs "cour","moyen","long","pas de préférences"
    -month est un string (représentant un entier) qui prend des valeurs de "1" à "12" (inclus) ou bien "pas de préférences"
    -place est un string qui prend comme valeurs "intérieur","exterieur","pas de préférences"
    """
    res=0
    res+=score_type(plant[1],criterions[0])
    res+=score_flower_color(plant[2],criterions[1])
    res+=score_care(plant[3],criterions[2])
    res+=score_growth(plant[4],criterions[3])
    res+=score_month(plant[5],criterions[4]) 
    res+=score_location(plant[6],plant[7],criterions[5])

    return((res,plant[0]))

def grading_global(plants,criterions):
    """renvoie la liste couples (name,grade)
plants est la liste des plantes au format [plant1,plant2....] où plant1 est de la forme indiquée dans grading_individual"""
    res=[]
    for plant in plants:
       res.append(grading_individual(plant,criterions))
    return(res)


PLANTS = createBase()
for plant in PLANTS:
    for i in range(len(plant)):
        if i==0 or i==1 or i==2 or i==5:
            if not(type(plant[i])==str):
                raise Exception('Name, type, flower_color and month should be Strings')
        elif i==3 or i==4:
            if not(type(plant[i])==int):
                raise Exception('care and growth should be ints')

def recommandation(type_="pas de préférences",
                   flower_color="pas de préférences",
                   care="pas de préférences",
                   growth="pas de préférences",
                   month="pas de préférences",
                   place="pas de préférences")->List[str]:
    """
        L'algorithme de recommandation à partir d'une liste de plantes et d'une liste de critère on renvoie 5 plantes dont les critères sont proches de ceux demandé par l'utilisateur. Le retour se fait aléatoirement entre les au plus 15 meilleures plantes
        Criterions vient de l'Application
        criterions: [type,flower_color,care,growth,month,place]
        -type est un string qui prend comme valeurs: "Arbre","Arbuste","Plante ornementale","plante comestible","fleur","pas de préférences"
        -flower_color est un string: "Noir", "bleu", "violet", "vert", "jaune", "orange", "rouge", "blanc", "rose", "mauve", "pas de préférences"
        -care est un string qui prend pour valeurs "facile","moyen","difficile",'pas de préférences'
        -growth est un string qui prend pour valeurs "cour","moyen","long","pas de préférences"
        -month est un string (représentant un entier) qui prend des valeurs de "1" à "12" (inclus) ou bien "pas de préférences"
        -place est un string qui prend comme valeurs "intérieur","exterieur","pas de préférences"
    """
    criterions = [type_, flower_color, care, growth, month, place]
    print(criterions)
    plants = PLANTS
    for i in range(len(criterions)):
        if i==0 or i==1 or i==4 or i==5:
            if not(type(criterions[i])==str):
                raise Exception('Name, type, flower_color, location and month should be Strings')

    res=sorted(grading_global(plants,criterions))
    """
    seuil=2
    while res[-seuil][0]<0.6 or res[-seuil][0]-res[-seuil][0]>0.2 or seuil>15:
        seuil=seuil+1
    shuffle(res[-seuil:])
    res1=[]
    seuil=int(seuil/3)
    for i in range(len(res)):
        res1.append(res[i][1])
    return(res1[-5:])
    """
    fin=[]
    for p in res[-5:]:
        fin.append(p[1])
    return fin
