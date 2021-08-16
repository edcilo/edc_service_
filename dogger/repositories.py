from django.http import Http404
from .models import Dog, DogSize, WalkerScheduler, Reservation


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


class WalkerScheduleRepository(Repository):
    def __init__(self):
        Repository.__init__(self, WalkerScheduler)

    def lists(self, user_id):
        return self.model.objects.filter(walker=user_id)

    def find(self, user_id, hour_id):
        walker = self.model.objects.filter(walker=user_id, pk=hour_id).first()
        if walker is None:
            raise Http404
        return walker

    def update(self, user_id, hour_id, data):
        sizes = DogSize.objects.filter(pk__in=data['sizes'])
        fields = ('day', 'start', 'end')
        data = {k: v for k, v in data.items() if k in fields}
        hour = self.find(user_id, hour_id)
        hour.sizes.set(sizes)
        return self.model.objects.filter(walker=user_id, pk=hour_id).update(**data)

    def delete(self, user_id, hour_id):
        hour = self.find(user_id, hour_id)
        hour.delete()


class ReservationRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Reservation)

    def lists(self, user_id, entity):
        if entity == 'walker':
            return self.model.objects.filter(walker=user_id)
        return self.model.objects.filter(owner=user_id)

    def find(self, user_id, reservation_id, entity):
        if entity == 'walker':
            reservation = self.model.objects.filter(walker=user_id, pk=reservation_id).first()
        else:
            reservation = self.model.objects.filter(owner=user_id, pk=reservation_id).first()
        if reservation is None:
            raise Http404
        return reservation

    def update(self, user_id, reservation_id, data):
        fields = ('walker', 'dog', 'schedule', 'date')
        data = {k: v for k, v in data.items() if k in fields}
        return self.model.objects.filter(owner=user_id, pk=reservation_id).update(**data)

    def delete(self, user_id, reservation_id, entity):
        reservation = self.find(user_id, reservation_id, entity)
        reservation.delete()
