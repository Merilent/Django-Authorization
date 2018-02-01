from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.


class SuperUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='SuperUser', on_delete=models.CASCADE)
    super_user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_super_user'

    def __str__(self):
        return self.user.username


class GroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.OneToOneField(Group, related_name='GroupPermissions', on_delete=models.CASCADE)
    super_group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_group_permissions'


