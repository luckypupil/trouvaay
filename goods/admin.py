from django.contrib import admin

from goods.models import Product, Segment, Style, Category, Subcategory, Material, ProductImage, Comment


# class SegmentInline(admin.TabularInline):
# 	model = Segment

# class MaterialInline(admin.TabularInline):
# 	model = Material

class ProductImageInline(admin.StackedInline):
	model = ProductImage
	fields = (('name','image','is_main'),)
	verbose_name = 'photo'

class CommentInline(admin.StackedInline):
	model = Comment
	fields = ('product','authuser','message')

class ProductAdmin(admin.ModelAdmin):
	model = Product
	filter_vertical = ('style','segment','category','subcategory','material')
	list_display = ['short_name', 'store', 'current_price', 'original_price']
	fields = ['short_name', 'store', 'units',('original_price', 'current_price'), 'pub_date','style','segment']
	
	inlines = [ProductImageInline, CommentInline]
	search_fields = ['short_name', 'long_name','store']
	list_filter = ['store']

	

admin.site.register(Product, ProductAdmin)

