from requests import get, post, delete

# Тестирование ответа сервера
print('Получение всех пользователей')
print(get('http://localhost:8080/api/v2/users').json())
print('Корректное получение одного пользователя')
print(get('http://localhost:8080/api/v2/users/1').json())
print('Ошибочный запрос на получение одного пользователя — неверный id')
print(get('http://localhost:8080/api/v2/users/999').json())
print('Ошибочный запрос на получение одного пользователя — строка')
print(get('http://localhost:8080/api/v2/users/s').json())

