# coding:utf8
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.
from .models import *
import json
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import ItemCreateForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
import time

from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives

from .DingDing import DingDing

def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


class ItemListView(ListView):
    queryset = Item.objects.filter(state=0)
    template_name = "workflow/item_list.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['current_page'] = "workflow-item-list"
        context['object_list'] = Item.objects.filter(state=0, applyUserId=self.request.user)
        context['working_queryset'] = Item.objects.filter(state=1)
        context['close_queryset'] = Item.objects.filter(state=2)
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "workflow/item_detail.html"

def itemcreate(request):
    if request.method == 'GET':
        form = ItemCreateForm(
            initial={
                'applyUserId': request.user
            }
        )
        return render_to_response('workflow/item_create.html', context_instance=RequestContext(request,locals()))
    else:
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # return render_to_response('workflow/item_create_success.html', context_instance=RequestContext(request,locals()))
            return redirect(reverse_lazy("workflow:item-list"))
        else:
            return render_to_response('workflow/item_create.html', context_instance=RequestContext(request,locals()))

# class ItemCreateView(CreateView):
#     template_name = "workflow/item_create.html"
#     form_class = ItemCreateForm
#
#     def get_context_data(self, **kwargs):
#         context = super(ItemCreateView, self).get_context_data(**kwargs)
#         context['current_page'] = "workflow-item-create"
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy("workflow:item-list")
#
#     def form_valid(self, form):
#         response = super(ItemCreateView, self).form_valid(form)
#         return response

    # def form_invalid(self, form):
    #     return HttpResponse("form is invalid.. this is just an")


class ItemUpdateView(UpdateView):
    template_name = "workflow/item_create.html"
    model = Item
    form_class = ItemCreateForm
    # Specifying both 'fields' and 'form_class' is not permitted.
    # fields = "__all__"
    # exclude = ['start_time', 'state']

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['current_page'] = "workflow-item-update"
        return context

    def get_success_url(self):
        return reverse("workflow:item-list")


class TaskListView(ListView):
    queryset = TaskList.objects.filter(state=0)
    close_queryset = TaskList.objects.filter(state=1)
    template_name = "workflow/task_list.html"

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        queryset = TaskList.objects.filter(state=0)
        close_queryset = TaskList.objects.filter(state=1)
        # 创建空字典
        open_dict = []
        close_dict = []
        # 存入数据对
        for a in queryset:
            actor_user = CurrentActorUser.objects.filter(actorId=a.actorId, task=a)
            open_dict.append((a, actor_user))

        for a in close_queryset:
            actor_user = CurrentActorUser.objects.filter(actorId=a.actorId, task=a)
            close_dict.append((a, actor_user))
        context['current_page'] = "workflow-task-list"
        context['close_queryset'] = close_dict
        context['open_queryset'] = open_dict
        return context


class GetActorUserFromTask(ListView):
    queryset = TaskList.objects.all()
    template_name = "workflow/actoruser_list.html"

    def get_context_data(self, **kwargs):
        open_task = TaskList.objects.filter(state=0)

        current_actor_user = CurrentActorUser.objects.none()
        for task in open_task:
            current_actor_user = current_actor_user | CurrentActorUser.objects.filter(task=task, actorId=task.actorId, operateUserId=self.request.user).exclude(state=True)

        # for a in open_task:
        #     actor = Actor.objects.get(id=a.actorId.id)
        #     actor_user = ActorUser.objects.get(actorId=actor.actorId)
        #     userset = CurrentActorUser.objects.filter(actorUser=actor_user, task=a)
        #     actoruser = ActorUser.objects.filter(actorId=actor.id)
        #     judge_list.append((a, actoruser))
        context = super(GetActorUserFromTask, self).get_context_data(**kwargs)
        context['current_page'] = "workflow-judge-list"
        context['judge_list'] = current_actor_user
        return context

