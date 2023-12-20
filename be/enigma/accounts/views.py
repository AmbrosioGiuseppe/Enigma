from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer

"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def test(request):
    person = {'name': 'test', 'age': 20}
    return Response(person)
"""

##################
###### GET #######
##################

##################
###### POST ######
##################

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    #DATA
    username = request.data.get('username')
    password = request.data.get('password')
    
    # I check if the user exists
    if not User.objects.filter(username=username).exists():
        data = {
            "status": "error",
            "errorCode": "ERR_006",
            "message": "The user entered does not exist"
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # I'm trying to authenticate
    auth = authenticate(username=username,password=password)
    
    if auth is not None:
        #User authenticate
        if not Token.objects.filter(user=User.objects.get(username=username)).exists():
            Token.objects.create(user=User.objects.get(username=username))
        token = Token.objects.get(user=User.objects.get(username=username))
        data = {
            "status": "success",
            "errorCode": "NO_ERR",
            "message": "Login successfully."
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            "status": "error",
            "errorCode": "ERR_003",
            "message": "Authentication failed, incorrect username or password."
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            # After this line, the user should be saved successfully.
            # Sending email for successful registration
            return Response({
                "status": "success",
                "errorCode": "NO_ERR",
                "message": "User registered successfully.",
            }, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle any integrity errors (e.g., duplicate username) here.
            return Response({
                "status": "error",
                "errorCode": "ERR_DB",
                "message": "Database error, generate exception: " + str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Handle other types of exceptions here.
            return Response({
                "status": "error",
                "errorCode": "ERR_UNKNOWN",
                "message": "Unknown error: " + str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # If the data is invalid, return validation errors.
    return Response({
        "status": "error",
        "errorCode": "ERR_002",
        "message": "Invalid or missing data.",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


##################
###### PUT #######
##################


##################
##### DELETE #####
##################


##################
##### PATCH ######
##################


##################
###### HEAD ######
##################


##################
#### OPTIONS #####
##################