from django.urls import path
from .views import *

urlpatterns = [
    path('register/student/', StudentRegistrationAPIView.as_view(), name='student-register'),
    path('register/mentor/', MentorRegistrationAPIView.as_view(), name='mentor-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/student/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('profile/student/<int:student_id>/', StudentProfileAPIView.as_view(), name='student-profile-detail'),
    path('profile/mentor/', MentorProfileAPIView.as_view(), name='mentor-profile'),
    path('students/', AllStudentsAPIView.as_view(), name='all-students'),
        path('tests/', TestListAPIView.as_view(), name='test-list'),
    path('test-scores/', TestScoreAPIView.as_view(), name='add-test-score'),
    path('test-scores/<int:score_id>/', TestScoreAPIView.as_view(), name='update-delete-test-score'),
]