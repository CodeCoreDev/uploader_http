# Загрузчик прошивки на http сервер

## Конфигурация nginx

```bash
sudo nano /etc/nginx/sites-available/my_blog
```

```nginx
server {
    listen 80 default_server;
    server_name xxx.xxx.xxx.xxx your-domain.ru www.your-domain.ru;
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /firmware/ {
    alias /var/www/firmware/;
    dav_methods PUT DELETE;
    create_full_put_path on;
    autoindex on;
    }
}
```

```bash
sudo nginx -t
sudo nginx -s reload
```
