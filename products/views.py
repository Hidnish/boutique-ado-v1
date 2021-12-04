from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# way to handle queries (check documentation)
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            # Create the sortkey variable
            sortkey = request.GET['sort']
            # Make a copy of it and call it sort which we'll use later to construct current_sorting =                     f'{sort}_{direction}'
            sort = sortkey
            # If the field we want to sort on is 'name'
            if sortkey == 'name':
                # Let's actually sort (i.e. order_by) on one called 'lower_name', in order to ensure it doesn't order Z before a just because the Z is uppercase
                sortkey = 'lower_name'
                # Annotate all the products w/ a new field, lower_name=Lower('name') and sort based on it
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)  # --> this becomes products.order_by('lower_name') now

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # double underscore syntax (__name__) is common when making queries in django here you are looking for the name field of the category model cause category and product are related with FK
            products = products.filter(category__name__in=categories)
            # convert string in list of categories into category objects to be accessed in the template
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'You did not enter any search criteria!')
                return redirect(reverse('products'))

            # 'i' makes the queries case insensitive
            queries = Q(name__contains=query) | Q(description__contains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """Add a product to the store"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added Product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """Edit a product in the store"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """Delete product from store"""
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "Product Deleted!")
    return redirect(reverse('products'))
