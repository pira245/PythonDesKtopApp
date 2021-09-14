# Librerias para la creación de la interface gráfica
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import *

# Librerias para la creación y gestión de la base de datos
import models
import db
from models import Producto, Categoria
import sqlite3


class Metodos(tk.Tk):
    """
        Clase que gestiona todas las operaciones relacionadas con la gestión de productos.
    """

    def __init__(self):
        super().__init__()
        self.categories = self.lista_categoria()
        self.canvas = tk.Canvas(self, width=700, height=600, bg="#15bebe")
        self.canvas.grid(columnspan=4, rowspan=5)

    # crear la ventana principal de la interface:
    def ventana_principal(self):
        """
            Este metodo crea la ventana principal de la aplicación.
        :return: ventana principal
        """
        # Creación de la ventana principal
        self.title("App Gestor de productos")  # Titulo de la ventana principal
        self.resizable(0, 0)  # Activar la redimensión de la ventana. Para activarla: (1,1)
        self.wm_iconbitmap('recursos/icon.ico')

    def area_crear_producto(self):
        """
            Este metodo crea un contenedor para la creacción de un nuevo producto
        :return: contenedor de registro
        """

        # Contenedor principal en el area de creación y registro de productos
        contenedor_registro = ttk.LabelFrame(self, text='Registrar un nuevo producto', relief='groove')
        contenedor_registro.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # # Etiqueta para el registro del nombre del producto
        self.etiqueta_nombre = ttk.Label(contenedor_registro, text='Nombre:*', font=('Calibri', 10, 'bold'))
        self.etiqueta_nombre.grid(column=2, row=1)  # Definir su posición usando grid
        # # Caja de registro del nombre
        self.nombre = ttk.Entry(contenedor_registro)
        self.nombre.focus()  # Para que el foco del raton vaya al registro de nombre al inicio
        self.nombre.grid(column=3, row=1)
        #
        # # Etiqueta para el registro del precio del producto
        self.etiqueta_precio = ttk.Label(contenedor_registro, text='Precio:*', font=('Calibri', 10, 'bold'))
        self.etiqueta_precio.grid(column=2, row=2)  # Definir su posición usando grid
        # # Caja de registro del precio
        self.precio = ttk.Entry(contenedor_registro)
        self.precio.grid(column=3, row=2)
        #
        # # Etiqueta para la selección de la categoria del producto
        self.etiqueta_categoria = ttk.Label(contenedor_registro, text='Categoria:*', font=('Calibri', 10, 'bold'))
        self.etiqueta_categoria.grid(column=2, row=3)  # Definir su posición usando grid
        #
        # # Caja de selcción de la categoria
        # self.lista_categoria = self.lista_categoria()  # Esta lista viene definida por el registro de nueva categoria
        self.combo_registrar = ttk.Combobox(contenedor_registro, values=self.categories)
        self.combo_registrar.grid(column=3, row=3)
        # self.combo_registrar.bind('<<ComboboxSelected>>', self.categories)
        #
        # # Etiqueta para el registro del proveedor del producto
        self.etiqueta_proveedor = ttk.Label(contenedor_registro, text='Proveedor:*', font=('Calibri', 10, 'bold'))
        self.etiqueta_proveedor.grid(column=2, row=4)  # Definir su posición usando grid
        # # Caja de registro del precio
        self.proveedor = ttk.Entry(contenedor_registro)
        self.proveedor.grid(column=3, row=4)
        #
        # # Boton para completar el registro del producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 12, 'bold', 'groove'))
        self.bton_registro_producto = ttk.Button(contenedor_registro, text='Guardar Producto',
                                                 command=lambda: self.registrar_producto(), style='my.TButton')
        self.bton_registro_producto.grid(column=1, row=5, columnspan=2)
        #
        # Mensaje informativo para el usuario en el area de registro
        self.mensaje_registro = ttk.Label(contenedor_registro, text='', foreground='red')
        self.mensaje_registro.grid(column=2, row=6, columnspan=2)
        #
        # # Etiqueta para la creación de  una categoria de productos
        self.etiqueta_instrución_categoria = ttk.Label(contenedor_registro, text='Define una nueva categoria:',
                                                       font=('Calibri', 10, 'bold'))
        self.etiqueta_instrución_categoria.grid(column=4, row=4)  # Definir su posición usando grid
        #
        # # Boton para registrar una nueva categoria de producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 12, 'bold'))
        self.bton_registro_categoria = ttk.Button(contenedor_registro, text='Registrar Categoria',
                                                  command=lambda: self.nueva_categoria(), style='my.TButton')
        self.bton_registro_categoria.grid(column=4, row=5, columnspan=2)

        for boton in contenedor_registro.winfo_children():
            boton.grid_configure(padx=2, pady=2)

    def area_editar_producto(self):
        # Contenedor para visualización y edicción de productos
        contenedor_producto = ttk.LabelFrame(self, width=600, height=300, text='Visualizar - Editar Productos')
        contenedor_producto.grid(row=1, column=2, columnspan=1, padx=5, pady=5)
        # Tabla de productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure('mystyle.Treeview', highlightthickness=0, bd=0,
                        font=('Calibri', 12))  # Se modifica la fuente de la tabla
        style.configure('mystyle.Treeview.Heading',
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout('mystyle.Treeview', [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes
        #
        # # Estructura de la tabla
        self.tabla = ttk.Treeview(contenedor_producto, columns=(1, 2, 3, 4, 5), show='headings', height=15,
                                  style='mystyle.Treeview')
        self.tabla.grid(row=0, column=0, columnspan=5)
        self.tabla['columns'] = ('Id', 'Nombre', 'Precio', 'Proveedor', 'Categoria')
        self.tabla.column('Id', anchor=CENTER, stretch=YES, width=30)
        self.tabla.column('Nombre', anchor=CENTER, width=100)
        self.tabla.column('Precio', anchor=CENTER, width=100)
        self.tabla.column('Proveedor', anchor=CENTER, width=100)
        self.tabla.column('Categoria', anchor=CENTER, width=100)

        self.tabla.heading('Id', text='Id', anchor=CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=CENTER)
        self.tabla.heading('Precio', text='Precio', anchor=CENTER)
        self.tabla.heading('Proveedor', text='Proveedor', anchor=CENTER)
        self.tabla.heading('Categoria', text='Categoria', anchor=CENTER)

        # Mensaje informativo para el usuario en el area de visualización
        self.mensaje_visual = ttk.Label(contenedor_producto, text='', foreground='red')
        self.mensaje_visual.grid(column=1, row=4, columnspan=3)
        #
        # Estilos para los botones
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 12, 'bold'))
        # # Botones Buscar
        # Combo para busqueda rapida de productos por categoria
        self.combo_vizualizar = ttk.Combobox(values=self.categories)
        self.combo_vizualizar.grid(column=2, row=5)
        # self.combo.bind('<<ComboboxSelected>>', self.combo_get_categoria())
        self.boton_buscar = ttk.Button(text='Buscar - Categoria', command=lambda: self.buscar_producto(),
                                       style='my.TButton')
        self.boton_buscar.grid(row=4, column=2)
        # # Botones Eliminar
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=lambda: self.eliminar_producto(), style='my.TButton')
        self.boton_eliminar.grid(row=5, column=0)
        # # Botones Editar
        self.boton_editar = ttk.Button(text='EDITAR', command=lambda: self.editar_producto(), style='my.TButton')
        self.boton_editar.grid(row=5, column=3)

    def editar_producto(self):
        self.mensaje_visual['text'] = ''  # Mensaje inicialmente vacio
        try:
            # Buscar el producto en bd
            attr = self.tabla.item(self.tabla.selection())
            producto = db.session.query(models.Producto).filter_by(producto_id=int(attr['values'][0])).first()
            db.session.commit()

            # Ventana de edicción de producto:
            self.ventana_editar = Toplevel()# Crear una ventana por delante de la principal
            self.ventana_editar.title = 'Editar Producto'  # Titulo de la ventana
            self.ventana_editar.resizable(1, 1)  # Activar el redimiencionamiento de la ventana/ desactivar resizable(0, 0)
            self.ventana_editar.wm_iconbitmap('recursos/icon.ico')  # Icono de la ventana
            titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 20, 'bold'))
            titulo.grid(column=0, row=0)
            # Contenedor para los atributos del producto
            frame_antiguo = LabelFrame(self.ventana_editar, text='Datos antiguos', font=('Calibri', 15, 'bold'))
            frame_antiguo.grid(row=1, column=0, columnspan=2, rowspan=3, pady=20)
            # # Label Nombre antiguo
            etiqueta_nombre_antiguo = Label(frame_antiguo, text='Nombre antiguo: ', font=('Calibri', 13))
            etiqueta_nombre_antiguo.grid(row=1, column=0)
            # # Entry nombre antiguo
            input_nombre_antiguo = Entry(frame_antiguo, textvariable=StringVar(self.ventana_editar, value=producto.nombre),
                                         state='readonly', font=('Calibri', 13))
            input_nombre_antiguo.grid(row=1, column=1)
            # # Label Precio antiguo
            etiqueta_precio_antiguo = Label(frame_antiguo, text='Precio antiguo: ', font=('Calibri', 13))
            etiqueta_precio_antiguo.grid(row=2, column=0)
            # # Entry Precio antiguo
            input_precio_antiguo = Entry(frame_antiguo, textvariable=StringVar(self.ventana_editar, value=producto.precio),
                                         state='readonly', font=('Calibri', 13))
            input_precio_antiguo.grid(row=2, column=1)
            # # Label Proveedor antiguo
            etiqueta_proveedor_antiguo = Label(frame_antiguo, text='Proveedor antiguo: ', font=('Calibri', 13))
            etiqueta_proveedor_antiguo.grid(row=3, column=0)
            # # Entry Proveedor antiguo
            input_proveedor_antiguo = Entry(frame_antiguo,
                                            textvariable=StringVar(self.ventana_editar, value=producto.proveedor),
                                            state='readonly', font=('Calibri', 13))
            input_proveedor_antiguo.grid(row=3, column=1)

            # Mensaje informativo para el usuario en el area de edicción
            self.mensaje_editar = ttk.Label(self.ventana_editar, text='', foreground='red')
            self.mensaje_editar.grid(column=0, row=4, columnspan=2)

            # Contenedor para editar los atributos del producto:
            frame_editar = LabelFrame(self.ventana_editar, text='Editar datos', font=('Calibri', 15, 'bold'))
            frame_editar.grid(row=5, column=0, columnspan=2, rowspan=4, pady=20)
            # # Etiqueta nombre
            etiqueta_nombre = ttk.Label(frame_editar, text='Nombre: ', font=('Calibri', 10, 'bold'))
            etiqueta_nombre.grid(column=0, row=1)
            # # Caja de registro del nombre
            nombre = ttk.Entry(frame_editar)
            nombre.focus()  # Para que el foco del raton vaya al registro de nombre al inicio
            nombre.grid(column=1, row=1)
            # # Etiqueta Precio
            etiqueta_precio = ttk.Label(frame_editar, text='Precio: ', font=('Calibri', 10, 'bold'))
            etiqueta_precio.grid(column=0, row=2)
            # # Caja de registro del precio
            precio = ttk.Entry(frame_editar)
            precio.grid(column=1, row=2)
            # # Etiqueta Proveedor
            etiqueta_proveedor = ttk.Label(frame_editar, text='Proveedor: ', font=('Calibri', 10, 'bold'))
            etiqueta_proveedor.grid(column=0, row=3)
            # # Caja de registro del proveedor
            proveedor = ttk.Entry(frame_editar)
            proveedor.grid(column=1, row=3)

            # # Boton Actualizar Producto
            s = ttk.Style()
            s.configure('my.TButton', font=('Calibri', 14, 'bold'))
            boton_actualizar = ttk.Button(frame_editar, text='Actualizar Producto', style='my.TButton',
                                          command=lambda: self.actualizar_producto(nombre.get(), precio.get(),
                                                                                   proveedor.get(), attr))
            boton_actualizar.grid(row=4, columnspan=2)


        except IndexError as e:
            self.mensaje_visual['text'] = 'Por favor, seleccione un producto '
            return

    def nueva_categoria(self):
        """
            Este metodo crea una nueva categoria y se guarda en la base de datos:
        :return: Nueva categoria
        """
        # ventana nueva (crear categoria producto)
        self.ventana = tk.Toplevel()  # Crear una ventana por delante de la principal
        self.ventana.title = 'Crear Categoria'  # Titulo de la ventana
        self.ventana.resizable(1, 1)  # Activar el redimiencionamiento de la ventana/ desactivar resizable(0, 0)
        self.ventana.wm_iconbitmap('recursos/icon.ico')  # Icono de la ventana
        #
        # contenedor
        contenedor_categoria = ttk.LabelFrame(self.ventana, text='Registrar una nueva categoria', width=600, height=600)
        contenedor_categoria.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        #
        # # Etiqueta para el registro del nombre del producto
        self.etiqueta_categoria = ttk.Label(contenedor_categoria, text='Categoria:', font=('Calibri', 10, 'bold'))
        self.etiqueta_categoria.grid(column=1, row=1)  # Definir su posición usando grid
        #
        # # Caja de registro de la categoria
        self.categoria = ttk.Entry(contenedor_categoria)
        self.categoria.focus()  # Para que el foco del raton vaya al registro de nombre al inicio
        self.categoria.grid(column=2, row=1)
        #
        # Mensaje informativo para el usuario
        self.mensaje = tk.Label(contenedor_categoria, text='', fg='red')
        self.mensaje.grid(column=1, row=3, columnspan=2)
        #
        # Boton de entrega de datos
        # # Boton para completar el registro del producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 12, 'bold'))
        self.bton_registro_categoria = ttk.Button(contenedor_categoria, text='Guardar Categoria',
                                                  command=lambda: Metodos.registrar_categoria(self), style='my.TButton')
        self.bton_registro_categoria.grid(column=2, row=2, columnspan=2)
        # self.area_crear_producto() # Actualizar la lista de categories

    def registrar_categoria(self):
        """
            Parte final del registro de una nueva categoria
        :return: None
        """
        if self.categoria.get() == '':
            self.mensaje['text'] = 'Por favor, introduce una categoria'  # Mensaje para el usuario
        else:
            self.mensaje['text'] = 'OK'  # Mensaje para el usuario
            cat = models.Categoria(categoria=self.categoria.get())
            db.session.add(cat)
            db.session.commit()
            self.ventana.destroy()  # Cerrar la ventana

    def registrar_producto(self):
        """
            Este metodo se usa pra registra un nuevo producto en la base de datos.
        :return:
        """
        # Se guarda los datos introducidos por el usuario:

        self.categoria = self.combo_registrar.get()
        lista_atributos = [self.nombre.get(), self.precio.get(), self.categoria, self.proveedor.get()]
        lista_validacion = []

        for item in lista_atributos:
            if item != '':
                lista_validacion.append(True)
            else:
                lista_validacion.append(False)

        # Comprobamos que no haya datos vacios:

        if (lista_validacion[0] and lista_validacion[1]) and lista_validacion[2]:
            self.mensaje_registro['text'] = 'Se puede guardar los datos'
            # Buscamos a categoria del producto según la elección del usuario
            categoria = db.session.query(models.Categoria).filter_by(categoria=lista_atributos[2]).first()
            # Se crea una instancia de la clase producto.
            prod = models.Producto(nombre=lista_atributos[0], precio=lista_atributos[1], proveedor=lista_atributos[3],
                                   grupo=categoria)

            db.session.add(prod)
            db.session.commit()
            self.mensaje_registro['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0, tk.END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, tk.END)  # Borrar el campo precio del formulario
            self.proveedor.delete(0, tk.END)  # Borrar el campo proveedor del formulario
            self.get_productos()
        else:
            self.mensaje_registro['text'] = 'Todos los campos con * son obligatorios'

    def get_productos(self):
        """
            Este metodo se usa para poblar la tabla de productos:
        :return: None
        """

        # Borrar todos los elementos existentes en la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Poblar elementos en la tabla sin busqueda con categoria:
        productos = db.session.query(models.Producto).all()
        for producto in productos:
            self.tabla.insert('', 'end', values=(
                producto.producto_id, producto.nombre, producto.precio, producto.proveedor,
                producto.categoria(producto.categoria_id)))

    def eliminar_producto(self):
        """
            Este metodo eliminar un producto en la base de datos:
        :return: None
        """
        self.mensaje_visual['text'] = ''  # Mensaje inicialmente vacio
        # comprobamos que se ha seleccionado un producto para eliminarlo
        try:
            attr = self.tabla.item(self.tabla.selection())
            print(attr['values'])
            productos = db.session.query(models.Producto).filter_by(producto_id=int(attr['values'][0])).delete()
            db.session.commit()
            self.mensaje_visual['text'] = 'El producto {} se ha eliminado con éxito'.format(attr['values'][1])
            self.get_productos()
        except IndexError as e:
            self.mensaje_visual['text'] = 'Por favor, seleccione un producto en la tabla'

    def buscar_producto(self):
        """
         Este metodo busca todos los productos que tienen la misma categoria en la base de datos.
        :return: None
        """
        try:
            categoria = self.combo_vizualizar.get()
            # Poblar elementos en la tabla con busqueda con categoria:
            categoria = db.session.query(models.Categoria).filter_by(categoria=str(categoria)).first()
            productos = db.session.query(models.Producto).filter_by(categoria_id=categoria.categoria_id).all()
            db.session.commit()
            # Borrar todos los elementos existentes en la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            # Poblar la tabla con el resultado
            for producto in productos:
                self.tabla.insert('', 'end', values=(
                    producto.producto_id, producto.nombre, producto.precio, producto.proveedor, categoria.categoria))

        except:
            self.mensaje_visual['text'] = 'Por favor, seleccione una categoria'

    def lista_categoria(self):
        """
            Este metodo se usa para actualizar continuamente la lista de categorias
        :return:
        """
        update_categoria = []
        lista_cat = []
        results = db.session.query(models.Categoria.categoria).all()
        lon = len(results)
        i = 0
        while i < lon:
            item = results[i]
            if item not in lista_cat:
                lista_cat.append(item)
            i += 1

        for item in lista_cat:
            update_categoria.append(item[0])

        return update_categoria

    def actualizar_producto(self, nombre, precio, proveedor, attr):
        if (nombre == '' and precio == '') and proveedor == '':
            self.mensaje_editar['text'] = 'Por favor, completa los campos vacios'
        else:
            producto = db.session.query(models.Producto).filter_by(producto_id=int(attr['values'][0])).first()
            producto.nombre = nombre
            producto.precio = float(precio)
            producto.proveedor = proveedor
            db.session.commit()
            self.ventana_editar.destroy()
            self.get_productos()