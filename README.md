# Проект Learning Management System

<i>Это DjangoRestFramework - проект системы управления обучением</i>

## Зависимости:
- Docker (должен быть установлен и запущен Docker Desktop)
- Docker Compose


## Установка:

1. Клонируйте репозиторий:
```
https://github.com/skazim9/Project31
```
2. Создайте и заполните файл .env согласно шаблону .env.example
3. Соберите и запустите контейнеры
```
docker-compose up --build
```
4. Примените миграции. Откройте новый терминал (или командную строку) и выполните:
```
docker-compose exec web python manage.py migrate
```

5. Создайте суперпользователя (опционально):

```
docker-compose exec web python manage.py createsuperuser
```
Теперь проект должен быть доступен по адресу http://localhost:8000/<br><br>
Документацию по работе с api можно изучить по адресу: http://localhost:8000/redoc/<br><br>
Для остановки контейнера выполните:
```
docker-compose down
```
Эта команда остановит и удалит контейнеры, но не удалит образы.
## Полезные советы
 Для просмотра логов всех сервисов в реальном времени, используйте:
```
docker-compose logs -f
```
Вы также можете проверить статус ваших контейнеров с помощью:
```
 docker-compose ps
```