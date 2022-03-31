import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from .exceptions import ColumnOrderError
from .utils import format_datetime
from django.utils.html import strip_tags
from .app_settings import STRIP_HTML_TAGS


class Column(object):

    def __init__(self, model_field, sort_field=None, allow_choices_lookup=True):
        try:
            self.name = model_field.name
            self.sort_column_name = sort_field or model_field.name
            self.model_field = model_field
            choices = model_field.choices

            if allow_choices_lookup and choices:
                self._choices_lookup = self.parse_choices(choices)
                # self._search_choices_lookup =\
                #     {v: k for k, v in six.iteritems(self._choices_lookup)}
                self._allow_choices_lookup = True
            else:
                self._allow_choices_lookup = False
        except AttributeError:
            self.name = model_field
            self.sort_column_name = sort_field or model_field
            self.model_field = None
            self._allow_choices_lookup = False

    # @staticmethod
    # def collect_model_columns(model, column_specs):
    #     """
    #     Build a list of either Columns or ForeignColumns as required
    #     """
    #     columns = [c['name'] for c in column_specs]
    #     foreign_fields = dict([(c['name'], c['foreign_field']) for c in column_specs if c['foreign_field']])

    #     fields = {f.name: f for f in model._meta.get_fields()}
    #     model_columns = {}
    #     for col_name in columns:
    #         if col_name in foreign_fields:
    #             new_column = ForeignColumn(
    #                 col_name,
    #                 model,
    #                 foreign_fields[col_name]
    #             )
    #         elif col_name in fields:
    #             new_column = Column(fields[col_name])
    #         else:
    #             new_column = Column(col_name)
    #         model_columns[col_name] = new_column
    #     return model_columns

    @staticmethod
    def column_factory(model, column_spec):
        """
        Build either a Column or a ForeignColumn as required
        """
        fields = {f.name: f for f in model._meta.get_fields()}
        col_name = column_spec['name']
        sort_field = column_spec['sort_field']
        foreign_field = column_spec.get('foreign_field', None)
        m2m_foreign_field = column_spec.get('m2m_foreign_field', None)

        if foreign_field:
            new_column = ForeignColumn(col_name, model, foreign_field)
        elif m2m_foreign_field:
            new_column = ManyToManyColumn(col_name, model, m2m_foreign_field)
        elif col_name in fields:
            new_column = Column(fields[col_name], sort_field=sort_field)
        else:
            new_column = Column(col_name, sort_field=sort_field)
        return new_column

    @property
    def has_choices_available(self):
        return self._allow_choices_lookup

    def get_field_search_path(self):
        return self.sort_column_name

    def parse_choices(self, choices):
        choices_dict = {}

        for choice in choices:
            try:
                choices_dict[choice[0]] = choice[1]
            except IndexError:
                choices_dict[choice[0]] = choice[0]
            except UnicodeDecodeError:
                choices_dict[choice[0]] = choice[1].decode('utf-8')

        return choices_dict

    def string_tags_in_case(self, value):
        if STRIP_HTML_TAGS and value is not None:
            return strip_tags(value)
        return value

    def render_column_value(self, obj, value):

        if self._allow_choices_lookup:
            #return self._choices_lookup[value]
            return self.string_tags_in_case(self._choices_lookup.get(value, ''))

        if isinstance(value, datetime.datetime):
            value = format_datetime(value, True)
        elif isinstance(value, datetime.date):
            value = format_datetime(value, False)
        elif isinstance(value, bool):
            value = _('Yes') if value else _('No')
        return self.string_tags_in_case(value)

    def render_column(self, obj):
        try:
            value = getattr(obj, self.name)
        except AttributeError:
            value = '???'
        return self.render_column_value(obj, value)

    def search_in_choices(self, pattern_list):
        if not self._allow_choices_lookup:
            return []
        # return [matching_value for key, matching_value in
        # six.iteritems(self._search_choices_lookup) if key.startswith(value)]
        values = []
        if type(pattern_list) != list:
            pattern_list = [pattern_list]
        for pattern in pattern_list:
            pattern = pattern.lower()
            # values = [key for (key, text) in self._choices_lookup.items() if text.lower().startswith(pattern)]
            values += [key for (key, text) in self._choices_lookup.items() if pattern in text.lower()]
        return values


