from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .models import Tag
from .models import Tag2
from .models import Artist
from .models import Album
from .models import Track
from .models import CustomPk


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag2)
class Tag2Admin(admin.ModelAdmin):
    pass

################################################################################
# BaseModelAdmin

class BaseModelAdmin(admin.ModelAdmin):
    """
    Base class for 'shared' model admins;
    manages common metadata
    """
    date_hierarchy = 'created'
    search_fields = ['=id', 'name', ]
    list_display = [
        '__str__',
        'view_on_site_link',
        'created_display',
        'updated_display',
    ]
    list_filter = ['created', ]
    readonly_fields = ['id', 'created', 'created_by', 'updated', 'updated_by', ]

    save_on_top = False
    list_per_page = 100

    def view_on_site_link(self, obj):
        url = obj.get_absolute_url()
        html = '<a href="%s" class="link-with-icon link-view">view</a>' % url
        return mark_safe(html)
    view_on_site_link.short_description = 'View'

    def save_model(self, request, obj, form, change):
        today = timezone.now()
        if not change:
            obj.created_by = request.user
            obj.created = today
        obj.updated_by = request.user
        obj.updated = today
        # obj.save()
        super(BaseModelAdmin, self).save_model(request, obj, form, change)


@admin.register(Artist)
class ArtistAdmin(BaseModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(BaseModelAdmin):

    list_filter = BaseModelAdmin.list_filter + ['artist', ]

    def get_list_display(self, request):
        items = self.list_display[:]
        items.insert(1, 'artist')
        items.insert(2, 'year')
        return items


@admin.register(Track)
class TrackAdmin(BaseModelAdmin):

    list_filter = BaseModelAdmin.list_filter + ['album__artist', ]
    filter_horizontal = ['tags', 'tags2', ]

    def get_list_display(self, request):
        items = self.list_display[:]
        items.insert(1, 'album')
        return items

################################################################################

@admin.register(CustomPk)
class CustomPkAdmin(admin.ModelAdmin):
    list_display= ['pk', 'name', ]
