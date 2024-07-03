from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('submit_application/', views.submit_application, name="submit_application"),
    path('confirmation/', views.application_confirmation, name="application_confirmation"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('application/<int:application_id>/', views.view_application, name='view_application'),
    path('candidate_list/', views.view_candidates, name="candidate_list"),
    path('candidates/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),

]