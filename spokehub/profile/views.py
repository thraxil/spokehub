from userena.utils import get_profile_model
import userena.views


class ProfileListView(userena.views.ProfileListView):
    def get_queryset(self):
        profile_model = get_profile_model()
        queryset = profile_model.objects.get_visible_profiles(
            self.request.user).order_by('user__username').select_related()
        return queryset
