import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class Habitacion:
    #Representa una entidad física del hotel.
    #Encapsula los atributos de identificación, categoría, costo y estado.

    def __init__(self, numero, tipo, precio_noche):
        self.numero = numero          # Identificador único de la habitación (string)
        self.tipo = tipo              # Categoria: Sencilla, Doble o Suite
        self.precio_noche = precio_noche # Tarifa flotante o entera por noche
        self.estado = "Disponible"    # Estado operativo: Disponible o Ocupada

class Huesped:  
    #Representa al cliente en el sistema CRM.
    #Mantiene la persistencia de la identidad y la relación histórica de consumo.

    def __init__(self, nombre, huesped_id):
        self.nombre = nombre
        self.id = huesped_id          # Llave primaria para búsquedas y consultas
        self.historial_reservaciones = [] # Lista de agregación que almacena objetos tipo Reservacion

class Reservacion:
    #Clase asociativa que vincula un Objeto Huesped con un Objeto Habitacion.
    #Gestiona la lógica temporal y el cálculo financiero de la estancia.
    
    def __init__(self, huesped, habitacion, fecha_entrada, fecha_salida):
        self.huesped = huesped        # Instancia de la clase Huesped
        self.habitacion = habitacion  # Instancia de la clase Habitacion
        self.fecha_entrada = fecha_entrada   # Instancia datetime (objeto nativo de tiempo)
        self.fecha_salida = fecha_salida     # Instancia datetime (objeto nativo de tiempo)
        
    def calcular_costo_total(self):
        #Calcula la diferencia de días a través del álgebra de objetos datetime.
        #Retorna el producto de las noches por la tarifa de la habitación vinculada.
    
        noches = (self.fecha_salida - self.fecha_entrada).days
        if noches <= 0:
            noches = 1 # Cláusula de salvaguarda: asegura el cobro mínimo de una noche
        return noches * self.habitacion.precio_noche

class Hotel:
    #Clase controladora central. Administra los almacenes de datos (en memoria)
    #y funciona como la API interna para la interfaz gráfica.
    
    def __init__(self):
        self.habitaciones = {}   # Diccionario indexado por 'numero' para acceso O(1)
        self.huespedes = {}      # Diccionario indexado por 'id' para búsquedas eficientes
        self.reservaciones = []  # Estructura lineal (lista) para el registro global de reservas
        self.inicializar_datos() # Método semilla para pruebas

    def inicializar_datos(self):
        #Puebla las estructuras de datos con instancias iniciales de simulación.
        self.habitaciones["101"] = Habitacion("101", "Sencilla", 500)
        self.habitaciones["102"] = Habitacion("102", "Sencilla", 500)
        self.habitaciones["201"] = Habitacion("201", "Doble", 800)
        self.habitaciones["202"] = Habitacion("202", "Doble", 800)
        self.habitaciones["301"] = Habitacion("301", "Suite", 1500)
        self.huespedes["123"] = Huesped("Daniel Perez", "123")



