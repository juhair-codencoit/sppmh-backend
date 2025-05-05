from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .authentication import *
from .serializers import *
from .models import *

class BatchViewA(APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not authenticated"}, status=401)
        batch = Batch.objects.all()
        if not batch:
            return Response({"message": "No batches found"}, status=404)
        serializer = BatchSerializer(batch, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not authenticated"}, status=401)
        if not user.is_staff:
            return Response({"error": "User is not authorized to create a batch"}, status=403)
        data = request.data
        serializer = BatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Batch created successfully",
                             "data": serializer.data
                             }, status=201)
        return Response({"error": serializer.errors}, status=400)




### User Registration API ###
class RegisterAPIView(APIView):
    def post(self, request):
        
        data = request.data

        if data.get('password') != data.get('confirm_password'):
            return Response({"error": "Passwords do not match"}, status=400)
        if CustomUser.objects.filter(email=data.get('email')).exists():
            return Response({"error": "Email already exists"}, status=400)
        
        serializer = UserRegistrationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully",
                             "data": serializer.data
                             }, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

### Login API ###        
class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)
        
        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=400)
        
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        response = Response(status=200)


        response.set_cookie(
            key = 'refresh_token',
            value= refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
        )

        response.set_cookie(
            key = 'access_token',
            value= access_token,
            httponly=True,
            secure=True,
            samesite='None',
        )
        
        serializer = CustomUserSerializer(user)
        response.data = {
            "message": "Login successful",
            "access_token": access_token,
            "user_data": serializer.data,
        }
        return response 

        
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        print(user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)


### Refresh Token API ###
class RefreshTokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token not found"}, status=401)
        
        try:
            old_refresh_token = RefreshToken(refresh_token)
            old_refresh_token.blacklist()

            payload = old_refresh_token.payload
            user_id = payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)

            new_refresh_token = RefreshToken.for_user(user)
            new_access_token = str(new_refresh_token.access_token)
            
            response = Response()
            response.set_cookie(
                key= 'access_token',
                value= new_access_token,
                httponly=True,
                secure=True,
                samesite='None',
            )
            response.set_cookie(
                key= 'refresh_token',
                value= new_refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
            )
            response.data = {
                "access_token": new_access_token,
            }
            return response
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=401)


### Logout API ###
class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token not found"}, status=401)
        
        
        old_refresh_token = RefreshToken(refresh_token)
        old_refresh_token.blacklist()


        response = Response({"message": "Logout successful"}, status=200)

        response.set_cookie(
            key='access_token',
            value='',
            httponly=True,
            secure=True,
            samesite='None',
        )

        response.set_cookie(
            key='refresh_token',
            value='',
            httponly=True,
            secure=True,
            samesite='None',
        )
        
        return response
    
