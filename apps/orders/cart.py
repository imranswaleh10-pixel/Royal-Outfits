from apps.products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        key = str(product.pk)
        if key not in self.cart:
            self.cart[key] = {'quantity': 0, 'price': str(product.price)}
        self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        key = str(product_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def update(self, product_id, quantity):
        key = str(product_id)
        if key in self.cart:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.cart[key]['quantity'] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = product
        for item in cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
