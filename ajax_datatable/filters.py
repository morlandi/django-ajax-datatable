import datetime
from django.db.models import Q
from django.db import models
from .utils import parse_date


def build_column_filter(column_name, column_obj, column_spec, search_value, global_filtering):
    search_filter = None

    # v4.0.2: we now accept multiple search values (to be ORed),
    # now implemented for text search: "aaa+bbb" --> Q("aaa") | Q("bbb")
    # TODO: check what happens with "choices"

    # if type(column_obj.model_field) == fields.CharField:
    #     # do something special with this field

    if column_obj.has_choices_available:

        choices = column_spec['choices']
        if choices and not global_filtering:
            # Since we're using choices (we provided a select box)
            # just use the selected key
            values = [search_value, ]
        else:
            values = column_obj.search_in_choices(search_value)

        # Fixed in v4.1.3; finger crossed ;)
        # search_filter = Q(**{column_obj.name + '__in': values})
        search_filter = Q(**{column_obj.get_field_search_path() + '__in': values})

    elif isinstance(column_obj.model_field, (models.DateTimeField, models.DateField)):

        # try:
        #     import ipdb; ipdb.set_trace()
        #     parsed_date = parse_date(search_value)
        #     date_range = [parsed_date.isoformat(), parsed_date.isoformat()]
        #     query_param_name = column_obj.get_field_search_path()
        #     if isinstance(column_obj.model_field, models.DateTimeField):
        #         search_filter = Q(**{query_param_name + '__date__range': date_range})
        #     else:
        #         search_filter = Q(**{query_param_name + '__range': date_range})
        # except ValueError:
        #     pass

        try:
            parsed_date = parse_date(search_value)
        except ValueError:
            # when the value entered so far is not a valid date,
            # let's clear the table content to give a feedback to the user
            parsed_date = datetime.date(1,1,1)
        date_range = [parsed_date.isoformat(), parsed_date.isoformat()]
        query_param_name = column_obj.get_field_search_path()
        if isinstance(column_obj.model_field, models.DateTimeField):
            search_filter = Q(**{query_param_name + '__date__range': date_range})
        else:
            search_filter = Q(**{query_param_name + '__range': date_range})


    # elif isinstance(column_obj.model_field, models.ManyToManyField):
    #     # query_param_name = column_obj.get_field_search_path()
    #     # search_filter = Q(**{query_param_name + '__in': [search_value, ]})
    #     raise Exception('Searching not supported for ManyToManyFields (yet)')
    #     pass
    else:
        query_param_name = column_obj.get_field_search_path()

        lookup_field = column_spec['lookup_field']
        # #search_filters |= Q(**{query_param_name + '__istartswith': search_value})
        # search_filter = Q(**{query_param_name + '__icontains': search_value})

        # See: "How do I do an OR filter in a Django query?"
        # https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
        if type(search_value) == list:
            search_filter = Q()
            for item in search_value:
                search_filter |= Q(**{query_param_name + lookup_field: item})
        else:
            search_filter = Q(**{query_param_name + lookup_field: search_value})

    return search_filter
