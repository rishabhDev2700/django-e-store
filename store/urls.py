"""store urls"""

from django.urls import path
from store.views import (
    homepage,
    explore,
    list_categories,
    list_all,
    list_best_sellers,
    list_new_arrivals,
    review_form,
    show_category,
    show_product,
    search_products,
    product_by_tag,
    terms_and_conditions,
    privacy
)

app_name = "store"
urlpatterns = [
    path("", homepage, name="home"),
    path("explore/", explore, name="explore"),
    path("categories/", list_categories, name="categories"),
    path("category/<slug:slug>/", show_category, name="show-category"),
    path("products/", list_all, name="all-products"),
    path("product/<slug:slug>/", show_product, name="show-product"),
    path("best-sellers/", list_best_sellers, name="best-sellers"),
    path("new-arrivals/", list_new_arrivals, name="new-arrivals"),
    path("review/<int:id>/", review_form, name="review-form"),
    path("search/", search_products, name="search"),
    path("tag/<slug:slug>/", product_by_tag, name="products-by-tag"),
    path("terms/", terms_and_conditions, name="terms"),
    path("privacy-policy/", privacy, name="privacy"),
    # path("checkout/<int:order_id>/", initiate_payment, name="checkout"),
    # path("payment/success/", payment_success, name="payment-success"),
    # path("payment/failure/", payment_failure, name="payment-failure"),
    # path("track-event/", track_event, name="track-event"),
]
