#coding: utf8
from django.db import models

# Create your models here.
class Rout(models.Model):
    """
    流程
    """
    name = models.CharField(max_length=255)


class Actor(models.Model):
    '''
    步骤,属于流程
    '''
    name = models.CharField(max_length=255) # 业务主管审批/专业工程师受理
    rout = models.ForeignKey('workorder.Rout')
    sort = models.IntegerField()


ACTORUSER_TYPE = (
    (0, '固定审批人'),
    (1, '加签审批人'),
)
class ActorUser(models.Model):
    '''
    步骤的处理人
    '''
    name = models.ForeignKey("auth.User", related_name='name')
    actor = models.ForeignKey("workorder.Actor", related_name='actor')
    type = models.CharField(choices=ACTORUSER_TYPE, default=0)


class Order(models.Model):
    """
    工单
    """
    name = models.CharField(max_length=255)
    owner = models.ForeignKey("auth.User", related_name='owner')

    operator = models.ForeignKey('auth.User', null=True, blank=True, related_name='operator')
    description = models.CharField(max_length=255, null=True, blank=True)


class Task(models.Model):
    """
    工单的流转是以任务为主线的
    """
    name = models.CharField(max_length=255)
    actor = models.ForeignKey("workorder.Actor")
    version = models.CharField(max_length=255) # 记录流转过程


class Category1(models.Model):
    """
    工单管理参照变更管理,一共6大类
    """
    name = models.CharField(max_length=255)
    manager = models.ForeignKey("auth.User")

    description = models.CharField(max_length=255, null=True, blank=True)


class Category2(models.Model):
    """
    工单管理参照变更管理,一共39小类
    """
    category1 = models.ForeignKey("workorder.Category1")
    name = models.CharField(max_length=255)

    description = models.CharField(max_length=255, null=True, blank=True)
