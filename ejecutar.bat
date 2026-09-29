@echo off
title Iniciando Concordia Alerta API con Entorno Virtual
cd /d "%~dp0"

:: 1. Comprobar si ya existe el entorno virtual, si no, crearlo
if not exist venv (
    echo Creando entorno virtual de Python por primera vez...
    python -m venv venv
)

:: 2. Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

:: 3. Actualizar pip e instalar dependencias de forma aislada
echo Instalando/Verificando librerías en entorno aislado...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo =======================================================
echo  Servidor listo. Abre en tu navegador:
echo  👉 http://127.0.0
echo =======================================================
echo.

:: 4. Iniciar la aplicación
python -m uvicorn app:app --reload
pause
