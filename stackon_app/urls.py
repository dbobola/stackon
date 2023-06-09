from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playground', views.playground, name='playground'),
    path('disconnect', views.disconnect, name='disconnect'),
    path('connect', views.connect, name='connect'), 
    path('add_features', views.add_features, name='add_features'),
    path('features_dict', views.features_dict, name='features_dict'),
    path('create_wallet', views.create_wallet, name='create_wallet'),
    path('delete_stream', views.delete_stream, name='delete_stream'),
    path('start_stream', views.start_stream, name='start_stream'),
    path('community', views.community, name='community'),
    path('livestream', views.livestream, name='livestream'),
    path('stacks', views.stacks, name='stacks'),
    path('stacks_view', views.stacks_view, name='stacks_view'),
    path('storefront', views.storefront, name='storefront'),
    path('disconnect_playground', views.disconnect_playground, name='disconnect_playground'),
    path('connect_playground', views.connect_playground, name='connect_playground'),
    path('search', views.search, name='search'),
    path('add_asset_to_stack', views.add_asset_to_stack, name='add_asset_to_stack'),
    path('update_asset_value', views.update_asset_value, name='update_asset_value'),
    path('delete_asset', views.delete_asset, name='delete_asset'),
    path('check_password_correct', views.check_password_correct, name='check_password_correct'),
    path('api/sentiment/<int:asset_id>/<str:platform>/<str:category>', views.get_sentiment_data, name='get_sentiment_data'),
    path('chainlink', views.chainlink, name='chainlink')

]

