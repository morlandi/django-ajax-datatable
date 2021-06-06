import uuid
import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from ajax_datatable.utils import format_datetime


class Tag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)

    def __str__(self):
        return self.name


################################################################################
# BaseModel

class BaseModel(models.Model):
    """
    Base class for all models;
    defines common metadata
    """
    class Meta:
        abstract = True
        ordering = ('-created', )  # better choice for UI
        get_latest_by = "-created"

    # Primary key
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
        null=False, blank=False, editable=False)
    name = models.CharField(null=False, blank=False, max_length=256)
    url = models.CharField(null=False, blank=True, max_length=256)

    # metadata
    created = models.DateTimeField(_('created'), null=True, blank=True, )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'), null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    updated = models.DateTimeField(_('updated'), null=True, blank=True, )
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('updated by'), null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" %
            (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_absolute_url(self):
        return self.get_admin_url()

    def created_display(self):
        return format_datetime(self.created)
    created_display.short_description = _('Created')
    created_display.admin_order_field = 'created'

    def updated_display(self):
        return format_datetime(self.updated)
    updated_display.short_description = _('Updated')
    updated_display.admin_order_field = 'updated'

    def save(self, *args, **kwargs):
        today = timezone.now()
        if self.created is None:
            self.created = today
        self.updated = today
        return super(BaseModel, self).save(*args, **kwargs)


class Artist(BaseModel):

    notes = models.TextField(null=False, blank=True)

    class Meta(BaseModel.Meta):
        abstract = False


class Album(BaseModel):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=False, blank=False)
    year = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        abstract = False
        get_latest_by = "-release_date"


class Track(BaseModel):

    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=False, blank=False)
    position = models.IntegerField(default=0, null=False, blank=False)
    tags = models.ManyToManyField(Tag)

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ['position', ]

    def clone(self, request=None):

        if request and not request.user.has_perm('backend.add_song'):
            raise PermissionDenied

        obj = Track.objects.get(id=self.id)
        obj.pk = uuid.uuid4()
        obj.description = increment_revision(self.description)
        obj.save()
        return obj


################################################################################

class CustomPk(models.Model):

    # Primary key
    auto_increment_id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=256)

