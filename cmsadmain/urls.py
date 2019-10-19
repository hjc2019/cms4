from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home),
    path('admainheader/',views.admainheader),
    path('admainheaderHandler/',views.admainheaderHandler),
    path('menus/',views.menus),
    path('menusHandler/',views.menusHandler),
    path('addmenu/',views.addmenu),
    path('addmenuHandler/',views.addmenuHandler),
    path('updatemenu/',views.updatemenu),
    path('updatemenuHandler/',views.updatemenuHandler),
    path('delmenu/',views.delmenu),
    path('article/',views.article),
    path('addarticle/',views.addarticle),
    path('addarticleHandler/',views.addarticleHandler),
    path('updatearticle/',views.updatearticle),
    path('updatearticleHandler/',views.updatearticleHandler),
    path('delarticle/',views.delarticel),
    path('user/', views.user),
    path('adduser/', views.adduser),
    path('adduserHandler/', views.adduserHandler),
    path('deleteUser/', views.deleteUser),
    path('reuser/', views.reuser),
    path('resave/',views.resave),
    path('positions/',views.positions),
    path('addposition/',views.addposition),
    path('updateposition/',views.updataposition),
    path('updatepositionHandler/',views.updatepositionHandler),
    path('delposition/',views.delposition),
    path('positioncontent/',views.positioncontent),
    path('addpositioncontent/',views.addpositioncontent),
    path('updatepositioncontent/',views.updatepositioncontent),
    path('update_position_content_Handler/',views.update_position_content_Handler),
    path('del_position_content/',views.del_position_content),
    path('login/',views.login),
    path('loginHandler/',views.loginHandler),
    path('clearImg/',views.clearImg),
    path('clearImgHandler/',views.clearImgHandler)
]