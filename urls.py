from django.urls import path
from .views import recruiter_signup, recruiter_login, pending_recruiters, approve_recruiter, reject_recruiter
from .views import RecruiterSignupView
from .views import recruiter_signup, ApproveRecruiterView  # Import ApproveRecruiterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RecruiterLoginView



urlpatterns = [
    path('signup/', recruiter_signup, name='recruiter_signup'),
    path('login/', recruiter_login, name='recruiter_login'),
    path('pending/', pending_recruiters, name='pending_recruiters'),
    path('approve/<int:recruiter_id>/', approve_recruiter, name='approve_recruiter'),
    path('reject/<int:recruiter_id>/', reject_recruiter, name='reject_recruiter'),
    path('signup/', RecruiterSignupView.as_view(), name='recruiter-signup'),
    path('approve/<int:recruiter_id>/', ApproveRecruiterView.as_view(), name='approve-recruiter'),  # Use .as_view() for class-based views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', RecruiterLoginView.as_view(), name='recruiter-login'),
    path('api/recruiter/approve/<int:recruiter_id>/', ApproveRecruiterView.as_view(), name='approve_recruiter'),
]
