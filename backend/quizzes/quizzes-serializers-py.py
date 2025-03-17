from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text', 'is_correct', 'order']
        extra_kwargs = {'is_correct': {'write_only': True}}

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_text', 'question_type', 'points', 'order', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit', 'pass_percentage',
            'max_attempts', 'created_at', 'updated_at', 'questions',
            'question_count', 'total_points'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_question_count(self, obj):
        return obj.questions.count()
    
    def get_total_points(self, obj):
        return sum(question.points for question in obj.questions.all())

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ['id', 'attempt', 'question', 'selected_choices', 'text_response', 'is_correct', 'points_earned']
        read_only_fields = ['is_correct', 'points_earned']

class QuizAttemptSerializer(serializers.ModelSerializer):
    responses = QuestionResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'user', 'score', 'passed', 'time_spent',
            'started_at', 'completed_at', 'responses'
        ]
        read_only_fields = ['score', 'passed', 'started_at']

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'score', 'passed', 'time_spent',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['quiz', 'score', 'passed', 'started_at', 'completed_at']