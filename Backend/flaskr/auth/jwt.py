import jwt
from jwt import ExpiredSignatureError, InvalidAudienceError, InvalidTokenError
import datetime
import time
from .roles import JWT_ROLE_ADMIN, JWT_ROLE_USER

# ich weiß, ich weiß, aber das ist ja für das projekt egal. (und auch nicht das einzige secret im source code :o )
_JWT_SECRET = "caephooze3quie1saht7phihahhah1Oagh1Airoh7naigaiquay5elie4ail5Phieciex3wei3iequ6sheedor2hoo0YaiwaePhia2oot7Quaighohgh7seiwoo6ahruThee1saejooShoCaeRee5oodaepho0uoquie5eisaetaeBolepoo4phoweiji0iwaeliephaedeexeeNeang2a"

def validate_session(session): 
    try:
        # Decode the token
        decoded = jwt.decode(
            session,
            _JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_signature": True, "require": ["iat", "exp", "aud"]},
            audience=[
                JWT_ROLE_ADMIN,
                JWT_ROLE_USER
                ] 
        )
        

        # check if the id field is present and well-formed
        if 'id' not in decoded:
            return False

        if type(decoded['id']) != int:
            return False

        return decoded


    except ExpiredSignatureError:
        return False
    except InvalidAudienceError:
        return False
    except Exception as e:
        return False


    return False


def _get_iat_time(): 
    return int(time.mktime((datetime.datetime.now()).timetuple()))

def _get_expire_time(): 
    # current time + 7 days (60 * 60 * 24 * 7 = 604800)
    return _get_iat_time() + 604800

# role represents the realm of the user. 
# for example: admin realm, location leader realm, or group leader realm
# the ID represents the id of the instance which the user manages. for example group id
def generate_session_token(role, id): 
    return jwt.encode(
                {
                    "iat": _get_iat_time(), 
                    "exp": _get_expire_time(),
                    "aud": role,
                    "id": id
                    },
                _JWT_SECRET, 
                "HS256"
                )
