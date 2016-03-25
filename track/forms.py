#coding:utf8
__author__ = 'Kevin gao'

from django.contrib.auth.models import User

from django import forms
from .models import *
from django.shortcuts import get_object_or_404

class EventCreateForm(forms.ModelForm):
    # 事件类选择，事件级别，标题，详细说明，紧急程度，上传附件
    # offer_people = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    name = forms.CharField(
        # queryset=Rout.objects.all(),
        required=True,
        label="* 事件标题",
        error_messages={'required': "必填项"},
        widget=forms.TextInput(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )

    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        required=True,
        label="* 选择事件类别",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
                'onChange': 'getSiteIdOptions(this.value)',
            }
        ),
    )

    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        required=True,
        label="* 选择事件级别",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )

    status = forms.ModelChoiceField(
        queryset=EventStatus.objects.all(),
        required=True,
        label="* 选择事件状态",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )

    desc = forms.CharField(
        required = True,
        label = "track log",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "后续处理人只能添加不能编辑",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )

    class Meta:
        model = Event
        exclude = ['offer_people', 'comment']


class EventUpdateForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        required=True,
        label="* 选择事件类别",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
                'onChange': 'getSiteIdOptions(this.value)',
            }
        ),
    )

    current_people = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="* 重新选择处理人",
        error_messages={'required': "必填项"},
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        ),
    )

    desc = forms.CharField(
        required = True,
        label = "track log",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "",
                'class': 'uk-width-1-1',
                'rows': 10,
                'readonly': 'true',
            }
        ),
    )

    comment = forms.CharField(
        required = True,
        label = "备注",
        error_messages = {'required': "必填项"},
        widget = forms.Textarea(
            attrs = {
                'placeholder': "所选处理人只能添加不能编辑你的备注",
                'class': 'uk-width-1-1',
                'rows': 3,
            }
        ),
    )
    class Meta:
        model = Event
        fields = ['desc', 'category', 'current_people', 'comment']

    def add_log(self):
        comment = self.cleaned_data['comment']
        event = get_object_or_404(Event, id=self.instance.id)
        event.desc += "\n{}".format(comment)
        event.save()
        print "f"