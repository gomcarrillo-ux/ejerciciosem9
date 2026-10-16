from flask import Flask, render_template, request, redirect, url_for, flash
import logica

app = Flask(__name__)
app.secret_key = "super_secreto" # Necesario para usar flash messages

@app.get("/")
def inicio():
    # Reto 1: Consultar siguiente
    siguiente = logica.consultar_siguiente()
    # Reto 5: Estadísticas
    stats = logica.obtener_estadisticas()
    
    # Reto 2: Búsqueda por ID (si viene en la URL)
    busqueda_id = request.args.get("id")
    resultado_busqueda = None
    if busqueda_id and busqueda_id.isdigit():
        req, estado = logica.buscar_solicitud(int(busqueda_id))
        if req:
            resultado_busqueda = f"Solicitud #{req['id']} ({req['cliente']}) encontrada en estado: {estado}."
        else:
            resultado_busqueda = f"Solicitud #{busqueda_id} no encontrada."

    return render_template(
        "index.html",
        pendientes=logica.cola_pendientes,
        historial=logica.pila_historial,
        siguiente=siguiente,
        stats=stats,
        resultado_busqueda=resultado_busqueda
    )

@app.post("/registrar")
def registrar():
    exito, mensaje = logica.registrar_solicitud(
        request.form.get("cliente", ""),
        request.form.get("asunto", "")
    )
    if not exito:
        flash(mensaje, "danger") # Reto 5: Avisa al usuario si está duplicada
    else:
        flash(mensaje, "success")
    return redirect(url_for("inicio"))

@app.post("/atender")
def atender():
    logica.atender_siguiente()
    return redirect(url_for("inicio"))

@app.post("/deshacer")
def deshacer():
    logica.deshacer_ultima_atencion()
    return redirect(url_for("inicio"))

# Reto 3: Cancelar
@app.post("/cancelar/<int:id>")
def cancelar(id):
    logica.cancelar_pendiente(id)
    flash(f"Solicitud #{id} cancelada.", "warning")
    return redirect(url_for("inicio"))

# Reto 4: Deshacer varias
@app.post("/deshacer-varias")
def deshacer_varias():
    cantidad_str = request.form.get("cantidad", "0")
    if cantidad_str.isdigit():
        recuperadas = logica.deshacer_varias(int(cantidad_str))
        flash(f"Se restauraron {recuperadas} solicitudes.", "info")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)

#Una cola FIFO tradicional no resuelve el manejo de prioridades porque su única regla es el orden de llegada,
# por lo que una solicitud urgente registrada al final quedaría atrapada detrás de todas las normales sin importar su gravedad. 
# Para solucionarlo, se tendría que modificar el modelo de datos agregando un campo de `prioridad` a cada registro
# y sustituir la lista simple por una **cola de prioridad** (o reordenar la lista al insertar), 
# de modo que la función de atención seleccione siempre el elemento de mayor importancia y use el orden de llegada 
# únicamente como criterio de desempate entre solicitudes del mismo nivel.