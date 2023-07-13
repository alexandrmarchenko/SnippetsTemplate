from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
                  path('', views.index_page, name='home'),
                  path('snippets/add', views.add_snippet_page, name='snippets-add'),
                  path('snippets/list', views.snippets_page, name='snippets-list'),
                  path('snippet/<int:id>', views.snippet_detail, name='snippet-detail'),
                  path('snippet/<int:id>/delete', views.snippet_delete, name='snippet-delete'),
                  path('snippet/<int:sid>/edit', views.snippet_edit, name='snippet-edit'),
                  path('login', views.login, name='login'),
                  path('logout', views.logout, name='logout'),
                  path('snippets/my', views.my_snippets, name='my-snippets'),
                  path('auth/register', views.create_user, name='register')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
