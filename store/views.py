from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from random import sample
from django.utils import timezone
from django.db.models import Avg, Count
from taggit.models import Tag
from store.forms import RatingForm
from store.models import Category, Product, ProductImage, Rating

# Import any additional models related to payments or analytics if needed.
# For example, if you created a Payment model, you might import it here:
# from store.models import Payment

# -----------------------
# Analytics Suggestions
# -----------------------
# Option 1: Frontend Analytics
#  - Integrate tools like Google Analytics, Mixpanel, or Matomo by adding their JS snippet in your base template.
#
# Option 2: In-app analytics
#  - Create a middleware or utility function to log page views or user events into your AnalyticsEvent model.
#  - For example, you might call an analytics logging function inside your view functions:
#
# def log_event(user, event_type, metadata=None):
#     AnalyticsEvent.objects.create(user=user, event_type=event_type, metadata=metadata)
#
# Then, inside a view:
# log_event(request.user, 'PAGE_VIEW', {'page': 'homepage'})
#
# -------------------------------
# Multiple Payment Processors
# -------------------------------
# Consider adding separate views for initiating payments. The logic in these views would:
#  - Determine which payment processor to use (e.g., based on user preference or location).
#  - Create a Payment record (if using a Payment model).
#  - Redirect the user to the payment processor’s checkout.
#
# Example placeholder view for payment initiation:
#
# def initiate_payment(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     # Determine payment method (this could be passed as a GET/POST parameter or based on user selection)
#     payment_method = request.GET.get('method', 'STRIPE')
#     # Create a Payment object or call the respective processor's API
#     # For example:
#     # payment = Payment.objects.create(order=order, payment_method=payment_method, amount=order.total, status='PENDING')
#     # Depending on the payment method, generate the appropriate checkout URL
#     # Redirect the user accordingly.
#     # For now, we'll simply redirect to a dummy page:
#     return render(request, "store/payment-initiation.html", {"order": order, "payment_method": payment_method})
#

# ----------------------------
# Updated Views (with comments)
# ----------------------------


def homepage(request):
    """
    Home page of the website
    """
    categories = Category.objects.all()
    new_arrivals = Product.objects.all()[:10]
    tags = Tag.objects.all()
    context = {
        "title": "Lumière Store",
        "products": new_arrivals,
        "tags": tags,
        "categories": categories,
    }

    # Optional: Log a page view event for analytics (if implementing backend analytics)
    # log_event(request.user, 'PAGE_VIEW', {'page': 'homepage'})

    return render(request, "store/home.html", context=context)


def explore(request):
    """
    Explore page of the website
    """
    # Fetch latest products
    latest_products = Product.objects.filter(is_available=True).order_by("-date_added")[
        :8
    ]

    # Fetch trending products (highest-rated)
    trending_products = (
        Product.objects.filter(is_available=True)
        .annotate(avg_rating=Avg("rating__rating"))
        .order_by("-avg_rating", "-date_added")[:8]
    )

    # Fetch products on discount
    discounted_products = Product.objects.filter(
        discount__valid_till__gte=timezone.now()
    )[:8]

    # Get featured categories (randomly selecting 4)
    all_categories = list(Category.objects.all())
    featured_categories = sample(all_categories, min(len(all_categories), 4))

    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        "latest_products": latest_products,
        "trending_products": trending_products,
        "discounted_products": discounted_products,
        "featured_categories": featured_categories,
        "categories": categories,
        "tags": tags,
    }
    # Optional: log analytics event
    # log_event(request.user, 'PAGE_VIEW', {'page': 'explore'})

    return render(request, "store/explore.html", context=context)


def list_all(request):
    """
    Shows all available products with pagination.
    """
    products = Product.objects.filter(is_available=True)
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    # Optional: record analytics event for product listing view
    # log_event(request.user, 'VIEW_PRODUCTS_LIST', {'page': page_number})

    context = {"products": page, "tags": Tag.objects.all()}
    return render(request, "store/list-all.html", context=context)


def show_product(request, slug):
    """Show a particular product along with reviews and images."""
    product = get_object_or_404(Product, slug=slug)
    reviews = Rating.objects.filter(product=product)[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    images = ProductImage.objects.filter(product=product)

    # Optional: log product view event for analytics
    # log_event(request.user, 'PRODUCT_VIEW', {'product_id': product.id})

    context = {
        "product": product,
        "reviews": reviews,
        "categories": categories,
        "tags": tags,
        "images": images,
    }
    return render(request, "store/single-item.html", context=context)


def list_categories(request):
    """
    Shows the list of categories.
    """
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # Optional: log event for category listing
    # log_event(request.user, 'VIEW_CATEGORIES')
    tags = Tag.objects.all()
    context = {"categories": categories, "tags": tags}
    return render(request, "store/categories.html", context=context)


def show_category(request, slug):
    """Shows all products in a given category."""
    category = get_object_or_404(
        Category.objects.prefetch_related("product_set"), slug=slug
    )
    products = category.product_set.filter(is_available=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # Optional: log category view event
    # log_event(request.user, 'CATEGORY_VIEW', {'category': category.name})

    context = {
        "title": category.name,
        "category": category,
        "products": products,
        "categories": categories,
        "tags": tags,
    }
    return render(request, "store/list-items.html", context=context)


def list_best_sellers(request):
    """Fetches the best sellers."""
    # Future enhancement: filter products based on sales data stored via analytics
    return render(request, "store/list-best-sellers.html")


def list_new_arrivals(request):
    """Fetches the new arrivals from the database."""
    # Future enhancement: you can order by 'date_added' and optionally record this page view.
    return render(request, "store/list-new-arrivals.html")


def review_form(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        data = request.POST.copy()
        form = RatingForm(data=data)
        if form.is_valid():
            form.save()
            # Optional: log review submission event
            # log_event(request.user, 'SUBMIT_REVIEW', {'product_id': product.id})
            return redirect("store:show-product", product.slug)
        else:
            return render(request, "store/review-page.html", context={"form": form})

    # Pre-populate form data if possible.
    form = RatingForm(initial={"product": product, "user": request.user})
    return render(
        request, "store/review-page.html", context={"form": form, "product": product}
    )


def search_products(request):
    query = request.GET.get("query")
    # Enhanced search: consider using full-text search via SearchVector for better results
    search_result = Product.objects.annotate(
        search=SearchVector("name", "description", "slug")
    ).filter(search=query)
    # search_result = Product.objects.filter(name__istartswith=query)

    # Optional: log search event with query details
    # log_event(request.user, 'SEARCH', {'query': query})

    context = {
        "products": search_result,
        "tags": Tag.objects.all(),
        "category": {"name": "Search results"},
    }
    return render(request, "store/list-items.html", context=context)


def product_by_tag(request, slug):
    products = Product.objects.filter(tags__slug=slug)
    tags = Tag.objects.all()

    # Optional: log event for tag filtering
    # log_event(request.user, 'TAG_FILTER', {'tag': slug})

    return render(
        request, "store/list-items.html", {"products": products, "tags": tags}
    )


def terms_and_conditions(request):
    return render(request, "store/terms.html")


def privacy(request):
    return render(request, "store/privacy.html")
