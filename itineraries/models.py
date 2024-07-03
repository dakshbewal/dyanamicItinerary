from django.db import models


class ItineraryTemp(models.Model):
    itinerary_id = models.AutoField(primary_key=True)
    travel_destination = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(blank=True, null=True)    
    lead_id = models.IntegerField(null=True)
    quotation_id = models.IntegerField(unique= True, null=True)

    def __str__(self):
        # Customize this string representation as needed
        return f"{self.travel_destination} {self.created_at} - {self.duration}"

    class Meta:
        managed = False
        db_table = 'itinerarytemp'

class ItineraryMaster(models.Model):
    detail_id = models.AutoField(primary_key=True)
    itinerary = models.ForeignKey(ItineraryTemp, on_delete=models.CASCADE)  # Link to master table
    title = models.CharField(max_length=50) #title of the itinerary day
    day_number = models.IntegerField()  # Which day of the itinerary
    activity = models.CharField(max_length=200)  # Activity description

    def __str__(self):
        return f"Day {self.day_number}: {self.activity}"
    class Meta:
        managed = False
        db_table = 'itinerarymaster'



