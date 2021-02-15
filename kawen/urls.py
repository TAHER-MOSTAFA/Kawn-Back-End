from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from users.views import login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("login/", login, name="login"),
    path("_nested_admin/", include("nested_admin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
