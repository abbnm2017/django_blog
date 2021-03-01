from django.shortcuts import render, HttpResponse, get_object_or_404,redirect

from django.http import JsonResponse

# Create your views here.
from django.contrib.auth.decorators import login_required

from User.models import UserProfile
from app01.models import ArticlePost

from comment.forms import CommentForm

from .models import Comment

from notifications.signals import notify


# 文章评论
@login_required(login_url='/app01/login')
def comment(request,article_id, parent_commet_id = None):
    print ("cur_article_id---->",article_id,parent_commet_id)
    # get_object_or_404()：它和Model.objects.get()
    # 的功能基本是相同的。区别是在生产环境下，如果用户请求一个不存在的对象时，Model.objects.get()
    # 会返回Error
    # 500（服务器内部错误），而get_object_or_404()
    # 会返回Error
    # 404。相比之下，返回404错误更加的准确。

    article = get_object_or_404(ArticlePost,id=article_id)

    if request.method == 'POST':
        print ("88991000,",article)
        print ("comment--data",request.POST)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            """
            parent_comment_id 
                此参数代表父评论的id值，若为None则表示评论为一级评论，
                若有具体值则为多级评论
                如果视图处理的是多级评论，则用MPTT的get_root()方法将其父级重置
                为树形结构最底部的一级评论
                然后在reply_to中保存实际的被回复人并保存。
                视图最终返回的是HttpResponse字符串，后面会用到
            """
            # 二级回复
            if parent_commet_id:
                parent_comment = Comment.objects.get(id=parent_commet_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                """
                actor：发送通知的对象
                recipient：接收通知的对象
                verb：动词短语
                target：链接到动作的对象（可选）
                action_object：执行通知的对象（可选）
                   
                杜赛 (actor) 在 Django搭建个人博客 (target) 中
                对 你 (recipient) 发表了 (verb) 评论 (action_object)
                """

                if not request.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object = new_comment,
                    )

                return HttpResponse('200 Ok')
            new_comment.save()
                # # 给其他用户发送通知
                # if not parent_comment.user.is_superuser and not parent_comment.user == request.user:

            # 新增代码，给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient= UserProfile.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )

            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

        # 处理错误请求
    elif request.method == 'GET':
        print ("open_reply:",parent_commet_id)
        comment_form = CommentForm()
        context = {
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_commet_id,
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("发表评论仅接受POST请求。")







    return HttpResponse('ok')


QUEUE_DICT = {}
import queue

#名称 是谁 就为谁创建一个队列

def home(request):

    name = request.GET.get("name")
    print ("长轮询的结果",name)

    if name != None:
        QUEUE_DICT[name] = queue.Queue()

    print("长轮询的结果queue", QUEUE_DICT)

    return render(request,'comment/home.html',{'name':name})

def send_message(request):
    #接受客户端浏览器接收的消息
    msg = request.POST.get('msg')
    print ("pppp",msg)
    #消息放所有队列
    for q in QUEUE_DICT.values():
        q.put(msg)

    return HttpResponse('成功')

def get_message(request):
    #浏览器自动获取消息
    name = request.GET.get('name')
    print ("auto_message",name)

    q = QUEUE_DICT[name]
    # q.get(timeout = 10)   #hangzhu 10s
    result = {'status':True,'data':None}
    try:
        data = q.get(timeout = 10)
        result['data'] = data
    except queue.Empty as e:
        result['status'] = False

    return JsonResponse(result)


    return  HttpResponse("123")