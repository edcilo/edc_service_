from django.shortcuts import render
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthorized


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthorized])
def protected(request):
    print('>>>>>>>>>>>', request.data)
    return Response(request.data['jwt-decode-data'])
