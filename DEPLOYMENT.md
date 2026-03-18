# Guía de Despliegue de InfoFlow en Producción

Este documento proporciona instrucciones detalladas para desplegar InfoFlow en un entorno de producción.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Preparación del Código](#preparación-del-código)
3. [Configuración del Servidor](#configuración-del-servidor)
4. [Despliegue en Heroku](#despliegue-en-heroku)
5. [Despliegue en AWS](#despliegue-en-aws)
6. [Despliegue Manual con Gunicorn](#despliegue-manual-con-gunicorn)
7. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)

## 🔧 Requisitos Previos

- **Servidor Linux** (Ubuntu 20.04 LTS recomendado)
- **Python 3.11+**
- **PostgreSQL 12+**
- **Nginx** (como proxy reverso)
- **Git**
- **Dominio** (opcional pero recomendado)
- **Certificado SSL** (Let's Encrypt gratuito)

## 🚀 Preparación del Código

### 1. Crear Archivo .env para Producción

```bash
# En tu servidor de producción
nano /home/usuario/infoflow/.env
```

Contenido:

```env
DEBUG=False
SECRET_KEY=your-very-secure-random-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=infoflow_prod
DB_USER=infoflow_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Generar SECRET_KEY Segura

```python
# En Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 🖥️ Configuración del Servidor

### 1. Instalar Dependencias del Sistema

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y git curl wget
```

### 2. Crear Usuario para la Aplicación

```bash
sudo useradd -m -s /bin/bash infoflow
sudo su - infoflow
```

### 3. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/infoflow.git
cd infoflow
```

### 4. Crear Entorno Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 5. Instalar Dependencias de Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configurar Base de Datos PostgreSQL

```bash
# Como usuario root
sudo su - postgres
createdb infoflow_prod
createuser infoflow_user
psql
```

En psql:

```sql
ALTER USER infoflow_user WITH PASSWORD 'your-secure-password';
ALTER ROLE infoflow_user SET client_encoding TO 'utf8';
ALTER ROLE infoflow_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE infoflow_user SET default_transaction_deferrable TO on;
ALTER ROLE infoflow_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE infoflow_prod TO infoflow_user;
\q
```

### 7. Ejecutar Migraciones

```bash
# Como usuario infoflow
cd ~/infoflow
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### 8. Crear Superusuario

```bash
python manage.py createsuperuser
```

## 🚀 Despliegue en Heroku

### 1. Instalar Heroku CLI

```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

### 2. Crear Aplicación en Heroku

```bash
heroku create tu-app-name
```

### 3. Agregar Base de Datos PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4. Configurar Variables de Entorno

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=tu-app-name.herokuapp.com
```

### 5. Crear Procfile

```bash
# En la raíz del proyecto
echo "web: gunicorn infoflow.wsgi --log-file -" > Procfile
```

### 6. Desplegar

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🌐 Despliegue Manual con Gunicorn

### 1. Crear Archivo de Servicio Systemd

```bash
sudo nano /etc/systemd/system/infoflow.service
```

Contenido:

```ini
[Unit]
Description=InfoFlow Django Application
After=network.target postgresql.service

[Service]
User=infoflow
Group=www-data
WorkingDirectory=/home/infoflow/infoflow
Environment="PATH=/home/infoflow/infoflow/venv/bin"
ExecStart=/home/infoflow/infoflow/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    --timeout 60 \
    infoflow.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 2. Habilitar Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable infoflow
sudo systemctl start infoflow
sudo systemctl status infoflow
```

### 3. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/infoflow
```

Contenido:

```nginx
upstream infoflow {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /home/infoflow/infoflow/staticfiles/;
    }

    location / {
        proxy_pass http://infoflow;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 4. Habilitar Sitio en Nginx

```bash
sudo ln -s /etc/nginx/sites-available/infoflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configurar SSL con Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 📊 Monitoreo y Mantenimiento

### 1. Ver Logs

```bash
# Logs de Gunicorn
sudo journalctl -u infoflow -f

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### 2. Actualizar Aplicación

```bash
cd /home/infoflow/infoflow
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart infoflow
```

### 3. Backup de Base de Datos

```bash
# Backup manual
pg_dump -U infoflow_user infoflow_prod > backup.sql

# Restore
psql -U infoflow_user infoflow_prod < backup.sql
```

### 4. Monitoreo de Rendimiento

```bash
# Ver uso de recursos
htop

# Ver conexiones a PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Ver procesos de Gunicorn
ps aux | grep gunicorn
```

## 🔒 Checklist de Seguridad

- ✅ `DEBUG=False` en producción
- ✅ `SECRET_KEY` es una cadena aleatoria larga
- ✅ HTTPS habilitado con certificado SSL válido
- ✅ Base de datos con contraseña fuerte
- ✅ Firewall configurado (UFW)
- ✅ Backups automáticos de base de datos
- ✅ Logs monitoreados regularmente
- ✅ Actualizaciones de seguridad instaladas
- ✅ ALLOWED_HOSTS configurado correctamente
- ✅ CORS configurado restrictivamente

## 🆘 Solución de Problemas

### Error: "Connection refused"

```bash
# Verificar que PostgreSQL está ejecutándose
sudo systemctl status postgresql

# Verificar que Gunicorn está ejecutándose
sudo systemctl status infoflow
```

### Error: "Static files not found"

```bash
python manage.py collectstatic --noinput
sudo systemctl restart infoflow
```

### Error: "Permission denied"

```bash
# Verificar permisos
sudo chown -R infoflow:www-data /home/infoflow/infoflow
sudo chmod -R 755 /home/infoflow/infoflow
```

### Error: "Database connection failed"

```bash
# Verificar credenciales en .env
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Probar conexión
psql -U infoflow_user -d infoflow_prod -h localhost
```

## 📞 Soporte

Para más información, consulta la documentación oficial:
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Última actualización:** 2024
