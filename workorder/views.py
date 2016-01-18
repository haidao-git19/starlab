#coding: utf8
from django.http.response import HttpResponse
from django.views.generic import ListView, CreateView, FormView
from .models import *
from django.http import JsonResponse
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import get_object_or_404
import time
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


class OrderOfUserListView(ListView):
    model = Order
    template_name = 'workorder/order_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(OrderOfUserListView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-order-list-user"
        context['ready_order_list'] = Order.objects.filter(owner=self.request.user).filter(state=0)
        context['working_order_list'] = Order.objects.filter(owner=self.request.user).filter(Q(state=1) | Q(state=2))
        context['closed_order_list'] = Order.objects.filter(owner=self.request.user).filter(state=3)
        context['task_list'] = Task.objects.all()
        return context


class OrderOfEngineerListView(ListView):
    models = Order

    def get_context_data(self, **kwargs):
        context = super(OrderOfEngineerListView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-order-list-engineer"
        return context


@csrf_exempt
def createTask(request):
    '''
    创建一个任务,状态为1:审批中
    :param request:
    :return:
    '''
    order_id = request.POST.get('id')
    try:
        order_object = get_object_or_404(Order, id=order_id)
        rout = get_object_or_404(Rout, id=order_object.rout.id)
        actor = get_object_or_404(Actor, rout=rout, sort='0')
        task = Task.objects.create(name='任务:{}-({}{})'.format(order_object.purpose,
                                                              request.user.last_name,
                                                              request.user.first_name),
                                   order=order_object,
                                   actor=actor,
                                   version='[{}]{}{}发起审批\n'.format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                               request.user.last_name,
                                                               request.user.first_name)
                                   )
        order_object.state = 1
        order_object.save()
        data = {
            'return': '任务已创建并通知类别主管({}{}),任务ID:{}'.format(order_object.category2.category1.manager.last_name,
                                                          order_object.category2.category1.manager.first_name,
                                                          task.id)
        }
        return JsonResponse(data, status=200)
    except Exception, e:
        data = {
            'return': e
        }
        return JsonResponse(data, status=400)
