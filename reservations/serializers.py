from rest_framework import serializers

from library.models import Book
from reservations.choices import StatusChoices
from reservations.models import Reservation


class CreateReservationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        book_id = self.context['book_id']
        user = self.context['request'].user
        status = validated_data.get('status', StatusChoices.ACTIVE)

        book = Book.objects.get(id=book_id)
        if book.quantity == 0:
            raise serializers.ValidationError('Book is not available for reservation')
        book.quantity -= 1
        book.save()

        reservation = Reservation.objects.create(
            book_id=book_id,
            borrower_id=user.borrower_profile.id,
            status=status
        )
        return reservation

    class Meta:
        model = Reservation
        fields = []
