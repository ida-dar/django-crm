from django.db import models


class Service(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=50)
  price = models.CharField(max_length=50)
  description = models.CharField(max_length=2000)

  def __str__(self):
    return f"{self.name} {self.price}"


class Record(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  phone = models.CharField(max_length=15)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=50)
  zipcode = models.CharField(max_length=15)
  activated_services = models.ForeignKey(Service, blank=True, null=True, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Product(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=50)
  price = models.CharField(max_length=50)
  amount = models.IntegerField(max_length=50)
  description = models.CharField(max_length=2000)

  def __str__(self):
    return f"{self.name}, {self.price}, {self.amount}"


class Order(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  client_name = models.ForeignKey(Record, blank=True, null=True, on_delete=models.DO_NOTHING)
  activated_services = models.ForeignKey(Service, blank=True, null=True, on_delete=models.DO_NOTHING)
  ordered_products = models.ForeignKey(Product, blank=True, null=True, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f"{self.client_name}, {self.activated_services}, {self.ordered_products}"
