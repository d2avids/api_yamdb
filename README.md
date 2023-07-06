### YamDb - групповой  проект с отзывами
### Описание
---
Команда разработки:
- :globe_with_meridians: [d2avids (в роли Python-разработчика Тимлид - разработчик 1)](https://github.com/d2avids)
- :globe_with_meridians: [Dimitresku (в роли Python-разработчика - разработчик 2)](https://github.com/Dimitresku)
- :globe_with_meridians: [Pletennyy роль (в роли Python-разработчика - разработчик 3)](https://github.com/Pletennyy)
---
Подробная документация проекта с описанием API 
доступна после развертывания на /redoc

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

---

### Ресурсы API YaMDb
Ресурс auth: аутентификация.
Ресурс users: пользователи.
Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Пользовательские роли и права доступа
Аноним — может просматривать описания произведений, читать отзывы и комментарии.
Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Самостоятельная регистрация новых пользователей
Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

---

### Стек технологий использованный в проекте:
- Python 3.10
- Django 3.2
- DRF
- DRF Simple JWT 

---

### Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке.

```bash
git clone git@github.com:d2avids/api_yamdb.git
```

- Переходим в папку с проектом

```bash
cd api_yamdb/
```

- Устанавливаем виртуальное окружение

```bash
python -m venv venv
```

- Активируем виртуальное окружение

```bash
source venv/Scripts/activate
```

- Затем нужно установить все зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Осуществить миграции:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

- Запуск проекта:

```bash
python manage.py runserver
```

---
## Авторы:
- :globe_with_meridians: [d2avids (в роли Python-разработчика Тимлид - разработчик 1)](https://github.com/d2avids)
- :globe_with_meridians: [Dimitresku (в роли Python-разработчика - разработчик 2)](https://github.com/Dimitresku)
- :globe_with_meridians: [Pletennyy роль (в роли Python-разработчика - разработчик 3)](https://github.com/Pletennyy)
