from django.contrib.auth import get_user_model
from ajax_datatable.views import AjaxDatatableView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission

from project.query_debugger import query_debugger
from backend.models import Track
from backend.models import Album
from backend.models import Artist
from backend.models import CustomPk


User = get_user_model()


class PermissionAjaxDatatableView(AjaxDatatableView):

    model = Permission
    title = 'Permissions'
    initial_order = [["app_label", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'codename', 'visible': True, },
        {'name': 'name', 'visible': True, },
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]

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
    show_date_filters = False

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': False, },
        {'name': 'name', 'visible': True, },
        {'name': 'album', 'foreign_field': 'album__name', 'visible': True, 'lookup_field': '__istartswith', },
        {'name': 'artist', 'title': 'Artist', 'foreign_field': 'album__artist__name',
            'visible': True, 'choices': True, 'autofilter': True, },
        # {'name': 'tags', 'visible': True, 'searchable': False, },
        {'name': 'tags', 'm2m_foreign_field': 'tags__name', 'searchable': True, 'choices': True, 'autofilter': True, },
    ]

    @query_debugger
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_initial_queryset(self, request=None):
    #     # Optimization: Reduce the number of queries due to ManyToMany "tags" relation
    #     return Track.objects.prefetch_related('tags')

    # def customize_row(self, row, obj):
    #     # 'row' is a dictionary representing the current row, and 'obj' is the current object.
    #     # Display tags as a list of strings
    #     row['tags'] = ','.join( [t.name for t in obj.tags.all()])
    #     return


class AlbumAjaxDatatableView(AjaxDatatableView):

    model = Album
    code = 'album'
    title = _('Album')
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': False, },
        {'name': 'name', 'visible': True, },
        {'name': 'release_date', 'visible': True, },
        {'name': 'year', 'visible': True, },
        {'name': 'artist', 'title': 'Artist', 'foreign_field': 'artist__name',
            'visible': True, 'choices': True, 'autofilter': True, },
    ]

    def get_initial_queryset(self, request=None):

        def get_numeric_param(key):
            try:
                value = int(request.POST.get(key))
            except (ValueError, AttributeError):
                value = None
            return value

        queryset = super().get_initial_queryset(request=request)

        check_year_null = get_numeric_param('check_year_null')
        if check_year_null is not None:
            if check_year_null == 0:
                queryset = queryset.filter(year=None)
            elif check_year_null == 1:
                queryset = queryset.exclude(year=None)

        from_year = get_numeric_param('from_year')
        if from_year is not None:
            queryset = queryset.filter(year__gte=from_year)

        to_year = get_numeric_param('to_year')
        if to_year is not None:
            queryset = queryset.filter(year__lte=to_year)

        return queryset


class ArtistAjaxDatatableView(AjaxDatatableView):

    model = Artist
    code = 'artist'
    title = _('Artist')
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
    show_date_filters = False

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': False, },
        {'name': 'name', 'visible': True, },
        {'name': 'edit', 'title': 'Edit', 'searchable': False, 'orderable': False, },
    ]

    def customize_row(self, row, obj):
        row['edit'] = """
            <a href="#" class="btn btn-info btn-edit"
               onclick="var id=this.closest('tr').id.substr(4); alert('Editing Artist: ' + id); return false;">
               Edit
            </a>
        """


class CustomPkAjaxDatatableView(AjaxDatatableView):

    model = CustomPk
    code = 'custompk'
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]

    column_defs = [
        # AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'pk', 'visible': True, },
        {'name': 'name', 'visible': True, },
    ]
