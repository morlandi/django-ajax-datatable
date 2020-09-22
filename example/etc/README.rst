etc
===

Sample Web Server configuration files:

- nginx.conf
- supervisor.conf

Sample deployment layout::

    /home/django-ajax-datatable-demo/
    ├── django-ajax-datatable
    ├── etc
    ├── logs
    ├── python
    ├── run
    ├── setenv.bash
    └── sservicesctl.py

Usage:

.. code:: bash

    cp -R /home/django-ajax-datatable-demo/django-ajax-datatable/example/etc /home/django-ajax-datatable-demo/
    ... adjust files if as required ...
    sudo ln -s /home/django-ajax-datatable-demo/etc/nginx.conf /etc/sites-enabled/django-ajax-datatable-demo.conf
    sudo ln -s /home/django-ajax-datatable-demo/etc/supervisor.conf /etc/supervisor/conf.d/django-ajax-datatable-demo.conf
