cola_pendientes = []
pila_historial = []
siguiente_id = 1

def registrar_solicitud(cliente, asunto):
    global siguiente_id
    c_limpio = cliente.strip()
    a_limpio = asunto.strip()

    if not c_limpio or not a_limpio:
        return False, "Datos inválidos"

    for solicitud in cola_pendientes:
        if (solicitud["cliente"].strip().lower() == c_limpio.lower() and
            solicitud["asunto"].strip().lower() == a_limpio.lower()):
            return False, "La solicitud ya se encuentra pendiente"

    solicitud = {
        "id": siguiente_id,
        "cliente": c_limpio,
        "asunto": a_limpio,
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return True, "Registrada exitosamente"

def atender_siguiente():
    if not cola_pendientes:
        return None
    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud

def deshacer_ultima_atencion():
    if not pila_historial:
        return None
    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud

def consultar_siguiente():
    if not cola_pendientes:
        return None
    return cola_pendientes[0]

def buscar_solicitud(id_solicitud):
    for solicitud in cola_pendientes:
        if solicitud["id"] == id_solicitud:
            return solicitud, "pendiente"
    for solicitud in pila_historial:
        if solicitud["id"] == id_solicitud:
            return solicitud, "atendido"
    return None, None

def cancelar_pendiente(id_solicitud):
    for i, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == id_solicitud:
            return cola_pendientes.pop(i)
    return None

def deshacer_varias(cantidad):
    if cantidad <= 0:
        return 0
    recuperadas = 0
    for _ in range(cantidad):
        if deshacer_ultima_atencion() is None:
            break
        recuperadas += 1
    return recuperadas

def obtener_estadisticas():
    unicas = set()
    for sol in cola_pendientes + pila_historial:
        unicas.add((sol["cliente"].lower(), sol["asunto"].lower()))
    
    return {
        "pendientes": len(cola_pendientes),
        "atenciones": len(pila_historial),
        "unicas": len(unicas)
    }