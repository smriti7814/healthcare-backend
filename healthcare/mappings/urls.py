from django.urls import path
from .views import (
    MappingCreateView,
    MappingListView,
    PatientDoctorListView,
    MappingDetailView
)

urlpatterns = [
    path('', MappingListView.as_view()),                  
    path('assign/', MappingCreateView.as_view()),           
    path('patient/<int:patient_id>/', PatientDoctorListView.as_view()),
    path('<int:pk>/', MappingDetailView.as_view()),         
]