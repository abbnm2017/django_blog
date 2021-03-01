from django.db import models

# Create your models here.

#导入内建的User模型
# from django.contrib.auth.models import User

# timezone 用于处理时间相关事物
from django.utils import timezone

from project import settings

from django.urls import reverse

from taggit.managers import TaggableManager

from PIL import Image


class Classes(models.Model):
    title = models.CharField(max_length=32)


class Student(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    age = models.IntegerField()
    cls = models.ForeignKey('Classes',on_delete = models.CASCADE)


class Teacher(models.Model):
    tname = models.CharField(max_length=32)

    c2t = models.ManyToManyField('Classes')

class ArticleColumn(models.Model):
    """
        栏目的 Model
    """

    # 栏目标题
    title = models.CharField(max_length=100, blank=True)

    # 创建时间
    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

# 博客文章数据模型
class ArticlePost(models.Model):
    #文章作者。参数 on_delete 用于指定数据删除的方式

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)
    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()
    #文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    total_views = models.PositiveIntegerField(default=0)

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(ArticleColumn,null = True,blank = True,on_delete = models.CASCADE,related_name = 'article',error_messages={'required':"你一定要填一个哦！"})

    # 文章标签
    tags = TaggableManager(blank=True)

    #文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True)

    #新增点赞数统计
    likes = models.PositiveIntegerField(default=0)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created'),


    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('app01:article_detail',args=[self.id])

    """
        save()是model内置的方法，它会在model实例每次保存时调用。这里改写它，将处理图片的逻辑“塞进去”。
        super(ArticlePost, self).save(*args, **kwargs)的作用是调用父类中原有的save()方法
        即将model中的字段数据保存到数据库中
        因为图片处理是基于已经保存的图片的
        所以这句一定要在处理图片之前执行，否则会得到找不到原始图片的错误。
        太好理解的是if中的这个not kwargs.get('update_fields')。还记得article_detail()视图中
        为了统计浏览量而调用了save(update_fields=['total_views'])吗？
        没错，就是为了排除掉统计浏览量调用的save()，免得每次用户进入文章详情页面都要处理标题图，太影响性能了
    """

    def save(self,*args,**kwargs):
        print ("keke_aritclepost_save1",args)
        print ("keke_aritclepost_save2", kwargs)
        # 调用原有的 save() 的功能
        article = super(ArticlePost,self).save(*args,**kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400
            new_y = int(new_x*(y / x))
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article









