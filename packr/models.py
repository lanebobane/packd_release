from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    name = models.CharField(max_length=100)
    weight = models.FloatField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    dimension_z = models.FloatField()
    is_bag = models.BooleanField(default=False)
    reference_pk = models.PositiveIntegerField(default=None, null=True, blank=True)

    traveler = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def volume(self):
        return self.dimension_x * self.dimension_y * self.dimension_z


class Pack(models.Model):
    name = models.CharField(max_length=100, default=None)
    bag = models.ForeignKey(
        Item, related_name="bag", null=True, on_delete=models.CASCADE
    )
    items = models.ManyToManyField(Item, related_name="items")

    traveler = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def volume_remaining(self):
        vol_remaining = self.bag.volume() if self.bag else 0
        for i in self.items.all():
            vol_remaining -= i.volume()
        return vol_remaining

    def pack_weight(self):
        return sum([item.weight for item in self.items.all()], self.bag.weight if self.bag else 0)
