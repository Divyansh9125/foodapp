from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['POST'])
def userSignUp(request):
    """
    Send user data for SignUp in the format below:
    {
        "work_email": "jdoe@mathworks.com",
        "fname": "John",
        "lname": "Doe",
        "contact": "0123456789"
    }
    """
    if request.method == 'POST':
        work_email = request.data['work_email']
        try:
            user = User.objects.get(work_email=work_email)
            return Response({
                'success': False,
                'error': 'user already exits'
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            userSerializer = UserSerializer()
            createdUser = userSerializer.create(request.data)
            if not createdUser is None:
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': 'user not created'
                }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'success': False,
        'error': 'wrong request method'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def giveFood(request):
    """
    Send user data for giveFood in the format below:
    {
        "work_email": "jdoe@mathworks.com",
        "portion": 0, // 0 for half, 1 for full
        "order_id": "123456",
        "veg": 1, // 1 for veg, 0 for non-veg
        "piece": 1 // 1 for 8 pcs and 0 for 5 pcs
    }
    """
    if request.method == 'POST':
        work_email = request.data['work_email']
        try:
            user = User.objects.get(work_email=work_email)
            data = {
                'user': user,
                'portion': request.data['portion'],
                'order_id': request.data['order_id'],
                'veg': request.data['veg'],
                'piece': request.data['piece']
            }

            giverSerializer = GiverSerializer()
            createdGiver = giverSerializer.create(data)

            if not createdGiver is None:
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': 'user not created'
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'user does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        'success': False,
        'error': 'wrong request method'
        }, status=status.HTTP_400_BAD_REQUEST)
