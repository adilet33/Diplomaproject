from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, SubmitApplicationView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_api'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('submit_application', SubmitApplicationView.as_view(), name="submit_application_api")

]
