from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from orders.bag import Bag
from store.models import Category, Order, OrderProduct
from store.models import Product as Item
from taggit.models import Tag


# Create your views here.
def bag_summary(request):
    bag = Bag(request)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        "bag": bag,
        "quantity": bag.__len__(),
        "categories": categories,
        "tags": tags,
    }
    return render(request, "orders/bag_summary.html", context=context)


def bag_add(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        item = get_object_or_404(Item, id=item_id)
        bag.add(item=item, quantity=quantity)
        bag_quantity = bag.__len__()
        messages.success(request, f"{item.name} added to bag")
        response = JsonResponse(
            {"quantity": bag_quantity, "message": f"{item.name} added"}
        )
        return response


def bag_delete(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        item = get_object_or_404(Item, id=item_id)
        bag.delete(item=item)
        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse(
            {
                "quantity": bag_quantity,
                "subtotal": bag_subtotal,
                "message": f"{item.name} removed",
            }
        )
        return response


def bag_update(request):
    bag = Bag(request)
    if request.POST.get("action") == "post":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity"))
        item = get_object_or_404(Item, id=item_id)
        bag.update(item=item, quantity=quantity)
        bag_quantity = bag.__len__()
        bag_subtotal = bag.get_subtotal()
        response = JsonResponse(
            {
                "quantity": bag_quantity,
                "subtotal": bag_subtotal,
                "message": f"{item.name} updated",
            }
        )
        return response


def bag_clear(request):
    bag = Bag(request)
    bag.clear()
    return JsonResponse({"quantity": 0, "subtotal": 0, "message": "Bag Cleared"})


def view_orders(request):
    all_orders = Order.objects.filter(user=request.user)
    print(all_orders)
    incompleted = all_orders.filter(is_completed=False)
    incompleted_orders = []
    for order in incompleted:
        items = OrderProduct.objects.filter(order=order)
        incompleted_orders.append([order, items])
    completed = all_orders.filter(is_completed=True)
    completed_orders = []
    for order in completed:
        items = OrderProduct.objects.filter(order=order)
        completed_orders.append([order, items])
    context = {
        "completed_orders": completed_orders,
        "incompleted_orders": incompleted_orders,
    }
    print(context)
    return render(request, "orders/view_orders.html", context=context)
