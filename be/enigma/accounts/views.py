from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import User, EmailVerificationToken, AccountsEmailSetting
from .serializers import UserSerializer
from .functions import sendVerificationEmail

"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def test(request):
    person = {'name': 'test', 'age': 20}
    return Response(person)
"""

## Settings
accountsEmailSetting = AccountsEmailSetting.load()

##################
###### GET #######
##################

@api_view(['GET'])
@permission_classes([AllowAny])
def verifyRegistrationEmail(request, token):
    try:
        # Look for the verification token
        verification_token = EmailVerificationToken.objects.get(token=token)

        # Check if the token is still valid (e.g. not expired)
        if verification_token.created_at < timezone.now() - timezone.timedelta(hours=accountsEmailSetting.emailLinkExpiration): # Hours of validity set via DB
            data = {
                "status": "error",
                "errorCode": "ERR_008",
                "message": "The request has expired."
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # Verify the user's email
        user = verification_token.user
        user.is_active = True
        user.save()

        # I delete the token after use to avoid reuse
        verification_token.delete()

        # Reindirizza a una pagina di conferma o restituisci una risposta
        data = {
            "status": "success",
            "errorCode": "NO_ERR",
            "message": "Email verified with success"
        }
        return Response(data, status=status.HTTP_200_OK)

    except EmailVerificationToken.DoesNotExist:
        data = {
            "status": "error",
            "errorCode": "ERR_005",
            "message": "The requested resource was not found in the backend."
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        data = {
            "status": "error",
            "errorCode": "ERR_01",
            "message": f"A generic error occurred in the backend. ERROR: {str(e)}"
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            sendVerificationEmail(user.id)
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