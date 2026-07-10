from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


"Sin modelo"
tabla_favoritos= db.Table(
    "tabla_favoritos",

    db.Column("user_id", ForeignKey('user.id'), primary_key=True),
    db.Column("publicacion_id", ForeignKey('publicacion.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorite_posts: Mapped[list["Publicacion"]] = relationship(
        secondary=tabla_favoritos,
        back_populates="favorite_users"
    )

    publicaciones: Mapped[list["Publicacion"]] = relationship(back_populates="user")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="user")

class Publicacion(db.Model):
    __tablename__ = 'publicacion'
    id: Mapped[int] = mapped_column(primary_key=True)
    media: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    descripcion: Mapped[str] = mapped_column( nullable=False)

    favorite_users: Mapped[list["User"]] = relationship(
        secondary=tabla_favoritos,
        back_populates="favorite_posts"
    )

    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="publicacion")

    user: Mapped["User"] = relationship(back_populates="publicaciones")
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="comentarios")
    publicacion: Mapped["Publicacion"] = relationship(back_populates="comentarios")

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('publicacion.id'), nullable=False)


