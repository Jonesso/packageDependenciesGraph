import requests
from graphviz import Digraph
import os
import PIL
from PIL import ImageTk
from PIL import Image
from tkinter import *

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin'  # необходимо для построения графика

dependencies = {}

site = 'https://pypi.org/pypi/'  # официальный сайт с документацией по пакетам


# парсинг JSON-файла с зависимостями, полученного с сайта
def add_dependency(package_name):
    request = requests.get(site + package_name + '/json')
    dependencies[package_name] = []

    if not request.json()["info"]['requires_dist'] is None:
        # добавление зависимостей в словарь
        for dependency in request.json()["info"]['requires_dist']:
            # extra-зависимости не включаются в график
            if "extra" not in dependency:
                # отбрасываем все, кроме названия зависимости
                dependency = re.sub('[^a-zA-Z_-]', '', dependency)
                dependencies[package_name].append(dependency)
        # рекурсивный вызов для зависимых пакетов
        for name in dependencies[package_name]:
            if name not in dependencies and requests.get(site + name + '/json').status_code == 200:
                add_dependency(name)

        # удаление пакетов, у которых нет зависимостей (уже встречаются как зависимости)
        for x in list(dependencies.keys()):
            if not dependencies[x]:
                del dependencies[x]


#   функция вывода кода для графа   
def make_graph(package_name):
    add_dependency(package_name)
    dot = Digraph(format='png')
    for package in dependencies.keys():
        for name in dependencies[package]:
            dot.edge(package, name)
    dot.render("graph", ".")

    graph_code_label.configure(text=dot.source)
    graph_code_label.place(x=20, y=150)

    img = ImageTk.PhotoImage(PIL.Image.open("graph.png"))
    can.delete("all")
    can.img = img
    can.place(x=300, y=150)
    can.config(width=img.width(), height=img.height())
    can.create_image(0, 0, anchor=NW, image=img)

    img_label.configure(text="You can also find your graph in current directory ('graph.png')",
                        font=("Courier New", 10, "bold"), fg="Green")
    img_label.place(x=300, y=550)
    # print(dot.source)  # если код графа нужно куда-то скопировать - раскомментируйте эту строку,
                         # ответ будет выведен в консоль
    dependencies.clear()


# Настройки внешнего вида окна приложения
window = Tk()
window.title('Package dependencies graph')
window.geometry("900x600")

label1 = Label(window, text="Enter package name:", bg="Indigo", fg="White", font=("Courier New", 12, "bold"), bd=10,
               justify=LEFT, height=2, width=20)
label1.place(x=20, y=20)

# поле для ввода названия пакета
entry1 = Entry(window, width=30)
entry1.place(x=250, y=40)

button1 = Button(window, text="Get my graph!", command=lambda: make_graph(str(entry1.get().lower())))
button1.place(x=450, y=35)

# код для графа
graph_code_label = Label(window, text="")

your_code_label = Label(window, text="Your graph code:", font=("Times New Roman", 16, "bold"))
your_code_label.place(x=30, y=100)

your_graph_label = Label(window, text="Your graph image:", font=("Times New Roman", 16, "bold"))
your_graph_label.place(x=450, y=100)

img_label = Label(window, text="")
can = Canvas(window)

window.mainloop()
