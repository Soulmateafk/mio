from fastapi import FastAPI
from metodos import consultarApi

app = FastAPI()

# Incluir todos los routers
app.include_router(consultarApi.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API Biblioteca - FastAPI"}

# @app.get("/health")
# async def health_check():
#     return {"status": "ok"}

# # Para ver rutas registradas (opcional)
# @app.on_event("startup")
# async def startup_event():
#     print("\n=== RUTAS REGISTRADAS ===")
#     for route in app.routes:
#         if hasattr(route, "methods"):
#             print(f"{route.methods} - {route.path}")
#     print("=======================\n")