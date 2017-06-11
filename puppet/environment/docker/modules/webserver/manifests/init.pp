###
### init.pp: start webserver, and ensure all client services exist, and
###          properly configured.
###

class webserver {
    ## install mariadb client
    contain mariadb::client
    contain mariadb::bindings

    ## install redis client
    contain package::redis_client

    ## ssl for nginx
    contain webserver::ssl

    ## install webserver
    contain package::gunicorn
    contain webserver::service
}
contain webserver