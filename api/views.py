from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import RegisterSerializer,StyleConfigSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import viewsets
from api.models import StyleConfig
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token=request.data['refresh']
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message" : "User logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class StyleConfigViewSet(viewsets.ModelViewSet):
    queryset = StyleConfig.objects.all()
    serializer_class = StyleConfigSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = StyleConfig.objects.filter(user=self.request.user)
        platform = self.request.query_params.get('platform')
        component_type = self.request.query_params.get('component_type')
        if platform:
            queryset = queryset.filter(platform=platform)
        if component_type:
            queryset = queryset.filter(component_type=component_type)
        return queryset
