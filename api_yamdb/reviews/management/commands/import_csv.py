import csv
import os

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


def read_file(file_name):
    file_path = os.path.join('static/data/', file_name)
    inputfile = open(file_path, encoding='utf-8')
    return csv.reader(inputfile, delimiter=',')


class Command(BaseCommand):

    def handle(self, *args, **options):
        reader = read_file('category.csv')
        next(reader, None)
        Category.objects.all().delete()
        for row in reader:
            print(row)
            Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('genre.csv')
        next(reader, None)
        Genre.objects.all().delete()
        for row in reader:
            print(row)
            Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('users.csv')
        next(reader, None)
        Comment.objects.all().delete()
        for row in reader:
            print(row)
            User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('titles.csv')
        next(reader, None)
        Title.objects.all().delete()
        for row in reader:
            print(row)
            category = get_object_or_404(Category, id=row[3])
            Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('review.csv')
        next(reader, None)
        Review.objects.all().delete()
        for row in reader:
            print(row)
            title = get_object_or_404(Title, id=row[1])
            user = get_object_or_404(User, id=row[3])
            Review.objects.get_or_create(
                id=row[0],
                title=title,
                text=row[2],
                author=user,
                score=row[4],
                pub_date=row[5]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('genre_title.csv')
        next(reader, None)
        TitleGenre.objects.all().delete()
        for row in reader:
            print(row)
            TitleGenre.objects.get_or_create(
                id=row[0],
                genre_id=row[2],
                title_id=row[1]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))

        reader = read_file('comments.csv')
        next(reader, None)
        Comment.objects.all().delete()
        for row in reader:
            print(row)
            # review_id = get_object_or_404(Review, id=row[1])
            # user = get_object_or_404(User, id=row[3])
            Comment.objects.get_or_create(
                id=row[0],
                # review=review_id,
                text=row[2],
                author_id=row[3],
                pub_date=row[4]
            )
        self.stdout.write(self.style.SUCCESS('Successfully  "%s"' % row))
