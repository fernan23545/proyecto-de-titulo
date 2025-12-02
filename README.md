Descripción
Este sistema web permite a ciudadanos de la comuna reservas servicios de emprendimientos locales previamente validados por el municipio.
Incluye gestión de usuarios, publicación de servicios, reserva con trazabilidad y calificación de atención

Tecnologias utilizadas
Python 3.12.4
Django 5.2.4
SQLite (modo desarrollo local)
Html, CSS(Django templates)
Git + GitHub

Roles del sistema
*Ciudadano: Puede registrarse, explorar servicios y hacer reservas
*Emprendedor: Publica sus servicios y gestiona las reservas
Funcionario municipal: valida emprendimientos registrados
Administrador: Gestión total desde el panel admin

Instalación local paso a paso
1. Clona el repositorio
git clone https://github.com/fernan23545/proyecto-de-titulo.git
cd proyecto-de-titulo

2. Crea y activa el entorno virtual
python -m venv env
# En Windows:
env\Scripts\activate
# En Mac/Linux:
source env/bin/activate

3. Instala las dependencias
pip install -r requirements.txt

4. configura el archivo .env
Crea un archivo .env en la raíz del proyecto con
DEBUG=True
SECRET_KEY=tu_clave_django_generada
ALLOWED_HOSTS=127.0.0.1,localhost

5. Aplica migraciones y crea la base de datos
python manage.py migrate

6. Inicia el servidor local
python manage.py runserver

Usuarios disponibles para pruebas

Admin:
Usuario: admin
Contraseña: P3tr0l30.3015

Funcionario municipal:
Usuario: municipal
Contraseña: NuevaClave123!

Emprendedor
Usuario: fcortes
Contraseña: P3tr0l30.3015

Pruebas sugeridas (fase actual)
*Registro de ciudadano y emprendedor
*Creación y validación de emprendimiento
*Publicación de servicios
*elegir un servicio disponible desde cuenta ciudadana
*verificacion de cuenta admin y municipal
*Agregar un servicio desde cuenta de emprendedor