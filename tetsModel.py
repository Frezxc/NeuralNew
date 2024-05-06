import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

classes = [
    "Аллергодиагностика",
    "Биохимия",
    "Латекс тест",
    "Гематология",
    "ИГА",
    "ИХА",
    "ИХА нарк",
    "Иное",
    "ИФА",
    "Гемостаз",
    "Гемостаз спец",
    "Лабораторные расходные материалы",
    "Микробиология",
    "Мочевая химия",
    "Не то",
    "Неонатальный скрининг",
    "ПЦР и молекулярная диагностика",
    "Газы крови и электролиты",
    "Гемоглобин",
    "Глик гемоглобин",
    "Глюкоза и лактат",
    "ТП Глюкоза"
]

# Загрузка обученной модели
model = load_model("product_classification_model.h5")

# Загрузка данных из файла Excel
file_path = "forModelTest.xlsx"
sheet_name = "Массив"
try:
    data = pd.read_excel(file_path, sheet_name=sheet_name)
except FileNotFoundError:
    print("Файл не найден. Убедитесь, что путь к файлу и имя листа корректны.")
    exit()

# Проверка наличия столбца 'Результат' в исходных данных
if 'Результат' in data.columns:
    print("Столбец 'Результат' уже существует в исходных данных. Выход.")
    exit()

# Подготовка данных для классификации
X = data['ОБЩ']  # Признаки (характеристики товаров)

# Преобразование текстовых данных в числовые последовательности
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)

# Заполнение нулями последовательностей до максимальной длины
max_sequence_length = max([len(seq) for seq in X_seq])
X_pad = pad_sequences(X_seq, maxlen=max_sequence_length)

X_pad_clipped = np.clip(X_pad, a_min=None, a_max=17610)
# Классификация данных
# Классификация данных
predictions = model.predict(X_pad_clipped)

# Получение индексов классов с наибольшей вероятностью
predicted_indices = predictions.argmax(axis=-1)

# Преобразование индексов в одномерный массив
predicted_indices = predicted_indices.flatten()

# Преобразование индексов в целые числа
predicted_indices = predicted_indices.astype(int)
print(predicted_indices)
# Преобразование числовых меток обратно в текстовые классы
label_encoder = LabelEncoder()
try:
    label_encoder.classes_ = model.get_layer('dense').get_weights()[1].tolist()  # Получение классов из модели
except Exception as e:
    print("Ошибка при получении классов из модели:", e)
    print("Пожалуйста, укажите соответствующие текстовые метки для обратного преобразования.")
    exit()

# Преобразование числовых меток обратно в текстовые классы
label_encoder = LabelEncoder()
label_encoder.classes_ = classes
predicted_classes = label_encoder.inverse_transform(predicted_indices)

# Добавление колонки с результатами классификации в исходные данные
data['Результат'] = predicted_classes

# Сохранение данных с результатами классификации в новый файл
output_file_path = "classified_data.xlsx"
data.to_excel(output_file_path, index=False)

print("Классификация данных завершена. Результаты сохранены в файл:", output_file_path)
