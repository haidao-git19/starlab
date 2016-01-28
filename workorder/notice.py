__author__ = 'yuan.gao'

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
# --------------------- ding -----------------
dd = DingDing()
over_CurrentActorUser = CurrentActorUser.objects.filter(task=task, actorId=task.actorId)
ids = over_CurrentActorUser.values_list('operateUserId__username', flat=True)
url = request.build_absolute_uri(reverse('workflow:actoruser-list'))
jsonmsg = {
    "title": "收到一个审批确认",
    "text": "{}\n任务ID:{}".format(task.itemId.itemName, task.id),
    "picUrl": "@lALOACZwe2Rk",
    "messageUrl": url,
}
for id in ids:
    dd.send_link_message(ddID=id, json_content=jsonmsg)
# --------------------- ding -----------------