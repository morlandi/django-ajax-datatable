# from django.test import TestCase
from django.db import models
import unittest
from ajax_datatable import AjaxDatatableView


class TestModel(models.Model):

    F5_CHOICES = [['aaa', 'AAA'], ['bbb', 'BBB'], ]

    f1 = models.CharField(max_length=20)
    f2 = models.CharField(max_length=20)
    f3 = models.CharField(max_length=20)
    f4 = models.CharField(max_length=20)
    f5 = models.CharField(max_length=20, choices=F5_CHOICES)
    f6 = models.CharField(max_length=20)
    f7 = models.CharField(max_length=20)

    class Meta:
        app_label = 'myappname'


class TestAjaxDatatableView(AjaxDatatableView):
    model = TestModel

    F4_CHOICES = (('one', 'One'), ('two', 'Two'), ('three', 'Three'), )

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {
            'name': 'id',
            'visible': False,
        }, {
            # Don't use choices
            'name': 'f1',
            # 'choices': None
        }, {
            # Don't use choices
            'name': 'f2',
            'choices': None,
        }, {
            # Don't use choices
            'name': 'f3',
            'choices': False,
        }, {
            # Use supplied choices
            'name': 'f4',
            'choices': F4_CHOICES,
        }, {
            # Copy from field's choices if any (found)
            'name': 'f5',
            'choices': True,
        }, {
            # Copy from field's choices if any (not found)
            'name': 'f6',
            'choices': True,
        }
    ]


class ChoicesFiltersTestCase(unittest.TestCase):

    def test_choices_filters_defs(self):

        request = None

        view = TestAjaxDatatableView()
        view.initialize(request)

        print(view.column_spec_by_name('f1'))
        print(view.column_spec_by_name('f2'))
        print(view.column_spec_by_name('f3'))
        print(view.column_spec_by_name('f4'))
        print(view.column_spec_by_name('f5'))
        print(view.column_spec_by_name('f6'))

        self.assertEqual(None, view.column_spec_by_name('f1')['choices'])
        self.assertEqual(None, view.column_spec_by_name('f2')['choices'])
        self.assertEqual(None, view.column_spec_by_name('f3')['choices'])
        self.assertSequenceEqual(TestAjaxDatatableView.F4_CHOICES, view.column_spec_by_name('f4')['choices'])
        self.assertSequenceEqual(TestModel.F5_CHOICES, view.column_spec_by_name('f5')['choices'])
        self.assertEqual(None, view.column_spec_by_name('f6')['choices'])
