from django.test import TestCase
from .models import Item, Pack
from django.contrib.auth.models import User

# Create your tests here.

# Test Ideas
# 1. validate that a user shouldn't see another users items (on their dashboard or when creating a Pack).


class ItemTest(TestCase):

    # Test Data
    def create_bag(
        self,
        traveler=None,
        name="Default Test Bag Name",
        weight=10,
        dimension_x=1,
        dimension_y=2,
        dimension_z=3,
        is_bag=True,
    ):
        return Item.objects.create(
            name=name,
            weight=weight,
            dimension_x=dimension_x,
            dimension_y=dimension_y,
            dimension_z=dimension_z,
            is_bag=is_bag,
            traveler=traveler,
        )

    def create_item(
        self,
        traveler=None,
        name="Default Test Item Name",
        weight=10,
        dimension_x=4,
        dimension_y=5,
        dimension_z=6,
        is_bag=False,
    ):
        return Item.objects.create(
            name=name,
            weight=weight,
            dimension_x=dimension_x,
            dimension_y=dimension_y,
            dimension_z=dimension_z,
            is_bag=is_bag,
            traveler=traveler,
        )

    def create_traveler_a(self, username="Traveler A", email="traveler_a@packd.com"):
        return User(username=username, email=email)

    def create_traveler_b(self, username="Traveler B", email="traveler_b@packd.com"):
        return User(username=username, email=email)

    def create_pack(
        self, traveler=None, name="Default Test Pack Name", bag=None, items=None
    ):
        pack = Pack.objects.create(name=name, bag=bag, traveler=traveler)
        pack.items.set(items)
        return pack

    # Test Bags

    def test_bag_creation(self):
        traveler = self.create_traveler_a()
        traveler.save()
        bag = self.create_bag(traveler)
        self.assertTrue(isinstance(bag, Item))
        self.assertEqual(bag.__str__(), bag.name)
        self.assertTrue(bag.traveler.id == traveler.id)

    def test_bag_volume(self):
        bag = self.create_bag()
        self.assertTrue(bag.volume() == 6)

    def test_is_bag(self):
        bag = self.create_bag()
        self.assertTrue(bag.is_bag)

    # Test Non-bag Items

    def test_item_creation(self):
        traveler = self.create_traveler_b()
        traveler.save()
        item = self.create_item(traveler)
        self.assertTrue(isinstance(item, Item))
        self.assertEqual(item.__str__(), item.name)
        self.assertTrue(item.traveler.id == traveler.id)

    def test_item_volume(self):
        item = self.create_item()
        self.assertTrue(item.volume() == 120)

    def test_is_not_bag(self):
        item = self.create_item()
        self.assertFalse(item.is_bag)

    # Test Packs

    def test_pack_creation(self):
        traveler = self.create_traveler_a()
        traveler.save()
        bag = self.create_bag(traveler)
        item1 = self.create_item(traveler)
        item2 = self.create_item(traveler)
        pack = self.create_pack(traveler, "test_pack_creation", bag, [item1, item2])
        self.assertTrue(isinstance(pack, Pack))
        self.assertEqual(pack.__str__(), "test_pack_creation")
        self.assertTrue(pack.traveler.id == traveler.id)
        self.assertTrue(len(pack.items.all()) == 2)

    def test_pack_volume_remaining(self):
	    traveler = self.create_traveler_a()
	    traveler.save()
	    bag = self.create_bag(traveler)
	    item1 = self.create_item(traveler)
	    item2 = self.create_item(traveler)
	    pack = self.create_pack(traveler, "test_pack_volume_remaining", bag, [item1, item2])
	    self.assertTrue(pack.volume_remaining() == -234)

    def test_pack_item_ownership(self):
    	traveler = self.create_traveler_a()
    	traveler.save()
    	bag = self.create_bag(traveler)
    	item1 = self.create_item(traveler)
    	item2 = self.create_item(traveler)
    	pack = self.create_pack(traveler, "test_pack_volume_remaining", bag, [item1, item2])
    	for item in pack.items.all():
    		if item.traveler.id != traveler.id:
    			self.assertFalse(True)
    	self.assertTrue(True)

    def test_pack_weight(self):
    	traveler = self.create_traveler_a()
    	traveler.save()
    	bag = self.create_bag(traveler)
    	item1 = self.create_item(traveler)
    	item2 = self.create_item(traveler)
    	pack = self.create_pack(traveler, "test_pack_volume_remaining", bag, [item1, item2])
    	self. assertTrue(pack.pack_weight() == 30)