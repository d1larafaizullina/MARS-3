from requests import get, post, delete

# Тестирование ответа сервера
print('Получение всех пользователей')
print(get('http://localhost:8080/api/users').json())
print('Корректное получение одной работы')
print(get('http://localhost:8080/api/users/1').json())
print('Ошибочный запрос на получение одной работы — неверный id')
print(get('http://localhost:8080/api/users/999').json())
print('Ошибочный запрос на получение одной работы — строка')
print(get('http://localhost:8080/api/users/s').json())
