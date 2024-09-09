from typing import Any, Optional, Tuple
import html

from graphviz import Digraph

import csv
notes = ''
with open('/Users/lymich/Documents/kes/TRABAJOS/4 SEMESTRE/EDD 2/dataset_movies.csv', newline='') as f:
    data = csv.reader(f, delimiter=',')
    notes = list(data)

class Movies:
    def __init__(self, title, year, worldwide_earnings, domestic_earnings, foreign_earnings, domestic_percent_earnings, foreign_percent_earnings) -> None:
        self.title = title
        self.year = year
        self.worldwide_earnings = worldwide_earnings
        self.domestic_earnings = domestic_earnings
        self.foreign_earnings = foreign_earnings
        self.domestic_percent_earnings = domestic_percent_earnings
        self.foreign_percent_earnings = foreign_percent_earnings
        pass

    #def __lt__(self, other):
    #    return self.title < other.title

    def __repr__(self):
        return (f'{self.title} ({self.year})')
    
    #def __repr__(self):
        return (f"{self.title} ({self.year}) - Worldwide Earnings: {self.worldwide_earnings}, "
                f"Domestic Earnings: {self.domestic_earnings}, Foreign Earnings: {self.foreign_earnings}, "
                f"Domestic Percent Earnings: {self.domestic_percent_earnings}, Foreign Percent Earnings: {self.foreign_percent_earnings}")

def getData(notes): #MANEJO DEL DATASET
    movies_list = []

    for i in range(1, len(notes)):
        movie = Movies(
            title=notes[i][0],
            worldwide_earnings=float(notes[i][1]),
            domestic_earnings=float(notes[i][2]),
            domestic_percent_earnings=float(notes[i][3]),
            foreign_earnings=float(notes[i][4]),
            foreign_percent_earnings=float(notes[i][5]),
            year=int(notes[i][6])
        )
        movies_list.append(movie)
    
    return movies_list

class Node:
    def __init__(self, data: Movies) -> None:
        self.data = data
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

