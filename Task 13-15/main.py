from Animals import Animals
from CounterAnimals import CounterAnimals


def search_type():
    class_animal = input('Введите класс животного (доступные: кошка, собака, хомяк, верблюд, лошадь, осёл): ')
    if class_animal.lower() == 'кошка':
        typee = 'Cats'
    elif class_animal.lower() == 'собака':
        typee = 'Dogs'
    elif class_animal.lower() == 'хомяк':
        typee = 'Hamsters'
    elif class_animal.lower() == 'верблюд':
        typee = 'Camels'
    elif class_animal.lower() == 'лошадь':
        typee = 'Horses'
    elif class_animal.lower() == 'осёл':
        typee = 'Donkeys'
    else:
        return 'Животное с такими параметрами не было найдено'
    return typee


def search_commands():
    name = input('Введите имя животного: ')
    typee = search_type()
    animal = Animals(f'select * from {typee} where name_animal = "{name}"')
    animal.animal_type = typee
    return animal


def add_commands():
    try:
        animal = search_commands()
        query = f'UPDATE {animal.animal_type} ' \
                f'SET commands = "{input("Введите новые команды: ")}" ' \
                f'WHERE id = {animal.animal_id};'
        animal.new_commands(query)
        return 200
    except:
        return 400


def new_animal():
    try:
        typee = search_type()
        query = f"INSERT INTO {typee} (name_animal, commands, birthday) " \
                f"VALUES ('{input('Введите имя нового животного: ')}', " \
                f"'{input('Введите команды животного: ')}', " \
                f"'{input('Введите дату рождения животного (в формате ГГГГ-ММ-ДД) : ')}');"
        Animals().new_commands(query)
        return 200
    except:
        return 400


print('Добро пожаловать в Систему учета для питомника! ')
animalCounter = CounterAnimals()
while True:
    print('\nДоступные действия:\n'
          '1) Завести новое животное.\n'
          '2) Увидеть список команд, которые выполняет животное.\n'
          '3) Обучить животное новым командам.\n'
          '4) Выход')
    action = input('Введите номер действия (число): ')
    if action == '1':
        if new_animal() == 200:
            print('Животное успешно добавлено в базу!')
            animalCounter.add()
            print('Всего животных было создано', animalCounter.return_counter())
        else:
            print('Информация не была добавлена в базу!')

    elif action == '2':
        try:
            answer = search_commands()
            print('Информация, которая была найдена по вашему запросу:')
            print(answer.commands)
        except:
            print("Информация не была найдена!")
    elif action == '3':
        if add_commands() == 200:
            print('Информация была обновлена!')
        else:
            print('Информация не была обновлена!')
    elif action == '4':
        break
    else:
        print('Данное действие не было найдено! Введите действие повторно.')