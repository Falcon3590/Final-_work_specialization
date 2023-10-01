# 7. В подключенном MySQL репозитории создать базу данных “Друзья человека”
``````
CREATE DATABASE PeopleFriends;
``````
# 8. Создать таблицы с иерархией из диаграммы в БД
``````
USE PeopleFriends;

CREATE TABLE Animals(
	id int auto_increment primary key,
    animal_type varchar(50)
);

INSERT INTO Animals (animal_type)
VALUES ('Домашние животные'), ('Вьючные животные');

CREATE TABLE Pets
(
	id INT AUTO_INCREMENT PRIMARY KEY,
	animal_kind VARCHAR(50),
	animal_type_id INT DEFAULT 1,
	FOREIGN KEY (animal_type_id) REFERENCES Animals (id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Pets (animal_kind)
VALUES ('Собаки'), ('Кошки'), ('Хомяки');

CREATE TABLE PackAnimals
(
	id INT AUTO_INCREMENT PRIMARY KEY,
	animal_kind VARCHAR(30),
	animal_type_id INT DEFAULT 2,
	FOREIGN KEY (animal_type_id) REFERENCES Animals (id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO PackAnimals (animal_kind)
VALUES ('Лошади'), ('Верблюды'), ('Ослы');
``````

# 9. Заполнить низкоуровневые таблицы именами(животных), командами которые они выполняют и датами рождения
``````
USE PeopleFriends;

CREATE TABLE Dogs 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(50), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 1,
    Foreign KEY (animal_kind_id) REFERENCES Pets (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Dogs (name_animal, commands, birthday)
VALUES ('Бобик', 'ко мне, рядом, сидеть', '2020-01-12'),
('Мира', 'лежать, голос, сидеть', '2021-12-12'),
('Рекс', 'сидеть, охраняй, голос', '2020-01-27');

CREATE TABLE Cats 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(30), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 2,
    Foreign KEY (animal_kind_id) REFERENCES Pets (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Cats (name_animal, commands, birthday)
VALUES ('Мила', 'кушать', '2020-10-10'),
('Дымка', 'кушать', '2022-08-26'),
('Рыжик', 'спать', '2021-03-15');

CREATE TABLE Hamsters 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(30), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 3,
    Foreign KEY (animal_kind_id) REFERENCES Pets (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Hamsters (name_animal, commands, birthday)
VALUES ('Хома 1', 'бегать в колесе', '2022-10-15'),
('Сеня', 'кушать, купаться', '2021-03-15'),
('Хома 2', 'кушать', '2022-12-21');

CREATE TABLE Horses 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(30), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 1,
    Foreign KEY (animal_kind_id) REFERENCES PackAnimals (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Horses (name_animal, commands, birthday)
VALUES ('Белла', 'стой, вперед, пошли', '2015-07-10'),
('Мак', 'стой, рысь', '2019-12-10'),
('Пинки', 'стой, встать, сесть', '2021-05-15');

CREATE TABLE Camels 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(30), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 2,
    Foreign KEY (animal_kind_id) REFERENCES PackAnimals (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Camels (name_animal, commands, birthday)
VALUES ('Джерри', 'стоять, идти, лежать', '2017-10-10'),
('Том', 'стоять, идти, лежать', '2016-11-11'),
('Тони', 'стоять, идти, лежать', '2015-12-12');

CREATE TABLE Donkeys 
(       
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name_animal VARCHAR(30), 
    commands VARCHAR(100),
    birthday DATE,
    animal_kind_id INT DEFAULT 3,
    Foreign KEY (animal_kind_id) REFERENCES PackAnimals (id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO Donkeys (name_animal, commands, birthday)
VALUES ('Гера', 'банан', '2019-11-17'),
('Зеб', 'стоять', '2021-02-10'),
('Асока', 'вперед, банан', '2020-07-29');
``````
# 10. Удалив из таблицы верблюдов, т.к. верблюдов решили перевезти в другой питомник на зимовку. Объединить таблицы лошади, и ослы в одну таблицу.
``````
DELETE FROM Camels where id != 0;
CREATE TABLE HorsesAndDonkeys SELECT * FROM Horses UNION SELECT * FROM Donkeys;
``````
# 11.Создать новую таблицу “молодые животные” в которую попадут все животные старше 1 года, но младше 3 лет и в отдельном столбце с точностью до месяца подсчитать возраст животных в новой таблице
``````
CREATE TEMPORARY TABLE AllAnimals SELECT * FROM Dogs UNION SELECT * FROM Cats UNION SELECT * FROM Hamsters
UNION SELECT * FROM Horses UNION SELECT * FROM Camels UNION SELECT * FROM Donkeys;

CREATE TABLE YoungAnimals
SELECT name_animal, commands, birthday, animal_kind_id, TIMESTAMPDIFF(MONTH, birthday, CURDATE()) AS age_in_month
FROM AllAnimals
WHERE birthday BETWEEN ADDDATE(CURDATE(), INTERVAL -3 YEAR) AND ADDDATE(CURDATE(), INTERVAL -1 YEAR);
``````
# 12. Объединить все таблицы в одну, при этом сохраняя поля, указывающие на прошлую принадлежность к старым таблицам.
``````
SELECT Dogs.name_animal, Dogs.commands, Dogs.birthday, Pets.animal_kind, Animals.animal_type
FROM Dogs
LEFT JOIN Pets ON Pets.id = Dogs.animal_kind_id
LEFT JOIN Animals ON Animals.id=Pets.animal_type_id
UNION
SELECT Cats.name_animal, Cats.commands, Cats.birthday, Pets.animal_kind, Animals.animal_type
FROM Cats
LEFT JOIN Pets ON Pets.id = Cats.animal_kind_id
LEFT JOIN Animals ON Animals.id=Pets.animal_type_id
UNION
SELECT Hamsters.name_animal, Hamsters.commands, Hamsters.birthday, Pets.animal_kind, Animals.animal_type
FROM Hamsters
LEFT JOIN Pets ON Pets.id = Hamsters.animal_kind_id
LEFT JOIN Animals ON Animals.id=Pets.animal_type_id
UNION
SELECT Horses.name_animal, Horses.commands, Horses.birthday, PackAnimals.animal_kind, Animals.animal_type
FROM Horses
LEFT JOIN PackAnimals ON PackAnimals.id = Horses.animal_kind_id
LEFT JOIN Animals ON Animals.id=PackAnimals.animal_type_id
UNION
SELECT Camels.name_animal, Camels.commands, Camels.birthday, PackAnimals.animal_kind, Animals.animal_type
FROM Camels
LEFT JOIN PackAnimals ON PackAnimals.id = Camels.animal_kind_id
LEFT JOIN Animals ON Animals.id=PackAnimals.animal_type_id
UNION
SELECT Donkeys.name_animal, Donkeys.commands, Donkeys.birthday, PackAnimals.animal_kind, Animals.animal_type
FROM Donkeys
LEFT JOIN PackAnimals ON PackAnimals.id = Donkeys.animal_kind_id
LEFT JOIN Animals ON Animals.id=PackAnimals.animal_type_id;
``````
