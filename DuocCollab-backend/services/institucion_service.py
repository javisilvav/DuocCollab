from bd.institucion import (
    obtener_sedes, crear_sede,
    obtener_carreras, crear_carrera,
    obtener_escuelas, crear_escuela,
    obtener_sede_escuela, crear_sede_escuela
)

def list_sedes(): return obtener_sedes()

def add_sede(data): return crear_sede(data)

def list_carreras(): return obtener_carreras()

def add_carrera(data): return crear_carrera(data)

def list_escuelas(): return obtener_escuelas()

def add_escuela(data): return crear_escuela(data)

def list_sede_escuela(): return obtener_sede_escuela()

def add_sede_escuela(data): return crear_sede_escuela(data)