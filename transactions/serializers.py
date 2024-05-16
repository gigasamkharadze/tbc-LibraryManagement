from rest_framework import serializers
from transactions.models import Transaction
from django.db import transaction as transaction_db, IntegrityError


class RetrieveTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ListTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    checkout_date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Transaction
        fields = ['book', 'borrower', 'checkout_date']

    def create(self, validated_data):
        with transaction_db.atomic():
            book = validated_data.get('book')
            borrower = validated_data.get('borrower')
            checkout_date = validated_data.get('checkout_date')
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                try:
                    transaction = Transaction.objects.create(book=book, borrower=borrower, checkout_date=checkout_date)
                    return transaction
                except IntegrityError:
                    raise serializers.ValidationError("Duplicate transaction")
            else:
                raise serializers.ValidationError("Book is not available")


class UpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['return_date']

    def update(self, instance, validated_data):
        with transaction_db.atomic():
            instance.return_date = validated_data.get('return_date', instance.return_date)
            instance.book.quantity += 1
            instance.book.save()
            instance.save()
        return instance
