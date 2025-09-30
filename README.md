# Sistema de Facturación (Flask)

Aplicación web desarrollada en **Python** con **Flask** para la gestión básica de:

- Usuarios (registro e inicio de sesión)
- Clientes
- Productos
- Facturas y detalles de factura
- Reportes (resumen mensual y totales)

La interfaz utiliza plantillas **Jinja2** y la persistencia de datos se realiza mediante **SQLAlchemy** sobre una base de datos **MySQL**. Se emplea `python-dotenv` para la carga de variables de entorno y `Flask-SQLAlchemy` como capa ORM integrada.

---

## Estructura Simplificada del Proyecto

```
flask_app/
├─ README.md
├─ .env                    # Variable DATABASE_URL (opcional, también puedes exportarla)
├─ requirements.txt        # Dependencias
└─ src/
   ├─ app.py               # Punto de entrada de la aplicación
   ├─ data/
   │  ├─ models/           # Modelos: User, Client, Product, Invoice, InvoiceDetail
   │  └─ mysql_db/init.py  # Inicialización de SQLAlchemy
   ├─ presentation/
   │  ├─ auth/             # Rutas de autenticación (login, register, dashboard)
   │  ├─ client/           # Rutas CRUD de clientes
   │  ├─ product/          # Rutas CRUD de productos
   │  ├─ invoice/          # Rutas de facturación
   │  ├─ reports/          # Rutas de reportes / resumen
   │  └─ templates/        # Plantillas HTML Jinja2
   └─ domain/              # (Espacio para lógica de dominio / errores)
```

---

## Requisitos Previos

- Python 3.12+ (recomendado)
- MySQL en ejecución (el ejemplo usa puerto `3307`)
- Acceso para crear base de datos (ej: `flask_db`)

---

## Configuración de la Base de Datos

Asegúrate de tener creada la base de datos:

```sql
CREATE DATABASE flask_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Variable de Entorno `DATABASE_URL`

Formato general:

```
mysql+pymysql://USUARIO:CLAVE@HOST:PUERTO/NOMBRE_BD
```

Ejemplo usado en el proyecto:

```
mysql+pymysql://root:123456@localhost:3307/flask_db
```

Puedes definirla de la siguiente manera:
Archivo `.env` en la raíz del proyecto (ya soportado por `python-dotenv`):

```env
DATABASE_URL="mysql+pymysql://root:123456@localhost:3307/flask_db"
```

---

## Instalación y Ejecución

A continuación se muestran pasos recomendados. Todos los comandos asumen que estás en la carpeta raíz del proyecto (`flask_app`).

### 1. Crear y activar entorno virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

(Opcionalmente: `pip install -r src/requirements.txt` si decides mantener ese archivo como fuente principal.)

### 3. Configurar variable de entorno `DATABASE_URL`

Si no usas `.env` coloca (temporal para la sesión actual):

```powershell
$env:DATABASE_URL="mysql+pymysql://root:123456@localhost:3307/flask_db"
```

### 4. Ejecutar la aplicación

Opción directa con Python:

```powershell
python src/app.py
```

O usando Flask CLI (requiere apuntar a la app):

```powershell
$env:FLASK_APP="src/app.py"
flask run --debug
```

La aplicación quedará accesible típicamente en: http://127.0.0.1:5000 y redirige a `/login`.

### 5. Creación de tablas

El archivo `app.py` ya ejecuta `database.create_all()` dentro del contexto de la app, por lo que al primer arranque se crearán las tablas si no existen.

---

## Modelos Principales

- User: Autenticación y roles.
- Client: Información básica de clientes.
- Product: Catálogo de productos.
- Invoice & InvoiceDetail: Encabezado y detalle de facturas (cálculo de totales, fecha, etc.).

---

## Flujo Básico

1. Ingresar a `/login` y autenticar usuario existente (o registrar uno nuevo en `/register`).
2. Ir al panel `/home` para ver métricas (clientes, productos, facturas del mes, total facturado).
3. Crear clientes y productos.
4. Generar facturas y revisar detalles.
5. Consultar reportes.

---

## Solución de Problemas (Troubleshooting)

| Problema                | Posible Causa                               | Solución                                                 |
| ----------------------- | ------------------------------------------- | -------------------------------------------------------- |
| Error de conexión MySQL | Puerto incorrecto                           | Verifica puerto real de tu instancia (`3306` vs `3307`). |
| Tablas no se crean      | Variable `DATABASE_URL` no cargada          | Imprime `echo $env:DATABASE_URL` o revisa `.env`.        |
| Unicode/locale error    | Locale `es_ES.UTF-8` no disponible en tu SO | Cambia o comenta `locale.setlocale(...)` en `app.py`.    |
| Módulos no encontrados  | Entorno virtual no activo                   | Activa `.venv` antes de ejecutar.                        |

---

## Resumen Rápido

```powershell
# Clonar / Descargar
git clone https://github.com/SantiagoArteche/urquiza-invoice.git

# Crear entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variable entorno
crear archivo .env con la variable DATABASE_URL="mysql+pymysql://USUARIO:CONTRASEÑA@localhost:PUERTO/flask_db"

# Ejecutar
python src/app.py
```
