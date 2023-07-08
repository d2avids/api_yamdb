import csv

from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, CustomUser, Genre, GenreTitle,
                            Review, Title)

DATA_MODEL = {
    'static/data/users.csv': CustomUser,
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': GenreTitle,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """Команда, добавляющая csv данные в БД."""
    help = 'Добавляет csv данные в БД.'

    def add_row_model(self, row):
        """Добавляет в строку таблицы данные от моделей."""
        try:
            if row.get('author'):
                row['author'] = CustomUser.objects.get(pk=row['author'])
            if row.get('review_id'):
                row['review'] = Review.objects.get(pk=row['review_id'])
            if row.get('title_id'):
                row['title'] = Title.objects.get(pk=row['title_id'])
            if row.get('category'):
                row['category'] = Category.objects.get(pk=row['category'])
            if row.get('genre'):
                row['genre'] = Genre.objects.get(pk=row['genre'])
        except Exception as error:
            print(f'{error}')
        return row

    def handle(self, *args, **options):
        """Наполняет модели данными."""
        for r in DATA_MODEL.items():
            csv_data, model = r
            count = 0
            with open(csv_data,  mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    count += 1
                    row = self.add_row_model(row)
                    try:
                        model.objects.get_or_create(**row)
                    except Exception as error:
                        print(f'{error}')
            self.stdout.write(
                self.style.SUCCESS('csv файлы успешно импортированы.\n'
                                   f'Модель {model.__name__} наполнена данными.\n'
                                   f'Количество строк: {count}.'
                )
            )