# ajax views
@csrf_exempt
def createTask(requests):
    id = requests.POST.get('id')
    id = int(id)
    try:
        # 得到所选工单
        item = get_object_or_404(Item, id=id)
        # 查到所选工单所用的流程模板
        rout = get_object_or_404(Rout, id=item.routID.id)
        # 查到流程模板的所有步骤模板
        allActor = Actor.objects.filter(routId=rout.id)
        # 查到流程模板的第一个步骤模板
        actorOne = get_object_or_404(allActor, sortNo='1')
        # 生成任务
        task = TaskList.objects.create(itemId=item, actorId=actorOne, state=0)

        # 获得当前流程模板的所有步骤模板的所有处理人
        all_actor_user = ActorUser.objects.none()
        for i in allActor:
            all_actor_user = all_actor_user | ActorUser.objects.filter(actorId=i)
        # 生成本任务独有的的处理结果表
        queryset_list = []
        for i in all_actor_user:
            queryset_list.append(CurrentActorUser(task=task, actorId=i.actorId, operateUserId=i.operateUserId))
        CurrentActorUser.objects.bulk_create(queryset_list)

        # 改变工单的状态为审批中
        item.state = 1
        item.save()
        # --------------------- ding -----------------
        # dd = DingDing()
        # allCurrentActorUser = CurrentActorUser.objects.filter(task=task, actorId=actorOne)
        # ids = allCurrentActorUser.values_list('operateUserId__username', flat=True)
        # url = requests.build_absolute_uri(reverse('workflow:actoruser-list'))
        # content = u"[审批确认]收到一个审批(任务ID:{})".format(task.id)
        #
        # jsonmsg = {
        #     "title": "审批确认",
        #     "text": "收到一个审批:{}".format(task.itemId.itemName),
        #     "picUrl": "@lALOACZwe2Rk",
        #     "messageUrl": "http://s.dingtalk.com/market/dingtalk/error_code.php",
        # }
        # for id in ids:
        #     dd.send_link_message(ddID=id, json_content=jsonmsg)
        # --------------------- ding -----------------
        # --------------------- email -----------------
        allActorUser = ActorUser.objects.filter(actorId=actorOne)
        to_list = allActorUser.values_list('operateUserId__email', flat=True)
        url = requests.build_absolute_uri(reverse('workflow:actoruser-list'))
        subject = u"[审批确认]收到一个审批(任务ID:{})".format(task.id)
        html_content = "<a href={}>点击电梯前往</a>".format(url)
        sender = "datadev@wz-inc.com"
        recipients = to_list
        msg = EmailMultiAlternatives(subject, html_content, sender, recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # --------------------- email -----------------
    except Exception, e:
        result =  {'return': "报错信息: {}".format(e)}
        return render_to_json_response(result, status=400)
    else:
        result = {'return': "任务ID: {}".format(task.id)}
        return render_to_json_response(result, status=200)

@csrf_exempt
def agree(request):
    # 当前审批的任务id
    taskid = request.POST.get('taskid')
    comment = request.POST.get('comment', None)
    if comment:
        pass
    else:
        comment = "空"
    task = TaskList.objects.get(id=taskid)
    # 当前审批的任务状态(第几步)
    actor = task.actorId
    # 当前登录用户对此任务的审批结果id
    currentactoruserid = request.POST.get('currentactoruserid')
    currentactoruserid = int(currentactoruserid)
    try:
        # 获得步骤处理人
        currentactoruser = CurrentActorUser.objects.get(id=currentactoruserid)
        # 处理结果边为agree
        currentactoruser.state = True
        currentactoruser.save()
        # 获得当前步骤的所有步骤处理人模板
        current_actor_user = CurrentActorUser.objects.filter(actorId=actor, task=task)
        # 获得当前步骤的所有处理人得所有处理结果
        judge_list = []
        for item in current_actor_user:
            judge_list.append(item.state)
        print judge_list
        # 如果全为True
        if False not in judge_list and None not in judge_list:
            # 获得当前任务的步骤编号
            sortNo = task.actorId.sortNo

            # # 拿到当前任务的模板对应的并且编号为sortNo的步骤
            # actor = Actor.objects.get(routId=task.actorId.routId, sortNo=sortNo)

            # 拿到当前任务使用*模板*的当前次序的所有步骤
            allactor = Actor.objects.filter(routId=task.actorId.routId)
            next_actor = allactor.get(sortNo=sortNo+1)
            if len(allactor) == sortNo + 1:
                # 任务流程推进一步
                task.actorId = next_actor
                # 任务变成完成状态
                task.state = 1
                # 增加审批历史到task
                task.version += u"{} {}{}同意,备注:{}\n[审批结束]".format(
                    time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    currentactoruser.operateUserId.last_name,
                    currentactoruser.operateUserId.first_name,
                    comment
                )
                task.save()
                # 任务对应工单变为关闭状态
                item = get_object_or_404(Item, id=task.itemId.id)
                item.state = 2
                item.save()
                # 直接删除当前任务所有当前审批人
                CurrentActorUser.objects.filter(task=task).all().delete()

                # --------------------- email -----------------
                over_ActorUser = ActorUser.objects.filter(actorId=task.actorId)
                list1 = over_ActorUser.values_list('operateUserId__email', flat=True)
                list2 = []
                email = str(task.itemId.applyUserId.email)
                list2.append(email)
                print list2

                url = request.build_absolute_uri(reverse('workflow:item-detail', args=[task.itemId.id]))
                subject = u"[审批结果]审批通过(任务ID:{})".format(task.id)
                html_content = "<a href={}>详情点击电梯前往</a>".format(url)
                sender = "datadev@wz-inc.com"
                msg = EmailMultiAlternatives(subject, html_content, sender, list1)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                msg1 = EmailMultiAlternatives(subject, html_content, sender, list2)
                msg1.attach_alternative(html_content, "text/html")
                msg1.send()
                # --------------------- email -----------------
                result = {'return': u"全部审批结束,任务状态确认:{}".format(task.actorId.actorName)}
            else:
                # 只是任务流程推进
                task.actorId = next_actor
                task.version += u"{} {}{}同意,备注:{}\n".format(
                    time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    currentactoruser.operateUserId.last_name,
                    currentactoruser.operateUserId.first_name,
                    comment
                )
                task.save()
                # --------------------- email -----------------
                # 获得第一步所有审批人组成一个list
                allActorUser = ActorUser.objects.filter(actorId=next_actor)
                to_list = allActorUser.values_list('operateUserId__email', flat=True)
                url = request.build_absolute_uri(reverse('workflow:actoruser-list'))
                subject = u"[审批确认]收到一个审批(任务ID:{})".format(task.id)
                html_content = "<a href={}>点击电梯前往</a>".format(url)
                sender = "datadev@wz-inc.com"
                recipients = to_list
                msg = EmailMultiAlternatives(subject, html_content, sender, recipients)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                # --------------------- email -----------------
                result = {'return': u"当前步骤审批人全部通过审批,状态自动改变为:{}".format(task.actorId.actorName)}
            return render_to_json_response(result, status=200)
        else:
            task.version += u"{} {}{}同意,备注:{}\n".format(
                time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                currentactoruser.operateUserId.last_name,
                currentactoruser.operateUserId.first_name,
                comment
            )
            task.save()
    except Exception, e:
        result = {'return': "报错信息:{}".format(e)}
        return render_to_json_response(result, status=400)
    else:
        result = {'return': "当前审批ID: {}".format(currentactoruserid)}
        return render_to_json_response(result, status=200)

#TODO
@csrf_exempt
def disagree(request):
    # 当前审批的任务id
    taskid = request.POST.get('taskid')
    task = TaskList.objects.get(id=taskid)
    # 当前审批的任务状态(第几步)
    actor = task.actorId
    # 当前登录用户对此任务的审批结果id
    currentactoruserid = request.POST.get('currentactoruserid')
    # 备注
    comment = request.POST.get('comment', None)
    if comment:
        pass
    else:
        comment = "空"
    try:
        # 状态
        currentactoruser = get_object_or_404(CurrentActorUser, id=currentactoruserid)
        # 拒绝并保存
        currentactoruser.state=False
        currentactoruser.save()
        # 任务变为完成
        task.state = 1
        task.version += u"{} {}{}拒绝,原因:{}\n".format(
            time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            currentactoruser.operateUserId.last_name,
            currentactoruser.operateUserId.first_name,
            comment
        )
        task.save()

        item = get_object_or_404(Item, id=task.itemId.id)
        item.state = 0
        item.save()
        # 直接删除当前任务所有当前审批人
        CurrentActorUser.objects.filter(task=task).all().delete()
    except Exception,e:
        result = {'return': "报错信息:{}".format(e)}
        return render_to_json_response(result, status=400)
    # --------------------- email -----------------
    to_list = [task.itemId.applyUserId.email,]
    url = request.build_absolute_uri(reverse('workflow:item-detail', args=[task.itemId.id]))
    subject = u"[审批结果]审批被{}拒绝(任务ID:{})".format(currentactoruser.operateUserId.email,task.id)
    html_content = "<a href={}>详情点击电梯前往</a>".format(url)
    sender = "datadev@wz-inc.com"
    recipients = to_list
    msg = EmailMultiAlternatives(subject, html_content, sender, recipients)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # --------------------- email -----------------
    result = {'return': u"任务结束,变更变为关闭,并已邮件通知申请人"}
    return render_to_json_response(result, status=200)


#TODO
@csrf_exempt
def add_sign(request):
    # 获得加签目标
    email = request.POST.get('email')
    # 去掉两遍的空格
    email = email.strip()
    # 当前审批的任务状态(第几步)
    taskid = request.POST.get('taskid')
    task = TaskList.objects.get(id=taskid)
    actorid = request.POST.get('actorid')
    actor = get_object_or_404(Actor, id=actorid)
    # # 当前登录用户对此任务的审批结果id
    # actoruserid = request.POST.get('actoruserid')
    try:
        user = get_object_or_404(User, email=email)
        print user
        actoruser = CurrentActorUser.objects.create(task=task, actorId=actor, operateUserId=user, type=1)
        # --------------------- email -----------------
        # 获得第一步所有审批人组成一个list
        to_list = [email, ]
        url = request.build_absolute_uri(reverse('workflow:actoruser-list'))
        subject = u"[审批加签]你被加签到一个变更审批,请确认"
        html_content = "<a href={}>点击电梯前往</a>".format(url)
        sender = "datadev@wz-inc.com"
        recipients = to_list
        msg = EmailMultiAlternatives(subject, html_content, sender, recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # --------------------- email -----------------
        result = {'return': u"用户:{}{}已加签到{}".format(user.last_name,user.first_name,  actor.actorName)}
        return render_to_json_response(result, status=200)
    except Exception, e:
        result = {'return': u"邮箱输入错误或账户未登录过(请通知该用户使用AD账号登录一次本系统)!({})".format(e)}
        return render_to_json_response(result, status=400)
