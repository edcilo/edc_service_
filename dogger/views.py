from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthorized, IsOwner
from .repositories import DogRepository
from .serializers import (
    DogModelSerializer,
    DogModelCreateSerializer,
)


# Create your views here.
dog_repo = DogRepository()


@api_view(['GET'])
@permission_classes([IsAuthorized])
def protected(request):
    print('>>>>>>>>>>>', request.data)
    return Response(request.data['jwt-decode-data'])


class DogsViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthorized, IsOwner]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = request.data['jwt-payload']
        dogs = dog_repo.lists(user['user_id'])
        serializer = DogModelSerializer(dogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.data['jwt-payload']
        dog = dog_repo.find(user['user_id'], pk)
        serializer = DogModelSerializer(dog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        serializer = DogModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        serializer = DogModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        updated = dog_repo.update(user['user_id'], pk, request.data)
        if updated:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        user = request.data['jwt-payload']
        deleted = dog_repo.delete(user['user_id'], pk)
        if deleted:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
