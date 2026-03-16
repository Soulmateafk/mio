from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# Enums para esquemas
class TipoDocumentoEnum(str, Enum):
    DNI = "DNI"
    PASAPORTE = "PASAPORTE"
    CEDULA = "CEDULA"

class TipoUsuarioEnum(str, Enum):
    ESTUDIANTE = "ESTUDIANTE"
    DOCENTE = "DOCENTE"
    ADMINISTRATIVO = "ADMINISTRATIVO"
    EXTERNO = "EXTERNO"

class EstadoPrestamoEnum(str, Enum):
    ACTIVO = "ACTIVO"
    DEVUELTO = "DEVUELTO"
    VENCIDO = "VENCIDO"
    PERDIDO = "PERDIDO"

class EstadoReservaEnum(str, Enum):
    ACTIVA = "ACTIVA"
    COMPLETADA = "COMPLETADA"
    EXPIRADA = "EXPIRADA"
    CANCELADA = "CANCELADA"

class EstadoMultaEnum(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    ANULADA = "ANULADA"

# Autor Schemas
class AutorBase(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    biografia: Optional[str] = None

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    autor_id: int
    class Config:
        from_attributes = True

# Editorial Schemas
class EditorialBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    sitio_web: Optional[str] = None

class EditorialCreate(EditorialBase):
    pass

class Editorial(EditorialBase):
    editorial_id: int
    class Config:
        from_attributes = True

# Categoria Schemas
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria_padre_id: Optional[int] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    categoria_id: int
    class Config:
        from_attributes = True

# Libro Schemas
class LibroBase(BaseModel):
    isbn: Optional[str] = None
    titulo: str
    subtitulo: Optional[str] = None
    editorial_id: int
    anio_publicacion: Optional[int] = None
    numero_paginas: Optional[int] = None
    idioma: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion_estante: Optional[str] = None
    ejemplares_totales: Optional[int] = 1
    ejemplares_disponibles: Optional[int] = 1

class LibroCreate(LibroBase):
    autor_ids: Optional[List[int]] = []
    categoria_ids: Optional[List[int]] = []

class Libro(LibroBase):
    libro_id: int
    class Config:
        from_attributes = True

class LibroDetalle(Libro):
    editorial: Optional[Editorial] = None
    autores: List[Autor] = []
    categorias: List[Categoria] = []

# Usuario Schemas
class UsuarioBase(BaseModel):
    tipo_documento: TipoDocumentoEnum = TipoDocumentoEnum.DNI
    numero_documento: str
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    tipo_usuario: TipoUsuarioEnum = TipoUsuarioEnum.ESTUDIANTE

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    usuario_id: int
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    class Config:
        from_attributes = True

# Prestamo Schemas
class PrestamoBase(BaseModel):
    usuario_id: int
    libro_id: int
    fecha_devolucion_estimada: date
    observaciones: Optional[str] = None

class PrestamoCreate(PrestamoBase):
    pass

class Prestamo(PrestamoBase):
    prestamo_id: int
    fecha_prestamo: Optional[datetime] = None
    fecha_devolucion_real: Optional[date] = None
    estado: EstadoPrestamoEnum = EstadoPrestamoEnum.ACTIVO
    class Config:
        from_attributes = True

# Multa Schemas
class MultaBase(BaseModel):
    prestamo_id: int
    usuario_id: int
    monto: float
    concepto: Optional[str] = None

class MultaCreate(MultaBase):
    pass

class Multa(MultaBase):
    multa_id: int
    fecha_multa: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None
    estado: EstadoMultaEnum = EstadoMultaEnum.PENDIENTE
    class Config:
        from_attributes = True

# Reserva Schemas
class ReservaBase(BaseModel):
    usuario_id: int
    libro_id: int
    fecha_expiracion: date

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    reserva_id: int
    fecha_reserva: Optional[datetime] = None
    estado: EstadoReservaEnum = EstadoReservaEnum.ACTIVA
    class Config:
        from_attributes = True