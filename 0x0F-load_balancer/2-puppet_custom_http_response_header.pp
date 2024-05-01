# Ensure NGINX is installed
package { 'nginx':
  ensure => installed,
}

# Define a custom fact to retrieve the hostname
Facter.add('nginx_hostname') do
  setcode 'hostname'
end

# Define NGINX configuration file
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "server {
                listen 80 default_server;
                listen [::]:80 default_server;
                
                root /var/www/html;
                index index.html index.htm index.nginx-debian.html;

                server_name _;

                location / {
                    try_files $uri $uri/ =404;
                    add_header X-Served-By $nginx_hostname;
                }
            }",
}

# Create a symbolic link to enable the site
file { '/etc/nginx/sites-enabled/default':
  ensure => link,
  target => '/etc/nginx/sites-available/default',
  require => File['/etc/nginx/sites-available/default'],
}

# Restart NGINX service to apply changes
service { 'nginx':
  ensure => running,
  enable => true,
  require => [File['/etc/nginx/sites-available/default'], File['/etc/nginx/sites-enabled/default']],
}
