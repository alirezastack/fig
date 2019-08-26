from graphene import ObjectType, String, Schema, Field, Int, List
from olive.http import Request
from fig import app


legacy_url = app.config['LEGACY']['base_url']
_LEGACY_BASE_URL = legacy_url if legacy_url[-1:] == '/' else '{}/'.format(legacy_url)
_LEGACY_KEY = app.config['LEGACY']['key']


class User(ObjectType):
    class Meta:
        description = 'Limited user model on zoodroom'

    mobile_number = String()
    email = String()
    fullname = String()

    @staticmethod
    def resolve_mobile_number(parent, info):
        return parent.mobile_number

    @staticmethod
    def resolve_email(parent, info):
        return parent.email

    @staticmethod
    def resolve_fullname(parent, info):
        return parent.fullname


class ReservationBed(ObjectType):
    title = String()
    type = String()

    @staticmethod
    def resolve_title(parent, info):
        return parent['title']

    @staticmethod
    def resolve_type(parent, info):
        return parent['type']


class Reservation(ObjectType):
    class Meta:
        description = 'User reservation on zoodroom'

    code_hash = String()
    code = String()
    checkout = String()
    beds = List(ReservationBed, description="List of Bed objects")

    @staticmethod
    def resolve_code_hash(parent, info):
        return parent.code_hash

    @staticmethod
    def resolve_bed(parent, info):
        return parent.beds


class Query(ObjectType):
    getUser = Field(User, user_id=Int(required=True))
    getReservation = Field(Reservation, reservation_id=Int())

    @staticmethod
    def resolve_getReservation(root, info, reservation_id):
        # TODO check authorization in the future using the below header
        # TODO info.context.headers['Authorization']

        url = '{}v3/internal-reservation/{}'.format(_LEGACY_BASE_URL, reservation_id)
        req = Request(url=url, headers={'X-INTERNAL-API-KEY': _LEGACY_KEY}, app=app)
        reservation = req.get()

        return Reservation(code_hash=reservation['code_hash'],
                           beds=reservation['beds'],
                           checkout=reservation['checkout'],
                           code=reservation['code'])

    @staticmethod
    def resolve_getUser(root, info, user_id):
        # TODO check authorization in the future using the below header
        # TODO info.context.headers['Authorization']

        url = f'{_LEGACY_BASE_URL}v1/internal-users/{user_id}'
        req = Request(url=url, headers={'X-INTERNAL-API-KEY': _LEGACY_KEY}, app=app)
        user = req.get()

        return User(mobile_number=user['mobile_number'],
                    email=user['email'],
                    fullname=user['fullname'])


GraphSchema = Schema(query=Query)
