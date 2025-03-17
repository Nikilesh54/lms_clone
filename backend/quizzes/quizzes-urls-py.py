from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet, QuestionViewSet, ChoiceViewSet,
    QuizAttemptViewSet, QuestionResponseViewSet
)

router = DefaultRouter()
router.register(r'', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'attempts', QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'responses', QuestionResponseViewSet, basename='question-response')

urlpatterns = [
    path('', include(router.urls)),
]