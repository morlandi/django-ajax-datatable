# from django.test import TestCase
from django.db import models
import unittest
from ajax_datatable import AjaxDatatableView


class TestModelWithoutLatestBy(models.Model):
    one = models.CharField(max_length=20)
    two = models.CharField(max_length=20)

    class Meta:
        app_label = 'myappname2'


class TestModelWithLatestBy(models.Model):
    one = models.CharField(max_length=20)
    two = models.CharField(max_length=20)

    class Meta:
        app_label = 'myappname2'
        get_latest_by = "one"


class DatatablesWithoutLatestByView(AjaxDatatableView):
    model = TestModelWithoutLatestBy


class DatatablesWithLatestByView(AjaxDatatableView):
    model = TestModelWithLatestBy

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {
            'name': 'id',
            'visible': False,
        }, {
            'name': 'one',
        }, {
            'name': 'two',
        }
    ]


class DatatablesForceFilterView(AjaxDatatableView):
    model = TestModelWithoutLatestBy

    def get_show_date_filters(self, request):
        return True


class DateFiltersTestCase(unittest.TestCase):

    def test_filters_flag(self):

        request = None

        view = DatatablesWithoutLatestByView()
        view.initialize(request)
        self.assertIsNone(view.latest_by)
        self.assertFalse(view.show_date_filters)

        view = DatatablesWithLatestByView()
        view.initialize(request)
        self.assertIsNotNone(view.latest_by)
        self.assertTrue(view.show_date_filters)

        column_spec = view.column_spec_by_name(view.latest_by)
        self.assertIsNotNone(column_spec)
        self.assertIn('latest_by', column_spec.get('className', ''))

        view = DatatablesForceFilterView()
        view.initialize(request)
        self.assertTrue(view.show_date_filters)
