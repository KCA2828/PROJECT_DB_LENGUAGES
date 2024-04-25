import cx_Oracle
import tkinter as tk
from tkinter import messagebox, ttk
import datetime

def init_oracle_client():
    try:
        cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient\instantclient_19_22",
                                     config_dir=r"C:\instantclient\instantclient_19_22\network\admin")
        print("Oracle Client inicializado.")
    except Exception as ex:
        messagebox.showerror("Error al inicializar el cliente Oracle", str(ex))

def conectar_db():
    try:
        connection = cx_Oracle.connect(
            user='PROYECTO',
            password='123',
            dsn='192.168.18.92:1521/ORCL',
            encoding='UTF-8'
        )
        print("Transacción completada con la base de datos de Oracle.")
        return connection
    except Exception as ex:
        messagebox.showerror("Error de conexión", str(ex))
        return None

#CRUD TABLA PROVEEDORES
def gestion_proveedores():
    proveedor_window = tk.Toplevel()
    proveedor_window.title("Gestión de Proveedores")
    proveedor_window.geometry("400x300")

    tk.Button(proveedor_window, text="Crear Proveedor", command=crear_proveedor).pack(pady=10)
    tk.Button(proveedor_window, text="Leer y Actualizar Proveedores", command=leer_proveedores).pack(pady=10)
    tk.Button(proveedor_window, text="Eliminar Proveedor", command=eliminar_proveedor).pack(pady=10)

