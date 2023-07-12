from django.contrib import admin
from . models import Question, Choice

class ChoinceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoinceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
