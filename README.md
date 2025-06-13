# README

## ¿Qué es este proyecto?

Este proyecto es una aplicación web llamada **snake**. Permite gestionar tareas y usuarios de manera sencilla a través de una página web.

---

## ¿Qué necesito para usarlo?

Solo necesitas una computadora con **Windows**, **Linux** o **Mac**.  

---

## Pasos para usar el proyecto

### 1. Instalar Python

- Ve a [https://www.python.org/downloads/](https://www.python.org/downloads/) y descarga la versión más reciente de **Python**.
- Instala Python en tu computadora (asegúrate de marcar la casilla que dice "Add Python to PATH" durante la instalación).

### 2. Descargar el proyecto

- Haz clic en el botón verde que dice **"Code"** en la página de GitHub del proyecto.
- Selecciona **"Download ZIP"**.
- Extrae el archivo ZIP en una carpeta de tu computadora.

### 3. Abrir una terminal o consola

- En **Windows**: Busca "cmd" o "Símbolo del sistema" y ábrelo.
- En **Linux/Mac**: Abre la aplicación llamada "Terminal".

### 4. Ir a la carpeta del proyecto

En la terminal, escribe el siguiente comando y presiona **Enter** (reemplaza `ruta/a/tu/carpeta` por la carpeta donde extrajiste el proyecto):

```bash
cd ruta/a/tu/carpeta/snake
```

### 5. Instalar las dependencias

Escribe este comando y presiona **Enter**:

```bash
pip install -r requirements.txt
```

Esto instalará todo lo necesario para que el proyecto funcione.

### 6. Crear la base de datos

Escribe este comando y presiona **Enter**:

```bash
python manage.py migrate
```

Esto prepara la base de datos para que la aplicación funcione.


### 7. Iniciar la aplicación

Escribe este comando y presiona **Enter**:

```bash
python manage.py runserver
```

Verás un mensaje que dice que el servidor está corriendo.

### 8. Abrir la aplicación en tu navegador

Abre tu navegador (Chrome, Firefox, Edge, etc.) y escribe la siguiente dirección:

```
http://127.0.0.1:8000/
```

¡Listo! Ahora puedes usar la aplicación web.


**¡Gracias por usar este proyecto!**
