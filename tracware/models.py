from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes import generic
from django.contrib.auth import get_user_model
from django.core.cache import cache

from . import defaults as defs

User = get_user_model()


@python_2_unicode_compatible
class Trac(models.Model):
    """
    Trac(k) objects for this user.
    """
    TRACWARE_TYPE_LIKE = 1
    TRACWARE_TYPE_STAR = 2
    TRACWARE_TYPE_WATCH = 3
    TRACWARE_TYPE_FOLLOW = 4
    TRACWARE_TYPE_BOOKMARK = 5
    TRACWARE_TYPE_OPTIONS = (
        (TRACWARE_TYPE_LIKE, "Like"),
        (TRACWARE_TYPE_STAR, "Star"),
        (TRACWARE_TYPE_WATCH, "Watch"),
        (TRACWARE_TYPE_FOLLOW, "Follow"),
        (TRACWARE_TYPE_BOOKMARK, "Bookmark"),
    )

    user = models.ForeignKey(User, related_name="%(class)s")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    trac_type = models.IntegerField(choices=TRACWARE_TYPE_OPTIONS)

    class Meta:
        verbose_name = _('trac')
        verbose_name_plural = _('tracs')
        unique_together = (('user', 'content_type', 'object_id', 'trac_type'),)

    def __str__(self):
        return u'{0}-[{1}]'.format(self.user, self.content_object)
