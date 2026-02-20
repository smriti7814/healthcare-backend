from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient
from doctors.models import Doctor


class MappingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.filter(
            patient__user=request.user
        )
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


class MappingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient_id = request.data.get("patient")
        doctor_id = request.data.get("doctor")

        # ownership check
        try:
            patient = Patient.objects.get(
                id=patient_id,
                user=request.user
            )
        except Patient.DoesNotExist:
            return Response(
                {"error": "You are not allowed to map this patient"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        mapping = PatientDoctorMapping.objects.create(
            patient=patient,
            doctor=doctor
        )

        serializer = PatientDoctorMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientDoctorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            Patient.objects.get(
                id=patient_id,
                user=request.user
            )
        except Patient.DoesNotExist:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        mappings = PatientDoctorMapping.objects.filter(
            patient_id=patient_id
        )
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


class MappingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return PatientDoctorMapping.objects.get(
                pk=pk,
                patient__user=user
            )
        except PatientDoctorMapping.DoesNotExist:
            return None

    def get(self, request, pk):
        mapping = self.get_object(pk, request.user)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)
        serializer = PatientDoctorMappingSerializer(mapping)
        return Response(serializer.data)

    def put(self, request, pk):
        mapping = self.get_object(pk, request.user)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        patient_id = request.data.get("patient")
        doctor_id = request.data.get("doctor")

        # ✅ patient update allowed BUT only if it belongs to same user
        if patient_id:
            try:
                Patient.objects.get(
                    id=patient_id,
                    user=request.user
                )
            except Patient.DoesNotExist:
                return Response(
                    {"error": "You cannot assign another user's patient"},
                    status=status.HTTP_403_FORBIDDEN
                )

        # ✅ doctor update allowed BUT only if it belongs to same user
        if doctor_id:
            try:
                Doctor.objects.get(
                    id=doctor_id,
                    user=request.user
                )
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "You cannot assign another user's doctor"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = PatientDoctorMappingSerializer(
            mapping,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mapping = self.get_object(pk, request.user)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)
        mapping.delete()
        return Response(
            {"message": "Mapping deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )