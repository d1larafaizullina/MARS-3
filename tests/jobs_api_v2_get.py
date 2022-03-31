from requests import get

# Тестирование ответа сервера
print('Получение всех работ')
print(get('http://localhost:8080/api/v2/jobs').json())
print('Корректное получение одной работы')
print(get('http://localhost:8080/api/v2/jobs/1').json())
print('Ошибочный запрос на получение одной работы — неверный id')
print(get('http://localhost:8080/api/v2/jobs/999').json())
print('Ошибочный запрос на получение одной работы — строка')
print(get('http://localhost:8080/api/v2/jobs/s').json())
