from django.conf.urls import patterns, include, url
from django.contrib import admin
from cms_barrapunto import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.inicio_pag, name = "Listado de las paginas"),
    url(r'^pagina/(\d+)$', views.pag),
    url(r'^update', views.update, name = "Muestrame la pagina seleccionada"),
)
