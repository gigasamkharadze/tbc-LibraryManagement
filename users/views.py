from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)
        else:
            return Response(serializer.errors, status=400)
