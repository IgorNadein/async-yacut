### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/IgorNadein/async-yacut.git

cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с пятью переменными окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=you_token
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```

После запуска проекта будут доступны:
- [Главная страница](http://127.0.0.1:5000/) представляюцая основной функционал.
- [Страница для загрузки файлов](http://127.0.0.1:5000/files)
- API для POST (/api/id/) и GET ('/api/id/<short>/') зпросов 
- [Документация к API](http://127.0.0.1:5000/api/docs)

Техно-стек:
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate
- **База данных**: SQLite (для разработки), PostgreSQL (прод)
- **Дополнительно**: Python-dotenv, Pytest (тестирование)
- **Инфраструктура**: Git, GitHub

Автор:
**Игорь Надеин**  
GitHub: [IgorNadein](https://github.com/IgorNadein)  
Email: [gari.music126@yandex.ru](gari.music126@yandex.ru)