# CAPA DE INTERFAZ GRÁFICA DE USUARIO (GUI)
class AppCRMHotel:
    #Clase principal de la UI. Construye el contenedor raíz, inicializa
    #los estilos de los componentes ttk y gestiona las ventanas modales.
    
    def __init__(self, root):
        self.hotel = Hotel() #Ingresa la lógica del hotel en la interfaz
        self.root = root
        self.root.title("CRM Hotelero - Premium Admin")
        self.root.geometry("850x600")
        self.root.configure(bg="#1e222b") # Aplicación de fondo a nivel contenedor raíz
        
        self.style = ttk.Style()
        self.style.theme_use("clam") # Activa el tema clam para permitir la personalización de colores
        
        # Ingresa propiedades CSS(parecidas) al componente de tablas
        self.style.configure("Treeview", 
                             background="#282c34", 
                             foreground="white", 
                             fieldbackground="#282c34", 
                             rowheight=28,
                             font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", 
                             background="#3e4451", 
                             foreground="white", 
                             font=("Segoe UI", 11, "bold"),
                             bordercolor="#1e222b")
        #Define el color de selección de filas
        self.style.map("Treeview", background=[('selected', '#4b5263')])

        # Construccion de header
        frame_header = tk.Frame(root, bg="#282c34", height=70)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False) # Evita que el frame colapse al tamaño de sus hijos
        
        lbl_titulo = tk.Label(frame_header, text="HOTEL CRM DASHBOARD", font=("Segoe UI", 16, "bold"), fg="#61afef", bg="#282c34")
        lbl_titulo.pack(side="left", padx=20, pady=15)
        
        # CONSTRUCCIÓN DE LA BARRA NAV LATERAL 
        frame_sidebar = tk.Frame(root, bg="#21252b", width=200)
        frame_sidebar.pack(fill="y", side="left")
        frame_sidebar.pack_propagate(False)
        
        # Diccionario de configuración empaquetado para homogeneizar los botones
        btn_props = {"font": ("Segoe UI", 10, "bold"), "fg": "#abb2bf", "bg": "#2c313c", 
                     "activebackground": "#61afef", "activeforeground": "#21252b", 
                     "bd": 0, "cursor": "hand2", "height": 2}
        
        # Enlace que invoca los métodos de ventanas secundarias
        tk.Button(frame_sidebar, text="Ver Disponibilidad", command=self.ventana_disponibilidad, **btn_props).pack(fill="x", padx=10, pady=10)
        tk.Button(frame_sidebar, text="Clientes y Huespedes", command=self.ventana_huespedes, **btn_props).pack(fill="x", padx=10, pady=10)
        tk.Button(frame_sidebar, text="Crear Reservacion", command=self.ventana_reservar, **btn_props).pack(fill="x", padx=10, pady=10)
        tk.Button(frame_sidebar, text="Check-In y Check-Out", command=self.ventana_CheckIn_CheckOut, **btn_props).pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame_sidebar, text="Salir del Sistema", bg="#e06c75", fg="white", font=("Segoe UI", 10, "bold"), bd=0, command=root.quit).pack(fill="x", side="bottom", padx=10, pady=20)

        # DASHBOARD con las funciones meras meras
        self.frame_main = tk.Frame(root, bg="#1e222b")
        self.frame_main.pack(fill="both", expand=True, side="right", padx=20, pady=20)
        
        lbl_resumen = tk.Label(self.frame_main, text="Estado en tiempo real de las habitaciones:", font=("Segoe UI", 12, "bold"), fg="white", bg="#1e222b")
        lbl_resumen.pack(anchor="w", pady=(0, 10))
        
        # La tabla principal del dashboard se actualiza dependiendo de lo que seleccione con el estado de las habitaciones. Se usa Treeview para la tabla y sus datos
        self.tabla_estado = ttk.Treeview(self.frame_main, columns=("Numero", "Tipo", "Precio", "Estado"), show="headings")
        self.tabla_estado.heading("Numero", text="No. Habitacion")
        self.tabla_estado.heading("Tipo", text="Tipo de Habitacion")
        self.tabla_estado.heading("Precio", text="Precio por Noche")
        self.tabla_estado.heading("Estado", text="Estado Actual")
        
        for col in ("Numero", "Tipo", "Precio", "Estado"):
            self.tabla_estado.column(col, anchor="center")
            
        self.tabla_estado.pack(fill="both", expand=True)
        self.actualizar_tabla_principal() # Carga inicial de datos en la cuadrícula

    def actualizar_tabla_principal(self):
        #Sincroniza la interfaz de ususario con el estado del objeto 'Hotel'.
        #Limpia el Treeview y renderiza los datos aplicando formato condicional(esto le pedi a la IA que me ayudara con los tags porque no lo vimos en clase).
        
        for item in self.tabla_estado.get_children():
            self.tabla_estado.delete(item) # Limpieza de regiustros para evitar duplicados
            
        for hab in self.hotel.habitaciones.values():
            tag = "dispo" if hab.estado == "Disponible" else "ocu"
            self.tabla_estado.insert("", "end", values=(hab.numero, hab.tipo, f"${hab.precio_noche}", hab.estado), tags=(tag,))
        
        #Cambia colores en dependencia del status de la habitacion 
        self.tabla_estado.tag_configure("dispo", foreground="#98c379") # Estado disponible -> Verde
        self.tabla_estado.tag_configure("ocu", foreground="#e06c75")   # Estado ocupado -> Rojo

    def configurar_subventana(self, titulo, dimensiones):
        #Aplica herencia visual y restringe el foco de eventos con grab_set().
        
        subwin = tk.Toplevel(self.root)
        subwin.title(titulo)
        subwin.geometry(dimensiones)
        subwin.configure(bg="#21252b")
        subwin.grab_set() # Se asegura de capturar solo un evento para evita clics si hay ventanas traseras abiertas.
        return subwin
    
    # MÓDULO VENTANA: DISPONIBILIDAD (READ-ONLY)

    def ventana_disponibilidad(self):
        subwin = self.configurar_subventana("Habitaciones Disponibles", "450x350")
        
        tk.Label(subwin, text="Habitaciones Disponibles", font=("Segoe UI", 13, "bold"), fg="#61afef", bg="#21252b").pack(pady=15)
        
        # Widget Text configurado temporalmente en modo lectura
        txt_dispo = tk.Text(subwin, width=50, height=10, bg="#282c34", fg="#abb2bf", font=("Consolas", 10), bd=0, padx=10, pady=10)
        txt_dispo.pack(pady=10)
        
        # Filtra las listas sobre el modelo de habitaciones
        disponibles = [h for h in self.hotel.habitaciones.values() if h.estado == "Disponible"]
        
        if not disponibles:
            txt_dispo.insert("end", "Aviso: No hay habitaciones disponibles en este momento.")
        else:
            for h in disponibles:
                txt_dispo.insert("end", f" Habicacion {h.numero} | {h.tipo:<10} | Tarifa: ${h.precio_noche}/noche\n")
        txt_dispo.config(state="disabled") #Esto bloquea que el ususario pueda editar el contenido del widget


    # MÓDULO VENTANA: GESTIÓN DE HUÉSPEDES 

    def ventana_huespedes(self):
        subwin = self.configurar_subventana("Gestion de Huespedes", "500x480")
        
        tk.Label(subwin, text="Registrar Nuevo Cliente", font=("Segoe UI", 12, "bold"), fg="#98c379", bg="#21252b").pack(pady=10)
        frame_reg = tk.Frame(subwin, bg="#21252b")
        frame_reg.pack(pady=5)
        
        lbl_style = {"bg": "#21252b", "fg": "#abb2bf", "font": ("Segoe UI", 10)}
        entry_style = {"bg": "#282c34", "fg": "white", "insertbackground": "white", "bd": 1, "relief": "flat"}
        
        tk.Label(frame_reg, text="ID / Pasaporte:", **lbl_style).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ent_id = tk.Entry(frame_reg, **entry_style, width=25)
        ent_id.grid(row=0, column=1, pady=5)
        
        tk.Label(frame_reg, text="Nombre Completo:", **lbl_style).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ent_nom = tk.Entry(frame_reg, **entry_style, width=25)
        ent_nom.grid(row=1, column=1, pady=5)
        
        def guardar_huesped():
            #Función interna que valida los datos ingresados
            id_h = ent_id.get().strip()
            nom_h = ent_nom.get().strip()
            
            # Validación de entradas nulas o vacías
            if not id_h or not nom_h:
                messagebox.showerror("Error", "Campos vacios.", parent=subwin)
                return
            # Validación para evitar duplicados de llaves y no haya dos huespedes con el mismo ID
            if id_h in self.hotel.huespedes:
                messagebox.showerror("Error", "Este ID ya existe.", parent=subwin)
                return
            
            # Instanciación y almacenamiento persistente en memoria
            self.hotel.huespedes[id_h] = Huesped(nom_h, id_h)
            messagebox.showinfo("Exito", "Huesped registrado perfectamente.", parent=subwin)
            ent_id.delete(0, "end")
            ent_nom.delete(0, "end")
            
        tk.Button(subwin, text="Guardar Cliente", bg="#98c379", fg="#21252b", font=("Segoe UI", 10, "bold"), bd=0, command=guardar_huesped, width=15).pack(pady=10)
        
        #Una linea de separacion coqueta pa que se vea bonito
        tk.Frame(subwin, bg="#3e4451", height=1).pack(fill="x", padx=20, pady=10)
        
        #Pequeno sistema de busqueda de Historial
        tk.Label(subwin, text="Buscar Historial de Cliente", font=("Segoe UI", 12, "bold"), fg="#61afef", bg="#21252b").pack(pady=5)
        frame_bus = tk.Frame(subwin, bg="#21252b")
        frame_bus.pack(pady=5)
        
        tk.Label(frame_bus, text="ID de Huesped:", **lbl_style).grid(row=0, column=0, padx=5)
        ent_buscar_id = tk.Entry(frame_bus, **entry_style, width=20)
        ent_buscar_id.grid(row=0, column=1, padx=5)
        
        txt_historial = tk.Text(subwin, width=55, height=6, bg="#282c34", fg="#abb2bf", font=("Consolas", 9), bd=0, padx=5, pady=5)
        txt_historial.pack(pady=10)
        
        def buscar_huesped():
            #Consulta los huéspedes mediante la llave de entrada.
            txt_historial.config(state="normal")
            txt_historial.delete("1.0", "end")
            id_b = ent_buscar_id.get().strip()
            
            if id_b in self.hotel.huespedes:
                hue = self.hotel.huespedes[id_b]
                # Lectura de la lista interna del objeto huésped para imprimir sus reservaciones previas
                txt_historial.insert("end", f"Cliente: {hue.nombre}\nID: {hue.id}\n")
                txt_historial.insert("end", "Historial de Reservas:\n")
                if not hue.historial_reservaciones:
                    txt_historial.insert("end", "   - Sin registros previos.\n")
                else:
                    for res in hue.historial_reservaciones:
                        txt_historial.insert("end", f"   - Habitacion {res.habitacion.numero} ({res.habitacion.tipo})\n")
            else:
                messagebox.showwarning("No encontrado", "El ID no esta registrado.", parent=subwin)
            txt_historial.config(state="disabled")
            
        tk.Button(subwin, text="Buscar", bg="#61afef", fg="#21252b", font=("Segoe UI", 10, "bold"), bd=0, command=buscar_huesped, width=12).pack()


    #LOGÍSITICA DE RESERVACIONES 

    def ventana_reservar(self):
        subwin = self.configurar_subventana("Nueva Reservacion", "480x380")
        
        tk.Label(subwin, text="Generar Reservacion", font=("Segoe UI", 13, "bold"), fg="#e5c07b", bg="#21252b").pack(pady=15)
        
        frame_res = tk.Frame(subwin, bg="#21252b")
        frame_res.pack(pady=5)
        
        lbl_style = {"bg": "#21252b", "fg": "#abb2bf", "font": ("Segoe UI", 10)}
        entry_style = {"bg": "#282c34", "fg": "white", "insertbackground": "white", "bd": 1, "relief": "flat"}
        
        tk.Label(frame_res, text="ID del Huesped:", **lbl_style).grid(row=0, column=0, sticky="e", pady=6, padx=5)
        ent_id = tk.Entry(frame_res, **entry_style, width=22)
        ent_id.grid(row=0, column=1, pady=6)
        
        tk.Label(frame_res, text="No. de Habitacion:", **lbl_style).grid(row=1, column=0, sticky="e", pady=6, padx=5)
        ent_hab = tk.Entry(frame_res, **entry_style, width=22)
        ent_hab.grid(row=1, column=1, pady=6)
        
        tk.Label(frame_res, text="Entrada (DD/MM/AAAA):", **lbl_style).grid(row=2, column=0, sticky="e", pady=6, padx=5)
        ent_entrada = tk.Entry(frame_res, **entry_style, width=22)
        ent_entrada.grid(row=2, column=1, pady=6)
        ent_entrada.insert(0, datetime.now().strftime("%d/%m/%Y")) # Inyección dinámica de fecha actual
        
        tk.Label(frame_res, text="Salida (DD/MM/AAAA):", **lbl_style).grid(row=3, column=0, sticky="e", pady=6, padx=5)
        ent_salida = tk.Entry(frame_res, **entry_style, width=22)
        ent_salida.grid(row=3, column=1, pady=6)
        
        def procesar_reserva():
            """Valida la integridad referencial de los ID y parsea las cadenas de fecha."""
            id_h = ent_id.get().strip()
            num_h = ent_hab.get().strip()
            f_ent_str = ent_entrada.get().strip()
            f_sal_str = ent_salida.get().strip()
            
            # Verificación de existencia en los diccionarios: 'huespedes' y 'habitaciones'
            if id_h not in self.hotel.huespedes or num_h not in self.hotel.habitaciones:
                messagebox.showerror("Error", "Huesped o Habitacion no encontrados.", parent=subwin)
                return
            
            hab = self.hotel.habitaciones[num_h]
            if hab.estado != "Disponible":
                messagebox.showerror("Error", "La habitacion esta ocupada.", parent=subwin)
                return
                
            try:
                # Análisis de tiempo 
                f_entrada = datetime.strptime(f_ent_str, "%d/%m/%Y")
                f_salida = datetime.strptime(f_sal_str, "%d/%m/%Y")
                if f_salida <= f_entrada:
                    messagebox.showerror("Error", "La salida debe ser posterior.", parent=subwin)
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha invalido (DD/MM/AAAA).", parent=subwin)
                return
            
            huesped = self.hotel.huespedes[id_h]
            
            # Creación del objeto de reservación 
            nueva_reserva = Reservacion(huesped, hab, f_entrada, f_salida)
            self.hotel.reservaciones.append(nueva_reserva)
            huesped.historial_reservaciones.append(nueva_reserva) # Vinculación 
            
            messagebox.showinfo("Exito", f"Reservacion procesada.\nTotal: ${nueva_reserva.calcular_costo_total()}", parent=subwin)
            subwin.destroy() # Libera los recursos de la subventana
            
        tk.Button(subwin, text="Confirmar Reservacion", bg="#e5c07b", fg="#21252b", font=("Segoe UI", 10, "bold"), bd=0, command=procesar_reserva).pack(pady=20)


    #CHECK-IN / CHECK-OUT (tambien facturazion)

    def ventana_CheckIn_CheckOut(self):
        subwin = self.configurar_subventana("Check-In / Check-Out", "500x420")
        
        lbl_style = {"bg": "#21252b", "fg": "#abb2bf", "font": ("Segoe UI", 10)}
        entry_style = {"bg": "#282c34", "fg": "white", "insertbackground": "white", "bd": 1, "relief": "flat"}

        # Sub-panel de Check-In (puede cambiar el estado a Ocupado)
        tk.Label(subwin, text="Check-In (Ingreso)", font=("Segoe UI", 12, "bold"), fg="#98c379", bg="#21252b").pack(pady=10)
        frame_ci = tk.Frame(subwin, bg="#21252b")
        frame_ci.pack()
        tk.Label(frame_ci, text="No. Habitacion:", **lbl_style).grid(row=0, column=0, padx=5)
        ent_hab_ci = tk.Entry(frame_ci, **entry_style, width=12)
        ent_hab_ci.grid(row=0, column=1)
        
        def hacer_checkin():
            num = ent_hab_ci.get().strip()
            if num in self.hotel.habitaciones and self.hotel.habitaciones[num].estado == "Disponible":
                self.hotel.habitaciones[num].estado = "Ocupada" # Cambio de estado directo en el objeto
                self.actualizar_tabla_principal()           
                messagebox.showinfo("Exito", f"Habitacion {num} marcada como Ocupada.", parent=subwin)
                ent_hab_ci.delete(0, "end")
            else:
                messagebox.showerror("Error", "Habitacion no disponible o no existe.", parent=subwin)
                
        tk.Button(subwin, text="Registrar Entrada", bg="#98c379", fg="#21252b", font=("Segoe UI", 9, "bold"), bd=0, command=hacer_checkin, width=18).pack(pady=5)
        
        tk.Frame(subwin, bg="#3e4451", height=1).pack(fill="x", padx=20, pady=15)
        
        # Sub-panel de Check-Out (Restablece el estado de habitacion a disponibles)
        tk.Label(subwin, text="Check-Out y Facturacion (Salida)", font=("Segoe UI", 12, "bold"), fg="#e06c75", bg="#21252b").pack(pady=5)
        frame_co = tk.Frame(subwin, bg="#21252b")
        frame_co.pack()
        tk.Label(frame_co, text="No. Habitacion:", **lbl_style).grid(row=0, column=0, padx=5)
        ent_hab_co = tk.Entry(frame_co, **entry_style, width=12)
        ent_hab_co.grid(row=0, column=1)
        
        def hacer_checkout():
            num = ent_hab_co.get().strip()
            if num in self.hotel.habitaciones and self.hotel.habitaciones[num].estado == "Ocupada":
                hab = self.hotel.habitaciones[num]
                
                # Búsqueda de reserva activa asociada a la habitación
                reserva_activa = next((r for r in self.hotel.reservaciones if r.habitacion.numero == num), None)
                
                hab.estado = "Disponible" # Mutación / Liberación del recurso
                self.actualizar_tabla_principal()
                
                if reserva_activa:
                    # Construccion de un ticket falso pero que da el pintazo
                    factura = (
                        f"FACTURA DIGITAL\n\n"
                        f"Cliente: {reserva_activa.huesped.nombre}\n"
                        f"ID: {reserva_activa.huesped.id}\n"
                        f"Habitacion: {hab.numero} ({hab.tipo})\n"
                        f"Total Cobrado: ${reserva_activa.calcular_costo_total()} MXN\n\n"
                        f"Check-Out completado con exito."
                    )
                else:
                    factura = f"Habitacion {num} liberada sin reserva previa.\nTarifa base: ${hab.precio_noche} MXN"
                
                messagebox.showinfo("Factura Generada", factura, parent=subwin)
                ent_hab_co.delete(0, "end")
            else:
                messagebox.showerror("Error", "La habitacion no esta ocupada o no existe.", parent=subwin)
                
        tk.Button(subwin, text="Generar Salida y Facturar", bg="#e06c75", fg="white", font=("Segoe UI", 9, "bold"), bd=0, command=hacer_checkout, width=22).pack(pady=5)



#  HILO PRINCIPAL DE EJECUCIÓN (ENTRY POINT)

if __name__ == "__main__":
    root = tk.Tk()              # Inicializa la instancia del despachador de ventanas de Tkinter
    app = AppCRMHotel(root)     # Carga e inicializa la lógica de nuestra clase UI
    root.mainloop()             # Arranca el bucle infinito de escucha y captura de eventos (Event Loop)