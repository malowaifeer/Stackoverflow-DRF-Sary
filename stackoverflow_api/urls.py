from django.urls import path

from .views import (
    UserListCreateAPIView,
    QuestionListCreateAPIView, 
    QuestionDetailsAPIView, 
    TagListCreateAPIView, 
    TagDetailsAPIView, 
    AnswerListCreateAPIView, 
    AnswerDetailsAPIView,
    QuestionCommentListCreateAPIView,
    QuestionCommentDetailsAPIView,
    AnswerCommentListCreateAPIView,
    AnswerCommentDetailsAPIView
)

app_name = 'stackoverflow_api'

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='api-user-list'),
    path('tags/', TagListCreateAPIView.as_view(), name='api-tag-list'),
    path('tags/<int:pk>/', TagDetailsAPIView.as_view(), name='api-tag-details'),
    path('questions/', QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('questions/<int:pk>/', QuestionDetailsAPIView.as_view(), name='api-question-details'),
    path('questions/<int:pk>/answers/', AnswerListCreateAPIView.as_view(), name='api-answer-list'),
    path('questions/comments/<int:pk>/', QuestionCommentDetailsAPIView.as_view(), name='api-question-comment-details'),
    path('questions/<int:pk>/comments/', QuestionCommentListCreateAPIView.as_view(), name='api-question-comment-list'),
    path('answers/<int:pk>/', AnswerDetailsAPIView.as_view(), name='api-answer-details'),
    path('answers/<int:pk>/comments/', AnswerCommentListCreateAPIView.as_view(), name='api-answer-comment-list'),
    path('answers/comments/<int:pk>/', AnswerCommentDetailsAPIView.as_view(), name='api-answer-comment-details'),
]