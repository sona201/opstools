from django.db import models
from django.utils import timezone


class BaseAbstract(models.Model):
    """
    基础继承模型
    """
    # shuhe_status = models.BooleanField(default=True, blank=True)
    status = models.BooleanField(default=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    """
    只有在调用 Model.save() 时，该字段才会自动更新。
    当以其他方式对其他字段进行更新时，如 QuerySet.update()，该字段不会被更新，尽管你可以在这样的更新中为该字段指定一个自定义值
    """

    class Meta:
        abstract = True


class BaseModel(models.Model):
    """
    基础继承模型
    """
    shuhe_status = models.BooleanField(default=True, blank=True)
    # status = models.BooleanField(default=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    """
    只有在调用 Model.save() 时，该字段才会自动更新。
    当以其他方式对其他字段进行更新时，如 QuerySet.update()，该字段不会被更新，尽管你可以在这样的更新中为该字段指定一个自定义值
    """

    class Meta:
        abstract = True
