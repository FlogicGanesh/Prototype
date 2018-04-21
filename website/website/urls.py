from django.conf.urls import url,include
from django.contrib import admin
#from website import views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/',include('accounts.urls')),
    #url(r'^$',views.login_redirect,name='login_redirect'),
    url(r'^$',accview.CalcView)
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
