# Importa la clase datetime para manejar fechas y horas
from datetime import datetime
# Importa tkinter para crear la interfaz gráfica
import tkinter as tk
# Importa messagebox y simpledialog para mostrar diálogos y cuadros de entrada
from tkinter import messagebox, simpledialog
# Importa json para guardar y cargar datos en formato JSON
import json
# Importa os para verificar si los archivos existen
import os


# Clase que representa una habitación del hotel
class Habitacion:
    # Constructor que inicializa los atributos de la habitación
    def __init__(self, numero, tipo, precio_por_noche):
        # Número único de la habitación
        self.numero = numero
        # Tipo de habitación (sencilla, doble, suite, etc.)
        self.tipo = tipo
        # Precio por noche de la habitación
        self.precio_por_noche = precio_por_noche
        # Estado inicial de la habitación (disponible por defecto)
        self.estado = "disponible"

    # Método que retorna una representación en texto de la habitación
    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo} - ${self.precio_por_noche} - {self.estado}"


# Clase que representa un huésped del hotel
class Huesped:
    # Constructor que inicializa los atributos del huésped
    def __init__(self, nombre, id_huesped):
        # Nombre completo del huésped
        self.nombre = nombre
        # Identificación única del huésped
        self.id_huesped = id_huesped
        # Lista de reservaciones previas del huésped
        self.reservaciones_previas = []

    # Método que retorna una representación en texto del huésped
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_huesped})"


# Clase que representa una reservación de habitación
class Reservacion:
    # Constructor que inicializa los atributos de la reservación
    def __init__(self, huesped, habitacion, fecha_entrada, fecha_salida, fecha_reservacion=None):
        # Objeto huésped que hace la reservación
        self.huesped = huesped
        # Objeto habitación que se está reservando
        self.habitacion = habitacion
        # Fecha de entrada del huésped (formato datetime)
        self.fecha_entrada = fecha_entrada
        # Fecha de salida del huésped (formato datetime)
        self.fecha_salida = fecha_salida
        # Fecha en que se realizó la reservación (usa la fecha actual si no se proporciona)
        self.fecha_reservacion = fecha_reservacion if fecha_reservacion else datetime.now()

    # Método que calcula el costo total de la reservación
    def calcular_costo(self):
        # Calcula la diferencia en días entre la salida y entrada
        dias = (self.fecha_salida - self.fecha_entrada).days
        # Si los días son menores a 1, se cuenta como 1 día mínimo
        if dias < 1:
            dias = 1
        # Retorna el costo total multiplicando días por el precio por noche
        return dias * self.habitacion.precio_por_noche

    # Método que retorna una representación en texto de la reservación
    def __str__(self):
        # Formatea la fecha de entrada al formato YYYY-MM-DD
        e = self.fecha_entrada.strftime("%Y-%m-%d")
        # Formatea la fecha de salida al formato YYYY-MM-DD
        s = self.fecha_salida.strftime("%Y-%m-%d")
        # Retorna una cadena con los detalles de la reservación
        return f"{self.huesped.nombre} - Hab {self.habitacion.numero} - {e} to {s} - ${self.calcular_costo()}"