class AVLTree:

    #BASICAS DE UN ARBOL

    def __init__(self, root: Optional["Node"] = None) -> None:
        self.root = root

    #RECORRIDOS

    def preorder(self) -> None:
        self.__preorder_r(self.root)
        print()

    def __preorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            print(node.data, end = ' ')
            self.__preorder_r(node.left)
            self.__preorder_r(node.right)

    def preorder_nr(self) -> None:
        s = []
        p = self.root
        while p is not None or len(s) > 0:
            if p is not None:
                print(p.data, end = ' ')
                s.append(p)
                p = p.left
            else:
                p = s.pop()
                p = p.right
        print()

    def inorder(self) -> None:
        self.__inorder_r(self.root)
        print()

    def __inorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__inorder_r(node.left)
            print(node.data, end = ' ')
            self.__inorder_r(node.right)

    def inorder_nr(self) -> None:
        s = []
        p = self.root
        while p is not None or len(s) > 0:
            if p is not None:
                s.append(p)
                p = p.left
            else:
                p = s.pop()
                print(p.data, end = ' ')
                p = p.right
        print()

    def postorder(self) -> None:
        self.__postorder_r(self.root)
        print()

    def __postorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__postorder_r(node.left)
            self.__postorder_r(node.right)
            print(node.data, end = ' ')

    def levels_nr(self) -> None:
        q = []
        p = self.root
        q.append(p)
        while len(q) > 0:
            p = q.pop(0)
            print(p.data, end = ' ')
            if p.left is not None:
                q.append(p.left)
            if p.right is not None:
                q.append(p.right)
        print()

    #POSIBLE OPCIÓN RECORRIDO POR NIVELES RECURSIVO
    
    def recorrido_por_niveles(self):
        altura = self.height()
        resultado = ""
        for nivel in range(1, altura + 1):
            resultado += self.recorrer_nivel(self.root, nivel) + "\n"
        return resultado

    def recorrer_nivel(self, node: Optional["Node"], nivel) -> str:
        if node is None:
            return ""
        
        if nivel == 1:
            return node.data.title + ", "
        
        elif nivel > 1:
            izquierda = self.recorrer_nivel(node.left, nivel-1)
            derecha = self.recorrer_nivel(node.right, nivel-1)
            return izquierda + derecha
   
    #ALTURA DE UN ARBOL o NODO

    def height(self) -> int:
        return self.__height_r(self.root)

    def __height_r(self, node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return 1 + max(self.__height_r(node.left), self.__height_r(node.right))

    #FUNCIONES PARA UN ABB
    def search_string(self, data: str) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if data == p.data.title:
                return p, pad
            else:
                pad = p
                if data < p.data.title:
                    p = p.left
                else:
                    p = p.right
        return p, pad

    def search(self, data: Movies) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if data == p.data.title:
                return p, pad
            else:
                pad = p
                if data < p.data.title:
                    p = p.left
                else:
                    p = p.right
        return p, pad
    
    #BUSQUEDA ESPECIAL CON CONDICIONES - PUNTO 4
    def search_condiciones_string(self, year: int, int_earnings: float):
        list = self.search_condiciones2(self.root, year, int_earnings)
        return list
    
    def search_condiciones2(self, node, year: int, int_earnings: float) -> list:
        List = []
        if node is not None:
            List.extend(self.search_condiciones2(node.left, year, int_earnings))
            if (node.data.year == year) and (node.data.domestic_percent_earnings < node.data.foreign_percent_earnings) and (node.data.foreign_earnings >= int_earnings):
                List.append(node)
            List.extend(self.search_condiciones2(node.right, year, int_earnings))
        
        return List  

    ################################################

    def insertar_string(self, data):
        movies = getData(notes)
        for movie in movies:
            if data == movie.title:
                self.insert(movie)
                self.visualize()

    def insert(self, data: Movies) -> bool:
        to_insert = Node(data)
        if self.root is None:
            self.root = to_insert
            return True
        else:
            p, pad = self.search(data.title)
            if p is not None:
                return False
            else:
                if data.title < pad.data.title:
                    pad.left = to_insert
                else:
                    pad.right = to_insert

                self.root = self.__balance_node_(self.root)

                return True
    
    def delete_string(self, data):
        movies = getData(notes)
        for movie in movies:
            if data == movie.title:
                self.delete(movie)
                self.visualize()

    def delete(self, data: Movies, mode: bool = True) -> bool:
        p, pad = self.search(data.title)
        if p is not None:
            if p.left is None and p.right is None:
                if p == self.root: 
                    self.root = None # Eliminar la raíz
                elif p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p

            elif p.left is None and p.right is not None:
                child = p.left if p.left else p.right
                if p == self.root:
                    self.root = child  # Eliminar la raíz
                elif p == pad.left:
                    pad.left = p.right
                else:
                    pad.right = p.right
                del p

            elif p.left is not None and p.right is None:
                child = p.left if p.left else p.right
                if p == self.root:
                    self.root = child  # Eliminar la raíz
                elif p == pad.left:
                    pad.left = p.left
                else:
                    pad.right = p.left
                del p

            else:
                if mode:
                    pred, pad_pred, son_pred = self.__pred(p)
                    p.data = pred.data
                    if p == pad_pred:
                        pad_pred.left = son_pred
                    else:
                        pad_pred.right = son_pred
                    del pred
                else:
                    sus, pad_sus, son_sus = self.__sus(p)
                    p.data = sus.data
                    if p == pad_sus:
                        pad_sus.right = son_sus
                    else:
                        pad_sus.left = son_sus
                    del sus
            self.root = self.__balance_node_(self.root)
            
            return True
        return False

    def __pred(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.left, node
        while p.right is not None:
            p, pad = p.right, p
        return p, pad, p.left

    def __sus(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.right, node
        while p.left is not None:
            p, pad = p.left, p
        return p, pad, p.right
    
    #ROTACIONES PARA BALANCEAR LOS AVL

    def simple_left_rotation(self, node: Optional["Node"]) -> Node:
        aux = node.right
        node.right = aux.left
        aux.left = node
        return aux
    
    def simple_right_rotation(self, node: Optional["Node"]) -> Node:
        aux = node.left
        node.left = aux.right
        aux.right = node
        return aux
    
    def double_right_left_rotation(self, node: Optional["Node"]) -> Node:
        node.right = self.simple_right_rotation(node.right)
        return self.simple_left_rotation(node)

    def double_left_right_rotation(self, node: Optional["Node"]) -> Node:
        node.left = self.simple_left_rotation(node.left)
        return self.simple_right_rotation(node)
        
    def balance_factor(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return self.__height_r(node.right)-self.__height_r(node.left)
    
    def __balance_node_(self, node: Node) -> Node:

        if node.left:
            node.left = self.__balance_node_(node.left)
        if node.right:
            node.right = self.__balance_node_(node.right)

        balance = self.balance_factor(node)
        
        #derecha esta cargada
        if balance > 1:
            if self.balance_factor(node.right) < 0:  # Right-left case
                node = self.double_right_left_rotation(node)
            else:
                node = self.simple_left_rotation(node)  #Left case
        
        #izquierda esta cargada
        if balance < -1:
            if self.balance_factor(node.left) > 0:  # Left-right case
                node = self.double_left_right_rotation(node)
            else:
                node = self.simple_right_rotation(node)  # Right case
            
        return node

    def search_parent(self, data: str) -> Optional["Node"]:
        p, pad = self.search(data)
        return pad
    
    def search_grandparent(self, data: str) -> Optional["Node"]:
        pad = self.search_parent(data)
        if pad is None:
            return None
        grandparent = self.search_parent(pad.data.title)
        return grandparent
    
    def search_uncle(self, data: str) -> Optional["Node"]:
        grandparent = self.search_grandparent(data)
        pad = self.search_parent(data)
        if grandparent is None:
            return None
        
        if pad == grandparent.left:
            return grandparent.right
        
        if pad == grandparent.right:
            return grandparent.left
        
        return None
    
    def level_node(self, node: Optional["Node"], data = str, nivel = 0) -> int:
        if node is None:
            return -1
        if node.data.title == data:
            return nivel
        elif data < node.data.title:
            return self.level_node(node.left, data, nivel + 1)
        else: 
            return self.level_node(node.right, data, nivel + 1)

    def visualize(self):
        dot = Digraph(format='png')
        dot.attr(bgcolor='#000f26')

        def add_edges(node):
            if node:
                label = html.escape(
                    f"{node.data.title} ({node.data.year})\n"
                    f"Worldwide Earnings: {node.data.worldwide_earnings}\n"
                    f"Domestic Earnings: {node.data.domestic_earnings}\n"
                    f"Foreign Earnings: {node.data.foreign_earnings}\n"
                    f"Domestic % Earnings: {node.data.domestic_percent_earnings}\n"
                    f"Foreign % Earnings: {node.data.foreign_percent_earnings}"
                )
                dot.node(
                    str(node.data.title), 
                    label=label,
                    shape='box',  # Forma del nodo: puede ser 'box', 'ellipse', 'circle', etc.
                    style='rounded, filled',  # Estilo del nodo: puede ser 'solid', 'dotted', etc.
                    fillcolor='white',  # Color de fondo del nodo
                    color='black',  # Color del borde del nodo
                    fontcolor='#000f26'  # Color del texto
                )
                if node.left:
                    dot.edge(
                        str(node.data.title), 
                        str(node.left.data.title),
                        color='white',  # Color de la arista
                        style='solid'  # Estilo de la arista: puede ser 'solid', 'dashed', etc.
                    )
                    add_edges(node.left)
                if node.right:
                    dot.edge(
                        str(node.data.title), 
                        str(node.right.data.title),
                        color='white',  # Color de la arista
                        style='solid'  # Estilo de la arista
                    )
                    add_edges(node.right)
        
        if self.root:
            add_edges(self.root)

        dot.render('avl_tree', format='png', view=True)

avl_tree = AVLTree()

movies = getData(notes)
for movie in movies[:20]:
    avl_tree.insert(movie)

####################################

from customtkinter import *
from CTkTable import CTkTable # type: ignore
from PIL import Image, ImageTk

app = CTk()
app.geometry("856x645")
app.resizable(0,0)
app.title("Banco de Películas")

set_appearance_mode("light")

def insertar_view():
    insertar_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=insertar_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="Insertar Nodo Movie", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")

    buscar_insertar_frame = CTkFrame(master=insertar_frame, height=50, width=32, fg_color="#F0F0F0")
    buscar_insertar_frame.pack(fill="x", pady=(200, 0), padx=20)

    insertar_entry = CTkEntry(master=buscar_insertar_frame, width=400, placeholder_text="Escriba la película", border_color="#003360", border_width=2)
    insertar_entry.pack(side="left", padx=(13, 0), pady=15)    
    movie_insertar = insertar_entry.get()

    insert_icon_img_data = Image.open("insert_btn.png")
    insert_icon_img = CTkImage(dark_image=insert_icon_img_data, light_image=insert_icon_img_data, size=(20, 20))

    def on_insert_click():  #Funcion para insertar la pelicula escrita
        movie_insertar = insertar_entry.get()
        avl_tree.insertar_string(movie_insertar)

    verificar_insercion_btn = CTkButton(master=buscar_insertar_frame, text="INSERTAR", fg_color="#00b74a", hover_color="#00e676", font=("Arial Black", 14), corner_radius=10,
                                        height=50, width=180, text_color="#F0F0F0", image=insert_icon_img, border_width=2, border_color="#40916c", command=on_insert_click)
    verificar_insercion_btn.pack(side="left", padx=(20, 0), pady=15)

    insertar_frame.pack(side="left", fill = "both", expand = True)
    insertar_frame.pack_propagate(0)

def eliminar_view():
    eliminar_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=eliminar_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="Eliminar Nodo Movie", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")
    
    eliminar_movie_frame = CTkFrame(master=eliminar_frame, height=50, width=32, fg_color="#F0F0F0")
    eliminar_movie_frame.pack(fill="x", pady=(200, 0), padx=20)

    eliminar_entry = CTkEntry(master=eliminar_movie_frame, width=400, placeholder_text="Escriba la película", border_color="#003360", border_width=2)
    eliminar_entry.pack(side="left", padx=(13, 0), pady=15)    
    movie_eliminar = eliminar_entry.get()

    trash_icon_img_data = Image.open("trash_icon.png") 
    trash_icon_img = CTkImage(dark_image=trash_icon_img_data, light_image=trash_icon_img_data)  

    def on_eliminar_click(): #Funcion para eliminar la pelicula escrita
        movie_eliminar = eliminar_entry.get()
        avl_tree.delete_string(movie_eliminar)

    elimnar_movie_btn = CTkButton(master=eliminar_movie_frame, text="ELIMINAR", fg_color="#e63946", hover_color="#a83232", font=("Arial Black", 14), corner_radius=10,
                                  height=50, width=180, text_color="#F0F0F0", image=trash_icon_img, border_width=2, border_color="#a83232", command=on_eliminar_click)
    elimnar_movie_btn.pack(side="left", padx=(20, 0), pady=15)

    eliminar_frame.pack(side="left", fill = "both", expand = True)
    eliminar_frame.pack_propagate(0)

def buscar_view():
    buscar_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=buscar_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="Buscar Nodo Movie", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")

    buscar_movie_frame = CTkFrame(master=buscar_frame, height=50, width=32, fg_color="#F0F0F0")
    buscar_movie_frame.pack(fill="x", pady=(45, 0), padx=20)

    buscar_movie_entry = CTkEntry(master=buscar_movie_frame, width=400, placeholder_text="Escriba la película", border_color="#003360", border_width=2)
    buscar_movie_entry.pack(side = "left", padx=(13, 0), pady=15)    
    movie_buscar = buscar_movie_entry.get()

    # Frame contenedor para alinear el TextBox y el CTkFrame
    contenedor1_frame = CTkFrame(master=buscar_frame, fg_color="#fff")
    contenedor1_frame.pack(fill="x", pady=(20, 0), padx=20)

    # Configuración del TextBox
    buscar_metrica_text = CTkTextbox(master=contenedor1_frame, font=("Arial", 18), height=140, width=420, fg_color="#F0F0F0", corner_radius=20)
    parrafo_recorrido = ""
    buscar_metrica_text.insert("0.0", parrafo_recorrido)
    buscar_metrica_text.configure(state="disabled")
    buscar_metrica_text.pack(fill = "x")

    # Configuración del TextBox1
    metricas1_text = CTkTextbox(master=buscar_frame, font=("Arial", 18), height=80, width=420, fg_color="#F0F0F0", corner_radius=20)
    parrafo1_recorrido = ""
    metricas1_text.insert("0.0", parrafo1_recorrido)
    metricas1_text.configure(state="disabled")

    # Crear frame para los botones debajo de "buscar_movie_frame"
    botones_frame = CTkFrame(master=buscar_frame, fg_color="#F0F0F0", height=220)
    botones_frame.pack(fill="x", padx=20, pady=20)

    #Metodos de cada boton

    def on_buscar_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)  # Buscar el nodo con la película

        # Habilitar el textbox para actualizar su contenido
        buscar_metrica_text.configure(state="normal")
        buscar_metrica_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            parrafo_recorrido = f"Title: {nodo_encontrado.data.title}\n"
            parrafo_recorrido += f"Year: {nodo_encontrado.data.year}\n"
            parrafo_recorrido += f"Worldwide Earnings: {nodo_encontrado.data.worldwide_earnings}\n"
            parrafo_recorrido += f"Domestic Earnings: {nodo_encontrado.data.domestic_earnings} ({nodo_encontrado.data.domestic_percent_earnings}%)\n"
            parrafo_recorrido += f"Foreign Earnings: {nodo_encontrado.data.foreign_earnings} ({nodo_encontrado.data.foreign_percent_earnings}%)\n"
        else:
            parrafo_recorrido = "Película no encontrada."

        buscar_metrica_text.insert("0.0", parrafo_recorrido)
        buscar_metrica_text.configure(state="disabled")  # Deshabilitar el textbox

    def on_nivelNodo_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)

        metricas1_text.configure(state="normal")
        metricas1_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            nivel_enc = avl_tree.level_node(avl_tree.root, nodo_encontrado.data.title, 0)
            parrafo1_recorrido = f"Nivel: {nivel_enc}\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas1_text.insert("0.0", parrafo1_recorrido)
        metricas1_text.configure(state="disabled")

    def on_factorBalanceo_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)

        metricas1_text.configure(state="normal")
        metricas1_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            factor_enc = avl_tree.balance_factor(nodo_encontrado)
            parrafo1_recorrido = f"Factor de balanceo: {factor_enc}\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas1_text.insert("0.0", parrafo1_recorrido)
        metricas1_text.configure(state="disabled")

    def on_parent_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)

        metricas1_text.configure(state="normal")
        metricas1_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            padre_enc = avl_tree.search_parent(nodo_encontrado.data.title)
            parrafo1_recorrido = f"Nodo padre: {padre_enc.data.title} ({padre_enc.data.year})\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas1_text.insert("0.0", parrafo1_recorrido)
        metricas1_text.configure(state="disabled")
    
    def on_grandParent_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)

        metricas1_text.configure(state="normal")
        metricas1_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            abuelo_enc = avl_tree.search_grandparent(nodo_encontrado.data.title)
            parrafo1_recorrido = f"Nodo abuelo: {abuelo_enc.data.title} ({abuelo_enc.data.year})\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas1_text.insert("0.0", parrafo1_recorrido)
        metricas1_text.configure(state="disabled")

    def on_uncle_click():
        movie_buscar = buscar_movie_entry.get()
        nodo_encontrado, _ = avl_tree.search_string(movie_buscar)

        metricas1_text.configure(state="normal")
        metricas1_text.delete("0.0", "end")  # Limpiar el contenido actual

        if nodo_encontrado is not None:
            tio_enc = avl_tree.search_uncle(nodo_encontrado.data.title)
            parrafo1_recorrido = f"Nodo tío: {tio_enc.data.title} ({tio_enc.data.year})\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas1_text.insert("0.0", parrafo1_recorrido)
        metricas1_text.configure(state="disabled")
    
    # Cargar íconos para los botones
    buscar_icon_img_data = Image.open("buscar_btn.png") 
    buscar_icon_img = CTkImage(dark_image=buscar_icon_img_data, light_image=buscar_icon_img_data)

    nivel_nodo_icon_data = Image.open("nivel_nodo_icon.png")
    nivel_nodo_icon = CTkImage(dark_image=nivel_nodo_icon_data, light_image=nivel_nodo_icon_data, size=(20, 20))

    factor_balanceo_icon_data = Image.open("factor_balanceo_icon.png")
    factor_balanceo_icon = CTkImage(dark_image=factor_balanceo_icon_data, light_image=factor_balanceo_icon_data, size=(20, 20))

    nodo_padre_icon_data = Image.open("nodo_padre_icon.png")
    nodo_padre_icon = CTkImage(dark_image=nodo_padre_icon_data, light_image=nodo_padre_icon_data, size=(20, 20))

    nodo_abuelo_icon_data = Image.open("nodo_abuelo_icon.png")
    nodo_abuelo_icon = CTkImage(dark_image=nodo_abuelo_icon_data, light_image=nodo_abuelo_icon_data, size=(20, 20))

    nodo_tio_icon_data = Image.open("nodo_tio_icon.png")
    nodo_tio_icon = CTkImage(dark_image=nodo_tio_icon_data, light_image=nodo_tio_icon_data, size=(20, 20))

    # Configurar el grid en el frame de botones para centrar los botones
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)
    botones_frame.grid_columnconfigure(2, weight=1)
    botones_frame.grid_rowconfigure(0, weight=1)
    botones_frame.grid_rowconfigure(1, weight=1)

    # Crear los botones
    buscar_movie_btn = CTkButton(master=buscar_movie_frame, text="BUSCAR", fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, height=50, width=180, text_color="#FFFFFF", image=buscar_icon_img, border_width=2, border_color="#006BBF", command=on_buscar_click)
    buscar_movie_btn.pack(side="left", padx=(20, 0), pady=15)

    nivel_nodo_btn = CTkButton(master=botones_frame, text="Nivel nodo", image=nivel_nodo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_nivelNodo_click)
    nivel_nodo_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    factor_balanceo_btn = CTkButton(master=botones_frame, text="Factor balanceo", image=factor_balanceo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_factorBalanceo_click)
    factor_balanceo_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    nodo_padre_btn = CTkButton(master=botones_frame, text="Nodo padre", image=nodo_padre_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_parent_click)
    nodo_padre_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    nodo_abuelo_btn = CTkButton(master=botones_frame, text="Nodo abuelo", image=nodo_abuelo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_grandParent_click)
    nodo_abuelo_btn.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    nodo_tio_btn = CTkButton(master=botones_frame, text="Nodo tío", image=nodo_tio_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_uncle_click)
    nodo_tio_btn.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    metricas1_text.pack(pady=(5, 0), padx=80)
    
    buscar_frame.pack(side="left", fill = "both", expand = True)
    buscar_frame.pack_propagate(0)
    
