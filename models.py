import db
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, desc, asc

class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True) #Automaticamente esta Primary Key se convertirá en identificador unico en el gestor.
    contenido = Column(String(200),nullable=False) #nullable al poner falso fuerza que el campo debe rellenarse obligatoriamente.
    categoria = Column(String(200))
    fecha_limite = Column(Integer)
    hecha = Column(Boolean)

    def __init__(self, contenido, categoria, fecha_limite, hecha):
        self.contenido = contenido
        self.categoria = categoria
        self.fecha_limite = fecha_limite
        self.hecha = hecha

    def __repr__(self):
        return "Tarea {}: {} {} {} ({})".format(self.id, self.contenido, self.categoria, self.fecha_limite, self.hecha)

    def __str__(self):
        return "Tarea({}: {}, {} {} {})".format(self.id, self.contenido, self.categoria, self.fecha_limite, self.hecha)


