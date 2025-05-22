#!/bin/bash

# Actualizar el sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependencias
sudo apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# Crear usuario de base de datos
sudo -u postgres psql -c "CREATE USER your-db-user WITH PASSWORD 'your-db-password';"
sudo -u postgres psql -c "CREATE DATABASE epilepsia_db OWNER your-db-user;"

# Crear directorio para la aplicación
sudo mkdir -p /var/www/epilepsia
sudo chown -R $USER:$USER /var/www/epilepsia

# Configurar Nginx
sudo tee /etc/nginx/sites-available/epilepsia << EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/epilepsia;
    }

    location /media/ {
        root /var/www/epilepsia;
    }

    location / {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

# Habilitar el sitio
sudo ln -s /etc/nginx/sites-available/epilepsia /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Configurar Gunicorn
sudo tee /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/epilepsia
ExecStart=/var/www/epilepsia/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    app.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Crear socket para Gunicorn
sudo tee /etc/systemd/system/gunicorn.socket << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
SocketUser=www-data
SocketGroup=www-data
SocketMode=0660

[Install]
WantedBy=sockets.target
EOF

# Habilitar y iniciar Gunicorn
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket

# Configurar firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Crear directorio para logs
sudo mkdir -p /var/www/epilepsia/logs
sudo chown -R $USER:$USER /var/www/epilepsia/logs

# Configurar SSL con Let's Encrypt
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

echo "Configuración completada. Por favor, actualiza las variables de entorno en .env" 