from rest_framework import serializers
from django.db import transaction

from library.models import Book, Author, Genre
from reservations.models import Reservation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class UpdateBookBorrowerSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if instance.quantity > 0:
            with transaction.atomic():
                instance.quantity -= 1
                instance.save()

                Reservation.objects.create(
                    book=instance,
                    borrower=self.context['request'].user.borrower_profile,
                )

        else:
            raise serializers.ValidationError('Book is not available')
        return instance

    class Meta:
        model = Book
        fields = ['id']
