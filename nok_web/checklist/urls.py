from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='home'),         # примеры регистрации маршрута для контроллера функций
    # path('category/<int:category_id>/', get_category, name='category'),
    # path('news/<int:pk>/', view_news, name='view_news'),
    # path('news/add-news/', add_news, name='add-news'),

    path('', HomeDepartments.as_view(), name='home'),         # примеры регистрации маршрута для контроллера классов
    # path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),     # В скобках NewsByCategory.as_view() можно передавать дополнительные параметры
    # path('library/', CreateChecklist.as_view(), name='library'),
    # path('library/<int:pk>/', ViewDepartments.as_view(), name='library'),
    # path('news/add-news/', CreateNews.as_view(), name='add-news'),


]