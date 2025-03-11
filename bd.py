import sqlite3

class BD:
    
    # Constructor de la clase donde le pasamos la ruta donde se creará la base de datos SQLite
    def __init__(self, bd = "todo.sqlite"):
        self.bd = bd
        self.conBD = sqlite3.connect(bd)
    
    # Crea la bd sqlite con la tabla "tareas" si no existe
    def crearBD(self):
        # Creamos la tabla "tareas", con clave primaria "codigo" autoincremental y 
        # el campo "autor" para mostrar a cada usuario sólo sus tareas
        sql = """CREATE TABLE IF NOT EXISTS tareas (
            codigo integer primary key autoincrement, 
            descripcion text, fecha date, autor, resuelta boolean)"""
        self.conBD.execute(sql)
        sql = "CREATE INDEX IF NOT EXISTS descripcionIndice ON tareas (descripcion ASC)"
        self.conBD.execute(sql)
        sql = "CREATE INDEX IF NOT EXISTS autorIndice ON tareas (autor ASC)"
        self.conBD.execute(sql)
        self.conBD.commit()
    
    # Añade una nueva tarea (siempre con el ID del chat del autor)
    def insertarTarea(self, tarea, fecha, autor, resuelta):
        sql = "INSERT INTO tareas (descripcion, fecha, autor, resuelta) VALUES (?, ? ,?, ?)"
        parametros = (tarea, fecha, autor, resuelta)
        self.conBD.execute(sql, parametros)
        self.conBD.commit()
    
    # Elimina la tarea indicada (filtrada por código y autor)
    def eliminarTarea(self, codigo, autor):
        sql = "DELETE FROM tareas WHERE codigo = (?) AND autor = (?)"
        parametros = (codigo, autor)
        self.conBD.execute(sql, parametros)
        self.conBD.commit()
    
    # Obtiene las tareas no resueltas (filtradas por autor)
    def obtenerTareas(self, autor):
        sql = """SELECT codigo, descripcion, fecha, resuelta
                 FROM tareas
                 WHERE autor = (?) and (resuelta = 0 or resuelta is null)"""
        parametros = (autor, )
        return [x for x in self.conBD.execute(sql, parametros)]
    
    # Obtiene una tarea filtrada por código y autor
    def obtenerTareaCodigo(self, codigo, autor):
        sql = """SELECT codigo, descripcion, fecha, resuelta
                 FROM tareas
                 WHERE codigo = (?) AND autor = (?)"""
        parametros = (codigo, autor)
        resultado = self.conBD.execute(sql, parametros).fetchone()
        return resultado
    
    # Obtiene todas las tareas de un autor
    def obtenerTareasTodas(self, autor):
        sql = """SELECT codigo, descripcion, fecha, resuelta
                 FROM tareas WHERE autor = (?)"""
        parametros = (autor, )
        return [x for x in self.conBD.execute(sql, parametros)]
    
    # Resuelve una tarea (filtrada por código y autor)
    def resolverTarea(self, codigo, autor):
        sql = """UPDATE tareas
                 SET resuelta = 1
                 WHERE codigo = (?) AND autor = (?)"""
        parametros = (codigo, autor)
        self.conBD.execute(sql, parametros)
        self.conBD.commit()
        
    # Reabrir una tarea (filtrada por código y autor)
    def reabrirTarea(self, codigo, autor):
        sql = """UPDATE tareas
                 SET resuelta = 0
                 WHERE codigo = (?) AND autor = (?)"""
        parametros = (codigo, autor)
        self.conBD.execute(sql, parametros)
        self.conBD.commit()