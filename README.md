# Threads KE — Online Clothing Store

A full Django-powered clothing store with:
- **Owner admin** — add products with photos, set prices and stock levels
- **Customer storefront** — browse, filter by category, search, view product detail
- **Shopping cart** — session-based, no login required
- **Checkout** — customer fills in name, phone, and delivery address
- **Order management** — owner sees all orders in the admin panel

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations products orders
python manage.py migrate

# 3. Create owner account (for /admin/)
python manage.py createsuperuser

# 4. Seed sample products (optional)
python manage.py shell < seed.py

# 5. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000/ — the shop is live.
Open http://127.0.0.1:8000/admin/ — log in as the owner.

---

## How the owner adds products

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser account
3. Click **Products → Add product**
4. Fill in: name, description, category, size, price, stock quantity
5. Upload a photo (JPG/PNG recommended, portrait orientation works best)
6. Click **Save** — the product appears on the store immediately

To update stock after a sale, just edit the product's **Stock** field.

---

## Pages

| URL | Page |
|-----|------|
| `/` | Shop — all products with category filter and search |
| `/product/<id>/` | Product detail with size, description, related items |
| `/cart/` | Shopping cart with quantity controls |
| `/cart/checkout/` | Checkout form (name, phone, address) |
| `/cart/confirmation/<id>/` | Order confirmation page |
| `/admin/` | Owner dashboard |

---

## Project structure

```
clothing_store/
├── manage.py
├── requirements.txt
├── seed.py
├── clothing_store/        # Project config
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── products/          # Category, Product models + storefront views
│   └── orders/            # Cart (session-based), Order, OrderItem
├── templates/
│   └── store/             # base, shop, product_detail, cart, checkout, confirmation
└── media/
    └── products/          # Uploaded product images go here
```

---

## Next steps

- [ ] Add M-Pesa / card payment integration (Pesapal or Paystack Kenya)
- [ ] Add customer login so they can track past orders
- [ ] Add SMS notifications via Africa's Talking API
- [ ] Add a discount/coupon system
- [ ] Deploy to Railway or Render (add `gunicorn` + WhiteNoise to requirements)
