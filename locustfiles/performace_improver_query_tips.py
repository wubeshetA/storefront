""" tips to improve query performance 
"""
from store.models import Product

# Preload related objects
Product.objects.select_related('...')
Product.objects.prefetch_related('...')

# Load only what you need
Product.objects.only('title')
Product.objects.defer('title')

# Use values
# We can use values if we won't need the model instances for further processing. values return dict or list
Product.objects.values('title', 'collection__title')
Product.objects.values_list('title', 'collection__title')

# Count properly
Product.objects.count()
len(Product.objects.all()) # This will load all objects into memory and is bad for performance

# Bulk create/update
Product.objects.bulk_create([])