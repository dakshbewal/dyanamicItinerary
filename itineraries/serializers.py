from rest_framework import serializers
from .models import ItineraryMaster, ItineraryTemp


class ItineraryMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItineraryMaster
        fields = ['detail_id', 'title', 'day_number', 'activity']

class ItineraryDetailsSerializer(serializers.ModelSerializer):
    details = ItineraryMasterSerializer(many=True, read_only=True, source='itinerarymaster_set')

    class Meta:
        model = ItineraryTemp
        fields = ['itinerary_id', 'travel_destination', 'created_at', 'duration', 'lead_id', 'quotation_id', 'details']
