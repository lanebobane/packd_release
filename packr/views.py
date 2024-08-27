from django.shortcuts import render, redirect, reverse
from .forms import ItemForm, PackForm
from .models import Item, Pack
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Create your views here.


@login_required
def dashboard(request):
    items = Item.objects.filter(is_bag=False, traveler=request.user)
    bags = Item.objects.filter(is_bag=True, traveler=request.user)
    packs = Pack.objects.filter(traveler=request.user)
    context = {"items": items, "bags": bags, "packs": packs}

    return render(request, "packr/dashboard.html", context)


@login_required
def add_item(request, **kwargs):
    pk = kwargs.get("pk")
    if pk:
        item = get_object_or_404(Item, pk=pk)
        if item.traveler != request.user:
            return HttpResponseForbidden()
    else:
        item = Item(traveler=request.user)

    form = ItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        item = form.save()
        item.reference_pk = item.id
        item.save()
        return redirect("/items/add")

    context = {"form": form}

    return render(request, "packr/additem.html", context)


@login_required
def add_pack(request, **kwargs):
    pk = kwargs.get("pk")
    if pk:
        pack = get_object_or_404(Pack, pk=pk)
        if pack.traveler != request.user:
            return HttpResponseForbidden()
    else:
        pack = Pack(traveler=request.user)

    form = PackForm(request.POST or None, instance=pack)
    form.fields["bag"].queryset = Item.objects.filter(
        is_bag=True, traveler=request.user
    )
    form.fields["items"].queryset = Item.objects.filter(traveler=request.user)

    if request.method == "POST" and form.is_valid():
        pack = form.save()
        return redirect("/dashboard")

    context = {"form": form}

    return render(request, "packr/addpack.html", context)


def shared_packs(request):
    anonymous_packs = Pack.objects.filter(traveler=None)
    context = {"packs": anonymous_packs}
    return render(request, "packr/sharedpacks.html", context)


def share_pack(request, pk):
    if request.method == "POST":
        obj = Pack.objects.filter(pk=pk)
        reference_items = obj[0].items.all()
        copied_items = []
        for item in reference_items:
            temp_item_data = {
                    'name': item.name,
                    'dimension_x': item.dimension_x,
                    'dimension_y': item.dimension_y,
                    'dimension_z': item.dimension_z,
                    'weight': item.weight,
                    'is_bag': item.is_bag,
                    'reference_pk': item.pk
                }
            item = Item.objects.create(**temp_item_data)
            copied_items.append(item)
        data = dict(obj.values()[0])
        data.pop("id")
        data.pop("traveler_id")
        # TODO: Do we want to add an option to share bag? Same with adopt.
        data.pop("bag_id")
        pack = Pack.objects.create(**data)
        pack.items.set(copied_items)

        return redirect("/dashboard")


def adopt_pack(request, pk):
    if request.method == "POST":
        pack = Pack.objects.filter(pk=pk) 
        reference_items = pack[0].items.all()
        
        # we only want to copy Items in the Pack that the user doesn't already have 
        # (e.g. has already copied via adopting another pack or the same pack previously).
        user_items = Item.objects.filter(traveler_id=request.user.id)
        user_items_values = user_items.values()
        user_items_dict = {}

        for item in user_items_values:
            user_items_dict[item['reference_pk']] = item
        
        copied_items = []
        existing_items_ids = []
        
        for item in reference_items:
            if item.id in user_items_dict:
                existing_items_ids.append(item.id)
            else:
                temp_item_data = {
                    'name': item.name,
                    'dimension_x': item.dimension_x,
                    'dimension_y': item.dimension_y,
                    'dimension_z': item.dimension_z,
                    'weight': item.weight,
                    'is_bag': item.is_bag,
                    'traveler_id': request.user.id,
                    'reference_pk': item.pk
                }
                item = Item.objects.create(**temp_item_data)
                copied_items.append(item)

        # avoid a second network call. just use the items we already queried for before. 
        for item in user_items:
            if item.reference_pk in existing_items_ids:
                copied_items.append(item)


        data = dict(pack.values()[0])
        data.pop("id")
        data["traveler_id"] = request.user.id
        new_pack = Pack.objects.create(**data)
        new_pack.items.set(copied_items)

        return redirect("/dashboard")


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()

        return redirect("/dashboard")


def delete_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    if request.method == "POST":
        pack.delete()

        return redirect("/dashboard")
