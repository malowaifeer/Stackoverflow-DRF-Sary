from django.contrib import admin
from stackoverflow.models import *


admin.site.register([
    Tag, 
    Question, 
    Answer,
    QuestionComment,
    AnswerComment,
])