def buscar_metrica_view():
    buscar_metrica_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=buscar_metrica_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="Buscar Nodo Movie por métrica", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")

    buscar_movie_metrica_frame = CTkFrame(master=buscar_metrica_frame, height=50, fg_color="#F0F0F0")
    buscar_movie_metrica_frame.pack(fill="x", pady=(45, 0), padx=20)

    # Configurar el grid en el frame para los CTkEntry y el botón
    buscar_movie_metrica_frame.grid_columnconfigure(0, weight=1)
    buscar_movie_metrica_frame.grid_columnconfigure(1, weight=1)
    buscar_movie_metrica_frame.grid_columnconfigure(2, weight=0)

    # Crear los CTkEntry
    buscar_movie_year_entry = CTkEntry(master=buscar_movie_metrica_frame, width=380, placeholder_text="Escriba el año de lanzamiento", border_color="#003360", border_width=2)
    buscar_movie_year_entry.grid(row=0, column=0, padx=(13, 5), pady=15, sticky="ew")
    #movie_buscar_year = buscar_movie_earnings_entry.get()

    buscar_movie_earnings_entry = CTkEntry(master=buscar_movie_metrica_frame, width=380, placeholder_text="Escriba las ganancias", border_color="#003360", border_width=2)
    buscar_movie_earnings_entry.grid(row=0, column=1, padx=(5, 5), pady=15, sticky="ew")
    #movie_buscar_earnings = buscar_movie_earnings_entry.get()

    buscar_metrica_icon_img_data = Image.open("buscar_btn.png") 
    buscar_metrica_icon_img = CTkImage(dark_image=buscar_metrica_icon_img_data, light_image=buscar_metrica_icon_img_data)

    # Frame contenedor para alinear el TextBox y el CTkFrame
    contenedor2_frame = CTkFrame(master=buscar_metrica_frame, fg_color="#fff")
    contenedor2_frame.pack(fill="x", pady=(20, 0), padx=20)

    # Configuración del TextBox
    buscar_metrica_text = CTkTextbox(master=contenedor2_frame, font=("Arial", 18), height=140, width=420, fg_color="#F0F0F0", corner_radius=20)
    parrafo_recorrido = ""
    buscar_metrica_text.insert("0.0", parrafo_recorrido)
    buscar_metrica_text.configure(state="disabled")
    buscar_metrica_text.pack(side="left", padx=(0, 20))

    # Configuración del TextBox2
    metricas2_text = CTkTextbox(master=buscar_metrica_frame, font=("Arial", 18), height=80, width=420, fg_color="#F0F0F0", corner_radius=20)
    parrafo2_recorrido = ""
    metricas2_text.insert("0.0", parrafo_recorrido)
    metricas2_text.configure(state="disabled")

    def on_buscar_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            buscar_metrica_text.configure(state="normal")
            buscar_metrica_text.delete("0.0", "end")
            buscar_metrica_text.insert("0.0", "Por favor ingrese valores válidos.")
            buscar_metrica_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Habilitar el textbox para actualizar su contenido
        buscar_metrica_text.configure(state="normal")
        buscar_metrica_text.delete("0.0", "end")  # Limpiar el contenido actual

        parrafo_recorrido = ""

        if Lista_movies:
            c = 1
            for movie in Lista_movies:
                parrafo_recorrido += (
                    f"{c}. Title: {movie.data.title}, Year: {movie.data.year}, "
                    f"Worldwide Earnings: {movie.data.worldwide_earnings}, "
                    f"Domestic Earnings: {movie.data.domestic_earnings} "
                    f"({movie.data.domestic_percent_earnings}%), Foreign Earnings: "
                    f"{movie.data.foreign_earnings} ({movie.data.foreign_percent_earnings}%)\n"
                )
                c += 1  # Incrementar contador
        else:
            parrafo_recorrido = "Película no encontrada con los parametros."

        buscar_metrica_text.insert("0.0", parrafo_recorrido)
        buscar_metrica_text.configure(state="disabled")  # Deshabilitar el textbox

    def on_nivelNodo_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        # Convertir los valores de entrada en los tipos adecuados
        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese valores válidos para el año y las ganancias.")
            metricas2_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Verificar si la lista está vacía
        if not Lista_movies:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "No se encontraron películas que coincidan con los criterios de búsqueda.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el número del nodo seleccionado
        try:
            numero = int(elegir_nodo_entry.get())
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese un número de nodo válido.")
            metricas2_text.configure(state="disabled")
            return

        # Verificar si el número ingresado está dentro del rango de la lista
        if numero < 1 or numero > len(Lista_movies):
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "El número de nodo ingresado está fuera de rango.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el objeto de película correspondiente
        objeto_movies = Lista_movies[numero-1]
        nivel_enc = avl_tree.level_node(avl_tree.root, objeto_movies.data.title, 0)

        # Actualizar el texto del nivel encontrado
        metricas2_text.configure(state="normal")
        metricas2_text.delete("0.0", "end")

        if nivel_enc > -1:
            parrafo1_recorrido = f"Nivel: {nivel_enc}\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas2_text.insert("0.0", parrafo1_recorrido)
        metricas2_text.configure(state="disabled")

    def on_factorBalanceo_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        # Convertir los valores de entrada en los tipos adecuados
        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese valores válidos para el año y las ganancias.")
            metricas2_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Verificar si la lista está vacía
        if not Lista_movies:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "No se encontraron películas que coincidan con los criterios de búsqueda.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el número del nodo seleccionado
        try:
            numero = int(elegir_nodo_entry.get())
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese un número de nodo válido.")
            metricas2_text.configure(state="disabled")
            return

        # Verificar si el número ingresado está dentro del rango de la lista
        if numero < 1 or numero > len(Lista_movies):
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "El número de nodo ingresado está fuera de rango.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el objeto de película correspondiente
        objeto_movies = Lista_movies[numero-1]

        # Actualizar el texto del factor de balanceo
        metricas2_text.configure(state="normal")
        metricas2_text.delete("0.0", "end")

        if objeto_movies is not None:
            factor_enc = avl_tree.balance_factor(objeto_movies)
            parrafo1_recorrido = f"Factor de balanceo: {factor_enc}\n"
        else:
            parrafo1_recorrido = "Película no encontrada."

        metricas2_text.insert("0.0", parrafo1_recorrido)
        metricas2_text.configure(state="disabled")

    def on_parent_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        # Convertir los valores de entrada en los tipos adecuados
        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese valores válidos para el año y las ganancias.")
            metricas2_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Verificar si la lista está vacía
        if not Lista_movies:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "No se encontraron películas que coincidan con los criterios de búsqueda.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el número del nodo seleccionado
        try:
            numero = int(elegir_nodo_entry.get())
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese un número de nodo válido.")
            metricas2_text.configure(state="disabled")
            return

        # Verificar si el número ingresado está dentro del rango de la lista
        if numero < 1 or numero > len(Lista_movies):
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "El número de nodo ingresado está fuera de rango.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el objeto de película correspondiente
        objeto_movies = Lista_movies[numero-1]

        # Actualizar el texto del nodo padre
        metricas2_text.configure(state="normal")
        metricas2_text.delete("0.0", "end")

        if objeto_movies is not None:
            padre_enc = avl_tree.search_parent(objeto_movies.data.title)
            if padre_enc is not None:
                parrafo_recorrido = f"Nodo padre: {padre_enc.data.title} ({padre_enc.data.year})\n"
            else:
                parrafo_recorrido = "Nodo padre no encontrado."
        else:
            parrafo_recorrido = "Película no encontrada."

        metricas2_text.insert("0.0", parrafo_recorrido)
        metricas2_text.configure(state="disabled")

    
    def on_grandParent_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        # Convertir los valores de entrada en los tipos adecuados
        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese valores válidos para el año y las ganancias.")
            metricas2_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Verificar si la lista está vacía
        if not Lista_movies:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "No se encontraron películas que coincidan con los criterios de búsqueda.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el número del nodo seleccionado
        try:
            numero = int(elegir_nodo_entry.get())
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese un número de nodo válido.")
            metricas2_text.configure(state="disabled")
            return

        # Verificar si el número ingresado está dentro del rango de la lista
        if numero < 1 or numero > len(Lista_movies):
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "El número de nodo ingresado está fuera de rango.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el objeto de película correspondiente
        objeto_movies = Lista_movies[numero-1]

        # Actualizar el texto del nodo abuelo
        metricas2_text.configure(state="normal")
        metricas2_text.delete("0.0", "end")

        if objeto_movies is not None:
            abuelo_enc = avl_tree.search_grandparent(objeto_movies.data.title)
            if abuelo_enc is not None:
                parrafo_recorrido = f"Nodo abuelo: {abuelo_enc.data.title} ({abuelo_enc.data.year})\n"
            else:
                parrafo_recorrido = "Nodo abuelo no encontrado."
        else:
            parrafo_recorrido = "Película no encontrada."

        metricas2_text.insert("0.0", parrafo_recorrido)
        metricas2_text.configure(state="disabled")


    def on_uncle_click_metrica():
        year_buscar = buscar_movie_year_entry.get()
        earnings_buscar = buscar_movie_earnings_entry.get()

        # Convertir los valores de entrada en los tipos adecuados
        try:
            year_buscar = int(year_buscar)
            earnings_buscar = float(earnings_buscar)
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese valores válidos para el año y las ganancias.")
            metricas2_text.configure(state="disabled")
            return

        Lista_movies = avl_tree.search_condiciones_string(year_buscar, earnings_buscar)

        # Verificar si la lista está vacía
        if not Lista_movies:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "No se encontraron películas que coincidan con los criterios de búsqueda.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el número del nodo seleccionado
        try:
            numero = int(elegir_nodo_entry.get())
        except ValueError:
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "Por favor ingrese un número de nodo válido.")
            metricas2_text.configure(state="disabled")
            return

        # Verificar si el número ingresado está dentro del rango de la lista
        if numero < 1 or numero > len(Lista_movies):
            metricas2_text.configure(state="normal")
            metricas2_text.delete("0.0", "end")
            metricas2_text.insert("0.0", "El número de nodo ingresado está fuera de rango.")
            metricas2_text.configure(state="disabled")
            return

        # Obtener el objeto de película correspondiente
        objeto_movies = Lista_movies[numero-1]

        # Actualizar el texto del nodo tío (hermano del padre)
        metricas2_text.configure(state="normal")
        metricas2_text.delete("0.0", "end")

        if objeto_movies is not None:
            padre_enc = avl_tree.search_parent(objeto_movies.data.title)
            if padre_enc is not None:
                tio_enc = avl_tree.search_uncle(objeto_movies.data.title)  # Asumiendo que hay un método search_uncle
                if tio_enc is not None:
                    parrafo_recorrido = f"Nodo tío: {tio_enc.data.title} ({tio_enc.data.year})\n"
                else:
                    parrafo_recorrido = "Nodo tío no encontrado."
            else:
                parrafo_recorrido = "Nodo padre no encontrado."
        else:
            parrafo_recorrido = "Película no encontrada."

        metricas2_text.insert("0.0", parrafo_recorrido)
        metricas2_text.configure(state="disabled")

    # Crear el botón
    buscar_movie_metrica_btn = CTkButton(master=buscar_movie_metrica_frame, text="BUSCAR", image= buscar_metrica_icon_img, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, height=50, width=180, text_color="#FFFFFF", border_width=2, border_color="#006BBF", command=on_buscar_click_metrica)
    buscar_movie_metrica_btn.grid(row=0, column=2, padx=(15, 10), pady=15)

    #buscar_metrica_text.pack(side="left", padx=(0, 20))

    elegir_nodo_frame = CTkFrame(master=contenedor2_frame, fg_color="#F0F0F0", width=250)
    elegir_nodo_frame.pack(side="left", fill="y")  # Usar 'fill="y"' para llenar el espacio vertical

    # Crear los widgets en el nuevo frame
    CTkLabel(master=elegir_nodo_frame, text="Elegir un nodo", font=("Arial Black", 14), text_color="#003360").pack(pady=(10, 5), side="top")
    elegir_nodo_entry = CTkEntry(master=elegir_nodo_frame, width=220, placeholder_text="Ingrese el nodo movie", border_color="#003360", border_width=2)
    elegir_nodo_entry.pack(pady=(4, 8), padx=10, anchor="center")
    #elegir_nodo2 = int(elegir_nodo_entry.get())

    # Crear frame para los botones debajo de "buscar_movie_frame"
    botones_metrica_frame = CTkFrame(master=buscar_metrica_frame, fg_color="#F0F0F0", height=220)
    botones_metrica_frame.pack(fill="x", padx=20, pady=20)

    # Cargar íconos para los botones
    nivel_nodo_icon_data = Image.open("nivel_nodo_icon.png")
    nivel_nodo_icon = CTkImage(dark_image=nivel_nodo_icon_data, light_image=nivel_nodo_icon_data, size=(20, 20))

    factor_balanceo_icon_data = Image.open("factor_balanceo_icon.png")
    factor_balanceo_icon = CTkImage(dark_image=factor_balanceo_icon_data, light_image=factor_balanceo_icon_data, size=(20, 20))

    nodo_padre_icon_data = Image.open("nodo_padre_icon.png")
    nodo_padre_icon = CTkImage(dark_image=nodo_padre_icon_data, light_image=nodo_padre_icon_data, size=(20, 20))

    nodo_abuelo_icon_data = Image.open("nodo_abuelo_icon.png")
    nodo_abuelo_icon = CTkImage(dark_image=nodo_abuelo_icon_data, light_image=nodo_abuelo_icon_data, size=(20, 20))

    nodo_tio_icon_data = Image.open("nodo_tio_icon.png")
    nodo_tio_icon = CTkImage(dark_image=nodo_tio_icon_data, light_image=nodo_tio_icon_data, size=(20, 20))

    # Configurar el grid en el frame de botones para centrar los botones
    botones_metrica_frame.grid_columnconfigure(0, weight=1)
    botones_metrica_frame.grid_columnconfigure(1, weight=1)
    botones_metrica_frame.grid_columnconfigure(2, weight=1)
    botones_metrica_frame.grid_rowconfigure(0, weight=1)
    botones_metrica_frame.grid_rowconfigure(1, weight=1)

    # Crear los botones
    nivel_nodo_metrica_btn = CTkButton(master=botones_metrica_frame, text="Nivel nodo", image=nivel_nodo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_nivelNodo_click_metrica)
    nivel_nodo_metrica_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    factor_balanceo_metrica_btn = CTkButton(master=botones_metrica_frame, text="Factor balanceo", image=factor_balanceo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_factorBalanceo_click_metrica)
    factor_balanceo_metrica_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    nodo_padre_metrica_btn = CTkButton(master=botones_metrica_frame, text="Nodo padre", image=nodo_padre_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_parent_click_metrica)
    nodo_padre_metrica_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    nodo_abuelo_metrica_btn = CTkButton(master=botones_metrica_frame, text="Nodo abuelo", image=nodo_abuelo_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_grandParent_click_metrica)
    nodo_abuelo_metrica_btn.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    nodo_tio_metrica_btn = CTkButton(master=botones_metrica_frame, text="Nodo tío", image=nodo_tio_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14), corner_radius=10, text_color="#FFFFFF", height=50, width=160, border_width=2, border_color="#006BBF", command=on_uncle_click_metrica)
    nodo_tio_metrica_btn.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    metricas2_text.pack(pady=(5, 0), padx=80)

    buscar_metrica_frame.pack(side="left", fill = "both", expand = True)
    buscar_metrica_frame.pack_propagate(0)

