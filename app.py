# Librerias para la creación de la base de datos
import db

# Librerias personal para la gestión de los metodos de la aplicación
from metodos import Metodos

class Producto(Metodos):
    """
        Interface gráfica para una aplicación de gestión de productos una base de datos SQL.
        Cada producto tiene associado:
        Categoria: grupos para facilitar la gestión de los productos
        Nombre: String que refleja el producto
        Precio: float del precio de mercado
        Proveedor: La empresa o entidad que subministra el producto
    """

    def __init__(self):
        super().__init__()
        self.ventana = Metodos.ventana_principal(self)
        self.area_registro = Metodos.area_crear_producto(self)
        self.area_producto = Metodos.area_editar_producto(self)
        self.productos = Metodos.get_productos(self)

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app = Producto()
    app.ventana
    app.area_registro
    app.area_producto
    app.productos
    app.mainloop()  # Mantener la ventana principal abierta en un bucle:
