# import pandas as pd

# # Путь к файлу Excel и имя листа
# file_path = "forModelThree.xlsx"
# sheet_name = "Массив"

# # Чтение данных из Excel файла
# data = pd.read_excel(file_path, sheet_name=sheet_name)

# # Извлечение уникальных имен классов направлений
# unique_directions = data['Направление'].unique()

# # Вывод уникальных имен классов направлений
# for direction in unique_directions:
#     print(direction)

# import pandas as pd

# # Считываем данные из файла
# file_path = "forModelThree.xlsx"
# data = pd.read_excel(file_path)

# # Создаем словарь для соответствия классов и чисел
# class_numbers = {
#     "Газы крови и электролиты": 1,
#     "ИХА": 2,
#     "Иное": 3,
#     "Биохимия": 4,
#     "Мочевая химия": 5,
#     "Гемостаз": 6,
#     "Гематология": 7,
#     "Гемостаз спец": 8,
#     "ИГА": 9,
#     "ПЦР и молекулярная диагностика": 10,
#     "Лабораторные расходные материалы": 11,
#     "ТП Глюкоза": 12,
#     "ИХА нарк": 13,
#     "Микробиология": 14,
#     "ИФА": 15,
#     "Глик гемоглобин": 16,
#     "Глюкоза и лактат": 17,
#     "Неонатальный скрининг": 18,
#     "КДЛ": 19,
#     "Аллергодиагностика": 20,
#     "Латекс Тест": 21,
#     "Гемоглобин": 22,
#     "Латекс тест": 23,
#     "Не то" : 24,
# }

# # Создаем новый столбец с номерами классов
# data['Класс номера'] = data['Направление'].map(class_numbers)

# # Сохраняем новую таблицу в файл
# new_file_path = "new_forModelThree_with_numbers.xlsx"
# data.to_excel(new_file_path, index=False)

# print("Новая таблица с номерами классов сохранена в", new_file_path)

import pandas as pd

# Считываем данные из Excel файла
file_path = "testTest.xlsx"
data = pd.read_excel(file_path)

# Сохраняем данные в формате CSV
csv_file_path = "testTest.csv"
data.to_csv(csv_file_path, index=False)

print("Данные сохранены в формате CSV в файле", csv_file_path)