class ForeignColumn(Column):
    def __init__(self, name, model, path_to_column, allow_choices_lookup=True):

        self._field_search_path = path_to_column
        self._field_path = path_to_column.split('__')
        foreign_field = self.get_foreign_field(model)
        super(ForeignColumn, self).__init__(foreign_field, allow_choices_lookup)

    def get_field_search_path(self):
        return self._field_search_path

    def get_foreign_field(self, model):
        path_items = self._field_path
        path_item_count = len(path_items)
        current_model = model

        for idx, cur_field_name in enumerate(path_items):
            fields = {f.name: f for f in current_model._meta.get_fields()}

            if idx < path_item_count-1:
                try:
                    current_field = fields[cur_field_name]
                except KeyError:
                    # six.reraise(
                    #     KeyError,
                    #     "Field %s doesn't exists (model %s, path: %s)"
                    #     % (cur_field_name, current_model.__name__,
                    #        '__'.join(path_items[0:idx])))
                    raise KeyError(
                        "Field %s doesn't exists (model %s, path: %s)" % (
                            cur_field_name,
                            current_model.__name__,
                            '__'.join(path_items[0:idx])
                        )
                    )
                try:
                    current_model = current_field.related_model
                except AttributeError:
                    # six.reraise(
                    #     AttributeError,
                    #     "Field %s is not a foreign key (model %s, path %s)" %
                    #     (cur_field_name, current_model.__name__,
                    #      '__'.join(path_items[0:idx])))
                    raise AttributeError(
                        "Field %s is not a foreign key (model %s, path %s)" % (
                            cur_field_name,
                            current_model.__name__,
                            '__'.join(path_items[0:idx])
                        )
                    )
            else:
                foreign_field = fields[cur_field_name]

        return foreign_field

    def get_foreign_value(self, obj):
        current_value = obj

        for current_path_item in self._field_path:
            try:
                current_value = getattr(current_value, current_path_item)
            except AttributeError:
                try:
                    current_value = [
                        getattr(current_value, current_path_item)
                        for current_value in current_value.get_queryset()
                    ]
                except AttributeError:
                    try:
                        current_value = [getattr(f, current_path_item) for f in current_value]
                    except AttributeError:
                        current_value = None

            if current_value is None:
                return None

        # use __str__() if no attribute has been specified by 'foreign_field'
        # TODO: what happens with search and choices/autofilter ?
        if isinstance(current_value, models.Model):
            current_value = str(current_value)

        return current_value

    def render_column(self, obj):
        value = self.get_foreign_value(obj)
        return self.render_column_value(obj, value)


class ManyToManyColumn(ForeignColumn):

    def get_foreign_value(self, obj):
        current_value = obj
        m2m_name, m2m_field = self._field_path

        to_eval = f'obj.{m2m_name}_list'
        # _list should be generated in optimize_queryset, if not we use regular .all() to get the m2m
        if not hasattr(obj, f'{m2m_name}_list'):
            to_eval = f'obj.{m2m_name}.all()'
        return [
            getattr(x, m2m_field)
            for x in eval(to_eval)]

    def render_column_value(self, obj, value_list):
        if self._allow_choices_lookup:
            return ', '.join([str(self._choices_lookup.get(value, '')) for value in value_list])

        return ', '.join([str(value) for value in value_list])

class ColumnLink(object):

    def __init__(self, name, model_column=None, searchable='true', orderable='true', search_value='',
                 placeholder=False):

        def to_bool(value):
            """
            accept either string or boolean
            """
            if type(value) == str:
                return value == "true"
            return value

        self.name = name
        self._model_column = model_column
        # self.searchable = True if searchable == "true" else False
        # self.orderable = True if orderable == "true" else False
        self.searchable = to_bool(searchable)
        self.orderable = to_bool(orderable)
        self.search_value = search_value
        self.placeholder = placeholder or (name == '')

    def __repr__(self):
        return '%s (searchable: %s, orderable: %s, search_value: "%s")' %\
            (self.name or '<placeholder>', self.searchable, self.orderable, self.search_value)

    def get_field_search_path(self):
        return self._model_column.get_field_search_path()

    def get_value(self, object_instance):
        return self._model_column.render_column(object_instance)

    def to_dict(self):
        """
        Get a dictionary representation of :class:`InstanceResource`
        """
        self_dict = {}
        # for key, value in six.iteritems(self.__dict__):
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                self_dict[key] = value
        return self_dict


class PlaceholderColumnLink(ColumnLink):

    def __init__(self):
        super(PlaceholderColumnLink, self).__init__(
            None, None, False, False, True)

    def get_value(self, object_instance):
        return None


class Order(object):

    def __init__(self, column_index, direction, column_links_list):
        try:
            self.ascending = True if direction == 'asc' else False
            self.column_link = column_links_list[int(column_index)]
            if self.column_link.placeholder:
                raise ColumnOrderError(
                    'Requested to order a placeholder column (index %d)' %
                    column_index)
        except KeyError:
            raise ColumnOrderError(
                'Requested to order a non-existing column (index %d)' %
                column_index)

    def __repr__(self):
        return '%s: %s' % (
            self.column_link.name, 'ASC' if self.ascending else 'DESC')

    def get_order_mode(self):
        if not self.ascending:
            return '-' + self.column_link.get_field_search_path()
        return self.column_link.get_field_search_path()

################################################################################