def leer_proveedores():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Proveedores")
    leer_window.geometry("600x400")

    columns = ("ID", "Nombre", "Dirección", "Correo", "Teléfono")
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_PROVEEDORES")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_actualizacion():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un proveedor para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Proveedor", command=seleccion_de_actualizacion)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Proveedor")
    labels = ["ID", "Nombre", "Dirección", "Correo", "Teléfono"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=f"{label}:").grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.grid(row=i, column=1)
        entry.insert(0, valores[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        proveedor_id = nuevos_datos[0]  # ID es el primer elemento
        try:
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                cursor.callproc("ProveedorPkg.ActualizarProveedor", [proveedor_id] + nuevos_datos[1:])
                connection.commit()
                actualizar_window.destroy()
                messagebox.showinfo("Éxito", "Proveedor actualizado exitosamente.")
                cursor.close()
                connection.close()
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {ex}")

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

def crear_proveedor():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Proveedor")
    labels = ["ID", "Nombre", "Dirección", "Correo", "Teléfono"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=f"{label}:").grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_proveedor():
        try:
            datos = [entry.get() for entry in entries]
            if any(not d for d in datos):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                cursor.callproc("ProveedorPkg.CrearProveedor", datos)
                connection.commit()
                crear_window.destroy()
                messagebox.showinfo("Éxito", "Proveedor creado exitosamente.")
                cursor.close()
                connection.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error al crear el proveedor: {ex}")

    save_btn = tk.Button(crear_window, text="Guardar", command=guardar_proveedor)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

def eliminar_proveedor():
    eliminar_window = tk.Toplevel()
    eliminar_window.title("Eliminar Proveedor")
    tk.Label(eliminar_window, text="ID del Proveedor:").grid(row=0, column=0)
    id_entry = tk.Entry(eliminar_window)
    id_entry.grid(row=0, column=1)

    def confirmar_eliminacion():
        proveedor_id = id_entry.get()
        try:
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                cursor.callproc("ProveedorPkg.EliminarProveedor", [proveedor_id])
                connection.commit()
                eliminar_window.destroy()
                messagebox.showinfo("Éxito", "Proveedor eliminado exitosamente.")
                cursor.close()
                connection.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error al eliminar el proveedor: {ex}")

    delete_btn = tk.Button(eliminar_window, text="Eliminar", command=confirmar_eliminacion)
    delete_btn.grid(row=1, columnspan=2, pady=10)

#CRUD TABLA CLIENTE
def gestion_clientes():
    cliente_window = tk.Toplevel()
    cliente_window.title("Gestión de Clientes")
    cliente_window.geometry("400x300")

    tk.Button(cliente_window, text="Crear Cliente", command=crear_cliente).pack(pady=10)
    tk.Button(cliente_window, text="Ver y Actualizar Clientes", command=leer_actualizar_clientes).pack(pady=10)
    tk.Button(cliente_window, text="Eliminar Cliente", command=lambda: eliminar_generico('Cliente')).pack(pady=10)

def crear_cliente():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Cliente")
    labels = ["ID Cliente", "Nombre", "Apellido", "Dirección", "Correo", "Teléfono"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cliente():
        datos = [entry.get() for entry in entries]
        if any(not d for d in datos):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            # Asumiendo que existe un procedimiento almacenado para crear clientes
            cursor.callproc("ClientePkg.CrearCliente", datos)
            connection.commit()
            messagebox.showinfo("Éxito", "Cliente creado exitosamente.")
            cursor.close()
            connection.close()
            crear_window.destroy()
        else:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")

    tk.Button(crear_window, text="Guardar Cliente", command=guardar_cliente).grid(row=len(labels), pady=10)

def leer_actualizar_clientes():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Clientes")
    leer_window.geometry("1280x720")

    columns = ("ID", "Nombre", "Apellido", "Dirección", "Correo", "Teléfono")
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_CLIENTES")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_cliente():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_cliente(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un cliente para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Cliente", command=seleccion_de_fila_cliente)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_cliente(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Cliente")
    labels = ["ID", "Nombre", "Apellido", "Dirección", "Correo", "Teléfono"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.grid(row=i, column=1)
        entry.insert(0, valores[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        try:
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                cursor.callproc("ClientePkg.ActualizarCliente", [valores[0]] + nuevos_datos[1:])
                connection.commit()
                messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
                actualizar_window.destroy()
                cursor.close()
                connection.close()
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {ex}")

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA COMPRA
def gestion_compras():
    compra_window = tk.Toplevel()
    compra_window.title("Gestión de Compras")
    compra_window.geometry("400x300")

    tk.Button(compra_window, text="Crear Compra", command=crear_compra).pack(pady=10)
    tk.Button(compra_window, text="Ver y Actualizar Compras", command=leer_actualizar_compras).pack(pady=10)
    tk.Button(compra_window, text="Eliminar Compra", command=lambda: eliminar_generico('Compra')).pack(pady=10)

def crear_compra():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Compra")
    labels = ["ID Compra", "Fecha (YYYY-MM-DD)", "Ganancia", "ID Cliente", "ID Producto"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_compra():
        datos = [entry.get() for entry in entries]
        if any(not d for d in datos):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Asumiendo que la fecha se proporciona en formato correcto y se valida en el cliente
        datos[1] = datetime.datetime.strptime(datos[1], '%Y-%m-%d').date()

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("CompraPkg.CrearCompra", datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Compra creada exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear la compra: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Compra", command=guardar_compra).grid(row=len(labels), pady=10)

def leer_actualizar_compras():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Compras")
    leer_window.geometry("1280x720")

    columns = ["ID Compra", "Fecha", "Ganancia", "ID Cliente", "ID Producto"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM V_COMPRAS")
            for row in cursor:
                # Asegurarse de que las fechas se manejen correctamente
                formatted_row = list(row)
                formatted_row[1] = row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'
                tree.insert("", "end", values=formatted_row)
        finally:
            cursor.close()
            connection.close()

    def seleccion_de_fila_compra():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_compra(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione una compra para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Compra", command=seleccion_de_fila_compra)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_compra(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Compra")
    labels = ["ID Compra", "Fecha (YYYY-MM-DD)", "Ganancia", "ID Cliente", "ID Producto"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.grid(row=i, column=1)
        # Insertar valores existentes en los campos
        entry.insert(0, valores[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        try:
            nuevos_datos[1] = datetime.datetime.strptime(nuevos_datos[1], '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error de formato de fecha", "La fecha debe estar en formato YYYY-MM-DD")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("CompraPkg.ActualizarCompra", [int(valores[0])] + nuevos_datos[1:])
                connection.commit()
                messagebox.showinfo("Éxito", "Compra actualizada exitosamente.")
                actualizar_window.destroy()
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=6, columnspan=2, pady=10)

#CRUD TABLA DEPARTAMENTO
def gestion_departamentos():
    departamento_window = tk.Toplevel()
    departamento_window.title("Gestión de Departamentos")
    departamento_window.geometry("400x300")

    tk.Button(departamento_window, text="Crear Departamento", command=crear_departamento).pack(pady=10)
    tk.Button(departamento_window, text="Ver y Actualizar Departamentos", command=leer_actualizar_departamentos).pack(pady=10)
    tk.Button(departamento_window, text="Eliminar Departamento", command=lambda: eliminar_generico('Departamento')).pack(pady=10)

def crear_departamento():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Departamento")
    labels = ["ID Departamento", "Nombre del Departamento"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_departamento():
        id_departamento, nombre = entries[0].get(), entries[1].get()
        if not (id_departamento and nombre):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("DepartamentoPkg.CrearDepartamento", [id_departamento, nombre])
                connection.commit()
                messagebox.showinfo("Éxito", "Departamento creado exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear el departamento: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Departamento", command=guardar_departamento).grid(row=len(labels), pady=10)

def leer_actualizar_departamentos():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Departamentos")
    leer_window.geometry("600x400")

    columns = ["ID", "Nombre"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_DEPARTAMENTOS")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_departamento():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_departamento(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un departamento para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Departamento", command=seleccion_de_fila_departamento)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_departamento(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Departamento")
    labels = ["ID", "Nombre"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        connection = None
        cursor = None
        try:
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                cursor.callproc("DepartamentoPkg.ActualizarDepartamento", nuevos_datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Departamento actualizado exitosamente.")
                actualizar_window.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo actualizar el departamento: {ex}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA EMPLEADO
def gestion_empleados():
    empleado_window = tk.Toplevel()
    empleado_window.title("Gestión de Empleados")
    empleado_window.geometry("400x300")

    tk.Button(empleado_window, text="Crear Empleado", command=crear_empleado).pack(pady=10)
    tk.Button(empleado_window, text="Ver y Actualizar Empleados", command=leer_actualizar_empleados).pack(pady=10)
    tk.Button(empleado_window, text="Eliminar Empleado", command=lambda: eliminar_generico('Empleado')).pack(pady=10)

def crear_empleado():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Empleado")
    labels = ["ID Empleado", "Nombre", "Apellido", "Puesto", "Salario", "Fecha de Contratación (YYYY-MM-DD)", "ID Departamento"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_empleado():
        datos = [entry.get() for entry in entries]
        if any(not d for d in datos):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Convertir la fecha de contratación de string a formato de fecha Oracle
        try:
            datos[5] = datetime.datetime.strptime(datos[5], '%Y-%m-%d').date()  # Convirtiendo la fecha
        except ValueError:
            messagebox.showerror("Error de formato de fecha", "La fecha debe estar en formato YYYY-MM-DD")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("EmpleadoPkg.CrearEmpleado", datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Empleado creado exitosamente.")
                crear_window.destroy()
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                messagebox.showerror("Error de base de datos", error.message)
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")

    tk.Button(crear_window, text="Guardar Empleado", command=guardar_empleado).grid(row=len(labels), pady=10)
    
def leer_actualizar_empleados():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Empleados")
    leer_window.geometry("1280x720")

    # Definir las columnas para el Treeview
    columns = ["ID", "Nombre", "Apellido", "Puesto", "Salario", "Fecha de Contratación", "ID Departamento"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Conectar a la base de datos y cargar los datos
    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM V_EMPLEADOS")
            for row in cursor:
                tree.insert("", "end", values=row)
        except Exception as ex:
            messagebox.showerror("Error al cargar datos", str(ex))
        finally:
            cursor.close()
            connection.close()

    def seleccion_de_fila_empleados():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_empleado(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un empleado para actualizar.")

    # Botón para actualizar empleado
    update_btn = tk.Button(leer_window, text="Actualizar Empleado", command=seleccion_de_fila_empleados)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_empleado(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Empleado")
    labels = ["ID", "Nombre", "Apellido", "Puesto", "Salario", "Fecha de Contratación", "ID Departamento"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=f"{label}:").grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.grid(row=i, column=1)
        entry.insert(0, valores[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        # Convertir fecha de contratación a formato de fecha de Python antes de enviar a la DB
        nuevos_datos[5] = datetime.datetime.strptime(nuevos_datos[5], '%Y-%m-%d').date()
        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("EmpleadoPkg.ActualizarEmpleado", [valores[0]] + nuevos_datos[1:])
                connection.commit()
                messagebox.showinfo("Éxito", "Empleado actualizado exitosamente.")
                actualizar_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"No se pudo actualizar el empleado: {ex}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA INGREDIENTE
def gestion_ingredientes():
    ingrediente_window = tk.Toplevel()
    ingrediente_window.title("Gestión de Ingredientes")
    ingrediente_window.geometry("400x300")

    tk.Button(ingrediente_window, text="Crear Ingrediente", command=crear_ingrediente).pack(pady=10)
    tk.Button(ingrediente_window, text="Ver y Actualizar Ingredientes", command=leer_actualizar_ingredientes).pack(pady=10)
    tk.Button(ingrediente_window, text="Eliminar Ingrediente", command=lambda: eliminar_generico('Ingrediente')).pack(pady=10)

def crear_ingrediente():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Ingrediente")
    labels = ["ID Ingrediente", "Nombre", "Cantidad", "Precio Unitario", "ID Proveedor"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_ingrediente():
        datos = [entry.get() for entry in entries]
        if any(not d for d in datos):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Asumiendo que el procedimiento almacenado acepta un ID de ingrediente
                cursor.callproc("IngredientePkg.CrearIngrediente", datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Ingrediente creado exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear el ingrediente: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Ingrediente", command=guardar_ingrediente).grid(row=len(labels), pady=10)

def leer_actualizar_ingredientes():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Ingredientes")
    leer_window.geometry("1280x720")

    columns = ["ID", "Nombre", "Cantidad", "Precio Unitario", "ID Proveedor"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_INGREDIENTES")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_ingrediente():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_ingrediente(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un ingrediente para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Ingrediente", command=seleccion_de_fila_ingrediente)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_ingrediente(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Ingrediente")
    labels = ["ID", "Nombre", "Cantidad", "Precio Unitario", "ID Proveedor"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.grid(row=i, column=1)
        entry.insert(0, valores[i])
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("IngredientePkg.ActualizarIngrediente", [valores[0]] + nuevos_datos[1:])
                connection.commit()
                messagebox.showinfo("Éxito", "Ingrediente actualizado exitosamente.")
                actualizar_window.destroy()
            finally:
                cursor.close()
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA INGREDIENTE_RECETA
def gestion_ingrediente_receta():
    ingrediente_window = tk.Toplevel()
    ingrediente_window.title("Gestión de Ingrediente Receta")
    ingrediente_window.geometry("400x300")

    tk.Button(ingrediente_window, text="Crear Ingrediente Receta", command=crear_ingrediente_receta).pack(pady=10)
    tk.Button(ingrediente_window, text="Ver y Actualizar Ingrediente Receta", command=leer_actualizar_ingredientes_recetas).pack(pady=10)
    tk.Button(ingrediente_window, text="Eliminar Asociación Ingrediente-Receta", command=eliminar_ingrediente_receta).pack(pady=10)

def crear_ingrediente_receta():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Asociación Ingrediente-Receta")
    labels = ["ID Ingrediente", "ID Receta", "Cantidad"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_asociacion():
        id_receta, id_ingrediente, cantidad = [entry.get() for entry in entries]
        if not (id_receta and id_ingrediente and cantidad.isdigit() and int(cantidad) > 0):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y la cantidad debe ser mayor que cero.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("IngredienteRecetaPkg.CrearIngredienteReceta", [id_receta, id_ingrediente, cantidad])
                connection.commit()
                messagebox.showinfo("Éxito", "Asociación Ingrediente-Receta creada exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear la asociación: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Asociación", command=guardar_asociacion).grid(row=len(labels), pady=10)

def leer_actualizar_ingredientes_recetas():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Asociaciones Ingredientes-Recetas")
    leer_window.geometry("600x400")

    columns = ["ID Receta", "ID Ingrediente", "Cantidad"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_INGREDIENTES_RECETAS")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_fila():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_ingrediente_receta(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione una asociación para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Asociación", command=seleccion_de_fila)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_ingrediente_receta(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Asociación Ingrediente-Receta")
    labels = ["ID Receta", "ID Ingrediente", "Cantidad"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        if not nuevos_datos[2].isdigit() or int(nuevos_datos[2]) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return
        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("IngredienteRecetaPkg.ActualizarIngredienteReceta", nuevos_datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Asociación Ingrediente-Receta actualizada exitosamente.")
                actualizar_window.destroy()
            finally:
                cursor.close()
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

def eliminar_ingrediente_receta():
    eliminar_window = tk.Toplevel()
    eliminar_window.title("Eliminar Asociación Ingrediente-Receta")
    tk.Label(eliminar_window, text="ID Receta:").grid(row=0, column=0)
    id_receta_entry = tk.Entry(eliminar_window)
    id_receta_entry.grid(row=0, column=1)

    tk.Label(eliminar_window, text="ID Ingrediente:").grid(row=1, column=0)
    id_ingrediente_entry = tk.Entry(eliminar_window)
    id_ingrediente_entry.grid(row=1, column=1)

    def confirmar_eliminacion():
        id_receta = id_receta_entry.get()
        id_ingrediente = id_ingrediente_entry.get()
        if not (id_receta and id_ingrediente):
            messagebox.showwarning("Advertencia", "Ambos IDs son obligatorios para eliminar.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("IngredienteRecetaPkg.EliminarIngredienteReceta", [id_receta, id_ingrediente])
                connection.commit()
                messagebox.showinfo("Éxito", "Asociación Ingrediente-Receta eliminada exitosamente.")
                eliminar_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al eliminar la asociación: {ex}")
            finally:
                cursor.close()
                connection.close()

    delete_btn = tk.Button(eliminar_window, text="Eliminar Asociación", command=confirmar_eliminacion)
    delete_btn.grid(row=2, columnspan=2, pady=10)

#CRUD TABLA ORDENES
def gestion_ordenes():
    orden_window = tk.Toplevel()
    orden_window.title("Gestión de Órdenes")
    orden_window.geometry("400x300")

    tk.Button(orden_window, text="Crear Orden", command=crear_orden).pack(pady=10)
    tk.Button(orden_window, text="Ver y Actualizar Órdenes", command=leer_actualizar_ordenes).pack(pady=10)
    tk.Button(orden_window, text="Eliminar Orden", command=lambda: eliminar_generico('Orden')).pack(pady=10)

def crear_orden():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Orden")
    labels = ["ID Orden", "Fecha de la Orden (YYYY-MM-DD)", "Estado de la Orden", "ID Cliente", "ID Producto"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_orden():
        id_orden, fecha, estado, id_cliente, id_producto = [entry.get() for entry in entries]
        try:
            fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showwarning("Error de formato", "La fecha debe estar en el formato YYYY-MM-DD.")
            return

        if not (id_orden and fecha and estado and id_cliente and id_producto):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("OrdenPkg.CrearOrden", [id_orden, fecha, estado, id_cliente, id_producto])
                connection.commit()
                messagebox.showinfo("Éxito", "Orden creada exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear la orden: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Orden", command=guardar_orden).grid(row=len(labels), pady=10)

def leer_actualizar_ordenes():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Órdenes")
    leer_window.geometry("600x400")

    columns = ["ID Orden", "Fecha", "Estado", "ID Cliente", "ID Producto"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ORDEN")
        for row in cursor:
            formatted_row = list(row)
            formatted_row[1] = row[1].strftime('%Y-%m-%d') if row[1] else 'N/A'
            tree.insert("", "end", values=formatted_row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_orden():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_orden(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione una orden para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Orden", command=seleccion_de_fila_orden)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_orden(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Orden")
    labels = ["ID Orden", "Fecha (YYYY-MM-DD)", "Estado", "ID Cliente", "ID Producto"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        try:
            nuevos_datos[1] = datetime.datetime.strptime(nuevos_datos[1], '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error de formato de fecha", "La fecha debe estar en formato YYYY-MM-DD")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("OrdenPkg.ActualizarOrden", nuevos_datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Orden actualizada exitosamente.")
                actualizar_window.destroy()
            finally:
                cursor.close()
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA RECETA
def gestion_recetas():
    receta_window = tk.Toplevel()
    receta_window.title("Gestión de Recetas")
    receta_window.geometry("400x300")

    tk.Button(receta_window, text="Crear Receta", command=crear_receta).pack(pady=10)
    tk.Button(receta_window, text="Ver y Actualizar Recetas", command=leer_actualizar_recetas).pack(pady=10)
    tk.Button(receta_window, text="Eliminar Receta", command=lambda: eliminar_generico('Receta')).pack(pady=10)

def crear_receta():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Receta")
    tk.Label(crear_window, text="ID Receta:").grid(row=0, column=0)
    id_entry = tk.Entry(crear_window)
    id_entry.grid(row=0, column=1)

    tk.Label(crear_window, text="Nombre de la Receta:").grid(row=1, column=0)
    nombre_entry = tk.Entry(crear_window)
    nombre_entry.grid(row=1, column=1)

    def guardar_receta():
        id_receta = id_entry.get()
        nombre_receta = nombre_entry.get()
        if not (id_receta and nombre_receta):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("RecetaPkg.CrearReceta", [id_receta, nombre_receta])
                connection.commit()
                messagebox.showinfo("Éxito", "Receta creada exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear la receta: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Receta", command=guardar_receta).grid(row=2, columnspan=2, pady=10)

def leer_actualizar_recetas():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Recetas")
    leer_window.geometry("600x400")

    columns = ["ID Receta", "Nombre de la Receta"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_RECETAS")
        for row in cursor:
            tree.insert("", "end", values=row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_receta():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_receta(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione una receta para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Receta", command=seleccion_de_fila_receta)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_receta(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Receta")
    labels = ["ID Receta", "Nombre de la Receta"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cambios():
        id_receta, nombre_receta = entries[0].get(), entries[1].get()
        if not (id_receta and nombre_receta):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("RecetaPkg.ActualizarReceta", [id_receta, nombre_receta])
                connection.commit()
                messagebox.showinfo("Éxito", "Receta actualizada exitosamente.")
                actualizar_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"No se pudo actualizar la receta: {ex}")
            finally:
                cursor.close()
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#CRUD TABLA PRODUCTO
def gestion_productos():
    receta_window = tk.Toplevel()
    receta_window.title("Gestión de Productos")
    receta_window.geometry("400x300")

    tk.Button(receta_window, text="Crear Producto", command=crear_productos).pack(pady=10)
    tk.Button(receta_window, text="Ver y Actualizar Producto", command=leer_actualizar_productos).pack(pady=10)
    tk.Button(receta_window, text="Eliminar Producto", command=lambda: eliminar_generico('Producto')).pack(pady=10)

def crear_productos():
    crear_window = tk.Toplevel()
    crear_window.title("Crear Producto")
    labels = ["ID Producto", "Nombre", "Precio", "Cantidad", "Fecha de Vencimiento (YYYY-MM-DD)"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(crear_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(crear_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_producto():
        id_producto, nombre, precio, cantidad, fecha_vencimiento = [entry.get() for entry in entries]
        try:
            fecha_vencimiento = datetime.datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showwarning("Error de formato", "La fecha debe estar en el formato YYYY-MM-DD.")
            return

        if not (id_producto and nombre and precio and cantidad and fecha_vencimiento):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("ProductoPkg.CrearProducto", [id_producto, nombre, precio, cantidad, fecha_vencimiento])
                connection.commit()
                messagebox.showinfo("Éxito", "Producto creado exitosamente.")
                crear_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error al crear el producto: {ex}")
            finally:
                cursor.close()
                connection.close()

    tk.Button(crear_window, text="Guardar Producto", command=guardar_producto).grid(row=len(labels), pady=10)

def leer_actualizar_productos():
    leer_window = tk.Toplevel()
    leer_window.title("Listado de Productos")
    leer_window.geometry("600x400")

    columns = ["ID Producto", "Nombre", "Precio", "Cantidad", "Fecha de Vencimiento"]
    tree = ttk.Treeview(leer_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar = tk.Scrollbar(leer_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V_PRODUCTOS")
        for row in cursor:
            formatted_row = list(row)
            formatted_row[4] = row[4].strftime('%Y-%m-%d') if row[4] else 'N/A'  # Formato de fecha
            tree.insert("", "end", values=formatted_row)
        cursor.close()
        connection.close()

    def seleccion_de_fila_producto():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            abrir_ventana_actualizacion_producto(item_values)
        else:
            messagebox.showinfo("Información", "Seleccione un producto para actualizar.")

    update_btn = tk.Button(leer_window, text="Actualizar Producto", command=seleccion_de_fila_producto)
    update_btn.grid(row=1, column=0, sticky='ew', pady=10)

def abrir_ventana_actualizacion_producto(valores):
    actualizar_window = tk.Toplevel()
    actualizar_window.title("Actualizar Producto")
    labels = ["ID Producto", "Nombre", "Precio", "Cantidad", "Fecha de Vencimiento (YYYY-MM-DD)"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(actualizar_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(actualizar_window)
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def guardar_cambios():
        nuevos_datos = [entry.get() for entry in entries]
        try:
            nuevos_datos[4] = datetime.datetime.strptime(nuevos_datos[4], '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error de formato de fecha", "La fecha debe estar en formato YYYY-MM-DD")
            return

        connection = conectar_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.callproc("ProductoPkg.ActualizarProducto", nuevos_datos)
                connection.commit()
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
                actualizar_window.destroy()
            finally:
                cursor.close()
                connection.close()

    save_btn = tk.Button(actualizar_window, text="Guardar Cambios", command=guardar_cambios)
    save_btn.grid(row=len(labels), columnspan=2, pady=10)

#FUNCION DE ELIMINACION PARA TODAS LAS TABLAS
def eliminar_generico(tipo):
    # Esta función puede ser utilizada para eliminar cualquier tipo de entidad, asumiendo que todos
    # tienen un campo ID único que puede ser especificado
    eliminar_window = tk.Toplevel()
    eliminar_window.title(f"Eliminar {tipo}")
    tk.Label(eliminar_window, text=f"ID del {tipo}:").grid(row=0, column=0)
    id_entry = tk.Entry(eliminar_window)
    id_entry.grid(row=0, column=1)

    def confirmar_eliminacion():
        identificador = id_entry.get()
        try:
            connection = conectar_db()
            if connection:
                cursor = connection.cursor()
                # Llamada genérica asumiendo un procedimiento almacenado de eliminación
                cursor.callproc(f"{tipo}Pkg.Eliminar{tipo}", [identificador])
                connection.commit()
                messagebox.showinfo("Éxito", f"{tipo} eliminado exitosamente.")
                cursor.close()
                connection.close()
                eliminar_window.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo eliminar el {tipo}: {ex}")

    tk.Button(eliminar_window, text="Eliminar", command=confirmar_eliminacion).grid(row=1, pady=10)

#FUNCIONES PARA USAR LA FUNCIONES DE LA BASE DE DATOS

def calcular_ganancias_totales_productos():
    connection = conectar_db()
    if connection is not None:
        try:
            cursor = connection.cursor()
            result = cursor.callfunc("calcular_ganancias_totales_productos", cx_Oracle.NUMBER)
            messagebox.showinfo("Total Ganancias", f"Las ganancias totales son: {result}")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo calcular las ganancias totales: {ex}")
        finally:
            cursor.close()
            connection.close()

def calcular_total_ventas_mes_anio1():
    connection = conectar_db()
    if connection is not None:
        try:
            cursor = connection.cursor()
            # Llamada a la función en la base de datos
            mes = 1  # Aquí deberías establecer el mes para el cual deseas calcular el total de ventas
            anio = 2024  # Aquí deberías establecer el año para el cual deseas calcular el total de ventas
            result = cursor.callfunc("calcular_total_ventas_mes_anio1", cx_Oracle.NUMBER, (mes, anio))
            messagebox.showinfo("Total Ventas", f"El total de ventas para el mes {mes} del año {anio} es: {result}")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo calcular el total de ventas para el mes {mes} del año {anio}: {ex}")
        finally:
            cursor.close()
            connection.close()

def main_window():
    root = tk.Tk()
    root.title("Sistema de Gestión - Andorias Cake")
    root.geometry("1280x720")

    tk.Label(root, text="Gestión de Datos", font=('Helvetica', 14, 'bold')).pack(pady=20)

    # Botones para cada CRUD
    tk.Button(root, text="Gestión de Proveedores", command=gestion_proveedores).pack(pady=5)
    tk.Button(root, text="Gestión de Clientes", command=gestion_clientes).pack(pady=5)
    tk.Button(root, text="Gestión de Compras", command=gestion_compras).pack(pady=5)
    tk.Button(root, text="Gestión de Departamentos", command=gestion_departamentos).pack(pady=5)
    tk.Button(root, text="Gestión de Empleados", command=gestion_empleados).pack(pady=5)
    tk.Button(root, text="Gestión de Ingredientes", command=gestion_ingredientes).pack(pady=5)
    tk.Button(root, text="Gestión de Ingredientes en Recetas", command=gestion_ingrediente_receta).pack(pady=5)
    tk.Button(root, text="Gestión de Órdenes", command=gestion_ordenes).pack(pady=5)
    tk.Button(root, text="Gestión de Recetas", command=gestion_recetas).pack(pady=5)
    tk.Button(root, text="Gestión de Productos", command=gestion_productos).pack(pady=5)


    # Botones para funciones
    tk.Label(root, text="Funciones", font=('Helvetica', 14, 'bold')).pack(pady=20)

    btn_calcular_ganancias_totales_productos = tk.Button(root, text="Calcular ganancias totales de los productos", command=calcular_ganancias_totales_productos)
    btn_calcular_ganancias_totales_productos.pack(pady=5)

    # btn_calcular_total_ingredientes_receta1 = tk.Button(root, text="Calcular Total Ingredientes Por Receta", command=calcular_total_ingredientes_receta1)
    # btn_calcular_total_ingredientes_receta1.pack(pady=5)

    btn_calcular_total_ventas_mes_anio1 = tk.Button(root, text="Calcular total ventas por mes y año", command=calcular_total_ventas_mes_anio1)
    btn_calcular_total_ventas_mes_anio1.pack(pady=5)

    # btn_CONSULTAR_INGREDIENTES = tk.Button(root, text="CONSULTAR INGREDIENTES", command=CONSULTAR_INGREDIENTES)
    # btn_CONSULTAR_INGREDIENTES.pack(pady=5)

    # btn_CONTAR_VENTAS_POR_PRODUCTO = tk.Button(root, text="CONTAR VENTAS POR PRODUCTO", command=CONTAR_VENTAS_POR_PRODUCTO)
    # btn_CONTAR_VENTAS_POR_PRODUCTO.pack(pady=5)

    # btn_LISTAR_PRODUCTOS_BAJO_STOCK = tk.Button(root, text="LISTAR PRODUCTOS BAJO STOCK", command=LISTAR_PRODUCTOS_BAJO_STOCK)
    # btn_LISTAR_PRODUCTOS_BAJO_STOCK.pack(pady=5)

    # btn_MOSTRAR_EMPLEADOS_POR_DEPARTAMENTO = tk.Button(root, text="MOSTRAR EMPLEADOS POR DEPARTAMENTO", command=MOSTRAR_EMPLEADOS_POR_DEPARTAMENTO)
    # btn_MOSTRAR_EMPLEADOS_POR_DEPARTAMENTO.pack(pady=5)

    # btn_MOSTRAR_ORDEN_POR_CLIENTE = tk.Button(root, text="MOSTRAR ORDEN POR CLIENTE", command=MOSTRAR_ORDEN_POR_CLIENTE)
    # btn_MOSTRAR_ORDEN_POR_CLIENTE.pack(pady=5)

    # btn_NUMERO_TOTAL_COMPRAS_POR_CLIENTE = tk.Button(root, text="NUMERO TOTAL COMPRAS POR CLIENTE", command=NUMERO_TOTAL_COMPRAS_POR_CLIENTE)
    # btn_NUMERO_TOTAL_COMPRAS_POR_CLIENTE.pack(pady=5)

    # btn_obtener_clientes_mas_3_compras1 = tk.Button(root, text="obtener clientes con mas de 3 compras", command=obtener_clientes_mas_3_compras1)
    # btn_obtener_clientes_mas_3_compras1.pack(pady=5)

    # btn_OBTENER_COMPRAS_POR_FECHA = tk.Button(root, text="OBTENER COMPRAS POR FECHA", command=OBTENER_COMPRAS_POR_FECHA)
    # btn_OBTENER_COMPRAS_POR_FECHA.pack(pady=5)

    # btn_OBTENER_EMPLEADO_POR_NOMBRE = tk.Button(root, text="OBTENER EMPLEADO POR NOMBRE", command=OBTENER_EMPLEADO_POR_NOMBRE)
    # btn_OBTENER_EMPLEADO_POR_NOMBRE.pack(pady=5)

    # btn_obtener_ordenes_pendientes1 = tk.Button(root, text="obtener ordenes pendientes", command=obtener_ordenes_pendientes)
    # btn_obtener_ordenes_pendientes1.pack(pady=5)

    # btn_obtener_productos_por_proveedor = tk.Button(root, text="obtener productos por proveedor", command=obtener_productos_por_proveedor)
    # btn_obtener_productos_por_proveedor.pack(pady=5)

    # btn_obtener_recetas_con_ingredientes1 = tk.Button(root, text="obtener recetas con ingredientes", command=obtener_recetas_con_ingredientes)
    # btn_obtener_recetas_con_ingredientes1.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    init_oracle_client()
    main_window()
