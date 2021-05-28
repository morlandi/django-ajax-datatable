#!/usr/bin/env python
import os
import sys

# See "Using the Django test runner to test reusable applications":
# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["ajax_datatable.tests"])
    sys.exit(bool(failures))


# #!/usr/bin/env python

# import os
# import sys

# import django
# from django.conf import settings
# from django.test.utils import get_runner


# def run_tests(*test_args):

#     # Since out app has no Models, we need to involve another 'tests' app
#     # with at least a Model to make sure that migrations are run for test sqlite database
#     if not test_args:
#         test_args = ['tests', 'ajax_datatable', ]

#     os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
#     django.setup()
#     TestRunner = get_runner(settings)
#     test_runner = TestRunner()
#     failures = test_runner.run_tests(test_args)
#     sys.exit(bool(failures))


# if __name__ == '__main__':
#     run_tests(*sys.argv[1:])
