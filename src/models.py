from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()


class Empresa(db.Model):
    __tablename__ = 'empresa'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    direccion: Mapped[str] = mapped_column(String(120), nullable=False)
    fundacion: Mapped[int] = mapped_column(nullable=False)

    administradores: Mapped[List["Administrador"]] = relationship(back_populates="empresa")
    programadores: Mapped[List["Programador"]] = relationship(back_populates="empresa")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "fundacion": self.fundacion
        }


class Administrador(db.Model):
    __tablename__ = 'administrador'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[str] = mapped_column(String(120), nullable=False)
    telefono: Mapped[int] = mapped_column(nullable=False)
    fecha_incorporación: Mapped[int] = mapped_column(nullable=False)
    función: Mapped[str] = mapped_column(String(120), nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates="administradores")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "funcion": self.función
        }


class Programador(db.Model):
    __tablename__ = 'programador'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[str] = mapped_column(String(120), nullable=False)
    telefono: Mapped[int] = mapped_column(nullable=False)
    fecha_incorporación: Mapped[int] = mapped_column(nullable=False)
    función: Mapped[str] = mapped_column(String(120), nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates="programadores")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "funcion": self.función
        }


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    biografia: Mapped[str] = mapped_column(String(500), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    notificaciones: Mapped[List["Notificacion"] ] = relationship(back_populates="user")
    seguidores: Mapped[List["Seguidor"]] = relationship(back_populates="user")
    publicaciones: Mapped[List["Publicacion"]] = relationship(back_populates="user")
    comentarios: Mapped[List["Comentario"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "email": self.email,
            "biografia": self.biografia
            # do not serialize the password and estado, its a security breach
        }


class Notificacion(db.Model):
    __tablename__ = 'notificacion'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    tipo: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    visto: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="notificaciones")

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "tipo": self.tipo,
            "visto": self.visto
        }


class Seguidor(db.Model):
    __tablename__ = 'seguidor'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_seguidor: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    usuario: Mapped[str] = mapped_column(String(120), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="seguidores")

    def serialize(self):
        return {
            "id": self.id,
            "id_seguidor": self.id_seguidor,
            "usuario": self.usuario,
            "activo": self.activo
        }


class Publicacion(db.Model):
    __tablename__ = 'publicacion'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="publicaciones")
    comentarios: Mapped[List["Comentario"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "index": self.index,
            "tipo": self.tipo
        }


class Comentario(db.Model):
    __tablename__ = 'comentario'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_publicacion: Mapped[int] = mapped_column(ForeignKey("publicacion.id"), nullable=False)
    contenido: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped["User"] = relationship(back_populates="comentarios")
    publicacion: Mapped["Publicacion"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "contenido": self.contenido,
            "fecha": self.fecha
        }

