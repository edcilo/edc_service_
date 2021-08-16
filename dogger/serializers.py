from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Dog, DogSize, Reservation, WalkerScheduler


class DogSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogSize
        fields = ['id', 'label',]


class DogModelSerializer(serializers.ModelSerializer):
    size = DogSizeSerializer(read_only=True)

    class Meta:
        model = Dog

        fields = (
            'id',
            'name',
            'owner',
            'size',
        )


class DogModelCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    owner = serializers.UUIDField()
    size = serializers.PrimaryKeyRelatedField(queryset=DogSize.objects.all())

    def create(self, data):
        return Dog.objects.create(**data)


class ScheduleModelSerializer(serializers.ModelSerializer):
    sizes = DogSizeSerializer(many=True)

    class Meta:
        model = WalkerScheduler

        fields = (
            'id',
            'walker',
            'day',
            'start',
            'end',
            'sizes'
        )


class ScheduleModelCreateSerializer(serializers.Serializer):
    walker = serializers.UUIDField()
    day = serializers.ChoiceField(choices=WalkerScheduler.DaysOfWeek.choices)
    start = serializers.IntegerField(min_value=360, max_value=1320)
    end = serializers.IntegerField(min_value=390, max_value=1410)
    sizes = serializers.PrimaryKeyRelatedField(many=True, queryset=DogSize.objects.all())

    def validate_start(self, value):
        data = self.initial_data
        hours = WalkerScheduler.objects.filter(walker=data['walker'], day=data['day'])
        for h in hours:
            if not (h.start >= data['end'] or h.end <= data['start']) and data['id'] != h.id:
                raise serializers.ValidationError("The start time is taked")
        return value

    def validate_end(self, value):
        data = self.initial_data
        if value < data['start']:
            raise serializers.ValidationError("The end time is invalid")
        return value

    def create(self, data):
        sizes = data.pop('sizes')
        schedule = WalkerScheduler.objects.create(**data)
        schedule.sizes.set(sizes)
        return schedule


class ReservationModelSerializer(serializers.ModelSerializer):
    schedule = ScheduleModelSerializer()
    dog = DogModelSerializer()

    class Meta:
        model = Reservation

        fields = ('id', 'status', 'walker', 'owner', 'schedule', 'date', 'dog')


class ReservationModelCreateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Reservation.Status)
    owner = serializers.UUIDField()
    walker = serializers.UUIDField()
    dog = serializers.PrimaryKeyRelatedField(queryset=Dog.objects.all())
    schedule = serializers.PrimaryKeyRelatedField(queryset=WalkerScheduler.objects.all())
    date = serializers.DateField()

    def validate_dog(self, value):
        user = self.initial_data['owner']
        dog = Dog.objects.filter(owner=user, pk=value.id).count()
        if dog == 1:
            return value
        raise serializers.ValidationError("The dog does not exists")

    def validate_schedule(self, value):
        walker = self.initial_data['walker']
        dog = Dog.objects.get(pk=self.initial_data['dog'])
        schedule = self.initial_data['schedule']
        date = self.initial_data['date']
        reservation = Reservation.objects.filter(owner=walker, date=date, schedule=schedule).count()
        if reservation > 0:
            raise serializers.ValidationError("The schedule is taked")
        sch = WalkerScheduler.objects.get(pk=schedule)
        size = sch.sizes.filter(size=dog).count()
        if size == 0:
            raise serializers.ValidationError("The size is invalid")

        return value

    def create(self, data):
        return Reservation.objects.create(**data)
