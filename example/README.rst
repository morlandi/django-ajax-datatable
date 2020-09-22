
Install
=======

Install Django dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Initialize database tables:

.. code-block:: bash

    python manage.py migrate

Create a super-user for the admin:

.. code-block:: bash

    python manage.py createsuperuser

Donwload js packages:

.. code-block:: bash

    npm install

Run
===

.. code-block:: bash

    python manage.py runserver

The map visible on http://127.0.0.1:8000/ can be edited from the AdminSite at ``/admin``.
