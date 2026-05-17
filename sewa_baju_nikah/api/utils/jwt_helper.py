from rest_framework_simplejwt.tokens import RefreshToken

# =========================================================
# GENERATE JWT TOKEN
# =========================================================

def generate_jwt_token(user):

    refresh = RefreshToken.for_user(user)

    return {

        'refresh': str(refresh),

        'access': str(refresh.access_token),

    }