from requests import get, post, delete


# Тестирование post запросов
print('Создание работы с пустым json')
print(post('http://localhost:8080/api/v2/users').json())

print('Создание пользователя с существующим id')
data_json = {'id': 1, 'address': 'module_1', 'age': 21,
             'name': 'Ridley', 'position': 'captain',
             'speciality': 'research engineer',
             'surname': 'Scott', 'email': 'scott_ridley@mars.org'}
print(post('http://localhost:8080/api/v2/users', json=data_json).json())

print('Создание пользователя с отсутствующим обязательным параметром email')
data_json = {'address': 'module_1', 'age': 21,
             'name': 'Ridley', 'position': 'captain',
             'speciality': 'research engineer',
             'surname': 'Scott'}
print(post('http://localhost:8080/api/v2/users', json=data_json).json())

print('Корректное создание пользователя')
data_json = {'address': 'module_10', 'age': 21,
             'name': 'Leonardo', 'position': 'hunter',
             'speciality': 'hunter',
             'surname': 'Di Caprio', 'email': 'leon@mars.org'}
print(post('http://localhost:8080/api/v2/users', json=data_json).json())

print('Получение всех пользователей')
print(get('http://localhost:8080/api/v2/users').json())

print('Корректное удаление пользователя')
print(delete('http://localhost:8080/api/v2/users/5').json())

print('Получение всех пользователей')
print(get('http://localhost:8080/api/v2/users').json())
