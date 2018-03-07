from django.db import models


# class Map(models.Model):
#     def __str__(self):
#         return self.map_text
#     map_text = models.CharField(max_length=200)

#     def was_published_recently(self):
#         return self.pub_date >=timezone.now() - datetime.timedelta(days=1)
#     pub_date = models.DateTimeField('date published')

class Trip(models.Model):
    attraction = models.CharField(unique=True, max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)  
    types = models.CharField(max_length=200, blank=True, null=True)
    place_id = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)  
    lng = models.FloatField(blank=True, null=True)  
    
    class Meta:
        managed = False
        db_table = 'trip'






# class Choice(models.Model):
#     def __str__(self):
#         return self.choice_text 
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)


