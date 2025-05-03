# Pumaflash

## Descripción

**Pumaflash** es una aplicación web desarrollada con Django para la creación de anuarios digitales. Permite a los usuarios registrar, visualizar y organizar información relacionada con estudiantes, profesores y grupos, ofreciendo una interfaz amigable y adaptable para diversas instituciones.

## Funcionalidades Principales

* Gestión de perfiles de estudiantes, docentes y grupos.
* Búsqueda y filtrado de perfiles.
* Interfaz web responsiva.
* Configuración de datos sensibles mediante variables de entorno.

## Tecnologías Utilizadas

* **Python 3.10**: Lenguaje principal.
* **Django**: Framework backend.
* **MySQL**: Sistema de gestión de base de datos (opcional, configurable).
* **django-crispy-forms**: Mejora el diseño y manejo de formularios.
* **django-environ**: Facilita el uso de variables de entorno.
* **Miniconda**: Manejo del entorno virtual.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/FranciscoMendiola/pumaflash.git
cd pumaflash
```

### 2. Crear entorno con Conda

```bash
conda env create -f environment.yml
conda activate pumaflash
```

### 4. Aplicar migraciones y ejecutar servidor

```bash
python3 manage.py makemigrations APP
python manage.py migrate
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`.
