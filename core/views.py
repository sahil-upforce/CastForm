from rest_framework import mixins, status
from rest_framework.response import Response


class CustomDestroyMessageMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = f"The record with public_id {instance.pk} has been deleted."
        return Response({"detail": message}, status=status.HTTP_204_NO_CONTENT)
