from django.contrib import admin
from .models import Question,Choice

# Register your models here.
class ChoiceInline(admin.TabularInline):
    '''创建自定义的投票问题选项关联的类'''
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    '''创建自定义的投票问题后台管理类'''
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date Information', {'fields':['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)