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
from DingDing import DingDing
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User, Group
import json
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
        context['working_order_list'] = Order.objects.filter(owner=self.request.user).filter(Q(state=1) | Q(state=2) | Q(state=3))
        context['closed_order_list'] = Order.objects.filter(owner=self.request.user).filter(state=4)
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
        # 待分发任务列表-在前端区分任务状态
        # caus = CurrentActorUser.objects.filter(name=self.request.user)
        # task_list = []
        # for cau in caus:
        #     if cau.task.state == 2:
        #         task_list.append(cau.task)
        # print task_list
        # context['task_list'] = task_list
        context['task_list'] = Task.objects.filter(order__category2__category1__manager=self.request.user)
        # 待审批任务
        context['current_actor_users'] = CurrentActorUser.objects.filter(name=self.request.user)
        category1_objects = Category1.objects.filter(manager=self.request.user)
        print category1_objects
        group_name = []
        for category1_object in category1_objects:
            group_name.append(category1_object.group.name)
        context['group_name'] = group_name
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
        # 找到订单
        order_object = get_object_or_404(Order, id=order_id)
        # 第一步流程与获得的申请人主管结合成一个审批实体
        rout_object = get_object_or_404(Rout, id=order_object.rout.id)
        actor_object1 = get_object_or_404(Actor, rout=rout_object, sort='1')
        # actor_object2 = get_object_or_404(Actor, rout=rout_object, sort='2')
        # 获得申请人主管
        proposer_group = Group.objects.none()
        proposer_groups = order_object.owner.groups.all()


        queryset_list = []

        for pg in proposer_groups:
            proposer_group = pg
            break
        print proposer_group
        try:
            porposer_manager = get_object_or_404(ProposerManager, group=proposer_group).user
        except Exception, e:
            data = {
                'return': "您的主管未设定,请联系管理员\n({})".format(str(e))
            }
            return JsonResponse(data, status=400)

        catogory_manager = order_object.category2.category1.manager
        if catogory_manager:
            pass
            # queryset_list.append(CurrentActorUser(task=task, name=catogory_manager, actor=actor_object2))
        else:
            data = {
                'return': "所选工单类主管未设定或者未开始服务,请联系管理员"
            }
            return JsonResponse(data, status=400)

        # 创建工单对应任务
        task = Task.objects.create(name='任务:{}-({}{})'.format(order_object.purpose,
                                                              request.user.last_name,
                                                              request.user.first_name),
                                   order=order_object,
                                   actor=actor_object1,
                                   state=1,
                                   version='[{}]{}{}发起申请\n'.format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                               request.user.last_name,
                                                               request.user.first_name)
                                   )
        # 创建当前审批人与流程和任务绑定
        queryset_list.append(CurrentActorUser(task=task, name=porposer_manager, actor=actor_object1))
        # queryset_list.append(CurrentActorUser(task=task, name=porposer_manager, actor=actor_object2))
        CurrentActorUser.objects.bulk_create(queryset_list)

        order_object.state = 1 # 审批中
        order_object.save()
        # --------------------- ding -------------------------------------------------------------------------
        dd = DingDing()
        proposer_group = Group.objects.none()
        proposer_groups = order_object.owner.groups.all()
        for pg in proposer_groups:
            proposer_group = pg
            break
        # querysets 不支持切片操作,只有出此下策
        print proposer_group
        # 这里只取第一个组
        id = porposer_manager.username
        print id
        url = request.build_absolute_uri(reverse('workorder:list-task'))
        jsonmsg = {
            "title": "您的组员({}{})有一个工单需要审批".format(order_object.owner.last_name, order_object.owner.first_name),
            "text": "{}".format(order_object.purpose),
            "picUrl": "@lALOACZwe2Rk",
            "messageUrl": url,
        }
        dd.send_link_message(ddID=id, json_content=jsonmsg)
        # --------------------- ding -------------------------------------------------------------------------
        data = {
            'return': '任务已创建并通知您的主管({}{})审批,任务ID:{}'.format(order_object.category2.category1.manager.last_name,
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
def agree(request):
    taskid = request.POST.get('taskid')
    comment = request.POST.get('comment')

    task_object = get_object_or_404(Task, id=taskid)
    # 通过任务拿到表单再拿到所用流程模板
    rout_in_use = task_object.order.rout
    # 流程模板有几个步骤
    actor_count = Actor.objects.filter(rout=rout_in_use).count()
    # 如果当前步骤的sort和count相同说明审批的流程已经结束,任务状态和工单状态均改变为分发2
    if task_object.actor.sort == actor_count:
        task_object.state = 2 # 审批结束
        task_object.version += "[{}]{}{}审批通过并备注:{}\n".format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                             request.user.last_name,
                                             request.user.first_name,
                                             comment)
        task_object.save() # debug了很久,我居然忘记了save -.-
        order_object = task_object.order
        order_object.comment = comment
        order_object.state = 2 # 审批结束
        order_object.save()
        # --------------------- ding -------------------------------------------------------------------------
        dd = DingDing()
        category_manager = order_object.category2.category1.manager
        id = category_manager.username
        url = request.build_absolute_uri(reverse('workorder:list-task'))
        jsonmsg = {
            "title": "您的组收到一个工单,请分发(申请人:{}{}).".format(order_object.owner.last_name, order_object.owner.first_name),
            "text": "{}".format(order_object.purpose),
            "picUrl": "@lALOACZwe2Rk",
            "messageUrl": url,
        }
        dd.send_link_message(ddID=id, json_content=jsonmsg)
        # --------------------- ding -------------------------------------------------------------------------

        # 删除临时审批表里此任务的条目
        CurrentActorUser.objects.filter(task=task_object).all().delete()
        data = {
            'return': '成功:已通知类别主管({}{})分发工单,ID:{}'.format(category_manager.last_name, category_manager.first_name, order_object.name),
            'id': taskid
        }
        return JsonResponse(data, status=200)
    else:
        # TODO
        pass

@csrf_exempt
def disagree(request):
    pass

@csrf_exempt
def addsign(request):
    pass

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
    order.state = 3
    if id:
        user = get_object_or_404(User, id=id)
        task.version += "[{}]由{}{}分发给{}{}\n".format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                    request.user.last_name,
                                                    request.user.first_name,
                                                    user.last_name,
                                                    user.first_name)
        task.operator = user
        task.state = 3 # 实施中
        task.save()
        # --------------------- ding -------------------------------------------------------------------------
        dd = DingDing()
        id = user.username
        url = request.build_absolute_uri(reverse('workorder:list-task-engineer'))
        jsonmsg = {
            "title": "收到一个任务.(分发人:{}{})".format(request.user.last_name, request.user.first_name),
            "text": "{}".format(order.purpose),
            "picUrl": "@lALOACZwe2Rk",
            "messageUrl": url,
        }
        dd.send_link_message(ddID=id, json_content=jsonmsg)
        # --------------------- ding -------------------------------------------------------------------------
        data = {
            'user_name': "{}{}".format(user.last_name, user.first_name),
            'status': 200,
        }
    else:
        data = {
            'status': 400,
            'error': '不能为空',
        }
    order.save()
    return JsonResponse(data, status=200)

