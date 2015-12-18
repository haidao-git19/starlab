# coding:utf8
__author__ = 'yuan.gao'
from django import forms
from .models import *
from django.contrib.auth.models import User

# itemName = models.CharField(max_length=255)
# routID = models.ForeignKey("workflow.Rout", verbose_name="使用流程")
# applyUserId = models.ForeignKey("auth.User", verbose_name="申请人")
# state = models.IntegerField(choices=STATE_CHOICES, default=0)
# itemType = models.IntegerField(null=True, blank=True)
# reason = models.CharField(null=True, blank=True, max_length=50, verbose_name="原因")
# content = models.CharField(null=True, blank=True, max_length=50, verbose_name="内容")
# start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
# end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
# incidence = models.CharField(null=True, blank=True, max_length=255, verbose_name="影响范围")
# operation = models.CharField(null=True, blank=True, max_length=255, verbose_name="具体操作")
# rollback = models.CharField(null=True, blank=True, max_length=255, verbose_name="回滚")
# comment = models.CharField(null=True, blank=True, max_length=255, verbose_name="注释")

TYPE_CHOICES = (
    (0, '常规变更'),
    (1, '紧急变更'),
)
class ItemCreateForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ItemCreateForm, self).__init__(*args, **kwargs)
    #     initial = kwargs.get('initial', {})
    #     # initial['project'] = Project.objects.order_by('-add_date')[0]
    #     kwargs['initial'] = initial

    itemName = forms.CharField(
        required = True,
        label = "* 变更名称",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.TextInput(
            attrs = {
                'class': 'uk-width-1-1',
            }
        ),
    )

    routID = forms.ModelChoiceField(
        queryset=Rout.objects.all(),
        required=True,
        label="* 选择流程模板",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )

    applyUserId = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required = True,
        label = "* 申请人",
        help_text = "注意:默认为当前登录用户,请不要随意修改",
        error_messages = {'required': "必填项"},
        widget = forms.Select(
            attrs = {
                'class': 'uk-width-1-1',
            }
        ),
    )


    itemType = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=True,
        label="发布类型",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )


    reason = forms.CharField(
        required = True,
        label = "* 变更原因",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "最大可以输入50字",
                'class': 'uk-width-1-1',
                'rows': 2,
            }
        ),
    )

    content = forms.CharField(
        required = True,
        label = "* 变更内容",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.TextInput(
            attrs = {
                'placeholder': "最大可以输入50字",
                'class': 'uk-width-1-1',
                'rows': 4,
            }
        ),
    )

    start_time = forms.CharField(
        label="计划开始时间",
        required=False,
        help_text="要加时间,按此格式：2015-05-01 14:00",
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': "若只有日期,时间默认为00:00",
                'data-uk-datepicker': u"{format:'YYYY-MM-DD'}",
                'class': 'uk-width-1-1',
            }
        ),
    )

    end_time = forms.CharField(
        label="计划结束时间",
        required=False,
        help_text="要加时间,按此格式：2015-05-01 14:00",
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': "若只有日期,时间默认为00:00",
                'data-uk-datepicker': u"{format:'YYYY-MM-DD'}",
                'class': 'uk-width-1-1',
            }
        ),
    )

    incidence = forms.CharField(
        required = True,
        label = "* 影响范围",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "最大可以输入5000字,不够再加",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )

    operation = forms.CharField(
        required = True,
        label = "* 具体操作",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "最大可以输入5000字",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )

    rollback = forms.CharField(
        required = True,
        label = "* 回滚方案",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "最大可以输入5000字",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )

    comment = forms.CharField(
        required = False,
        label = "备注",
        # help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "最大可以输入5000字",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )


    class Meta:
        model = Item
        # fields = '__all__'
        exclude = ['state']
        # uncomment this line and specify any field to exclude it from the form