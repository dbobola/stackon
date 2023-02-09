from django.db import models

# Create your models here.


class Collection(models.Model):
    name = models.CharField(max_length=200)
    open_price = models.DecimalField(max_digits=15, decimal_places=4)
    volume_24h = models.IntegerField(blank=True)
    tweets = models.IntegerField()
    sentiment = models.CharField(max_length=200)
    nft_index = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='collection_images')

    def __str__(self):
        return self.name

    class Meta:
      pass
   