def recorrido_view():
    recorrido_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=recorrido_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x", padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="Recorrido por Niveles", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")
    
    recorrido_icon_data = Image.open("recorrido_icon.png")
    recorrido_icon = CTkImage(dark_image=recorrido_icon_data, light_image=recorrido_icon_data, size=(20, 20))

    def on_recorrido_click():
        parrafo_recorrido = avl_tree.recorrido_por_niveles()
        recorrido_text.configure(state="normal")
        recorrido_text.delete("0.0", "end") # Limpiar el contenido actual y actualizar con el nuevo texto
        recorrido_text.insert("0.0", parrafo_recorrido)
        recorrido_text.configure(state="disabled") # Deshabilitar el textbox

    recorrido_btn = CTkButton(master=recorrido_frame, text="RECORRIDO", image=recorrido_icon, fg_color="#008CFF", hover_color="#00A3FF", font=("Arial Black", 14),
                              corner_radius=10, height=80, width=180, text_color="#FFFFFF", border_width=2, border_color="#006BBF", command=on_recorrido_click)
    recorrido_btn.pack(pady=130) 

    recorrido_text = CTkTextbox(master=recorrido_frame, font=("Arial", 18), height=180, width=600, fg_color="#adb5bd", corner_radius=20)
    # Inicialmente vaciar el contenido
    recorrido_text.pack(pady=0)

    recorrido_frame.pack(side="left", fill="both", expand=True)
    recorrido_frame.pack_propagate(0)

