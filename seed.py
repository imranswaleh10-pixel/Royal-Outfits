"""
Run: python manage.py shell < seed.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from apps.products.models import Category, Product

cats = {}
for name, slug in [('Tops', 'tops'), ('Bottoms', 'bottoms'), ('Dresses', 'dresses'), ('Outerwear', 'outerwear')]:
    c, _ = Category.objects.get_or_create(name=name, slug=slug)
    cats[slug] = c
    print(f'Category: {name}')

products = [
    dict(name='Ankara wrap top', category=cats['tops'], price=1800, stock=12, size='M', description='Vibrant Ankara print wrap top. Perfect for casual outings or office wear.'),
    dict(name='High-waist denim jeans', category=cats['bottoms'], price=3200, stock=3, size='L', description='Classic high-waist jeans in dark wash. Slim fit, very comfortable.'),
    dict(name='Floral maxi dress', category=cats['dresses'], price=4500, stock=0, size='one_size', description='Light, flowy maxi dress with a floral print. Great for events and weekends.'),
    dict(name='Bomber jacket', category=cats['outerwear'], price=5800, stock=7, size='XL', description='Warm bomber jacket with ribbed cuffs. Pairs well with anything.'),
    dict(name='Striped linen shirt', category=cats['tops'], price=2200, stock=9, size='S', description='Breathable linen shirt in navy stripes. Perfect for Nairobi afternoons.'),
    dict(name='Pleated midi skirt', category=cats['bottoms'], price=2600, stock=5, size='M', description='Elegant pleated skirt in dusty rose. Office to evening ready.'),
]

for data in products:
    p, created = Product.objects.get_or_create(name=data['name'], defaults=data)
    print(f'{"Created" if created else "Exists"}: {p.name} — KES {p.price}')

print('\nSeed complete! Log in at /admin/ to add product images.')
