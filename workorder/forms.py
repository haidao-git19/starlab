#coding:utf8
__author__ = 'yuan.gao'
from django.contrib.auth.models import User

from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    name = forms.CharField(widget=forms.HiddenInput())
    owner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    state = forms.IntegerField(widget=forms.HiddenInput())
    category2 = forms.ModelChoiceField(
        required = True,
        label='* 类型:',
        queryset=Category2.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'uk-width-1-1',
            }
        )
    )
    purpose = forms.CharField(
        required=True,  # 前端的校验
        label="* 目的:",
        error_messages={'required': "必填项"},
        widget=forms.Textarea(
            attrs={
                'placeholder': u'不能为空',
                'rows': 3,
                'class': 'uk-width-1-1',
            }
        ),
    )
    comment = forms.CharField(
        required=False,  # 前端的校验
        label="备注:",
        error_messages={'required': "必填项"},
        widget=forms.Textarea(
            attrs={
                'placeholder': u'可为空',
                'rows': 3,
                'class': 'uk-width-1-1',
            }
        ),
    )
    description = forms.CharField(
        required=False,  # 前端的校验
        label="描述:",
        error_messages={'required': "必填项"},
        widget=forms.Textarea(
            attrs={
                'placeholder': u'可为空',
                'rows': 3,
                'class': 'uk-width-1-1',
            }
        ),
    )
    class Meta:
        model = Order
        exclude = ['rout', 'enddatetime']

