
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf import settings
from django.conf.urls.static import static
from users.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('login/',login)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)