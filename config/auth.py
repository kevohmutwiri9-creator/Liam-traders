"""Custom authentication with enhanced logging for debugging."""
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError

logger = logging.getLogger(__name__)


class EnhancedJWTAuthentication(JWTAuthentication):
    """JWT Authentication with detailed error logging for debugging."""
    
    def authenticate(self, request):
        """
        Authenticate and log validation failures in detail.
        """
        try:
            return super().authenticate(request)
        except AuthenticationFailed as e:
            # Log the detailed error
            auth_header = request.META.get('HTTP_AUTHORIZATION', 'No header')
            token_type = auth_header.split()[0] if ' ' in auth_header else 'unknown'
            
            logger.warning(
                f'JWT Authentication Failed: {str(e)}',
                extra={
                    'token_type': token_type,
                    'auth_header_present': bool(auth_header and auth_header != 'No header'),
                    'path': request.path,
                    'method': request.method,
                }
            )
            raise
        except Exception as e:
            logger.error(
                f'JWT Authentication Error: {type(e).__name__}: {str(e)}',
                exc_info=True,
                extra={
                    'path': request.path,
                    'method': request.method,
                }
            )
            raise AuthenticationFailed('Invalid token') from e

    def get_validated_token(self, raw_token):
        """
        Log token validation attempts with details.
        """
        try:
            return super().get_validated_token(raw_token)
        except InvalidSignatureError:
            logger.warning('JWT: Invalid signature - SECRET_KEY may be mismatched')
            raise
        except ExpiredSignatureError:
            logger.warning('JWT: Token expired')
            raise
        except DecodeError:
            logger.warning('JWT: Token decode failed - malformed token')
            raise
        except Exception as e:
            logger.warning(f'JWT: Validation failed - {type(e).__name__}: {str(e)}')
            raise
