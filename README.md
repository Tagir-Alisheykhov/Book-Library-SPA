LIBRARY

`GET/POST    /api/library/authors/`         # Список авторов / создание
`GET/PUT/DELETE /api/library/authors/1/`     # Конкретный автор

`GET/POST    /api/library/books/`            # Список книг / создание  
`GET/PUT/DELETE /api/library/books/1/`       # Конкретная книга


`GET/POST    /api/library/book-issues/`      # Список выдач / создание
`GET/PUT     /api/library/book-issues/1/`    # Конкретная выдача

Фильтрация
http://localhost:8000/api/library/books/?title=ключ&author=алишейхов