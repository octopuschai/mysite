import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    '''创建自动测试投票问题的类'''

    def test_was_published_recently_with_future_question(self):
        '''当创建投票问题的时间选择为将来的某个时间，was_published_recently()返回失败'''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''当创建投票问题的时间是24小时前的某个时间，was_published_recently()返回失败'''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''当创建投票问题的时间是24小时之内的某个时间，was_publish_recently()返回成功'''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)