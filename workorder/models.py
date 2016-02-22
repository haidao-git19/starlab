#coding: utf8
from django.db import models

# Create your models here.
class Rout(models.Model):
    """
    流程
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "流程模板"
        verbose_name_plural = "流程模板"


class Actor(models.Model):
    '''
    步骤,属于流程
    '''
    name = models.CharField(max_length=255) # 业务主管审批/专业工程师受理
    rout = models.ForeignKey('workorder.Rout')
    sort = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "分步骤"
        verbose_name_plural = "分步骤"


ACTORUSER_TYPE = (
    (0, '固定审批人'),
    (1, '加签审批人'),
)
class ActorUser(models.Model):
    '''
    步骤的处理人
    '''
    name = models.ForeignKey("auth.User", related_name='actorusername')
    actor = models.ForeignKey("workorder.Actor", related_name='actoruseractor')
    type = models.IntegerField(choices=ACTORUSER_TYPE, default=0)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        verbose_name = "步骤处理人"
        verbose_name_plural = "步骤处理人"


class CurrentActorUser(models.Model):
    '''
    当前处理人,在ActorUser的基础上,增加了加签的人
    '''
    # new
    task = models.ForeignKey('workorder.Task', related_name='task')
    # old
    name = models.ForeignKey("auth.User", related_name='currentactorusername')
    actor = models.ForeignKey("workorder.Actor", related_name='currentactoruseractor')
    type = models.IntegerField(choices=ACTORUSER_TYPE, default=0)
    state = models.NullBooleanField(default=None)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        verbose_name = "当前步骤处理人"
        verbose_name_plural = "当前步骤处理人"


STATE_CHOICES = (
    (0, '待创建任务'),
    (1, '工单审批中'),
    (2, '工单分发中'),
    (3, '工单实施中'),
    (4, '工单已关闭'),
)
class Order(models.Model):
    """
    工单
    """
    name = models.CharField(max_length=255, verbose_name='工单编号')
    owner = models.ForeignKey("auth.User")
    startdatetime = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name="状态")
    # category1 = models.ForeignKey("workorder.Category1", related_name='ordercategory1')
    category2 = models.ForeignKey("workorder.Category2", related_name='ordercategory2', verbose_name='类型')
    rout = models.ForeignKey("workorder.Rout",default=1, related_name='orderrout')

    enddatetime = models.DateTimeField(null=True, blank=True)
    purpose = models.CharField(max_length=5000, null=True, blank=True, verbose_name='目的') # 申请人填写申请目的
    comment = models.CharField(max_length=5000, null=True, blank=True, verbose_name='备注') # 操作人加上去的
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "工单"
        verbose_name_plural = "工单"
        ordering = ['-state']


TASK_STATE_CHOICES = (
    (0, '新创建任务'),
    (1, '任务审批中'),
    (2, '任务分发中'),
    (3, '任务实施中'),
    (4, '任务已结束'),
)
class Task(models.Model):
    """
    工单的流转是以任务为主线的
    """
    name = models.CharField(max_length=255)
    order = models.ForeignKey('workorder.Order', related_name='taskorder')
    actor = models.ForeignKey("workorder.Actor", related_name='taskactor')
    operator = models.ForeignKey('auth.User', null=True, blank=True, related_name='taskoperator')
    version = models.CharField(max_length=5000) # 记录流转过程
    state = models.IntegerField(choices=TASK_STATE_CHOICES, default=0, verbose_name="状态")
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        ordering = ['state']


class Category1(models.Model):
    """
    工单管理参照变更管理,一共6大类
    """
    name = models.CharField(max_length=255)
    manager = models.ForeignKey("auth.User", related_name='category1manager')
    defaultOperator = models.ForeignKey("auth.User", related_name='categorydefaultuser')
    group = models.ForeignKey("auth.Group", related_name='category1group')

    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "大类"
        verbose_name_plural = "大类"
        ordering = ['id']


class Category2(models.Model):
    """
    工单管理参照变更管理,一共39小类
    """
    category1 = models.ForeignKey("workorder.Category1", related_name='category')
    name = models.CharField(max_length=255)

    auto_template = models.TextField(max_length=5000, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "{} -- {}".format(self.category1.name, self.name)

    class Meta:
        verbose_name = "小类"
        verbose_name_plural = "小类"
        ordering = ['category1', 'id']


class ProposerManager(models.Model):
    """
    申请人的负责人先审批
    """
    group = models.ForeignKey("auth.Group")
    user = models.ForeignKey("auth.User")

    def __unicode__(self):
        return "{}-{}".format(self.group.name, self.user.username)