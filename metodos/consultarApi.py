
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date

from database import get_db
from modelos import model_biblioteca as models
from esquemas import eschemas as schemas

router = APIRouter()

# ==================== AUTORES ====================
@router.get("/autores_all", response_model=List[schemas.Autor])
def get_autores(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()

@router.get("/autores/{autor_id}", response_model=schemas.Autor)
def get_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.autor_id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.post("/autores", response_model=schemas.Autor, status_code=status.HTTP_201_CREATED)
def create_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    db_autor = models.Autor(**autor.model_dump())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

@router.put("/autores/{autor_id}", response_model=schemas.Autor)
def update_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    db_autor = db.query(models.Autor).filter(models.Autor.autor_id == autor_id).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    for key, value in autor.model_dump().items():
        setattr(db_autor, key, value)
    
    db.commit()
    db.refresh(db_autor)
    return db_autor

@router.delete("/autores/{autor_id}")
def delete_autor(autor_id: int, db: Session = Depends(get_db)):
    db_autor = db.query(models.Autor).filter(models.Autor.autor_id == autor_id).first()
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    db.delete(db_autor)
    db.commit()
    return {"detail": "Autor eliminado"}

# ==================== EDITORIALES ====================
@router.get("/editoriales", response_model=List[schemas.Editorial])
def get_editoriales(db: Session = Depends(get_db)):
    return db.query(models.Editorial).all()

@router.get("/editoriales/{editorial_id}", response_model=schemas.Editorial)
def get_editorial(editorial_id: int, db: Session = Depends(get_db)):
    editorial = db.query(models.Editorial).filter(models.Editorial.editorial_id == editorial_id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editorial

@router.post("/editoriales", response_model=schemas.Editorial, status_code=status.HTTP_201_CREATED)
def create_editorial(editorial: schemas.EditorialCreate, db: Session = Depends(get_db)):
    db_editorial = models.Editorial(**editorial.model_dump())
    db.add(db_editorial)
    db.commit()
    db.refresh(db_editorial)
    return db_editorial

@router.put("/editoriales/{editorial_id}", response_model=schemas.Editorial)
def update_editorial(editorial_id: int, editorial: schemas.EditorialCreate, db: Session = Depends(get_db)):
    db_editorial = db.query(models.Editorial).filter(models.Editorial.editorial_id == editorial_id).first()
    if not db_editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    for key, value in editorial.model_dump().items():
        setattr(db_editorial, key, value)
    
    db.commit()
    db.refresh(db_editorial)
    return db_editorial

@router.delete("/editoriales/{editorial_id}")
def delete_editorial(editorial_id: int, db: Session = Depends(get_db)):
    db_editorial = db.query(models.Editorial).filter(models.Editorial.editorial_id == editorial_id).first()
    if not db_editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    db.delete(db_editorial)
    db.commit()
    return {"detail": "Editorial eliminada"}

# ==================== CATEGORIAS ====================
@router.get("/categorias", response_model=List[schemas.Categoria])
def get_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()

@router.get("/categorias/{categoria_id}", response_model=schemas.Categoria)
def get_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.categoria_id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/categorias", response_model=schemas.Categoria, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# ==================== LIBROS ====================
@router.get("/libros", response_model=List[schemas.Libro])
def get_libros(db: Session = Depends(get_db)):
    return db.query(models.Libro).all()

@router.get("/libros/detalle", response_model=List[schemas.LibroDetalle])
def get_libros_detalle(db: Session = Depends(get_db)):
    return db.query(models.Libro).options(
        joinedload(models.Libro.editorial),
        joinedload(models.Libro.autores),
        joinedload(models.Libro.categorias)
    ).all()

@router.get("/libros/{libro_id}", response_model=schemas.Libro)
def get_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.libro_id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.get("/libros/{libro_id}/detalle", response_model=schemas.LibroDetalle)
def get_libro_detalle(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).options(
        joinedload(models.Libro.editorial),
        joinedload(models.Libro.autores),
        joinedload(models.Libro.categorias)
    ).filter(models.Libro.libro_id == libro_id).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.post("/libros", response_model=schemas.Libro, status_code=status.HTTP_201_CREATED)
def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    # Crear libro
    db_libro = models.Libro(**libro.model_dump(exclude={'autor_ids', 'categoria_ids'}))
    db.add(db_libro)
    db.flush()
    
    # Agregar autores
    if libro.autor_ids:
        autores = db.query(models.Autor).filter(models.Autor.autor_id.in_(libro.autor_ids)).all()
        db_libro.autores = autores
    
    # Agregar categorías
    if libro.categoria_ids:
        categorias = db.query(models.Categoria).filter(models.Categoria.categoria_id.in_(libro.categoria_ids)).all()
        db_libro.categorias = categorias
    
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.put("/libros/{libro_id}", response_model=schemas.Libro)
def update_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.libro_id == libro_id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Actualizar campos básicos
    for key, value in libro.model_dump(exclude={'autor_ids', 'categoria_ids'}).items():
        setattr(db_libro, key, value)
    
    # Actualizar autores
    if libro.autor_ids is not None:
        autores = db.query(models.Autor).filter(models.Autor.autor_id.in_(libro.autor_ids)).all()
        db_libro.autores = autores
    
    # Actualizar categorías
    if libro.categoria_ids is not None:
        categorias = db.query(models.Categoria).filter(models.Categoria.categoria_id.in_(libro.categoria_ids)).all()
        db_libro.categorias = categorias
    
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.delete("/libros/{libro_id}")
def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.libro_id == libro_id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    db.delete(db_libro)
    db.commit()
    return {"detail": "Libro eliminado"}

# ==================== USUARIOS ====================
@router.get("/usuarios", response_model=List[schemas.Usuario])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario_id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.model_dump().items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.usuario_id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_usuario.activo = False  # Soft delete como en guía
    db.commit()
    return {"detail": "Usuario desactivado"}

# ==================== PRESTAMOS ====================
@router.get("/prestamos", response_model=List[schemas.Prestamo])
def get_prestamos(db: Session = Depends(get_db)):
    return db.query(models.Prestamo).all()

@router.get("/prestamos/activos", response_model=List[schemas.Prestamo])
def get_prestamos_activos(db: Session = Depends(get_db)):
    return db.query(models.Prestamo).filter(models.Prestamo.estado == "ACTIVO").all()

@router.get("/prestamos/usuario/{usuario_id}", response_model=List[schemas.Prestamo])
def get_prestamos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(models.Prestamo).filter(models.Prestamo.usuario_id == usuario_id).all()

@router.get("/prestamos/{prestamo_id}", response_model=schemas.Prestamo)
def get_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(models.Prestamo).filter(models.Prestamo.prestamo_id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo

@router.post("/prestamos", response_model=schemas.Prestamo, status_code=status.HTTP_201_CREATED)
def create_prestamo(prestamo: schemas.PrestamoCreate, db: Session = Depends(get_db)):
    # Verificar disponibilidad
    libro = db.query(models.Libro).filter(models.Libro.libro_id == prestamo.libro_id).first()
    if not libro or libro.ejemplares_disponibles < 1:
        raise HTTPException(status_code=400, detail="No hay ejemplares disponibles")
    
    # Crear préstamo
    db_prestamo = models.Prestamo(**prestamo.model_dump())
    db.add(db_prestamo)
    
    # Actualizar disponibilidad
    libro.ejemplares_disponibles -= 1
    
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo

@router.put("/prestamos/{prestamo_id}/devolver")
def devolver_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(models.Prestamo).filter(models.Prestamo.prestamo_id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    if prestamo.estado == "DEVUELTO":
        raise HTTPException(status_code=400, detail="Libro ya devuelto")
    
    # Actualizar préstamo
    prestamo.fecha_devolucion_real = date.today()
    prestamo.estado = "DEVUELTO"
    
    # Restaurar disponibilidad
    libro = db.query(models.Libro).filter(models.Libro.libro_id == prestamo.libro_id).first()
    libro.ejemplares_disponibles += 1
    
    db.commit()
    return {"detail": "Libro devuelto exitosamente"}

# ==================== RESERVAS ====================
@router.get("/reservas", response_model=List[schemas.Reserva])
def get_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()

@router.get("/reservas/activas", response_model=List[schemas.Reserva])
def get_reservas_activas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).filter(models.Reserva.estado == "ACTIVA").all()

@router.post("/reservas", response_model=schemas.Reserva, status_code=status.HTTP_201_CREATED)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    db_reserva = models.Reserva(**reserva.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@router.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.reserva_id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    db.delete(db_reserva)
    db.commit()
    return {"detail": "Reserva eliminada"}