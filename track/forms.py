#coding:utf8
__author__ = 'Kevin gao'

from django.contrib.auth.models import User

from django import forms
from .models import *

class EventForm(forms.ModelForm):
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
        required = False,
        label = "备注",
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
        model = Event
        exclude = ['offer_people']