from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse  # для ссылок на обьекты

from transliterate import translit

# Create your models here.

#******************************************************************************

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)  # blank - обязательность заполнения
    def __str__(self):
        return self.name

    # для ссылок на обьекты
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})

# автозаполнение поля slug
def pre_save_category_slug_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug
pre_save.connect(pre_save_category_slug_category, sender=Category)

#******************************************************************************

class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#******************************************************************************

# сохраняет картинки с правильными именами
def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)

class ProductManager(models.Manager):
    # переопределяем all() для выборки относительно флага available
    def all(self, *args, **kwarks):
        return super(ProductManager, self).get_queryset().filter(available=True)

class Product(models.Model):
    category = models.ForeignKey(Category)
    brand = models.ForeignKey(Brand)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    # для ссылок на обьекты
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})
#******************************************************************************
# элемент корзины
class CartItem(models.Model):

    product = models.ForeignKey(Product)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart item for product {0}".format(self.product.title)


#******************************************************************************
# корзина
class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()
        return

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()
        return

