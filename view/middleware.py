from django.utils.deprecation import MiddlewareMixin
# from user_agents import parse


class DeviceDetectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
        # user_agent = request.META.get('HTTP_USER_AGENT', '')
        # user_agent_obj = parse(user_agent)
        #
        # # Add a new attribute to the request object
        # request.is_mobile = user_agent_obj.is_mobile
        # request.is_tablet = user_agent_obj.is_tablet
        # request.is_desktop = user_agent_obj.is_pc
