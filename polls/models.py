from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Question(models.Model):
    '''创建投票应用的问题'''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        '''判断问题是否是最近24小时内发布的'''
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    '''创建投票应用问题的选项'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
