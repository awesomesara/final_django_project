from django.db import models


class BookModel(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name=None)
    public_date = models.DateField(auto_now_add=True)
    borrow = models.ForeignKey('BorrowModel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books', blank=True, null=True)


class CategoryModel(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)


class AuthorModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class BorrowModel(models.Model):
    available = models.BooleanField()
    borrowed_date = models.DateField(auto_now_add=True)
    period = models.IntegerField()