def perfil_view(): #Panel extra, sin correcciones
    start_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
    title_frame = CTkFrame(master=start_frame, fg_color="transparent")
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

    CTkLabel(master=title_frame, text="DataSet Movie's Tree", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")

    descripcion_frame = CTkFrame(master=start_frame, height=650, width=50, fg_color="transparent", corner_radius=20)
    descripcion_frame.pack(fill="x", pady=(70, 0), padx=60)

    descripcion_text = CTkTextbox(master=descripcion_frame, font=("Arial", 18), height=165, width=60, fg_color="#adb5bd", corner_radius=20)
    parrafo = """¡Bienvenido al Sistema de Gestión de Películas! Aquí podrás administrar tu colección de películas de manera fácil y rápida. Ya sea que desees agregar nuevas películas, buscar tus favoritas, actualizar información o eliminar títulos, este programa te brinda todas las herramientas necesarias para mantener organizada tu biblioteca de películas. ¡Comencemos!"""
    descripcion_text.insert("0.0", parrafo)
    descripcion_text.configure(state="disabled")
    descripcion_text.pack(fill="both", expand=True)

    autores_frame = CTkFrame(master=start_frame, fg_color="transparent")
    autores_frame.pack(anchor="n", fill="x",  padx=27, pady=(110, 0))

    autora_metrica = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
    autora_metrica.grid_propagate(0)
    autora_metrica.pack(side="left")

    mujer_img_data = Image.open("mujer.png")
    mujer_img = CTkImage(light_image=mujer_img_data, dark_image=mujer_img_data, size=(43, 43))

    CTkLabel(master=autora_metrica, image=mujer_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

    CTkLabel(master=autora_metrica, text="Kesly Rodríguez", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
    CTkLabel(master=autora_metrica, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


    autor1_metric = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
    autor1_metric.grid_propagate(0)
    autor1_metric.pack(side="left",expand=True, anchor="center")

    hombre2_img_data = Image.open("hombre2.png")
    hombre2_img = CTkImage(light_image=hombre2_img_data, dark_image=hombre2_img_data, size=(43, 43))
    CTkLabel(master=autor1_metric, image=hombre2_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

    CTkLabel(master=autor1_metric, text="Santiago V.", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
    CTkLabel(master=autor1_metric, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

    autor2_metric = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
    autor2_metric.grid_propagate(0)
    autor2_metric.pack(side="right",)

    hombre1_img_data = Image.open("hombre1.png")
    hombre1_img = CTkImage(light_image=hombre1_img_data, dark_image=hombre1_img_data, size=(43, 43))

    CTkLabel(master=autor2_metric, image=hombre1_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

    CTkLabel(master=autor2_metric, text="Joshua Lobo", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
    CTkLabel(master=autor2_metric, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

    start_frame.pack(side="left", fill = "both", expand = True)
    start_frame.pack_propagate(0)

sidebar_frame = CTkFrame(master=app, fg_color="#000f26",  width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

logo_img_data = Image.open("logo_movie.png")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(120, 120))    

CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

# Función para cambiar el color del botón al hacer clic
current_button = None
def on_button_click(button):
    global current_button
    if current_button:
        current_button.configure(fg_color="transparent")  # Color inicial del botón
    button.configure(fg_color="#003360")  # Color del hover_color
    current_button = button

def delete_pages():
    for frame in app.winfo_children():
        if frame != sidebar_frame:
            frame.destroy()

def combined_function1():
    delete_pages()
    insertar_view()
    on_button_click(insertar_btn)
    
def combined_function2():
    delete_pages()
    eliminar_view()
    on_button_click(eliminar_btn)

def combined_function3():
    delete_pages()
    buscar_view()
    on_button_click(buscar_btn)

def combined_function4():
    delete_pages()
    buscar_metrica_view()
    on_button_click(buscar_metrica_btn)
    
def combined_function5():
    delete_pages()
    recorrido_view()
    on_button_click(recorrido_btn)

def combined_function6():
    delete_pages()
    perfil_view()
    on_button_click(perfil_btn)

insertar_img_data = Image.open("insertar.png")
insertar_img = CTkImage(dark_image=insertar_img_data, light_image=insertar_img_data)

insertar_btn = CTkButton(master=sidebar_frame, image=insertar_img, text="Insertar película", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command= combined_function1)
insertar_btn.pack(anchor="center", ipady=5, pady=(60, 0))


eliminar_img_data = Image.open("eliminar.png")
eliminar_img = CTkImage(dark_image=eliminar_img_data, light_image=eliminar_img_data)

eliminar_btn = CTkButton(master=sidebar_frame, image=eliminar_img, text="Eliminar película", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command= combined_function2)
eliminar_btn.pack(anchor="center", ipady=5, pady=(16, 0))


buscar_img_data = Image.open("buscar.png")
buscar_img = CTkImage(dark_image=buscar_img_data, light_image=buscar_img_data)

buscar_btn = CTkButton(master=sidebar_frame, image=buscar_img, text="Buscar película", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command= combined_function3)
buscar_btn.pack(anchor="center", ipady=5, pady=(16, 0))


buscar_metrica_img_data = Image.open("buscar_metrica.png")
buscar_metrica_img = CTkImage(dark_image=buscar_metrica_img_data, light_image=buscar_metrica_img_data)

buscar_metrica_btn = CTkButton(master=sidebar_frame, image=buscar_metrica_img, text="Métrica especif.", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command= combined_function4)
buscar_metrica_btn.pack(anchor="center", ipady=5, pady=(16, 0))


recorrido_img_data = Image.open("arbol_binario.png")
recorrido_img = CTkImage(dark_image=recorrido_img_data, light_image=recorrido_img_data)
recorrido_btn = CTkButton(master=sidebar_frame, image=recorrido_img, text="Recorrido niveles", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command= combined_function5)
recorrido_btn.pack(anchor="center", ipady=5, pady=(16, 0))


person_img_data = Image.open("person_icon.png")
person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
perfil_btn = CTkButton(master=sidebar_frame, image=person_img, text="Perfil", fg_color="transparent", font=("Arial Bold", 14), hover_color="#003360", anchor="w", command=combined_function6)
perfil_btn.pack(anchor="center", ipady=5, pady=(120, 0))

start_frame = CTkFrame(master=app, fg_color="#fff",  width=680, height=645, corner_radius=0)
title_frame = CTkFrame(master=start_frame, fg_color="transparent")
title_frame.pack(anchor="n", fill="x",  padx=27, pady=(35, 0))

CTkLabel(master=title_frame, text="DataSet Movie's Tree", font=("Arial Black", 30), text_color="#003360").pack(anchor="nw", side="left")

descripcion_frame = CTkFrame(master=start_frame, height=650, width=50, fg_color="transparent", corner_radius=20)
descripcion_frame.pack(fill="x", pady=(70, 0), padx=60)

descripcion_text = CTkTextbox(master=descripcion_frame, font=("Arial", 18), height=165, width=60, fg_color="#adb5bd", corner_radius=20)
parrafo = """¡Bienvenido al Sistema de Gestión de Películas! Aquí podrás administrar tu colección de películas de manera fácil y rápida. Ya sea que desees agregar nuevas películas, buscar tus favoritas, actualizar información o eliminar títulos, este programa te brinda todas las herramientas necesarias para mantener organizada tu biblioteca de películas. ¡Comencemos!"""
descripcion_text.insert("0.0", parrafo)
descripcion_text.configure(state="disabled")
descripcion_text.pack(fill="both", expand=True)

autores_frame = CTkFrame(master=start_frame, fg_color="transparent")
autores_frame.pack(anchor="n", fill="x",  padx=27, pady=(110, 0))

autora_metrica = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
autora_metrica.grid_propagate(0)
autora_metrica.pack(side="left")

mujer_img_data = Image.open("mujer.png")
mujer_img = CTkImage(light_image=mujer_img_data, dark_image=mujer_img_data, size=(43, 43))

CTkLabel(master=autora_metrica, image=mujer_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=autora_metrica, text="Kesly Rodríguez", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=autora_metrica, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


autor1_metric = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
autor1_metric.grid_propagate(0)
autor1_metric.pack(side="left",expand=True, anchor="center")

hombre2_img_data = Image.open("hombre2.png")
hombre2_img = CTkImage(light_image=hombre2_img_data, dark_image=hombre2_img_data, size=(43, 43))
CTkLabel(master=autor1_metric, image=hombre2_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=autor1_metric, text="Santiago V.", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=autor1_metric, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

autor2_metric = CTkFrame(master=autores_frame, fg_color="#003360", width=200, height=60)
autor2_metric.grid_propagate(0)
autor2_metric.pack(side="right",)

hombre1_img_data = Image.open("hombre1.png")
hombre1_img = CTkImage(light_image=hombre1_img_data, dark_image=hombre1_img_data, size=(43, 43))

CTkLabel(master=autor2_metric, image=hombre1_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=autor2_metric, text="Joshua Lobo", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=autor2_metric, text="Ing. Sistemas", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

start_frame.pack(side="left", fill = "both", expand = True)
start_frame.pack_propagate(0)

avl_tree.visualize()
app.mainloop()