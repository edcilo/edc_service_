from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthorized, IsOwner, IsWalker
from .repositories import DogRepository, WalkerScheduleRepository, ReservationRepository
from dogger import serializers, models


# Create your views here.
dog_repo = DogRepository()
walker_scheduler_repo = WalkerScheduleRepository()
reservation_repo = ReservationRepository()


@api_view(['GET'])
@permission_classes([IsAuthorized, IsOwner])
def walker_schedules(request):
    walker = request.GET.get('walker')
    schedule = walker_scheduler_repo.lists(walker)
    serializer = serializers.ScheduleModelSerializer(schedule, many=True)
    return Response(serializer.data)


class DogsViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthorized, IsOwner]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = request.data['jwt-payload']
        dogs = dog_repo.lists(user['user_id'])
        serializer = serializers.DogModelSerializer(dogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.data['jwt-payload']
        dog = dog_repo.find(user['user_id'], pk)
        serializer = serializers.DogModelSerializer(dog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        serializer = serializers.DogModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        serializer = serializers.DogModelCreateSerializer(data=request.data, context={"request": self.request})
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


class ScheduleViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthorized, IsWalker]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = request.data['jwt-payload']
        hours = walker_scheduler_repo.lists(user['user_id'])
        serializer = serializers.ScheduleModelSerializer(hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.data['jwt-payload']
        hour = walker_scheduler_repo.find(user['user_id'], pk)
        serializer = serializers.ScheduleModelSerializer(hour)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.data['jwt-payload']
        request.data['walker'] = user['user_id']
        request.data['id'] = None
        serializer = serializers.ScheduleModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.data['jwt-payload']
        request.data['walker'] = user['user_id']
        request.data['id'] = int(pk)
        serializer = serializers.ScheduleModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        updated = walker_scheduler_repo.update(user['user_id'], pk, request.data)
        if updated:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        user = request.data['jwt-payload']
        deleted = walker_scheduler_repo.delete(user['user_id'], pk)
        if deleted:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class ReservationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthorized, IsOwner]
        return [permission() for permission in permission_classes]

    def list(self, request):
        user = request.data['jwt-payload']
        reservations = reservation_repo.lists(user['user_id'], 'owner')
        serializer = serializers.ReservationModelSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.data['jwt-payload']
        reservation = reservation_repo.find(user['user_id'], pk, 'owner')
        serializer = serializers.ReservationModelSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        request.data['status'] = models.Reservation.Status.OPEN
        serializer = serializers.ReservationModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.data['jwt-payload']
        request.data['owner'] = user['user_id']
        request.data['status'] = models.Reservation.Status.OPEN
        reservation_repo.find(user['user_id'], pk, 'owner')
        serializer = serializers.ReservationModelCreateSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        reservation_repo.update(user['user_id'], pk, request.data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        user = request.data['jwt-payload']
        reservation_repo.find(user['user_id'], pk, 'owner')
        reservation_repo.delete(user['user_id'], pk, 'owner')
        return Response(None, status=status.HTTP_204_NO_CONTENT)
