# Framework SAS - Gestión de Requisitos

## Descripción General

Framework SAS es una aplicación web diseñada para gestionar requisitos legales, crear planes de cumplimiento, asociar usuarios a empresas y realizar el seguimiento del cumplimiento de dichos requisitos. Esta aplicación está construida utilizando el framework Django y proporciona una solución integral para la gestión del cumplimiento dentro de las organizaciones.

## Tabla de Contenidos

-   [Características](#características)
-   [Primeros Pasos](#primeros-pasos)
    -   [Prerrequisitos](#prerrequisitos)
    -   [Instalación](#instalación)
    -   [Ejecutando la Aplicación](#ejecutando-la-aplicación)
-   [Manual de Operación](#manual-de-operación)
    -   [Configuración Inicial (Solo Administradores)](#configuración-inicial-solo-administradores)
        -   [Creación de Países](#creación-de-países)
        -   [Creación de Industrias](#creación-de-industrias)
        -   [Creación de Empresas](#creación-de-empresas)
        -   [Creación de Usuarios](#creación-de-usuarios)
        -   [Asociación de Usuarios con Empresas](#asociación-de-usuarios-con-empresas)
        -   [Creación de Requisitos Legales](#creación-de-requisitos-legales)
    -   [Creación de Requisitos por Empresa (Solo Administradores)](#creación-de-requisitos-por-empresa-solo-administradores)
        -   [Creación de Requisitos por Empresa](#creación-de-requisitos-por-empresa)
        -   [Asociación de Requisitos Legales con Empresas](#asociación-de-requisitos-legales-con-empresas)
    -   [Creación de Planes (Solo Administradores)](#creación-de-planes-solo-administradores)
        -   [Creación de Planes](#creación-de-planes)
    -   [Ejecución de Planes (Usuarios)](#ejecución-de-planes-usuarios)
        -   [Iniciar Sesión](#iniciar-sesión)
        -   [Ejecutar Planes](#ejecutar-planes)
    -   [Consultar Reportes y Dashboards](#consultar-reportes-y-dashboards)
    -   [Cerrar Sesión](#cerrar-sesión)
-   [Consideraciones](#consideraciones)
-   [Recomendaciones](#recomendaciones)
-   [Dependencias](#dependencias)
-   [Contribuciones](#contribuciones)
-   [Licencia](#licencia)

## Características

-   **Gestión de Requisitos Legales:** Crear, editar y gestionar requisitos legales.
-   **Planificación de Cumplimiento:** Crear y gestionar planes de cumplimiento para empresas.
-   **Gestión de Usuarios y Empresas:** Asociar usuarios con empresas y gestionar sus permisos.
-   **Ejecución de Planes:** Realizar el seguimiento de la ejecución y el cumplimiento de los planes.
-   **Reportes y Dashboards:** Consultar reportes y dashboards para monitorear el cumplimiento.
-   **Duplicar al Plan:** Duplicar requisitos a los planes.
-   **Panel de Administración Personalizable:** La aplicación utiliza `django-semantic-admin` y `django-semantic-forms` para proporcionar un panel de administración personalizable.
-   **Importar y Exportar:** La aplicación utiliza `django-import-export` para proporcionar funcionalidad de importación y exportación.
- **Filtros personalizados:** La aplicacion cuenta con filtros personalizados en el panel de administracion.
- **Validaciones:** La aplicacion cuenta con validaciones en el panel de administracion.
- **Middleware:** La aplicacion cuenta con middleware para el manejo de errores y para la seleccion de la empresa.

## Primeros Pasos

### Prerrequisitos

-   Python 3.8+
-   pip (instalador de paquetes de Python)
-   Un navegador web (Chrome, Firefox, Safari, etc.)

### Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/OsvaldoAguilar2024/Frameworksas_gestreq.git
    cd Frameworksas_gestreq
    ```
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python3 -m venv venv
    ```
3.  **Activar el entorno virtual:**
    -   **En Windows:**
        ```bash
        venv\Scripts\activate
        ```
    -   **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Crear la base de datos:**
    ```bash
    python manage.py migrate
    ```
6.  **Crear un superusuario:**
    ```bash
    python manage.py createsuperuser
    ```
7. **Recolectar archivos estáticos:**
    ```bash
    python manage.py collectstatic
    ```

### Ejecutando la Aplicación

1.  **Iniciar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
2.  **Acceder a la aplicación:**
    Abrir su navegador web e ir a `http://127.0.0.1:8000/`.
3. **Acceder al panel de administración:**
    Abrir su navegador web e ir a `http://127.0.0.1:8000/admin/`.

## Manual de Operación

### Configuración Inicial (Solo Administradores)

#### Creación de Países

1.  Ir al panel de administración: `http://127.0.0.1:8000/admin/`.
2.  Navegar a "Gestión de Requisitos" -> "Países".
3.  Hacer clic en "Añadir Pais".
4.  Completar los campos:
    -   **Código:** Código único del país (ej: COL, USA).
    -   **Nombre:** Nombre del país (ej: Colombia, Estados Unidos).
5.  Hacer clic en "Guardar".

#### Creación de Industrias

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Industrias".
3.  Hacer clic en "Añadir Industria".
4.  Completar los campos:
    -   **Nombre:** Nombre de la industria (ej: Manufactura, Servicios).
    -   **Descripción:** Breve descripción de la industria (opcional).
5.  Hacer clic en "Guardar".

#### Creación de Empresas

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Empresas".
3.  Hacer clic en "Añadir Empresa".
4.  Completar los campos:
    -   **Código de Empresa:** Código único de la empresa.
    -   **Nombre de Empresa:** Nombre de la empresa.
    -   **Dirección:** Dirección física de la empresa.
    -   **Teléfono:** Número telefónico de la empresa (opcional).
    -   **Email:** Correo electrónico de la empresa (opcional).
    -   **Logo:** Logo de la empresa (opcional).
    -   **Activo:** Seleccionar si la empresa está activa.
5.  Hacer clic en "Guardar".

#### Creación de Usuarios

1.  Ir al panel de administración.
2.  Navegar a "Usuarios por Empresa" -> "Usuarios Empresa".
3.  Hacer clic en "Añadir Usuario Empresa".
4.  Completar los campos:
    -   **Usuario:** Nombre de usuario único.
    -   **Contraseña:** Contraseña del usuario.
    -   **Nombre:** Nombre del usuario.
    -   **Apellido:** Apellido del usuario.
    -   **Correo electrónico:** Correo electrónico del usuario.
    -   **Es parte del equipo:** Seleccionar si el usuario es parte del equipo.
    -   **Está activo:** Seleccionar si el usuario está activo.
5.  Hacer clic en "Guardar".

#### Asociación de Usuarios con Empresas

1.  En el formulario de creación/edición de usuario, buscar la sección "Empresa del usuario".
2.  Hacer clic en "añadir otra empresa del usuario" tantas veces como sea necesario.
3.  Seleccionar la empresa a la que pertenece el usuario.
4.  Hacer clic en "Guardar".

#### Creación de Requisitos Legales

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Requisitos Legales".
3.  Hacer clic en "Añadir Requisito Legal".
4.  Completar los campos:
    -   **Tema:** Tema del requisito legal.
    -   **Entidad que emite:** Entidad que emite el requisito legal.
    -   **Jerarquía de la norma:** Jerarquía del requisito legal.
    -   **Número:** Número del requisito legal.
    -   **Fecha:** Fecha de emisión.
    -   **Artículo Aplicable:** Artículo aplicable.
    -   **Obligación:** Obligación del requisito legal.
    -   **Proceso que aplica:** Proceso que aplica.
    -   **Tipo de Requisito:** Tipo de requisito.
    -   **País:** País al que pertenece el requisito.
    -   **Industria:** Industria a la que pertenece el requisito.
5.  Hacer clic en "Guardar".

### Creación de Requisitos por Empresa (Solo Administradores)

#### Creación de Requisitos por Empresa

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Requisitos Por Empresa".
3.  Hacer clic en "Añadir Requisitos Por Empresa".
4.  Completar los campos:
    -   **Empresa:** Seleccionar la empresa a la que aplica este requisito.
    -   **Nombre:** Nombre del requisito por empresa.
    -   **Descripción:** Breve descripción del requisito por empresa.
5.  Hacer clic en "Guardar".

#### Asociación de Requisitos Legales con Empresas

1.  En el formulario de creación/edición de requisitos por empresa, buscar la sección "Requisitos por empresa detalle".
2.  Hacer clic en "añadir otro Requisito por empresa detalle" tantas veces como sea necesario.
3.  Seleccionar el requisito legal a asociar.
4.  Completar los campos:
    -   **Descripción de cumplimiento:** Ingresar una descripción de cumplimiento.
    -   **Periodicidad:** Seleccionar la periodicidad del cumplimiento.
    -   **Fecha de inicio:** Ingresar la fecha de inicio.
5.  Hacer clic en "Guardar".

### Creación de Planes (Solo Administradores)

#### Creación de Planes

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Planes".
3.  Hacer clic en "Añadir Plan".
4.  Completar los campos:
    -   **Empresa:** Seleccionar la empresa a la que pertenece el plan.
    -   **Requisito por empresa:** Seleccionar el requisito por empresa al que pertenece el plan.
    -   **Periodicidad:** Seleccionar la periodicidad del plan.
    -   **Fecha de inicio:** Ingresar la fecha de inicio.
    -   **Fecha próximo cumplimiento:** Ingresar la fecha del próximo cumplimiento.
    -   **Descripción periodicidad:** Ingresar la descripción de la periodicidad, si es necesario.
    - **Year:** Ingresar el año al cual pertenece el plan.
5.  Hacer clic en "Guardar".

### Ejecución de Planes (Usuarios)

#### Iniciar Sesión

1.  Abrir su navegador web e ir a `http://127.0.0.1:8000/`.
2.  Hacer clic en "Login".
3.  Ingresar sus credenciales de usuario.
4.  Si el usuario pertenece a varias empresas, seleccionar la empresa con la que desea trabajar.

#### Ejecutar Planes

1.  Ir al panel de administración.
2.  Navegar a "Gestión de Requisitos" -> "Ejecución Del Plan".
3.  Buscar el plan que desea ejecutar.
4.  Completar los campos:
    -   **Porcentaje de Cumplimiento:** Ingresar el porcentaje de cumplimiento.
    -   **Evidencia de Cumplimiento:** Cargar la evidencia de cumplimiento (opcional).
    -   **Responsable:** Ingresar el nombre del responsable.
    -   **Notas:** Ingresar las notas necesarias.
    -   **Resultado evaluación:** Ingresar el resultado de la evaluación.
    -   **Ejecución:** Elegir si fue ejecutado o no.
    -   **Conforme:** Elegir si fue conforme o no.
    -   **Razón no conforme:** Si fue no conforme, ingresar la razón.
5.  Hacer clic en "Guardar".

### Consultar Reportes y Dashboards

1.  Ir a la página principal.
2.  Ir a la sección "Dashboard y Reportes".
3.  Hacer clic en "Reportes" o en "Dashboard".

### Cerrar Sesión

1.  En la barra de navegación superior, hacer clic en la opción desplegable del usuario.
2.  Hacer clic en "Logout".

## Consideraciones

-   Los usuarios regulares solo tienen acceso a la sección "Ejecución de Planes".
-   Solo los administradores pueden crear Países, Industrias, Empresas, Usuarios, Requisitos Legales, Requisitos por Empresa y Planes.
-   Recuerde que el proceso para agregar usuarios a una empresa se hace en la creación o edición del usuario.
-   **Duplicar al Plan:** La opción "Duplicar al Plan" en la sección "Requisitos Por Empresa" permite duplicar los requisitos a los planes, debe seleccionar el año.

## Recomendaciones

-   Mantener una comunicación constante con los usuarios para aclarar dudas y recibir retroalimentación.
-   Recordar que todos los cambios deben ser validados.

## Dependencias

-   asgiref==3.8.1
-   crispy-bootstrap5==2024.10
-   defusedxml==0.7.1
-   diff-match-patch==20241021
-   Django==4.2.11
-   django-bootstrap==0.2.4
-   django-crispy-forms==2.3
-   django-environ==0.12.0
-   django-import-export==3.3.7
-   django-semantic-admin==0.4.1
-   django-semantic-forms==0.1.8
-   et_xmlfile==2.0.0
-   MarkupPy==1.14
-   odfpy==1.4.1
-   openpyxl==3.1.5
-   pillow==11.1.0
-   PyYAML==6.0.2
-   sqlparse==0.5.3
-   tablib==3.5.0
-   tzdata==2025.1
-   xlrd==2.0.1
-   xlwt==1.3.0

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1.  Haz un fork del repositorio.
2.  Crea una nueva rama para tu funcionalidad o corrección de errores.
3.  Realiza tus cambios y haz commit de ellos.
4.  Sube tus cambios a tu repositorio forkeado.
5.  Envía un pull request.

## Licencia

Licencia MIT
