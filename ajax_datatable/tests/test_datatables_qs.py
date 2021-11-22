# from django.test import TestCase
from django.db import models
import unittest
from ajax_datatable import Column, ColumnLink, Order, ColumnOrderError


class MyTestModel(models.Model):
    one = models.CharField(max_length=20)
    two = models.CharField(max_length=20)

    class Meta:
        app_label = 'myappname'


# class TestAuth(TestCase):
class TestDatatablesQs(unittest.TestCase):

    def test_order(self):

        column_specs = [{
            'name': 'one',
            'sort_field': 'one',
            'foreign_field': '',
        }, {
            'name': 'two',
            'sort_field': 'one',
            'foreign_field': '',
        }]

        # model_columns = Column.collect_model_columns(MyTestModel, ['one', 'two'])
        # model_columns = Column.collect_model_columns(MyTestModel, column_specs)
        model_columns = {
            'one': Column.column_factory(MyTestModel, column_specs[0]),
            'two': Column.column_factory(MyTestModel, column_specs[1]),
        }
        column_links = [
            ColumnLink('one', model_columns['one']),
            ColumnLink('two', model_columns['two'], placeholder=True),
        ]

        order_one_asc = Order(0, 'asc', column_links)
        print(order_one_asc)
        self.assertEqual('one', order_one_asc.get_order_mode())

        order_one_desc = Order(0, 'desc', column_links)
        print(order_one_desc)
        self.assertEqual('-one', order_one_desc.get_order_mode())

        self.assertRaises(
            ColumnOrderError,
            lambda: Order(1, 'asc', column_links)
        )
