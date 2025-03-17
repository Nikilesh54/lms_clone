from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse
from .serializers import (
    QuizSerializer, QuestionSerializer, ChoiceSerializer,
    QuizAttemptSerializer, QuestionResponseSerializer, QuizResultSerializer
)
from courses.permissions import IsInstructorOrReadOnly, IsEnrolledOrInstructor

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[IsEnrolledOrInstructor])
    def start(self, request, pk=None):
        quiz = self.get_object()
        user = request.user
        
        # Check max attempts if set
        if quiz.max_attempts > 0:
            attempt_count = QuizAttempt.objects.filter(quiz=quiz, user=user).count()
            if attempt_count >= quiz.max_attempts:
                return Response(
                    {'detail': f'You have reached the maximum number of attempts ({quiz.max_attempts}) for this quiz.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check for incomplete attempts
        incomplete_attempt = QuizAttempt.objects.filter(
            quiz=quiz,
            user=user,
            completed_at__isnull=True
        ).first()
        
        if incomplete_attempt:
            serializer = QuizAttemptSerializer(incomplete_attempt)
            return Response(serializer.data)
        
        # Create new attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=user
        )
        
        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def my_attempts(self, request, pk=None):
        quiz = self.get_object()
        attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            user=request.user
        )
        
        serializer = QuizResultSerializer(attempts, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        quiz_id = self.request.query_params.get('quiz_id')
        if quiz_id:
            return Question.objects.filter(quiz_id=quiz_id)
        return Question.objects.all()

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        question_id = self.request.query_params.get('question_id')
        if question_id:
            return Choice.objects.filter(question_id=question_id)
        return Choice.objects.all()

class QuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Students can see only their attempts
        if user.user_type == 'student':
            return QuizAttempt.objects.filter(user=user)
        
        # Instructors can see attempts for their quizzes
        # This assumes Quiz has a foreign key to Course which has instructor
        elif user.user_type == 'instructor':
            return QuizAttempt.objects.filter(quiz__lesson__section__course__instructor=user)
        
        # Admins can see all attempts
        return QuizAttempt.objects.all()
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        
        # Check if attempt belongs to user
        if attempt.user != request.user:
            return Response(
                {'detail': 'You do not have permission to submit this attempt.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if attempt is already completed
        if attempt.completed_at is not None:
            return Response(
                {'detail': 'This quiz attempt has already been submitted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process responses
        responses_data = request.data.get('responses', [])
        
        # Mark attempt as completed
        attempt.completed_at = timezone.now()
        
        # Calculate time spent
        time_spent = (attempt.completed_at - attempt.started_at).total_seconds()
        attempt.time_spent = int(time_spent)
        
        # Process each response
        total_points = 0
        earned_points = 0
        
        for response_data in responses_data:
            question_id = response_data.get('question')
            selected_choice_ids = response_data.get('selected_choices', [])
            text_response = response_data.get('text_response', '')
            
            try:
                question = Question.objects.get(id=question_id, quiz=attempt.quiz)
                total_points += question.points
                
                # Create response object
                response = QuestionResponse.objects.create(
                    attempt=attempt,
                    question=question,
                    text_response=text_response
                )
                
                # Add selected choices
                for choice_id in selected_choice_ids:
                    try:
                        choice = Choice.objects.get(id=choice_id, question=question)
                        response.selected_choices.add(choice)
                    except Choice.DoesNotExist:
                        pass
                
                # Score the response
                is_correct = False
                
                if question.question_type in ['multiple_choice', 'true_false']:
                    # For these types, all correct choices must be selected and no incorrect ones
                    correct_choices = set(Choice.objects.filter(question=question, is_correct=True).values_list('id', flat=True))
                    selected_choices = set(selected_choice_ids)
                    
                    is_correct = correct_choices == selected_choices
                
                elif question.question_type == 'short_answer':
                    # For short answer, use exact match for now
                    # This could be enhanced with more sophisticated matching
                    correct_answers = [
                        choice.choice_text.lower().strip()
                        for choice in Choice.objects.filter(question=question, is_correct=True)
                    ]
                    is_correct = text_response.lower().strip() in correct_answers
                
                # Update response with score
                response.is_correct = is_correct
                if is_correct:
                    response.points_earned = question.points
                    earned_points += question.points
                
                response.save()
                
            except Question.DoesNotExist:
                continue
        
        # Calculate final score
        if total_points > 0:
            attempt.score = (earned_points / total_points) * 100
        
        # Determine if passed
        attempt.passed = attempt.score >= attempt.quiz.pass_percentage
        attempt.save()
        
        # Return result
        serializer = QuizResultSerializer(attempt)
        return Response(serializer.data)

class QuestionResponseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        attempt_id = self.request.query_params.get('attempt_id')
        if attempt_id:
            attempt = QuizAttempt.objects.get(id=attempt_id)
            
            # Check if user has permission to view
            if (self.request.user == attempt.user or 
                self.request.user.is_staff or 
                (hasattr(attempt.quiz, 'lesson') and 
                 attempt.quiz.lesson.section.course.instructor == self.request.user)):
                return QuestionResponse.objects.filter(attempt=attempt)
            
            return QuestionResponse.objects.none()
        
        return QuestionResponse.objects.filter(attempt__user=self.request.user)
                        