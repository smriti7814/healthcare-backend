from rest_framework import generics, permissions
from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ sirf logged-in user ke patients
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # ✅ patient automatically current user se attach
        serializer.save(user=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ dusre user ke patient pe 404
        return Patient.objects.filter(user=self.request.user)