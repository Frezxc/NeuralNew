import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Список классов
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

# Загрузка данных из файла Excel
file_path = "forModel.xlsx"
sheet_name = "Массив"
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Подготовка данных
X = data['ОБЩ']  # Признаки (характеристики товаров)
y = data['Направление']  # Переменная (направление)

# Преобразование текстовых классов в числовые метки
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)


# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Преобразование текстовых данных в числовые последовательности
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Заполнение нулями последовательностей до максимальной длины
max_sequence_length = max([len(seq) for seq in X_train_seq])
X_train_pad = pad_sequences(X_train_seq, maxlen=max_sequence_length)
X_test_pad = pad_sequences(X_test_seq, maxlen=max_sequence_length)

# Создание нейронной сети
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_sequence_length))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(classes), activation='softmax'))

# Компиляция модели
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучение модели
model.fit(X_train_pad, y_train, epochs=10, batch_size=32, validation_data=(X_test_pad, y_test))

# Оценка качества модели на тестовых данных
score = model.evaluate(X_test_pad, y_test, verbose=0)
print(f'Test loss: {score[0]}')
print(f'Test accuracy: {score[1]}')

# Сохранение модели
model.save("product_classification_model.h5")

# Сохранение LabelEncoder
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
