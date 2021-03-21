# django-flatpages-api
Тестовое задание по разработке простого API с использованием Django и DRF. 

### Пример получения списка страниц
**Request:**
```
GET http://localhost:8000/page/
```

**Response:**
```
HTTP 200 OK
{
    "count": 20,
    "next": "http://localhost:8000/page/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "id": 20,
            "title": "Page 20",
            "url": "http://localhost:8000/page/20/"
        },
        {
            "id": 19,
            "title": "Page 19",
            "url": "http://localhost:8000/page/19/"
        },
        ...
    ]
}
```

### Пример получения детальной информации о странице
**Request:**
```
GET http://localhost:8000/page/20
```

**Response:**
```
HTTP 200 OK
{
    "id": 20,
    "title": "Page 20",
    "content": [
        {
            "id": 152,
            "title": "Video block 1",
            "views_count": 17,
            "video_link": "https://www.youtube.com/watch?v=-pHwBf1qB1M",
            "subtitle_link": "https://www.youtube.com/pHwBf1qB1M.sub",
            "resourcetype": "Video"
        },
        {
            "id": 151,
            "title": "Text block 3",
            "views_count": 17,
            "text_field": "Text block 3 content 3",
            "resourcetype": "Text"
        }
    ]
}
```
