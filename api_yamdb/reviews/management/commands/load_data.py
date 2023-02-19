from django.core.management.base import BaseCommand

from .services import (get_categories, get_comments, get_genres, get_reviews,
                       get_titles, get_users)


class Command(BaseCommand):
    """ Команда предназначена для импорта csv данных в БД"""

    def handle(self, *args, **options):
        """ Импортируем категории в БД"""
        get_categories(self)
        """ Импортируем жанры в БД"""
        get_genres(self)
        """ Импортируем произведния в БД"""
        get_titles(self)
        """ Импортируем пользователей в БД"""
        get_users(self)
        """ Импортируем отзывы в БД"""
        get_reviews(self)
        """ Импортируем комментарии к отзывам в БД"""
        get_comments(self)
