from rest_framework import serializers
from transactions.models import Transaction


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
        try:
            transaction = Transaction.objects.create(
                book=validated_data['book'],
                borrower=validated_data['borrower'],
                checkout_date=validated_data['checkout_date']
            )
            return transaction
        except Exception as e:
            raise serializers.ValidationError(e)


class UpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['return_date']

    def update(self, instance, validated_data):
        instance.return_date = validated_data.get('return_date', instance.return_date)
        instance.save()
        return instance
