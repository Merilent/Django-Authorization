from rest_framework import permissions
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


class ISCheckPermission(permissions.BasePermission):
    '''
    Inherites permissions class to create custom permission
    to check user has assign any super users.
    '''
    def has_permission(self, request, view, *args,**kwargs):
        logger.info('ISCheckPermission Started.')
        if str(request.user) == 'AnonymousUser':
            request._cached_user = get_user(request)
            user_name = request._cached_user
        else:
            user_name = request.user
        user_list = []
        user = User.objects.get(username=user_name).id or []
        superuser_list = SuperUser.objects.filter(super_user_id=user).values('user_id') or []
        if superuser_list:
            new_list = list(map(lambda x: x['user_id'], superuser_list))
            user_list = list(set(new_list))

        logger.info('ISCheckPermission Ended.')
        if user_list:
            return True
        else:
            return False


class Authorize(object):
    '''
    Multiple parameter pass in argument
    '''
    def __init__(self, argument=[]):
        self.group_name = argument

    def __call__(self, fn):
        ''' To check group level permissions
        user assign in predefined group than he authorize user
        '''
        def check_permission(request):
            group_name = self.group_name
            logger.info('Authorize Started.')
            if str(request.user) == 'AnonymousUser':
                request._cached_user = get_user(request)
                user_name = request._cached_user
            else:
                user_name = request.user

            user = User.objects.get(username=user_name).id or []
            # find out user list of predefined group and also check parent group
            if group_name and user_name:
                group_ids = [x.id for x in Group.objects.filter(name__in=group_name)]
                super_group_ids = [x.super_group_id for x in GroupPermissions.objects.filter(group__in=group_ids)]
                if super_group_ids:
                    group_ids.extend(super_group_ids)
                user_list = [x.id for x in User.objects.filter(groups__in=group_ids)]

                logger.info('Authorize Ended.')
                if user in user_list:
                    return fn(request)
                else:
                    raise PermissionDenied
            else:
                return fn(request)
        return check_permission

