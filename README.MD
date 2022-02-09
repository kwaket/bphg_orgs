# Биоресурсный центр

## Запуск в режиме разработки
### Через docker
```
docker-compose -f local.yml build
docker-compose -f local.yml up
```

### Локально
1. `$ pipenv shell && pipenv sync`
2. Укажите параметры базы данных в файле .envrc и экспортируйте их
1. `$ python manage.py migrate`
2. `$ python manage.py collectstatic`
3. `$ python manange.py runserver`
Для использования поиска в приложении "Организации ведущие разработки в области бактериофагов" необходимо
4. [Запустить elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
5. Обновить индексы elasticsearch после добавления новых дынных командой `python manage.py rebuild_index` или `python manage.py update_index`
