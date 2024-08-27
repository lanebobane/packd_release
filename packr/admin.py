from django.contrib import admin
from .models import Item, Pack


admin.site.site_header = "Packd Header Placeholder"
admin.site.site_title = "Packd Website Title Placeholder"
admin.site.index_title = "Packd Index Title Placeholder"


# Register your models here.


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = (
        "pack_name",
        "traveler",
    )

    def traveler(self, obj):
        return obj.traveler.username

    def pack_name(self, obj):
        return obj.name


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_name",
        "traveler",
        "weight",
        "dimension_x",
        "dimension_y",
        "dimension_z",
        "is_bag",
    )

    def item_name(self, obj):
        return obj.name

    def traveler(self, obj):
        return item.travler.username

    def weight(self, obj):
        return obj.weight

    def dimenson_x(self, obj):
        return obj.dimenson_x

    def dimenson_y(self, obj):
        return obj.dimenson_y

    def dimenson_z(self, obj):
        return obj.dimenson_z

    def is_bag(self, obj):
        return obj.is_bag
