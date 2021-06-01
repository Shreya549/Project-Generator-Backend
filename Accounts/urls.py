from django.urls import path, include
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from .views import (
    FacultyRegistration,
    StudentRegistration,
    UserLogin,
    # OTPCheckView,
    # OTPVerification,
    ChangePasswordView,
    ContactUsView
)

router = SimpleRouter()
router.register('contact', ContactUsView, basename = 'contact')

urlpatterns = router.urls

urlpatterns += [
    path('register-faculty/', FacultyRegistration.as_view()),
    path('register-student/', StudentRegistration.as_view()),
    path('login/', UserLogin.as_view()),
    path('changePassword', ChangePasswordView.as_view()),

]