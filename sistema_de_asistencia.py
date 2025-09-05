import sqlite3
from datetime import datetime, timedelta

conexion = sqlite3.connect("asistencia.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    clave_huella TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS asistencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TEXT,
    hora_salida TEXT,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
)
""")
conexion.commit()

empleados = [
    ("Juan Pérez", "1010"),
    ("María López", "2020"),
    ("Carlos Sánchez", "3030"),
    ("Ana Torres", "4040"),
    ("Luis Ramírez", "5050"),
    ("Sofía Díaz", "6060"),
    ("Pedro Gómez", "7070"),
    ("Laura Vargas", "8080"),
    ("José Hernández", "9090"),
    ("Marta Jiménez", "0001"),
]

for nombre, clave in empleados:
    cursor.execute("INSERT OR IGNORE INTO empleados (nombre, clave_huella) VALUES (?,?)", (nombre, clave))
conexion.commit()

def identificar_empleado(clave):
    cursor.execute("SELECT id, nombre FROM empleados WHERE clave_huella=?", (clave,))
    return cursor.fetchone()

def checar_asistencia(empleado_id):
    fecha = datetime.now().date()
    hora_actual = datetime.now().strftime("%H:%M:%S")
    cursor.execute("""
        SELECT * FROM asistencia 
        WHERE empleado_id=? AND fecha=? 
        ORDER BY id DESC LIMIT 1
    """, (empleado_id, fecha))
    registro = cursor.fetchone()

    if registro is None or registro[4] is not None:
        cursor.execute("INSERT INTO asistencia (empleado_id, fecha, hora_entrada) VALUES (?,?,?)",
                       (empleado_id, fecha, hora_actual))
        conexion.commit()
        return "✅ Entrada registrada"
    elif registro[4] is None:
        hora_entrada = datetime.strptime(registro[3], "%H:%M:%S")
        hora_actual_dt = datetime.strptime(hora_actual, "%H:%M:%S")
        if hora_actual_dt - hora_entrada < timedelta(minutes=5):
            return "⚠ No puedes registrar salida antes de 5 minutos de la entrada."
        cursor.execute("UPDATE asistencia SET hora_salida=? WHERE id=?", (hora_actual, registro[0]))
        conexion.commit()
        return "✅ Salida registrada"

def mostrar_asistencia():
    cursor.execute("""
        SELECT asistencia.id, empleados.nombre, asistencia.fecha, asistencia.hora_entrada, asistencia.hora_salida
        FROM asistencia
        JOIN empleados ON empleados.id = asistencia.empleado_id
        ORDER BY asistencia.fecha DESC, asistencia.hora_entrada DESC
    """)
    registros = cursor.fetchall()
    print("\n📋 Reporte de asistencia:")
    print(f"{'ID':<5}{'Empleado':<20}{'Fecha':<12}{'Entrada':<10}{'Salida':<10}")
    print("-"*60)
    for r in registros:
        print(f"{r[0]:<5}{r[1]:<20}{r[2]:<12}{r[3]:<10}{r[4] if r[4] else '---':<10}")

print("🚪 Sistema de asistencia activo. (Escribe 'reporte' para ver registros o 'salir' para apagar)\n")

while True:
    clave = input("👉 Coloca tu huella digital: ")

    if clave.lower() == "salir":
        print("🔴 Sistema apagado.")
        break
    elif clave.lower() == "reporte":
        mostrar_asistencia()
        continue

    empleado = identificar_empleado(clave)
    if empleado:
        print(f"👤 Bienvenido {empleado[1]}")
        mensaje = checar_asistencia(empleado[0])
        print("➡", mensaje)
    else:
        print("❌ Huella no reconocida.")

