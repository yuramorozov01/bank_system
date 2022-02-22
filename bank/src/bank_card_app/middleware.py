import jwt
from bank_card_app.models import BankCard
from decouple import config
from django.http import JsonResponse


class BankCardAuthenticationMiddleware:
    '''
    Middleware to provide bank card authentication.
    To authenticate bank card request has to contain header `X-Bank-Card-Authorization` with JWT.
    JWT doesn't need to contain any tags (JWT/Bearer/etc).
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.bank_card = None
        jwt_token = request.headers.get('X-Bank-Card-Authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, config('SECRET_KEY'), algorithms=['HS256'])
                bank_card_number = payload.get('bank_card_number')
                if bank_card_number is not None:
                    request.bank_card = BankCard.objects.get(number=bank_card_number)
            except (BankCard.DoesNotExist, jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
                pass

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def send_json_response(self, message, status):
        return JsonResponse({'message': message}, status=status)
