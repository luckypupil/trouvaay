from django.views import generic
from goods.models import Product, Category, FurnitureType, Segment, ProductImage, Color, Style, Subcategory
from members.models import AuthUserActivity, OfferType, PromotionOffer
from django.core.serializers import serialize
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
# from goods.forms import CommentForm
from random import randint
import logging
from django.conf import settings
from random import shuffle

from helper import is_time_to_show_modal, hide_modal, Neighborhoods
import uuid

# from helper import get_liked_items

from pprint import pprint as pp
from endless_pagination.views import AjaxListView



logger = logging.getLogger(__name__)

BASE_URL = 'http://res.cloudinary.com/trouvaay/image/upload/'


class LandingView(AjaxListView):
    template_name = 'goods/main/landing_ajax.html'
    page_template = 'goods/main/landing_ajax_page.html'
    context_object_name = 'products'
    model = Product
    key = 'page'


    def get_queryset(self):
        try:
            furn_type = self.request.GET['type']
            try:
                furniture_type_object = FurnitureType.objects.get(select=furn_type)
            except Exception, e:
                logger.debug(str(e))
                furniture_type_object = None
            queryset = list(self.model.objects.filter(is_published=True, furnituretype = furniture_type_object, store__is_featured=True))
        except:
            queryset = self.model.objects.filter(is_published=True, store__is_featured=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['BaseUrl'] = BASE_URL
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['searchfilter'] = {
                                   'price_slider_min': 0,
                                   'price_slider_max': 10000,
                                   'height_slider_min': 0,
                                   'height_slider_max': 1000,
                                   'width_slider_min': 0,
                                   'width_slider_max': 1000,
                                   'depth_slider_min': 0,
                                   'depth_slider_max': 1000,
                                   'segments': Segment.objects.all(),
                                   'colors': Color.objects.all(),
                                   'styles': Style.objects.all(),
                                   'furnituretypes': FurnitureType.objects.all(),
                                   'neighborhoods': Neighborhoods['SF']
                                   }

        # TODO: do not add 'site_name' to context
        # once the 'sites' are setup in settings
        context['site_name'] = settings.SITE_NAME
        # removed until profile page implemented
        # context['liked_items'] = get_liked_items(self.request.user)
        return context


class SearchFilterView(AjaxListView):
    template_name = 'goods/main/landing_ajax_page.html'
    page_template = 'goods/main/landing_ajax_page.html'

    context_object_name = 'products'
    model = Product
    key = 'page'

    def get_queryset(self):

        queryset = self.model.objects.filter(is_published=True)
        segments = [int(i) for i in self.request.GET.getlist('filter-segment')]
        if(segments):
            queryset = queryset.filter(segment__in=segments)

        subcategories = [int(i) for i in self.request.GET.getlist('filter-subcategory')]
        if(segments):
            queryset = queryset.filter(subcategory__in=subcategories)

        colors = [int(i) for i in self.request.GET.getlist('filter-color')]
        if(colors):
            queryset = queryset.filter(color__in=colors)

        # TODO: enable styles, styles are for now disabled
        # styles = [int(i) for i in self.request.GET.getlist('filter-style')]
        # if(styles):
        #    queryset = queryset.filter(style__in=styles)

        furnituretypes = [int(i) for i in self.request.GET.getlist('filter-furnituretype')]
        if(furnituretypes):
            queryset = queryset.filter(furnituretype__in=furnituretypes)

        neighborhoods = self.request.GET.getlist('filter-neighborhood')
        if(neighborhoods):
            queryset = queryset.filter(store__neighborhood__in=neighborhoods)

        price_min = self.request.GET.get('filter-price-min', None)
        if(price_min):
            price_min = int(price_min)
            queryset = queryset.filter(current_price__gte=price_min)

        price_max = self.request.GET.get('filter-price-max', None)
        if(price_max):
            price_max = int(price_max)
            queryset = queryset.filter(current_price__lte=price_max)

        height_min = self.request.GET.get('filter-height-min', None)
        if(height_min):
            height_min = int(height_min)
            queryset = queryset.filter(height__gte=height_min)

        height_max = self.request.GET.get('filter-height-max', None)
        if(height_max):
            height_max = int(height_max)
            queryset = queryset.filter(height__lte=height_max)

        width_min = self.request.GET.get('filter-width-min', None)
        if(width_min):
            width_min = int(width_min)
            queryset = queryset.filter(width__gte=width_min)

        width_max = self.request.GET.get('filter-width-max', None)
        if(width_max):
            width_max = int(width_max)
            queryset = queryset.filter(width__lte=width_max)

        depth_min = self.request.GET.get('filter-depth-min', None)
        if(depth_min):
            depth_min = int(depth_min)
            queryset = queryset.filter(depth__gte=depth_min)

        depth_max = self.request.GET.get('filter-depth-max', None)
        if(depth_max):
            depth_max = int(depth_max)
            queryset = queryset.filter(depth__lte=depth_max)

        return queryset


class DetailView(generic.DetailView):
    template_name = 'goods/detail/detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['returns'] = settings.RETURN_POLICY
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

        product = self.get_object()

        # click counter
        exclude_emails = settings.CLICK_EXCLUSIONS
        if(self.request.user.is_authenticated()):
            if not self.request.user.email in exclude_emails:
                product.click_count += 1
                product.save()
                logger.debug('added to click-count')
        else:
            product.click_count += 1
            product.save()
            logger.debug('added to click-count')

        return context


class AboutView(generic.TemplateView):
    template_name = 'goods/copy/about.html'

class ReturnsView(generic.TemplateView):
    template_name = 'goods/copy/returns.html'


# class DirectionsView(LoginRequiredMixin, generic.DetailView):
#     template_name = 'goods/detail/map.html'
#     context_object_name = 'product'
#     model = Product

#     def get_context_data(self, **kwargs):
#         context = super(DirectionsView, self).get_context_data(**kwargs)
#         context['store'] = self.object.store
#         return context


# Gets list of liked items to populate 'active' hearts


#####Additional views for copy pages######

# class ContactView(generic.TemplateView):
#     template_name = 'goods/copy/contact.html'


# class BlogView(generic.TemplateView):
#     template_name = 'goods/copy/blog.html'


# class BlogPostView(generic.TemplateView):
#     template_name = 'goods/copy/blogpost.html'
