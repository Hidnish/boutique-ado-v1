from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Jsm1AK3t42VTVBEFu4rR3Sw6CyHHB2pWPmTVqxpuKGCH1jUm0PPV7NokU9ZpiTSg8Uczm1DDHTaVVAZbNRDE2pB005q4M8TIe',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
