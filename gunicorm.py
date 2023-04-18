


# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target

# [Service]
# User=sammy
# Group=www-data
# WorkingDirectory=/home/ubuntu/main_project
# ExecStart=/home/ubuntu/main_project/myprojectenv/bin/gunicorn \
#           --access-logfile - \
#           --workers 3 \
#           --bind unix:/run/gunicorn.sock \
#           ecommerce.wsgi:application

# [Install]
# WantedBy=multi-user.target



# server {
#     listen 80;
#     server_name 13.50.13.43;

#     location = /favicon.ico { access_log off; log_not_found off; }
    

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
# }