# Clase que representa el hotel y gestiona todas sus operaciones
class Hotel:
    # Constructor que inicializa los atributos del hotel
    def __init__(self, nombre):
        # Nombre del hotel
        self.nombre = nombre
        # Lista de todas las habitaciones del hotel
        self.habitaciones = []
        # Lista de todas las reservaciones activas
        self.reservaciones = []
        # Lista de todos los huéspedes registrados
        self.huespedes = []
        # Nombre del archivo donde se guardan los datos (JSON)
        self.data_file = "datos_hotel.json"

    # Método que agrega una nueva habitación al hotel
    def agregar_habitacion(self, habitacion):
        # Añade la habitación a la lista de habitaciones
        self.habitaciones.append(habitacion)

    # Método que busca una habitación por su número
    def buscar_habitacion(self, numero):
        # Recorre todas las habitaciones
        for h in self.habitaciones:
            # Si el número coincide, retorna la habitación
            if h.numero == numero:
                return h
        # Si no encuentra la habitación, retorna None
        return None

    # Método que retorna todas las habitaciones disponibles
    def habitaciones_disponibles(self):
        # Retorna una lista con las habitaciones cuyo estado es disponible
        return [h for h in self.habitaciones if h.estado == "disponible"]

    # Método que busca un huésped por su ID
    def buscar_huesped(self, id_huesped):
        # Recorre todos los huéspedes
        for hu in self.huespedes:
            # Si el ID coincide, retorna el huésped
            if hu.id_huesped == id_huesped:
                return hu
        # Si no encuentra el huésped, retorna None
        return None

    # Método que registra un nuevo huésped o retorna uno existente
    def registrar_huesped(self, nombre, id_huesped):
        # Busca si el huésped ya existe
        hu = self.buscar_huesped(id_huesped)
        # Si el huésped ya existe, lo retorna
        if hu:
            return hu
        # Crea un nuevo objeto Huesped
        nuevo = Huesped(nombre, id_huesped)
        # Añade el nuevo huésped a la lista
        self.huespedes.append(nuevo)
        # Guarda los datos en el archivo JSON
        self.guardar_datos()
        # Retorna el nuevo huésped
        return nuevo

    # Método que crea una nueva reservación
    def hacer_reservacion(self, id_huesped, nombre, numero_habitacion, fecha_entrada, fecha_salida, fecha_reservacion=None):
        # Busca la habitación por su número
        hab = self.buscar_habitacion(numero_habitacion)
        # Si la habitación no existe, retorna None y un mensaje de error
        if hab is None:
            return None, "Habitación no encontrada"
        # Si la habitación no está disponible, retorna None y un mensaje de error
        if hab.estado != "disponible":
            return None, "Habitación ocupada"
        # Si la fecha de salida no es después de la entrada, retorna None y un mensaje de error
        if fecha_salida <= fecha_entrada:
            return None, "Fecha de salida debe ser después"
        # Registra o obtiene el huésped
        hu = self.registrar_huesped(nombre, id_huesped)
        # Crea un nuevo objeto Reservacion
        r = Reservacion(hu, hab, fecha_entrada, fecha_salida, fecha_reservacion)
        # Añade la reservación a la lista
        self.reservaciones.append(r)
        # Marca la habitación como ocupada
        hab.estado = "ocupada"
        # Guarda los datos en el archivo JSON
        self.guardar_datos()
        # Retorna la reservación creada y un mensaje de éxito
        return r, "Reservación creada"

    # Método que guarda todos los datos en un archivo JSON
    def guardar_datos(self):
        # Intenta ejecutar el código para capturar posibles errores
        try:
            # Crea un diccionario con los datos de huéspedes y reservaciones
            data = {
                # Lista de diccionarios con los datos de cada huésped
                "huespedes": [
                    {"nombre": h.nombre, "id": h.id_huesped} for h in self.huespedes
                ],
                # Lista de diccionarios con los datos de cada reservación
                "reservaciones": [
                    {
                        # ID del huésped que hizo la reservación
                        "id_huesped": r.huesped.id_huesped,
                        # Número de la habitación reservada
                        "habitacion": r.habitacion.numero,
                        # Fecha de entrada en formato YYYY-MM-DD
                        "entrada": r.fecha_entrada.strftime("%Y-%m-%d"),
                        # Fecha de salida en formato YYYY-MM-DD
                        "salida": r.fecha_salida.strftime("%Y-%m-%d"),
                        # Fecha de realización de la reservación en formato YYYY-MM-DD HH:MM:SS
                        "reservacion": r.fecha_reservacion.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for r in self.reservaciones
                ],
            }
            # Abre el archivo en modo escritura con codificación UTF-8
            with open(self.data_file, "w", encoding="utf-8") as f:
                # Escribe los datos en formato JSON con indentación de 2 espacios
                json.dump(data, f, ensure_ascii=False, indent=2)
        # Si hay un error, lo ignora silenciosamente
        except Exception:
            pass

    # Método que carga los datos desde el archivo JSON
    def cargar_datos(self):
        # Verifica si el archivo de datos existe
        if not os.path.exists(self.data_file):
            # Si no existe, termina la función
            return
        # Intenta ejecutar el código para capturar posibles errores
        try:
            # Abre el archivo en modo lectura con codificación UTF-8
            with open(self.data_file, "r", encoding="utf-8") as f:
                # Lee el contenido del archivo JSON
                data = json.load(f)
            # Carga los huéspedes desde el archivo
            for h in data.get("huespedes", []):
                # Verifica si el huésped ya existe
                if not self.buscar_huesped(h.get("id")):
                    # Si no existe, crea un nuevo huésped y lo añade a la lista
                    self.huespedes.append(Huesped(h.get("nombre", ""), str(h.get("id"))))
            # Carga las reservaciones desde el archivo
            for r in data.get("reservaciones", []):
                # Busca el huésped de la reservación
                hu = self.buscar_huesped(str(r.get("id_huesped")))
                # Busca la habitación de la reservación
                hab = self.buscar_habitacion(r.get("habitacion"))
                # Intenta convertir las fechas al formato datetime
                try:
                    # Convierte la fecha de entrada
                    fe = datetime.strptime(r.get("entrada"), "%Y-%m-%d")
                    # Convierte la fecha de salida
                    fs = datetime.strptime(r.get("salida"), "%Y-%m-%d")
                    # Convierte la fecha de reservación (o usa la fecha actual si no existe)
                    fr = datetime.strptime(r.get("reservacion", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                # Si hay un error en la conversión de fechas, continúa con la siguiente reservación
                except Exception:
                    continue
                # Si el huésped y la habitación existen, crea la reservación
                if hu and hab:
                    # Crea un nuevo objeto Reservacion
                    reserva = Reservacion(hu, hab, fe, fs, fr)
                    # Añade la reservación a la lista
                    self.reservaciones.append(reserva)
        # Si hay un error, lo ignora silenciosamente
        except Exception:
            pass

    # Método que realiza el check-in de un huésped en una habitación
    def hacer_checkin(self, numero_habitacion):
        # Busca la habitación por su número
        hab = self.buscar_habitacion(numero_habitacion)
        # Si la habitación no existe, retorna un mensaje de error
        if hab is None:
            return "Habitación no encontrada"
        # Si la habitación ya está ocupada, retorna un mensaje de error
        if hab.estado == "ocupada":
            return "La habitación ya está ocupada"
        # Marca la habitación como ocupada
        hab.estado = "ocupada"
        # Guarda los datos en el archivo JSON
        self.guardar_datos()
        # Retorna un mensaje de éxito
        return "Check-in hecho"

    # Método que realiza el check-out de un huésped y libera la habitación
    def hacer_checkout(self, numero_habitacion):
        # Busca la habitación por su número
        hab = self.buscar_habitacion(numero_habitacion)
        # Si la habitación no existe, retorna None y un mensaje de error
        if hab is None:
            return None, "Habitación no encontrada"
        # Si la habitación ya está disponible, retorna None y un mensaje de error
        if hab.estado == "disponible":
            return None, "La habitación ya está libre"
        # Inicializa la variable reserva en None
        reserva = None
        # Recorre todas las reservaciones para encontrar la que corresponde a esta habitación
        for r in self.reservaciones:
            # Si la habitación de la reservación coincide
            if r.habitacion.numero == numero_habitacion:
                # Asigna la reservación encontrada
                reserva = r
                # Sale del bucle
                break
        # Marca la habitación como disponible
        hab.estado = "disponible"
        # Si se encontró una reservación
        if reserva:
            # Elimina la reservación de la lista de activas
            self.reservaciones.remove(reserva)
            # Añade la reservación a las reservaciones previas del huésped
            reserva.huesped.reservaciones_previas.append(reserva)
            # Guarda los datos en el archivo JSON
            self.guardar_datos()
            # Retorna la factura y un mensaje de éxito
            return self.generar_factura(reserva), "Check-out hecho"
        # Si no se encontró una reservación
        else:
            # Guarda los datos en el archivo JSON
            self.guardar_datos()
            # Retorna None y un mensaje informativo
            return None, "No había reservación, habitación liberada"

    # Método que genera una factura para una reservación
    def generar_factura(self, r):
        # Calcula el costo total de la reservación
        total = r.calcular_costo()
        # Inicializa el texto de la factura
        texto = "Factura\n"
        # Añade el nombre del huésped
        texto += "Huésped: " + r.huesped.nombre + "\n"
        # Añade el número de la habitación
        texto += "Habitación: " + str(r.habitacion.numero) + "\n"
        # Añade la fecha de entrada
        texto += "Entrada: " + r.fecha_entrada.strftime("%Y-%m-%d") + "\n"
        # Añade la fecha de salida
        texto += "Salida: " + r.fecha_salida.strftime("%Y-%m-%d") + "\n"
        # Añade el costo total
        texto += "Total: $" + str(total) + "\n"
        # Retorna el texto de la factura
        return texto


# Función que crea la interfaz gráfica principal
def crear_interfaz():
    # Crea un nuevo objeto Hotel
    hotel = Hotel("Hotel Simple")
    # Agrega una habitación sencilla con número 101 y precio de $50
    hotel.agregar_habitacion(Habitacion(101, "sencilla", 50))
    # Agrega una habitación sencilla con número 102 y precio de $55
    hotel.agregar_habitacion(Habitacion(102, "sencilla", 55))
    # Agrega una habitación doble con número 201 y precio de $80
    hotel.agregar_habitacion(Habitacion(201, "doble", 80))
    # Agrega una habitación doble con número 202 y precio de $85
    hotel.agregar_habitacion(Habitacion(202, "doble", 85))
    # Agrega una suite con número 301 y precio de $120
    hotel.agregar_habitacion(Habitacion(301, "suite", 120))
    # Carga los datos guardados si existen
    hotel.cargar_datos()

    # Imprime un mensaje de depuración
    print("[DEBUG] Iniciando interfaz gráfica...")
    # Crea la ventana principal de Tkinter
    root = tk.Tk()
    # Imprime un mensaje de depuración
    print("[DEBUG] Ventana Tk creada")
    # Establece el título de la ventana
    root.title("Sistema de Reservaciones - Hotel Simple")
    # Establece el tamaño de la ventana
    root.geometry("400x350")
    # Intenta poner la ventana en primer plano
    try:
        # Levanta la ventana al frente
        root.lift()
        # Establece la ventana como siempre en primer plano
        root.attributes('-topmost', True)
        # Después de 500 milisegundos, desactiva que sea siempre en primer plano
        root.after(500, lambda: root.attributes('-topmost', False))
    # Si hay un error, lo ignora silenciosamente
    except Exception:
        pass

    # Crea una etiqueta con el título de bienvenida
    lbl = tk.Label(root, text="Bienvenido al Hotel Simple", font=(None, 14))
    # Empaqueta la etiqueta en la ventana
    lbl.pack(pady=8)
    # Después de 100 milisegundos, muestra un cuadro de información
    root.after(100, lambda: messagebox.showinfo("Info", "Interfaz iniciada"))

    # Función que muestra las habitaciones disponibles
    def ver_disponibles():
        # Obtiene la lista de habitaciones disponibles
        disp = hotel.habitaciones_disponibles()
        # Si no hay habitaciones disponibles
        if not disp:
            # Muestra un mensaje informativo
            messagebox.showinfo("Disponibles", "No hay habitaciones disponibles")
            # Termina la función
            return
        # Convierte la lista de habitaciones en un texto
        texto = "\n".join([str(h) for h in disp])
        # Muestra un cuadro de información con las habitaciones disponibles
        messagebox.showinfo("Habitaciones disponibles", texto)

    # Función que realiza una nueva reservación
    def hacer_reserva():
        # Solicita el nombre del huésped
        nombre = simpledialog.askstring("Reservación", "Nombre del huésped:")
        # Si el usuario no ingresa un nombre, termina la función
        if not nombre:
            return
        # Solicita el ID del huésped
        idh = simpledialog.askstring("Reservación", "ID del huésped:")
        # Si el usuario no ingresa un ID, termina la función
        if not idh:
            return
        # Intenta obtener el número de habitación
        try:
            # Solicita el número de habitación y lo convierte a entero
            num = int(simpledialog.askstring("Reservación", "Número de habitación:"))
        # Si hay un error en la conversión
        except Exception:
            # Muestra un cuadro de error
            messagebox.showerror("Error", "Número de habitación inválido")
            # Termina la función
            return
        # Solicita la fecha de reservación
        fecha_res = simpledialog.askstring("Reservación", "Fecha de reservación (YYYY-MM-DD HH:MM:SS) o dejar en blanco para hoy:")
        # Si el usuario ingresa una fecha de reservación
        if fecha_res:
            # Intenta convertir la fecha al formato datetime
            try:
                # Convierte la cadena a formato datetime
                fr = datetime.strptime(fecha_res, "%Y-%m-%d %H:%M:%S")
            # Si hay un error en la conversión
            except Exception:
                # Muestra un cuadro de error
                messagebox.showerror("Error", "Formato de fecha de reservación inválido")
                # Termina la función
                return
        # Si el usuario no ingresa una fecha
        else:
            # Asigna None para usar la fecha actual
            fr = None
        # Solicita la fecha de entrada
        fecha_e = simpledialog.askstring("Reservación", "Fecha de entrada (YYYY-MM-DD):")
        # Solicita la fecha de salida
        fecha_s = simpledialog.askstring("Reservación", "Fecha de salida (YYYY-MM-DD):")
        # Intenta convertir las fechas al formato datetime
        try:
            # Convierte la fecha de entrada
            fe = datetime.strptime(fecha_e, "%Y-%m-%d")
            # Convierte la fecha de salida
            fs = datetime.strptime(fecha_s, "%Y-%m-%d")
        # Si hay un error en la conversión
        except Exception:
            # Muestra un cuadro de error
            messagebox.showerror("Error", "Formato de fecha inválido")
            # Termina la función
            return
        # Realiza la reservación y obtiene el objeto reservación y el mensaje
        reserva, msg = hotel.hacer_reservacion(idh, nombre, num, fe, fs, fr)
        # Muestra un cuadro de información con el mensaje
        messagebox.showinfo("Reservación", msg)
        # Si la reservación fue exitosa
        if reserva:
            # Muestra los detalles de la reservación creada
            messagebox.showinfo("Reservación creada", str(reserva))

    # Función que realiza el check-in
    def checkin():
        # Intenta obtener el número de habitación
        try:
            # Solicita el número de habitación y lo convierte a entero
            num = int(simpledialog.askstring("Check-in", "Número de habitación:"))
        # Si hay un error en la conversión
        except Exception:
            # Muestra un cuadro de error
            messagebox.showerror("Error", "Número inválido")
            # Termina la función
            return
        # Realiza el check-in y obtiene el mensaje
        msg = hotel.hacer_checkin(num)
        # Muestra un cuadro de información con el mensaje
        messagebox.showinfo("Check-in", msg)

    # Función que realiza el check-out
    def checkout():
        # Intenta obtener el número de habitación
        try:
            # Solicita el número de habitación y lo convierte a entero
            num = int(simpledialog.askstring("Check-out", "Número de habitación:"))
        # Si hay un error en la conversión
        except Exception:
            # Muestra un cuadro de error
            messagebox.showerror("Error", "Número inválido")
            # Termina la función
            return
        # Realiza el check-out y obtiene la factura y el mensaje
        factura, msg = hotel.hacer_checkout(num)
        # Muestra un cuadro de información con el mensaje
        messagebox.showinfo("Check-out", msg)
        # Si se generó una factura
        if factura:
            # Muestra la factura en un cuadro de información
            messagebox.showinfo("Factura", factura)

    # Función que busca un huésped por su ID
    def buscar_huesped_gui():
        # Solicita el ID del huésped
        idh = simpledialog.askstring("Buscar huésped", "ID del huésped:")
        # Si el usuario no ingresa un ID, termina la función
        if not idh:
            return
        # Busca el huésped en la base de datos
        hu = hotel.buscar_huesped(idh)
        # Si el huésped no existe
        if not hu:
            # Muestra un mensaje informativo
            messagebox.showinfo("Buscar huésped", "Huésped no encontrado")
            # Termina la función
            return
        # Inicializa el texto con los datos del huésped
        texto = str(hu) + "\nReservaciones previas:\n"
        # Si el huésped no tiene reservaciones previas
        if not hu.reservaciones_previas:
            # Añade un mensaje indicando que no tiene reservaciones
            texto += "No tiene reservaciones previas"
        # Si el huésped tiene reservaciones previas
        else:
            # Recorre todas las reservaciones previas
            for r in hu.reservaciones_previas:
                # Añade cada reservación al texto
                texto += str(r) + "\n"
        # Muestra un cuadro de información con los datos del huésped
        messagebox.showinfo("Huésped", texto)

    # Crea un botón para ver habitaciones disponibles
    btn_ver = tk.Button(root, text="Ver habitaciones disponibles", width=30, command=ver_disponibles)
    # Empaqueta el botón en la ventana
    btn_ver.pack(pady=4)
    # Crea un botón para hacer una reservación
    btn_res = tk.Button(root, text="Hacer reservación", width=30, command=hacer_reserva)
    # Empaqueta el botón en la ventana
    btn_res.pack(pady=4)
    # Crea un botón para hacer check-in
    btn_in = tk.Button(root, text="Check-in", width=30, command=checkin)
    # Empaqueta el botón en la ventana
    btn_in.pack(pady=4)
    # Crea un botón para hacer check-out y factura
    btn_out = tk.Button(root, text="Check-out y factura", width=30, command=checkout)
    # Empaqueta el botón en la ventana
    btn_out.pack(pady=4)
    # Crea un botón para buscar un huésped
    btn_bus = tk.Button(root, text="Buscar huésped", width=30, command=buscar_huesped_gui)
    # Empaqueta el botón en la ventana
    btn_bus.pack(pady=4)
    # Crea un botón para salir de la aplicación
    btn_salir = tk.Button(root, text="Salir", width=30, command=root.destroy)
    # Empaqueta el botón en la ventana
    btn_salir.pack(pady=8)

    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()


# Verifica si el script se ejecuta directamente (no como módulo importado)
if __name__ == "__main__":
    # Llama a la función para crear la interfaz
    crear_interfaz()
