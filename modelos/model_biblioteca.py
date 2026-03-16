from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey, Boolean, Table, Text, DECIMAL
from database import Base
import enum

# Tablas intermedias
libros_autores = Table(
    'libros_autores',
    Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.libro_id', ondelete='CASCADE'), primary_key=True),
    Column('autor_id', Integer, ForeignKey('autores.autor_id', ondelete='CASCADE'), primary_key=True)
)

libros_categorias = Table(
    'libros_categorias',
    Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.libro_id', ondelete='CASCADE'), primary_key=True),
    Column('categoria_id', Integer, ForeignKey('categorias.categoria_id', ondelete='CASCADE'), primary_key=True)
)

# Enums
class TipoDocumento(str, enum.Enum):
    DNI = "DNI"
    PASAPORTE = "PASAPORTE"
    CEDULA = "CEDULA"

class TipoUsuario(str, enum.Enum):
    ESTUDIANTE = "ESTUDIANTE"
    DOCENTE = "DOCENTE"
    ADMINISTRATIVO = "ADMINISTRATIVO"
    EXTERNO = "EXTERNO"

class EstadoPrestamo(str, enum.Enum):
    ACTIVO = "ACTIVO"
    DEVUELTO = "DEVUELTO"
    VENCIDO = "VENCIDO"
    PERDIDO = "PERDIDO"

class EstadoReserva(str, enum.Enum):
    ACTIVA = "ACTIVA"
    COMPLETADA = "COMPLETADA"
    EXPIRADA = "EXPIRADA"
    CANCELADA = "CANCELADA"

class EstadoMulta(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    ANULADA = "ANULADA"

# Modelo Autor
class Autor(Base):
    __tablename__ = "autores"
    autor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    nacionalidad = Column(String(50))
    fecha_nacimiento = Column(Date)
    biografia = Column(String(500))

# Modelo Editorial
class Editorial(Base):
    __tablename__ = "editoriales"
    editorial_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String(200))
    telefono = Column(String(20))
    email = Column(String(100))
    sitio_web = Column(String(100))

# Modelo Categoria
class Categoria(Base):
    __tablename__ = "categorias"
    categoria_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(200))
    categoria_padre_id = Column(Integer, ForeignKey("categorias.categoria_id"), nullable=True)

# Modelo Libro
class Libro(Base):
    __tablename__ = "libros"
    libro_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    isbn = Column(String(20), unique=True)
    titulo = Column(String(200), nullable=False)
    subtitulo = Column(String(200))
    editorial_id = Column(Integer, ForeignKey("editoriales.editorial_id"), nullable=False)
    anio_publicacion = Column(Integer)
    numero_paginas = Column(Integer)
    idioma = Column(String(30))
    descripcion = Column(String(500))
    ubicacion_estante = Column(String(20))
    ejemplares_totales = Column(Integer, default=1)
    ejemplares_disponibles = Column(Integer, default=1)

# Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    usuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_documento = Column(Enum(TipoDocumento), default="DNI")
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    fecha_registro = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    fecha_nacimiento = Column(Date)
    tipo_usuario = Column(Enum(TipoUsuario), default="ESTUDIANTE")
    activo = Column(Boolean, default=True)

# Modelo Prestamo
class Prestamo(Base):
    __tablename__ = "prestamos"
    prestamo_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.libro_id"), nullable=False)
    fecha_prestamo = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    fecha_devolucion_estimada = Column(Date, nullable=False)
    fecha_devolucion_real = Column(Date)
    estado = Column(Enum(EstadoPrestamo), default="ACTIVO")
    observaciones = Column(String(500))

# Modelo Multa
class Multa(Base):
    __tablename__ = "multas"
    multa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prestamo_id = Column(Integer, ForeignKey("prestamos.prestamo_id"), nullable=False, unique=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    monto = Column(DECIMAL(10,2), nullable=False)
    fecha_multa = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    fecha_pago = Column(DateTime)
    estado = Column(Enum(EstadoMulta), default="PENDIENTE")
    concepto = Column(String(255))

# Modelo Reserva
class Reserva(Base):
    __tablename__ = "reservas"
    reserva_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.libro_id"), nullable=False)
    fecha_reserva = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    fecha_expiracion = Column(Date, nullable=False)
    estado = Column(Enum(EstadoReserva), default="ACTIVA")