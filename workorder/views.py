#coding: utf8
from django.http.response import HttpResponse
from django.views.generic import ListView, CreateView, FormView
from .models import *
from django.http import JsonResponse
from .forms import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class CategoryListView(ListView):
    queryset = Category1.objects.all()
    template_name = "workorder/index.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-category-list"
        return context


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            data = {
                'info': "带星号的为必填项",
                'status': 400,
                'error': form.errors
            }
            return JsonResponse(data)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        # form = OrderForm(
        #     initial={
        #         'owner': 1
        #     }
        # )
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'info': '表单合法,创建成功',
                'status': 200,
                'error': form.errors
            }
            return JsonResponse(data)
        else:
            return response

class OrderCreateView(AjaxableResponseMixin, CreateView):
    form_class = OrderForm
    template_name = ''
    success_url = '/'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(OrderCreateView, self).dispatch(request, *args, **kwargs)
