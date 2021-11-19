
import unittest

from django.db.models import CharField, Q

from ajax_datatable.columns import Column
from ajax_datatable.filters import build_column_filter


class ColumnFilterTest(unittest.TestCase):
    def test_build_column_filter(self):
        model_field = CharField()
        column = Column(model_field=model_field, sort_field="fooo")
        column_spec = {
            'lookup_field': "foo",
        }
        filters = build_column_filter("foo", column, column_spec, "bar", True)
        self.assertEquals(filters, Q(fooofoo='bar'))

    def test_build_column_filter_multiple_field(self):
        """ Search for multiple fields """
        model_field = CharField(choices=[("foo", "boo"), ("far", "bar")])
        column = Column(model_field=model_field, sort_field="fooo")
        column_spec = {
            'lookup_field': "foo",
            'choices': "foo",
        }
        filters = build_column_filter("foo", column, column_spec, ["bar", "boo"], True)
        self.assertEquals(filters, Q(fooo__in=["far", "foo"]))