@csrf_exempt
def complete(request):
    taskid = request.POST.get('taskid')
    comment = request.POST.get('comment')
    if comment:
        task_object = get_object_or_404(Task, id=taskid)
        task_object.version += "[{}]由{}{}完成并备注:{}".format(time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                         request.user.last_name,
                                         request.user.first_name,
                                         comment)
        task_object.state = 4 # 任务结束
        task_object.save()
        order_object = task_object.order
        order_object.comment = comment
        order_object.state = 4
        order_object.save()
        # --------------------- ding -------------------------------------------------------------------------
        dd = DingDing()
        id = order_object.owner.username
        url = request.build_absolute_uri(reverse('workorder:order-list-user'))
        jsonmsg = {
            "title": "恭喜:你的工单已被操作(操作人:{}{})".format(request.user.last_name, request.user.first_name),
            "text": "结果:{}".format(comment),
            "picUrl": "@lALOACZwe2Rk",
            "messageUrl": url,
        }
        dd.send_link_message(ddID=id, json_content=jsonmsg)
        # --------------------- ding -------------------------------------------------------------------------
        data = {
            'return': '任务结束,ID:{}'.format(taskid)
        }
        return JsonResponse(data, status=200)
    else:
        data = {
            'return': '处理结果不能为空'
        }
    return JsonResponse(data, status=400)

@csrf_exempt
def autoComplete(request):
    category_id = request.POST.get('category_id')
    queryset = get_object_or_404(Category2, id=category_id)
    if queryset.auto_template:
        data = {
            'return': queryset.auto_template,
        }
        return JsonResponse(data, status=200)
    else:
        data = {
            'return': "空",
        }
        return JsonResponse(data, status=400)