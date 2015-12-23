# coding:utf8
from django.db import models
from django.contrib import admin



# 项目申请后，任务列表插入一条记录.用户审批通过或者拒绝后，
# update当前步骤ID（上一步骤或者下一步骤）.某个步骤可能有多个审批人，
# 如果要审批，必须先检出.version字段是为了乐观锁控制，保证只能有一人检出.

# 每个步骤的操作，都写入任务历史记录

# 流程草稿状态是可以修改删除，发布状态就不能修改和删除，
# 只能新增一个版本，或者新增一个流程，或者停止流程。

# 步骤序号是步骤执行的顺序，审批的时候，根据当前序号，
# 查找下一步骤，然后将下一步骤update任务列表的步骤ID,审批拒绝，
# 则查找上一步骤，然后update任务列表的步骤ID

# 一个步骤，是有多个处理人。处理人先检出任务列表，然后才能审批。


# Create your models here.
STATE_CHOICES = (
    (0, '待审批'),
    (1, '审批中'),
    (2, '已关闭'),
)

TYPE_CHOICES = (
    (0, '常规变更'),
    (1, '紧急变更'),
)
import datetime
# 工单
class Item(models.Model):
    itemName = models.CharField(max_length=255)
    routID = models.ForeignKey("workflow.Rout", verbose_name="使用流程")
    applyUserId = models.ForeignKey("auth.User", verbose_name="申请人")
    state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name="版本类型")
    itemType = models.IntegerField(choices=TYPE_CHOICES, default=0)
    reason = models.CharField(null=True, blank=True, max_length=50, verbose_name="原因")
    content = models.CharField(null=True, blank=True, max_length=50, verbose_name="内容")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    incidence = models.TextField(null=True, blank=True, max_length=5000, verbose_name="影响范围")
    operation = models.TextField(null=True, blank=True, max_length=5000, verbose_name="具体操作")
    rollback = models.TextField(null=True, blank=True, max_length=5000, verbose_name="回滚")
    comment = models.TextField(null=True, blank=True, max_length=5000, verbose_name="注释")


    def __unicode__(self):
        return u"{}({})".format(self.itemName, self.get_state_display())

    class Meta:
        verbose_name = "工单"
        verbose_name_plural = "工单"
        ordering = ['-start_time', ]

    def get_absolute_url(self):
        """
            one of usages:
            <a href="{{ object.get_absolute_url }}">{{ object.name }}</a>
        """
        from django.core.urlresolvers import reverse
        return reverse('workflow:item-detail', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     from .views import createTask
    #     createTask(self.id)
    #     super(self.__class__, self).save(*args, **kwargs)

STATE_CHOICES1 = (
    (0, '检出'),
    (1, '结束'),
)

STATE_CHOICES2 = (
    (0, '草稿'),
    (1, '已发布'),
    (2, '停止'),
)


class TaskList(models.Model):
    itemId = models.ForeignKey(Item, verbose_name="工单")
    actorId = models.ForeignKey("workflow.Actor", verbose_name="步骤")
    state = models.IntegerField(choices=STATE_CHOICES1, default=1)
    version = models.CharField(max_length=500, default=u"[任务开始]\n")

    def __unicode__(self):
        return u"{}--({})".format(self.itemId, self.actorId)

    class Meta:
        verbose_name = "任务列表"
        verbose_name_plural = "任务列表"
        ordering = ['-id', ]


# 流程 第一步,第二步等等
class Rout(models.Model):
    routName = models.CharField(max_length=255)
    deptId = models.CharField(max_length=50)
    version = models.IntegerField()
    state = models.IntegerField(choices=STATE_CHOICES2)

    def __unicode__(self):
        return u"{}({})".format(self.routName, self.get_state_display())

    class Meta:
        verbose_name = "流程"
        verbose_name_plural = "流程"


# 步骤
class Actor(models.Model):
    sortNo = models.IntegerField(verbose_name="步骤编号(从1开始)")
    actorName = models.CharField(max_length=50)
    routId = models.ForeignKey(Rout)

    def __unicode__(self):
        return u"{}--{}".format(self.routId, self.actorName)

    class Meta:
        verbose_name = "步骤"
        verbose_name_plural = "步骤"
        ordering = ['routId', ]

# 步骤处理人

ACTORUSER_TYPE = (
    (0, '固定审批人'),
    (1, '加签审批人'),
)
class ActorUser(models.Model):
    actorId = models.ForeignKey(Actor)
    type = models.IntegerField(choices=ACTORUSER_TYPE, default=0)
    operateUserId = models.ForeignKey("auth.User")
    state = models.NullBooleanField(default=None)

    def __unicode__(self):
        return u"{}--{}({})决定是否通过:{}".format(self.actorId, self.operateUserId.username, self.get_type_display(), self.state)

    class Meta:
        verbose_name = "步骤处理人"
        verbose_name_plural = "步骤处理人"
        ordering = ['actorId', ]


class CurrentActorUser(models.Model):
    # new
    task = models.ForeignKey('workflow.TaskList')
    comment = models.CharField(max_length=255, blank=True, null=True)
    # old
    actorId = models.ForeignKey('workflow.Actor')
    type = models.IntegerField(choices=ACTORUSER_TYPE, default=0)
    operateUserId = models.ForeignKey('auth.User')
    state = models.NullBooleanField(default=None)

    def __unicode__(self):
        return u"{}--{}({})决定是否通过:{}".format(self.task, self.operateUserId.username, self.get_type_display(), self.state)

class TaskHistory(models.Model):
    itemId = models.ForeignKey(Item)
    actorId = models.ForeignKey(Actor)
    memo = models.CharField(max_length=255)
    operateUserId = models.ForeignKey("auth.User")
    createDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "任务历史记录"
        verbose_name_plural = "任务历史记录"


admin.site.register(Item)
admin.site.register(TaskList)
admin.site.register(Rout)
admin.site.register(Actor)
admin.site.register(ActorUser)
admin.site.register(CurrentActorUser)
admin.site.register(TaskHistory)
# ----------------------------------


class NewChangeApply(models.Manager):

    def get_queryset(self):
        superclass = super(NewChangeApply, self)
        return superclass.get_queryset().filter(gopass=None)


class CloseChangeApply(models.Manager):

    def get_queryset(self):
        superclass = super(CloseChangeApply, self)
        return superclass.get_queryset().filter(gopass=False)


class PassChangeApply(models.Manager):

    def get_queryset(self):
        superclass = super(PassChangeApply, self)
        return superclass.get_queryset().filter(gopass=True)


class ChangeApply(models.Model):
    name = models.CharField(max_length=50)
    reason = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    operator = models.ForeignKey("auth.User")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    incidence = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)
    rollback = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    add_sign = models.ManyToManyField("auth.User", related_name="signer")
    gopass = models.NullBooleanField(null=True, default=None)
    # add_sign = models.ManyToManyField("workflow.Sign")

    objects = models.Manager()
    newapplys = NewChangeApply()
    closeapplys = CloseChangeApply()
    passapplys = PassChangeApply()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "变更申请"
        verbose_name_plural = "变更申请"


class Sign(models.Model):
    operator = models.ForeignKey("auth.User")
    add_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)
    agree = models.BooleanField(default=False)
    comment = models.CharField(max_length=255)

    def __unicode__(self):
        return self.comment

    class Meta:
        verbose_name = "加签"
        verbose_name_plural = "加签"


# admin.site.register(ChangeApply)
# admin.site.register(Sign)


# class PollManager(models.Manager):
#     def with_counts(self):
#         from django.db import connection
#         cursor = connection.cursor()
#         cursor.execute("""
#             SELECT p.id, p.question, p.poll_date, COUNT(*)
#             FROM polls_opinionpoll p, polls_response r
#             WHERE p.id = r.poll_id
#             GROUP BY p.id, p.question, p.poll_date
#             ORDER BY p.poll_date DESC""")
#         result_list = []
#         for row in cursor.fetchall():
#             p = self.model(id=row[0], question=row[1], poll_date=row[2])
#             p.num_responses = row[3]
#             result_list.append(p)
#         return result_list
