import json
import datetime
import sys
import inspect
#import dateutil.parser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ajax_datatable.views import AjaxDatatableView
from ajax_datatable.utils import trace
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.db.models import Count, Min, Sum, Avg
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import truncatechars

from backend.models import Track
from backend.models import CustomPk


User = get_user_model()


# @login_required
# def object_list_view(request, model, template_name="frontend/pages/object_list.html"):
#     """
#     Render the page which contains the table.
#     That will in turn invoke (via Ajax) object_datatable_view(), to fill the table content
#     """
#     return render(request, template_name, {
#         'model': model,
#     })


# class BaseDatatablesView(AjaxDatatableView):

#     length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]
#     show_column_filters = None

#     # def get_model_admin(self):
#     #     from django.contrib import admin
#     #     if self.model in admin.site._registry:
#     #         return admin.site._registry[self.model]
#     #     return None

#     @classmethod
#     def list_visible_columns(cls):
#         """
#         Utilizzata per esporre le colonne disponibili all'utente, al fine di
#         personalizzare il layout della tabella
#         """

#         def get_title_for_column(col):
#             if 'title' in col:
#                 title = col['title']
#             else:
#                 try:
#                     title = cls.model._meta.get_field(col['name']).verbose_name.title()
#                 except:
#                     title = col['name']
#             return title

#         columns = [
#             {
#                 'code': col['name'],
#                 'title': get_title_for_column(col),
#             }
#             for col in cls.column_defs[1:] if col.get('visible', True)
#         ]

#         return columns


class TrackAjaxDatatableView(AjaxDatatableView):

    model = Track
    code = 'track'
    title = _('Tracks')
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': False, },
        {'name': 'name', 'visible': True, },
        {'name': 'album', 'foreign_field': 'album__name', 'visible': True, },
        {'name': 'artist', 'title':'Artist', 'foreign_field': 'album__artist__name', 'visible': True, 'choices': True, 'autofilter': True, },
        # {'name': 'username', }
    ]


class CustomPkAjaxDatatableView(AjaxDatatableView):

    model = CustomPk
    code = 'custompk'
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]

    column_defs = [
        #AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': True, },
        {'name': 'name', 'visible': True, },
    ]


