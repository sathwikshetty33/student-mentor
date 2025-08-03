# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import StudentProfile, MentorProfile, Test, TestScore

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = StudentProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 
                 'leetcode', 'github', 'photo', 'bio']
    
    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create student profile
        student_profile = StudentProfile.objects.create(user=user, **validated_data)
        return student_profile
class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = StudentProfile
        fields = ['leetcode', 'github', 'photo', 'bio', 'first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        # Extract user fields
        user_fields = {}
        if 'first_name' in validated_data:
            user_fields['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user_fields['last_name'] = validated_data.pop('last_name')
        if 'email' in validated_data:
            user_fields['email'] = validated_data.pop('email')
        
        # Update user fields if any
        if user_fields:
            for field, value in user_fields.items():
                setattr(instance.user, field, value)
            instance.user.save()
        
        # Update profile fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        
        return instance
class MentorRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = MentorProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 
                 'expertise', 'github', 'photo', 'bio']
    
    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create mentor profile
        mentor_profile = MentorProfile.objects.create(user=user, **validated_data)
        return mentor_profile
class MentorProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = MentorProfile
        fields = ['expertise', 'github', 'photo', 'bio', 'first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        # Extract user fields
        user_fields = {}
        if 'first_name' in validated_data:
            user_fields['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user_fields['last_name'] = validated_data.pop('last_name')
        if 'email' in validated_data:
            user_fields['email'] = validated_data.pop('email')
        
        # Update user fields if any
        if user_fields:
            for field, value in user_fields.items():
                setattr(instance.user, field, value)
            instance.user.save()
        
        # Update profile fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        
        return instance
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return data

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class TestScoreSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    
    class Meta:
        model = TestScore
        fields = ['id', 'test', 'score', 'date_taken']


class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MentorProfile
        fields = ['id', 'user', 'expertise', 'github', 'dateJoined', 'photo', 'bio']

class TestScoreCreateSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    test_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TestScore
        fields = ['student_id', 'test_id', 'score']
    
    def validate_student_id(self, value):
        try:
            StudentProfile.objects.get(id=value)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("Student does not exist")
        return value
    
    def validate_test_id(self, value):
        try:
            Test.objects.get(id=value)
        except Test.DoesNotExist:
            raise serializers.ValidationError("Test does not exist")
        return value
    
    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100")
        return value
    
    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        test_id = validated_data.pop('test_id')
        
        student = StudentProfile.objects.get(id=student_id)
        test = Test.objects.get(id=test_id)
        
        # Check if score already exists for this student and test
        existing_score = TestScore.objects.filter(student=student, test=test).first()
        if existing_score:
            raise serializers.ValidationError("Test score already exists for this student and test")
        
        test_score = TestScore.objects.create(
            student=student,
            test=test,
            score=validated_data['score']
        )
        return test_score
class TestScoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScore
        fields = ['score']
    
    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100")
        return value
class TestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name', 'description']
    
    def validate_name(self, value):
        if Test.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A test with this name already exists")
        return value
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class TestScoreSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    
    class Meta:
        model = TestScore
        fields = ['id', 'test', 'score', 'date_taken']
class TestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name', 'description']
    
    def validate_name(self, value):
        # Check for duplicate name excluding current instance
        if self.instance and Test.objects.filter(name__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A test with this name already exists")
        elif not self.instance and Test.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A test with this name already exists")
        return value

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    test_scores = TestScoreSerializer(many=True, read_only=True, source='testscore_set')
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'leetcode', 'github', 'dateJoined', 
                 'photo', 'bio', 'test_scores']