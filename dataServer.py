import sqlite3

"""
TABLE PLANTS

plant_id : int
common_name : str
latin_name :str
family : str - family in which plant belongs
type : str - type of plant ["None", "Arbre", "Arbuste", "Plante comestible", "Plante ornementale"]
color: str - color possible of plant ["None", "blanches", "bleues" "jaunes", "rouges", "roses", "vertes", "violettes" , "grises", "oranges", "multicolores ou panachées", "noires"]
vegetation: str - type of vegetation ["None", "Vivace", "Bisannuelle", "Annuelle"]
care : int - grade from 1 to 3 of difficulty of care (1 = easy, 2 = intermediate, 3 = hard)
humidity : int - grade from 1 to 3 of humidity level recquiered (1 = low, 2 = medium, 3 = high)
growth : int - grade from 1 to 3 of speed of growth (1 = slow, 2 = intermediate, 3 = fast)
hardiness : int grade from 1 to 3 of hardiness (resistance to cold) level recquiered (1 = low, 2 = medium, 3 = high)
soil : str - type of soil in which can evolve the plant ["None","Sol argileux", "Sol calcaire", "Sol sableux", "Sol caillouteux", "Humifère", "Terre de bruyère", "Terreau"]
lighting : int - grade from 1 to 3 of lighting level recquiered (1 = low, 2 = medium, 3 = high)
image :str - string used to get url for image
description : str - short description of plant
plantation : str - months in which should be planted (ex : "3 - 8" for march to august)
"""


def convertRow(list):
    """
        takes for argument a a tuple (row that results from a sql request) and returns a list of dictionnaries with all the charactericts of each plant (except image and link column) of SQL research
    """
    columns = ["plant_id", "common_name", "latin_name", "family", "type", "color", "vegetation", "care", "humidity",
               "growth", "hardiness", "soil", "lighting", "plantation"]
    L = []
    for k in range(len(list)):
        res = {}
        for i in range(len(columns) - 1):
            res[columns[i]] = list[k][i]
        res[columns[len(columns) - 1]] = list[k][len(columns) + 1]
        L.append(res)
    return L


def description(name):
    """
        return description of a plant (str) according to its name
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    res = {}
    cursor.execute('SELECT description FROM plants WHERE common_name =?', (name,))
    res["description"] = cursor.fetchone()[0]
    return res
    connection.close()


def image(name):
    """
        return link image of a plant (str) according to its name
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    res = {}
    cursor.execute('SELECT description FROM plants WHERE common_name =?', (name,))
    res["image"] = cursor.fetchone()[0]
    connection.close()
    return res


def plantation(name):
    """
        return period of plantation of a plant (str) according to its name
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    res = {}
    cursor.execute('SELECT plantation FROM plants WHERE common_name =?', (name,))
    res["plantation"] = cursor.fetchone()[0]
    connection.close()
    return res


def characteristics(name):
    """
        return characteristics (lighting, humidity, hardiness) of plant according to common_name.
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    res = {}
    cursor.execute('SELECT humidity FROM plants WHERE common_name = ?', (name,))
    res["humidity"] = cursor.fetchone()[0]
    cursor.execute('SELECT lighting FROM plants WHERE common_name = ?', (name,))
    res["lighting"] = cursor.fetchone()[0]
    cursor.execute('SELECT hardiness FROM plants WHERE common_name = ?', (name,))
    res["hardiness"] = cursor.fetchone()[0]
    connection.close()
    return res


def table_plant():
    """
        return a dictionnary for every plant in the table
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    list = []
    for row in cursor.execute('SELECT * FROM plants'):
        list.append(row)
    connection.close()
    return convertRow(list)


def searchByName(name: str, n_max: int = 10):
    """
        return list of dictionnaries of plants according by searching common_name close to name (takes str for argument) (ex : 'Oranger' not Oranger)
        returns empty list if it doesn't correspond to any plant
    """
    connection = sqlite3.connect("smart.db")
    cursor = connection.cursor()
    list = []
    name = name + '%'
    c = 1
    for row in cursor.execute('SELECT * FROM plants WHERE common_name  LIKE ? ORDER BY common_name', (name,)):
        if c <= n_max:
            list.append(row)
            c += 1
        else:
            break
    connection.close()
    return convertRow(list)
