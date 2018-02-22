from threading import local
try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django.contrib.auth import get_user
from .models import *
from django.core.exceptions import PermissionDenied
_user = local()
import logging
logger = logging.getLogger(__name__)
import memcache
from django.conf import settings


class Authorize(object):
    '''
    Multiple parameter pass in argument
    '''
    def __init__(self, argument=[]):
        self.group_name = argument

    def __call__(self, fn):
        ''' To check group level permissions
        if user belong to group present in predefined group of argument than he authorize user
        '''
        def check_permission(request):
            group_name = self.group_name
            # here cache connections
            cache_location = settings.CACHES['default']['LOCATION']
            mc = memcache.Client([str(cache_location)])
            logger.info('Authorize Started.')
            if str(request.user) == 'AnonymousUser':
                request._cached_user = get_user(request)
                user_name = request._cached_user
            else:
                user_name = request.user

            if group_name and user_name:
                user = User.objects.get(username=user_name).id or 0
                # first user group check in memory cache if not present than check in database
                # here code for check user group in memory cache
                cache_group_name = mc.get(str(user)) or []
                if isinstance(cache_group_name, str):
                    cache_group_name = eval(cache_group_name)
                if set(group_name) & set(cache_group_name):
                    logger.info('user are authorize')
                    return fn(request)
                else:
                    # find out user list of passing in argument of the group list and also check parent group
                    group_ids = [x.id for x in Group.objects.filter(name__in=group_name)]
                    super_group_ids = [x.super_group_id for x in GroupPermissions.objects.filter(group__in=group_ids)]
                    if super_group_ids:
                        group_ids.extend(super_group_ids)
                    # To calculate total no of user in group list
                    user_list = [x.id for x in User.objects.filter(groups__in=group_ids)]

                    logger.info('Authorize Ended.')
                    # To check user are present in user list
                    if user in user_list:
                        # To calculate current user group list
                        user_group_ids = [x.id for x in Group.objects.filter(user=user)]
                        super_user_group_ids = [x.group_id for x in
                                           GroupPermissions.objects.filter(super_group__in=user_group_ids)]
                        if super_user_group_ids:
                            user_group_ids.extend(super_user_group_ids)
                        user_group_name = [x.name for x in Group.objects.filter(id__in=user_group_ids)]
                        # User and group list store in memory cache for 300000 second timeperiod after the cache is clear
                        response = mc.set(str(user), str(user_group_name), 300000)
                        logger.info('User group data store in cache')
                        return fn(request)
                    else:
                        raise PermissionDenied
            else:
                return fn(request)
        return check_permission

# class ISCheckPermission(permissions.BasePermission):
#     ''' Inherites default Authorization permission class in that we have check user has assign manager
#         then manager should be access child records'''
#     def has_permission(self, request, view, *args,**kwargs):
#         logger.info('ISCheckPermission Started.')
#         if str(request.user) == 'AnonymousUser':
#             request._cached_user = get_user(request)
#             user_name = request._cached_user
#         else:
#             user_name = request.user
#         user_list = []
#         user = User.objects.get(username=user_name).id or []
#         superuser_list = SuperUser.objects.filter(super_user_id=user).values('user_id') or []
#         if superuser_list:
#             new_list = list(map(lambda x: x['user_id'], superuser_list))
#             user_list = list(set(new_list))
#
#         logger.info('ISCheckPermission Ended.')
#         if user_list:
#             return True
#         else:
#             return False
