cola_pendientes = []
pila_historial = []
siguiente_id = 1

def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)

def registrar_solicitud(cliente, asunto):
    global siguiente_id
    c_limpio = cliente.strip()
    a_limpio = asunto.strip()

    if not c_limpio or not a_limpio:
        return None

    for solicitud in cola_pendientes:
        if (solicitud["cliente"].strip().lower() == c_limpio.lower() and
            solicitud["asunto"].strip().lower() == a_limpio.lower()):
            return None

    solicitud = {
        "id": siguiente_id,
        "cliente": c_limpio,
        "asunto": a_limpio,
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud

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
            return solicitud, "historial"
            
    return None

def cancelar_pendiente(id_solicitud):
    for i, solicitud in enumerate(cola_pendientes):
        if solicitud["id"] == id_solicitud:
            return cola_pendientes.pop(i)
    return None

def deshacer_varias(cantidad):
    if not isinstance(cantidad, int) or cantidad <= 0:
        return 0, []

    restauradas = []
    for _ in range(cantidad):
        solicitud = deshacer_ultima_atencion()
        if solicitud is None:
            break
        restauradas.append(solicitud)

    return len(restauradas), restauradas

def obtener_estadisticas():
    pendientes = len(cola_pendientes)
    atenciones = len(pila_historial)
    
    unicas = set()
    for sol in cola_pendientes + pila_historial:
        unicas.add((sol["cliente"].lower(), sol["asunto"].lower()))
        
    return {
        "pendientes": pendientes,
        "atenciones_historial": atenciones,
        "total_unicas": len(unicas)
    }

def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Deshacer varias atenciones")
        print("5. Consultar siguiente")
        print("6. Buscar solicitud por ID")
        print("7. Cancelar solicitud pendiente")
        print("8. Obtener estadísticas")
        print("9. Mostrar estado")
        print("10. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            resultado = registrar_solicitud(cliente, asunto)
            print("Registrada:", resultado if resultado else "Datos inválidos o solicitud duplicada en pendientes")
        elif opcion == "2":
            print("Atendida:", atender_siguiente())
        elif opcion == "3":
            print("Restaurada:", deshacer_ultima_atencion())
        elif opcion == "4":
            try:
                cantidad = int(input("Cantidad a deshacer: "))
                recuperadas, lista = deshacer_varias(cantidad)
                print(f"Se recuperaron {recuperadas} solicitud(es): {lista}")
            except ValueError:
                print("Por favor, ingresa un número entero positivo.")
        elif opcion == "5":
            print("Siguiente en cola:", consultar_siguiente())
        elif opcion == "6":
            try:
                id_buscar = int(input("ID de la solicitud: "))
                resultado = buscar_solicitud(id_buscar)
                if resultado:
                    print(f"Encontrada en '{resultado[1]}': {resultado[0]}")
                else:
                    print("Solicitud no encontrada.")
            except ValueError:
                print("Por favor, ingresa un número de ID válido.")
        elif opcion == "7":
            try:
                id_cancelar = int(input("ID de la solicitud a cancelar: "))
                resultado = cancelar_pendiente(id_cancelar)
                if resultado:
                    print("Cancelada:", resultado)
                else:
                    print("No se encontró la solicitud en la cola de pendientes.")
            except ValueError:
                print("Por favor, ingresa un número de ID válido.")
        elif opcion == "8":
            print("Estadísticas:", obtener_estadisticas())
        elif opcion == "9":
            mostrar_estado()
        elif opcion == "10":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    ejecutar_menu()