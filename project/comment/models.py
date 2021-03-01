from django.db import models

from User.models import UserProfile

from app01.models import ArticlePost

from ckeditor.fields import RichTextField

from mptt.models import MPTTModel,TreeForeignKey

# Create your models here.

# 博文的评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        UserProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ('created',)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
