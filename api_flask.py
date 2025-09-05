from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

#Plantilla para la tabla en Web
HTML_PLANTILLA = """
<!doctype html>
<html>
<head>
    <title>Asistencia</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>📋 Asistencia de Empleados</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Empleado</th>
            <th>Fecha</th>
            <th>Entrada</th>
            <th>Salida</th>
        </tr>
        {% for r in registros %}
        <tr>
            <td>{{ r[0] }}</td>
            <td>{{ r[1] }}</td>
            <td>{{ r[2] }}</td>
            <td>{{ r[3] }}</td>
            <td>{{ r[4] if r[4] else '---' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""
#Servidor Flask
@app.route("/")
def ver_asistencia():
    conn = sqlite3.connect("asistencia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT asistencia.id, empleados.nombre, asistencia.fecha, asistencia.hora_entrada, asistencia.hora_salida
        FROM asistencia
        JOIN empleados ON empleados.id = asistencia.empleado_id
        ORDER BY asistencia.fecha DESC, asistencia.hora_entrada DESC
    """)
    registros = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_PLANTILLA, registros=registros)
#Iniciar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


