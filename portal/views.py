from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import StudentProfile, MentorProfile, TestScore
from .serializers import *

class StudentRegistrationAPIView(APIView):
    """
    Register a new student
    """
    permission_classes = [AllowAny]
    authentication_classes = [] 
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            student_profile = serializer.save()
            # Create token for the user
            token, created = Token.objects.get_or_create(user=student_profile.user)
            
            response_data = {
                'message': 'Student registered successfully',
                'token': token.key,
                'user_id': student_profile.user.id,
                'student_id': student_profile.id,
                'username': student_profile.user.username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MentorRegistrationAPIView(APIView):
    """
    Register a new mentor
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = MentorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            mentor_profile = serializer.save()
            # Create token for the user
            token, created = Token.objects.get_or_create(user=mentor_profile.user)
            
            response_data = {
                'message': 'Mentor registered successfully',
                'token': token.key,
                'user_id': mentor_profile.user.id,
                'mentor_id': mentor_profile.id,
                'username': mentor_profile.user.username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    """
    Login for both students and mentors
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Check if user is student or mentor
            user_type = None
            profile_id = None
            
            try:
                student_profile = StudentProfile.objects.get(user=user)
                user_type = 'student'
                profile_id = student_profile.id
            except StudentProfile.DoesNotExist:
                try:
                    mentor_profile = MentorProfile.objects.get(user=user)
                    user_type = 'mentor'
                    profile_id = mentor_profile.id
                except MentorProfile.DoesNotExist:
                    return Response({
                        'error': 'User is neither a student nor a mentor'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            response_data = {
                'message': 'Login successful',
                'token': token.key,
                'user_id': user.id,
                'user_type': user_type,
                'profile_id': profile_id,
                'username': user.username
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentProfileAPIView(APIView):
    """
    Get student profile with test scores
    Accessible by the student themselves or any mentor
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, student_id=None):
        user = request.user
        
        # Check if user is a mentor
        is_mentor = MentorProfile.objects.filter(user=user).exists()
        
        if student_id:
            # If student_id is provided, check permissions
            student_profile = get_object_or_404(StudentProfile, id=student_id)
            
            # Allow access if user is the student themselves or a mentor
            if not is_mentor and student_profile.user != user:
                return Response({
                    'error': 'You do not have permission to view this student profile'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # If no student_id provided, return current user's profile (must be student)
            try:
                student_profile = StudentProfile.objects.get(user=user)
            except StudentProfile.DoesNotExist:
                return Response({
                    'error': 'User is not a student'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentProfileSerializer(student_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MentorProfileAPIView(APIView):
    """
    Get mentor profile
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            mentor_profile = MentorProfile.objects.get(user=request.user)
            serializer = MentorProfileSerializer(mentor_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'User is not a mentor'
            }, status=status.HTTP_400_BAD_REQUEST)

class AllStudentsAPIView(APIView):
    """
    Get all students (only accessible by mentors)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Check if user is a mentor
        try:
            MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'Only mentors can access this endpoint'
            }, status=status.HTTP_403_FORBIDDEN)
        
        students = StudentProfile.objects.all()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TestListAPIView(APIView):
    """
    Get all available tests and create new tests (mentor only for POST)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tests = Test.objects.all().order_by('-created_at')
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Check if user is a mentor
        try:
            MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'Only mentors can create tests'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TestCreateSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()
            response_serializer = TestSerializer(test)
            return Response({
                'message': 'Test created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestScoreAPIView(APIView):
    """
    Add and update test scores (mentor only)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Check if user is a mentor
        try:
            MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'Only mentors can add test scores'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TestScoreCreateSerializer(data=request.data)
        if serializer.is_valid():
            test_score = serializer.save()
            response_serializer = TestScoreSerializer(test_score)
            return Response({
                'message': 'Test score added successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, score_id):
        # Check if user is a mentor
        try:
            MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'Only mentors can update test scores'
            }, status=status.HTTP_403_FORBIDDEN)
        
        test_score = get_object_or_404(TestScore, id=score_id)
        serializer = TestScoreUpdateSerializer(test_score, data=request.data)
        if serializer.is_valid():
            test_score = serializer.save()
            response_serializer = TestScoreSerializer(test_score)
            return Response({
                'message': 'Test score updated successfully',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, score_id):
        # Check if user is a mentor
        try:
            MentorProfile.objects.get(user=request.user)
        except MentorProfile.DoesNotExist:
            return Response({
                'error': 'Only mentors can delete test scores'
            }, status=status.HTTP_403_FORBIDDEN)
        
        test_score = get_object_or_404(TestScore, id=score_id)
        test_score.delete()
        return Response({
            'message': 'Test score deleted successfully'
        }, status=status.HTTP_200_OK)
