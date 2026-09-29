# 🚨 Concordia Alerta API

Este repositorio contiene el prototipo del backend para una aplicación de seguridad ciudadana y colaboración vecinal (estilo SOSAFE) diseñada específicamente para la ciudad de **Concordia, Entre Ríos**.

Desarrollado en **Python** utilizando **FastAPI**, el sistema permite la gestión en tiempo real de reportes comunitarios geolocalizados.

## 📁 Estructura del Proyecto

*   `app.py`: Código principal del servidor API REST con rutas de alertas y usuarios.
*   `ejecutar.bat`: Script automatizado para instalar dependencias y encender el servidor en Windows.
*   `requirements.txt`: Listado de librerías de Python requeridas para el entorno.
*   `README.md`: Guía de documentación del proyecto.

## 🚀 Instrucciones de Instalación y Uso

### Requisitos Previos
*   Tener instalado [Python 3.8 o superior](https://www.python.org/).

### Ejecución Rápida (Windows)
1. Descarga o clona este repositorio.
2. Haz doble clic sobre el archivo `ejecutar.bat`.
3. El script instalará automáticamente los módulos necesarios y encenderá el servidor de pruebas.

### Acceso a la Interfaz de Pruebas
Una vez que la consola muestre que el servidor está corriendo, abre tu navegador web e ingresa a:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Desde este panel visual (Swagger UI) podrás simular registros de vecinos y alertas utilizando coordenadas reales de la ciudad.
