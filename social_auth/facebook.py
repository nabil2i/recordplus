
import facebook


class Facebook:
    """
    Facebook class to fetch the user info 
    """

    @staticmethod
    def validate(auth_token):
        """
        validate user via facebook GraphAPI
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expired."
          