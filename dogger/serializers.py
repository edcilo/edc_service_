from rest_framework import serializers
from .models import Dog, DogSize


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
    size = serializers.IntegerField()

    def validate_size(self, value):
        try:
            return DogSize.objects.get(pk=value)
        except DogSize.DoesNotExist:
            raise serializers.ValidationError('The size is not valid')

    def create(self, data):
        return Dog.objects.create(**data)
