from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from .models import Trac
from . import defaults as defs


def trac_get_type_id_by_name(trac_type_name):
    """
    Returns a numeric version of a trac type.
    """
    for t in Trac.TRACWARE_TYPE_OPTIONS:
        if trac_type_name.lower() == t[1].lower():
            return t[0]
    return 0


def trac_get_type_name_by_id(trac_type_id):
    """
    Returns a string version of a trac type.
    """
    for t in Trac.TRACWARE_TYPE_OPTIONS:
        if trac_type_id == t[0]:
            return t[1]
    return 'Unknown_Trac'


def trac_get_cache_key(uid, oid, cid, tid):
    """
    Build a cache key for trac.
    """
    trac_key_token = [
        'trac',
        Site.objects.get_current().domain,
        uid,  # user
        oid,  # instance
        cid,  # content type
        tid,  # trac type
    ]
    cache_key = '-'.join([str(t) for t in trac_key_token])
    return cache_key


def trac_exists(user, obj, trac_type):
    """
    True if Trac exists.
    """
    trac = trac_get_trac_for_user(user, obj, trac_type)
    if not trac:
        return False
    return True


def trac_get_tracs_for_model(model, user=None, trac_type=None):
    """
    Returns tracs for a specific model.
    """
    content_type = ContentType.objects.get_for_model(model)
    qs = Trac.objects.filter(content_type=content_type)
    if user:
        qs = qs.filter(user=user)
    if trac_type:
        qs = qs.filter(trac_type=trac_type)
    return qs


def trac_get_tracs_for_object(obj, user=None, trac_type=None):
    """
    Returns tracs for a specific object.
    """
    content_type = ContentType.objects.get_for_model(type(obj))
    qs = Trac.objects.filter(content_type=content_type, object_id=obj.pk)
    if user:
        qs = qs.filter(user=user)
    if trac_type:
        qs = qs.filter(trac_type=trac_type)
    return qs


def trac_get_tracs_for_user(user, trac_type=None):
    """
    Returns tracs for a specific user.
    """

    qs = Trac.objects.filter(user=user)
    if trac_type:
        qs = qs.filter(trac_type=trac_type)
    return qs


def trac_get_trac_for_user(user, obj, trac_type):
    """
    Returns a specific trac of a specific type for a specific user.
    """
    trac = None
    content_type = ContentType.objects.get_for_model(type(obj))
    try:
        trac = Trac.objects.get(user=user, content_type=content_type, object_id=obj.pk, trac_type=trac_type)
    except Trac.DoesNotExist:
        pass
    return trac


def trac_get_or_create(user, obj, trac_type):
    """
    Get or create a trac.
    """
    trac = trac_get_trac_for_user(user, obj, trac_type)
    if trac is None:
        content_type = ContentType.objects.get_for_model(type(obj))
        trac = Trac(user=user, content_type=content_type, object_id=obj.pk, content_object=obj, trac_type=trac_type)
        trac.save()
    return trac


def trac_delete(user, obj, trac_type):
    """
    Delete a trac.
    """
    trac = trac_get_trac_for_user(user, obj, trac_type)
    if trac is not None:
        trac.delete()
    return trac


def trac_get_stats_for_obj(obj):
    """
    Fill up the proper stat counts.
    """
    stat_dict = {}
    for ttype in defs.TRACWARE_TRAC_COUNTER_TYPES:
        stat_dict[ttype] = '-1'
        if hasattr(obj, ttype):
            stat_dict[ttype] = obj.__dict__[ttype]
    return stat_dict


def trac_delete_trac_for_object(sender, instance, **kwargs):
    """
    Delete a matching trac when an instance object is deleted.
    """
    tracs = util.trac_get_tracs_for_object(obj=instance)
    for trac in tracs:
        trac.delete()
