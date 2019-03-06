import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

def create_question(question_text, days):
    '''
    创建投票问题
    :param question_text:问题内容
    :param days:发布时间的偏移量
    :return:创建的投票问题实例
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    '''创建自动测试欢迎页Index的类'''

    def test_no_question(self):
        '''
        如果没有投票问题，页面应该显示的信息
        :return:
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '没有投票问题')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''
        如果是过去发布的投票问题，页面应该显示过去的信息
        :return:
        '''
        create_question(question_text='过去的投票问题', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 过去的投票问题>'])

    def test_future_question(self):
        '''
        如果是将来发布的投票问题，页面应该不显示将来的信息
        :return:
        '''
        create_question(question_text='将来的投票问题', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, '没有投票问题')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        '''
        如果是将来和过去发布的投票问题都有，页面应该只显示过去发布的投票问题信息
        :return:
        '''
        create_question(question_text='过去的投票问题', days=-30)
        create_question(question_text='将来的投票问题', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: 过去的投票问题>'])

    def test_two_past_questions(self):
        '''
        如果是过去发布的2个投票问题，页面应该显示过去发布的2个投票问题信息
        :return:
        '''
        create_question(question_text='过去的投票问题1', days=-5)
        create_question(question_text='过去的投票问题2', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: 过去的投票问题1>', '<Question: 过去的投票问题2>'],
        )

class QuestionDetailViewTests(TestCase):
    '''创建自动测试欢迎页Detail的类'''

    def test_future_question(self):
        '''
        如果是将来发布的投票问题，返回404错误
        :return:
        '''
        future_question = create_question(question_text='将来的投票问题', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        如果是过去发布的投票问题，页面应该显示过去的信息
        :return:
        '''
        past_question = create_question(question_text='过去的投票问题', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)