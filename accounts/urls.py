from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customers/<int:customer_id>/', views.customers, name="customers"),
    path('create_order/<int:customer_id>/', views.create_order, name="create_order"),
    path('update_order/<int:order_id>/', views.update_order, name="update_order"),
    path('delete_order/<int:order_id>/', views.delete_order, name="delete_order"),
    path('add_product/', views.add_product, name="add_product"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('user/', views.user_view, name="user"),
    path('register/', views.register, name="register"),
    path('settings/', views.account_settings, name="settings"),
    # django default auth views
    path('forgot_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/forgot_password.html"),
         name="reset_password"),
    path('reset_link_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('set_password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_changed_sucess/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")


]