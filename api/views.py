from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import RegisterSerializer,StyleConfigSerializer,StyleSuggestSerializer
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

class StyleSuggestView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer = StyleSuggestSerializer(data=request.data)
        if serializer.is_valid():
            platform=serializer.validated_data['platform']
            component_name=serializer.validated_data['component_name']
            description=serializer.validated_data['description']
            class_names = self.generate_classname(platform,component_name,description)
            return Response({'class_names':class_names},status=status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    def generate_classname(self, platform, component_type, description):
        if platform == 'tailwind':
            if component_type == 'layout':
                return 'container mx-auto p-6 grid grid-cols-12 gap-4'
            elif component_type == 'navigation':
                return 'flex items-center justify-between bg-gray-800 text-white px-4 py-3 shadow-md'
            elif component_type == 'forms':
                return 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500'
            elif component_type == 'buttons':
                return 'bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded-lg shadow'
            elif component_type == 'feedback':
                return 'p-4 rounded-md bg-green-100 text-green-800 border border-green-300'
            elif component_type == 'data_display':
                return 'overflow-x-auto border rounded-lg shadow divide-y divide-gray-200'
            elif component_type == 'special':
                return 'bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 text-white p-6 rounded-xl shadow-xl'
            else:
                return 'text-gray-700 bg-white p-4 rounded shadow'

        elif platform == 'bootstrap':
            if component_type == 'layout':
                return 'container-fluid row gx-4 gy-3'
            elif component_type == 'navigation':
                return 'navbar navbar-expand-lg navbar-dark bg-dark shadow'
            elif component_type == 'forms':
                return 'form-control mb-3'
            elif component_type == 'buttons':
                return 'btn btn-primary px-4 py-2'
            elif component_type == 'feedback':
                return 'alert alert-success'
            elif component_type == 'data_display':
                return 'table table-striped table-bordered'
            elif component_type == 'special':
                return 'card text-center border-0 shadow-lg bg-primary text-white'
            else:
                return 'card p-3'

        return 'default-style'
