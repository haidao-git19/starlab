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
from django import forms
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
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderOfEngineerListView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-order-list-engineer"
        return context


class TaskListView(ListView):
    model = Task
    template_name = 'workorder/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-task-list"
        context['task_list'] = Task.objects.filter(order__category2__category1__manager=self.request.user)
        category1_objects = Category1.objects.filter(manager=self.request.user)
        print category1_objects
        group_name = []
        for category1_object in category1_objects:
            group_name.append(category1_object.group.name)
        print group_name
        class GroupUserForm(forms.Form):
            users = forms.ModelChoiceField(
                queryset=User.objects.filter(groups__name__in=group_name).all().distinct(),
                # queryset=User.objects.filter(groups__name__in=['PE']).all(),
                widget=forms.Select(
                    attrs={
                        'class': 'uk-width-1-1',
                    }
                ),
            )
        form = GroupUserForm()
        context['form'] = form
        return context


class TaskListEngineerView(ListView):
    model = Task
    template_name = 'workorder/task_list_engineer.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListEngineerView, self).get_context_data(**kwargs)
        context['current_page'] = "workorder-task-list-engineer"
        context['task_list'] = Task.objects.filter(operator=self.request.user)
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
                                   state=1,
                                   version='[{}]{}{}发起申请\n'.format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
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

@csrf_exempt
def dispense(request):
    '''
    任务分发,按组
    :param request:
    :return:
    '''
    id = request.POST.get('users')
    task_id = request.POST.get('task_id')
    task = get_object_or_404(Task, id=task_id)
    order = task.order
    order.state = 2
    order.save()
    if id:
        user = get_object_or_404(User, id=id)
        task.version += "[{}]由{}{}分发给{}{}\n".format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                    request.user.last_name,
                                                    request.user.first_name,
                                                    user.last_name,
                                                    user.first_name)
        task.operator = user
        task.state = 2 # 实施中
        task.save()
        data = {
            'user_name': "{}{}".format(user.last_name, user.first_name),
            'status': 200,
        }
    else:
        data = {
            'status': 400,
            'error': '不能为空',
        }
    return JsonResponse(data, status=200)

@csrf_exempt
def complete(request):
    taskid = request.POST.get('taskid')
    comment = request.POST.get('comment')
    if comment:
        task_object = get_object_or_404(Task, id=taskid)
        task_object.version += "[{}]由{}{}完成并备注:{}\n".format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                         request.user.last_name,
                                         request.user.first_name,
                                         comment)
        task_object.state = 3
        task_object.save()
        order_object = task_object.order
        order_object.comment = comment
        order_object.state = 3
        order_object.save()
        data = {
            'return': '任务结束,ID:{}'.format(taskid)
        }
        return JsonResponse(data, status=200)
    else:
        data = {
            'return': '处理结果不能为空哦'
        }
    return JsonResponse(data, status=400)