from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """ Add a quantity of a specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # get or create the bag variable in the session if it doesn't exist already
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        # update quantity if it already exists
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # overwrite the session with the updated version
    request.session['bag'] = bag
    return redirect(redirect_url)
