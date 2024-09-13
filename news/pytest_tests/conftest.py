from datetime import datetime, timedelta

import pytest
from django.test.client import Client  # type: ignore
from django.utils import timezone  # type: ignore

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def ten_news_on_main_page(author):
    today = datetime.today()
    for element in range(10):
        news = News.objects.create(
            title=f'Заголовок{element}',
            text=f'Текст заметки{element}',
            date=today - timedelta(days=element)
        )
    return news


@pytest.fixture
def ten_comments_fixture(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            text=f'Текст заметки{index}',
            author=author,
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comment


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст заметки',
        author=author,
    )
    return comment


@pytest.fixture
def id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст New',
    }
