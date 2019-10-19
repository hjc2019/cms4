from django.db import models

# Create your models here.
class admain(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    resume=models.CharField(max_length=100,null=True)
    headimg=models.CharField(max_length=50,null=True)
    lasttime = models.DateField(null=True)
    class Meta:
        db_table ="admain"

class menu(models.Model):
    menuname = models.CharField(max_length=30)
    menutype = models.CharField(max_length=20,null=True)
    menustate = models.CharField(max_length=30,null=True)
    class Meta:
        db_table ="menu"

class news(models.Model):
    catid = models.IntegerField(max_length=10)
    title = models.CharField(max_length=50)
    titlt_font_color = models.CharField(max_length=20,null=True)
    thumb = models.CharField(max_length=30,null=True)
    num = models.IntegerField(max_length=10)
    time = models.DateTimeField(null=True)
    class Meta:
        db_table ="news"

class news_content(models.Model):
    newsid = models.IntegerField(max_length=10)
    content = models.TextField()
    class Meta:
        db_table = "news_content"

class position(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        db_table = "position"

class position_content(models.Model):
    positionid = models.IntegerField(max_length=10)
    newsid = models.IntegerField(max_length=10)
    class Meta:
        db_table = "position_content"
