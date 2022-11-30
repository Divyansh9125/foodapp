from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from . import Utility

@api_view(['POST'])
def login(request):
    """
    Send user data for SignUp in the format below:
    #
    ###{
        "work_email": "jdoe@mathworks.com",
        "password": "jnedq@2u10"
    ###}
    """
    if request.method == 'POST':
        work_email = request.data['work_email']
        password = request.data['password']

        try:
            user = User.objects.get(work_email=work_email)
            if user.password == password :
                token = Utility.getToken(16)
                user.token = token
                user.save()

                return Response({
                'success': True,
                'token': token
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
                'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def userSignUp(request):
    """
    Send user data for SignUp in the format below:
    #
    ###{
        "work_email": "jdoe@mathworks.com",
        "password": "jnedq@2u10"
        "fname": "John",
        "lname": "Doe",
        "contact": "0123456789"
    ###}
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
            createdUserToken = userSerializer.create(request.data)
            if not createdUserToken is None:
                return Response({'success': True, 'token': createdUserToken}, status=status.HTTP_201_CREATED)
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
    #
    ###{
        "token": "lksjenfowuhnfown",
        "portion": 0, // 0 for half, 1 for full
        "order_id": "123456",
        "veg": 1, // 1 for veg, 0 for non-veg
        "piece": 1 // 1 for 8 pcs and 0 for 5 pcs
    ###}
    """
    if request.method == 'POST':
        token = request.data['token']
        try:
            user = User.objects.get(token=token)
            data = {
                'user': user,
                'portion': request.data['portion'],
                'order_id': request.data['order_id'],
                'veg': request.data['veg'],
                'piece': request.data['piece']
            }

            giverSerializer = GiverSerializer()
            createdGiver = giverSerializer.create(data)

            token = Utility.getToken(16)
            user.token = token
            user.save()

            if not createdGiver is None:
                return Response({'success': True, 'token': token}, status=status.HTTP_201_CREATED)
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


@api_view(['GET'])
def numFoodAvailable(request, option, piece):
    """
    Get number of available food in the database
    """
    if request.method == 'GET':
        if option == 'veg':
            if piece == 5:
                num = Giver.objects.filter(available=1, veg=1, piece=0).count()
            elif piece == 8:
                num = Giver.objects.filter(available=1, veg=1, piece=1).count()
            else:
                return Response({
                    'success': False,
                    'error': 'wrong query params'
                    }, status=status.HTTP_400_BAD_REQUEST)
        elif option == 'non-veg':
            if piece == 5:
                num = Giver.objects.filter(available=1, veg=0, piece=0).count()
            elif piece == 8:
                num = Giver.objects.filter(available=1, veg=0, piece=1).count()
            else:
                return Response({
                    'success': False,
                    'error': 'wrong query params'
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': False,
                'error': 'wrong query params'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': 1,
            'num': num
            }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'error': 'wrong request method'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def regTaker(request):
    """
    Send user data for giveFood in the format below:
    #
    ###{
        "work_email": "jdoe@mathworks.com",
        "req_portion": 0, // 0 for half, 1 for full
        "got_food": 0, // 0 if registered in waitlist, 1 if taken food while registering
        "veg_preference": 1, // 1 for veg, 0 for non-veg
    ###}
    """
    if request.method == 'POST':
        work_email = request.data['work_email']
        try:
            user = User.objects.get(work_email=work_email)
            data = {
                'user': user,
                'req_portion': request.data['req_portion'],
                'got_food': request.data['got_food'],
                'veg_preference': request.data['veg_preference']
            }

            takerSerializer = TakerSerializer()
            createdTaker = takerSerializer.create(data)

            if not createdTaker is None:
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'error': 'taker not created'
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


@api_view(['POST'])
def placeOrder(request, option, piece):
    """
    Send taker data in the format below:
    #
    ###{
        'token': 'ehfwh299`9394'
    ###}
    """
    print(request.method)
    if request.method == 'POST':
        token = request.data['token']
        try:
            user = User.objects.get(token=token)
            taker = Taker.objects.get(user=user)
            print("user: ", user.fname)
            if taker.got_food == 0:
                if option == 'veg':
                    if piece == 5:
                        giverNum = Giver.objects.all().filter(available=1, veg=1, piece=0).count()
                        print("giverNum: ", giverNum)
                        if giverNum > 0:
                            giver = Giver.objects.all().filter(available=1, veg=1, piece=0)
                            giver = giver[0]
                            order_id = giver.order_id
                            taker.got_food = 1
                            taker.save()
                            giver.available = 0
                            giver.save()

                            print("entered", request.method)

                            return Response({
                                'success': 1,
                                'order_id': order_id
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'success': 0,
                                'error': 'food not available'
                            }, status=status.HTTP_200_OK)
                    elif piece == 8:
                        giverNum = Giver.objects.all().filter(available=1, veg=1, piece=0).count()
                        if giverNum > 0:
                            giver = Giver.objects.all().filter(available=1, veg=1, piece=0)
                            giver = giver[0]
                            order_id = giver.order_id
                            taker.got_food = 1
                            taker.save()
                            giver.available = 0
                            giver.save()

                            return Response({
                                'success': 1,
                                'order_id': order_id
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'success': 0,
                                'error': 'food not available'
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                                'success': 0,
                                'error': 'wrong query params'
                            }, status=status.HTTP_400_BAD_REQUEST)
                elif option == 'non-veg':
                    if piece == 5:
                        giverNum = Giver.objects.all().filter(available=1, veg=1, piece=0).count()
                        if giverNum > 0:
                            giver = Giver.objects.all().filter(available=1, veg=1, piece=0)
                            giver = giver[0]
                            order_id = giver.order_id
                            taker.got_food = 1
                            taker.save()
                            giver.available = 0
                            giver.save()

                            return Response({
                                'success': 1,
                                'order_id': order_id
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'success': 0,
                                'error': 'food not available'
                            }, status=status.HTTP_200_OK)
                    elif piece == 8:
                        giverNum = Giver.objects.all().filter(available=1, veg=1, piece=0).count()
                        if giverNum > 0:
                            giver = Giver.objects.all().filter(available=1, veg=1, piece=0)
                            giver = giver[0]
                            order_id = giver.order_id
                            taker.got_food = 1
                            taker.save()
                            giver.available = 0
                            giver.save()

                            return Response({
                                'success': 1,
                                'order_id': order_id
                            }, status=status.HTTP_200_OK)
                        else:
                            return Response({
                                'success': 0,
                                'error': 'food not available'
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'success': 0,
                            'error': 'wrong query params'
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'success': 0,
                        'error': 'wrong query params'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                        'success': 0,
                        'error': 'taker got food'
                    }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': 0,
                'error': 'user not registered'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Taker.DoesNotExist:
            return Response({
                'success': 0,
                'error': 'taker not registered'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("not entered", request.method)
        return Response({
        'success': False,
        'error': 'wrong request method'
        }, status=status.HTTP_400_BAD_REQUEST)