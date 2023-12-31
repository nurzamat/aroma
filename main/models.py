from django.db import models


# Модель продукта
class News(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=True, verbose_name="Изображение")
    video = models.URLField(max_length=200, blank=True, verbose_name="Ссылка на видео")
    description = models.TextField(blank=True, verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

class Testimonials (models.Model):
    name=models.CharField(max_length=200,db_index=True,verbose_name="ФИО")
    profession=models.CharField(max_length=200,verbose_name="Профессия")
    text=models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name

# Модель продукта
class Sliders(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=True, verbose_name="Изображение")
    video = models.URLField(max_length=200, blank=True, verbose_name="Ссылка на видео")
    description = models.TextField(blank=True, verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'

    def __str__(self):
        return self.title