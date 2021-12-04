from django.db import models

# Create your models here.
    
class Property(models.Model):
     name = models.CharField(max_length = 100)
     title = models.CharField(max_length = 100)
     description = models.TextField()
     price = models.IntegerField()
     created_at = models.DateTimeField(auto_now_add = True)
     
     def __str__(self):
          return self.title
      
     class Meta:
             ordering = ['-created_at']
             
class Property_Image(models.Model):
     property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name = 'media')
     images = models.ImageField( upload_to = 'pictures/', verbose_name ='Property Picture',null = False)
     
     def __str__(self):
          return f'{self.id}'
     
     