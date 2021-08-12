from .models import Dog


class Repository(object):
    def __init__(self, model):
        self.model = model


class DogRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Dog)

    def lists(self, user_id):
        return self.model.objects.filter(owner=user_id)

    def find(self, user_id, dog_id):
        return self.model.objects.filter(owner=user_id, pk=dog_id).first()

    def update(self, user_id, dog_id, data):
        fields = ('name', 'size',)
        data = {k: v for k, v in data.items() if k in fields}
        return self.model.objects.filter(owner=user_id, pk=dog_id).update(**data)

    def delete(self, user_id, dog_id):
        dog = self.model.objects.filter(owner=user_id, pk=dog_id).first()
        if dog is not None:
            dog.delete()
            return True
        return False
