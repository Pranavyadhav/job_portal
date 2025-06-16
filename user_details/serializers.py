from rest_framework import serializers
from .models import User, Profile, WorkExperience, Education, SkillAssessment, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        exclude = ['profile']  # or set read_only_fields = ['profile']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ['profile']  # or set read_only_fields = ['profile']

class SkillAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillAssessment
        fields = '__all__'
        read_only_fields = ['user', 'profile'] 
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
