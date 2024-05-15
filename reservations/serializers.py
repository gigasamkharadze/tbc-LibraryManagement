from rest_framework import serializers
from reservations.choices import StatusChoices
from reservations.models import Reservation


class CreateReservationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        book_id = self.context['book_id']
        borrower = self.context['request'].user
        status = validated_data.get('status', StatusChoices.ACTIVE)
        reservation = Reservation.objects.create(
            book_id=book_id,
            borrower_id=borrower.id,
            status=status
        )
        return reservation

    class Meta:
        model = Reservation
        fields = []
