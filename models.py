import db

"""
 Creamos una clase llamada Productos 
 Esta clase va ser nuestro modelo de datos de los productos ( el cual nos servirá luego para la base de datos)
 Esta clase va a almacenar toda la información referente a un producto
"""

class Categoria(db.Base):
    __tablename__ = "categoria"
    categoria_id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(200), nullable=False)
    # 1 to many relationship: Relación uno para muchos entre categoria y productos.
    producto = db.relationship('Producto', backref='grupo')


class Producto(db.Base):
    __tablename__ = "producto"
    producto_id = db.Column(db.Integer, primary_key=True)
    # id, por eso es primary key.
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    proveedor = db.Column(db.String(200), nullable=False)
    # 1 to many relationship: Relación uno para muchos entre categoria y productos.
    categoria_id = db.Column(db.Integer(), db.ForeignKey('categoria.categoria_id'))

    def categoria(self, cat_id):
        """
        Devuelve el valor categoria de la clase Categoria
        :param cat_id: Producto.categoria_id
        :return: Categoria.categoria
        """
        cat = db.session.query(Categoria).filter_by(categoria_id=int(cat_id)).first()
        return cat.categoria





