import requests
import re
from graphviz import Digraph
import os

dependencies = {}

site = 'https://pypi.org/pypi/'

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin'


# функция парсинга JSON
def json_parse(package_name):
    request = requests.get(site + package_name + '/json')
    dependencies[package_name] = []
    # проверка, есть ли необходимые пакеты
    if request.json()["info"]['requires_dist'] is not None:
        # добавление необходимых пакетов в словарь
        for dependency in request.json()["info"]['requires_dist']:
            if "extra" not in dependency:
                dependency = re.sub('[^a-zA-Z_-]', '', dependency)
                dependencies[package_name].append(dependency)
        # рекурсивный вызов функции для пакетов, зависимых от текущего 
        for name in dependencies[package_name]:
            if name not in dependencies and requests.get(site + name + '/json').status_code == 200:
                json_parse(name)

        for x in list(dependencies.keys()):
            if not dependencies[x]:
                del dependencies[x]


#   функция вывода кода для графа   
def graph_creation(package_name):
    dot = Digraph(format='png')
    for package in dependencies.keys():
        for name in dependencies[package]:
            dot.edge(package, name)
    # dot.render("graph", ".", True)
    print(dot.source)


package_name = input("Enter package name: ").lower()
json_parse(package_name)
# print(dependencies)
graph_creation()

