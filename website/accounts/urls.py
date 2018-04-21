from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$', views.CalcView),
    url(r'^login/$',login,{'template_name':'accounts/login.html'}),
    url(r'^logout/$',logout,{'template_name':'accounts/logout.html'}),
    url(r'^register/$',views.register,name='register'),
    url(r'^form$',views.CalcView),
    url(r'^weather$',views.index),
    url(r'^temperature$',views.temperature),
    url(r'^drop/(?P<index>[0-9a-z-]+)/$', views.drop_val, name='drop'),
    url(r'^result$',views.result),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^profile/edit/$',views.edit_profile,name='edit_profile'),
    url(r'^profileform$',views.ProfileView.as_view(),name='ProfileView')
]