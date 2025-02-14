import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Загрузка данных (предположим, что данные уже загружены в DataFrame)
# Пример структуры данных: Дата, Тикер, Цена открытия, Минимальная цена, Максимальная цена, Объем, Цена закрытия
data = pd.read_csv('moex_data.csv')

# Предобработка данных
data['Дата'] = pd.to_datetime(data['Дата'])
data = data.sort_values(by=['Тикер', 'Дата'])

# Создание признаков (например, скользящие средние)
data['SMA_7'] = data.groupby('Тикер')['Цена закрытия'].transform(lambda x: x.rolling(window=7).mean())
data['SMA_30'] = data.groupby('Тикер')['Цена закрытия'].transform(lambda x: x.rolling(window=30).mean())

# Удаление строк с пропущенными значениями
data = data.dropna()

# Выбор признаков и целевой переменной
features = ['Цена открытия', 'Минимальная цена', 'Максимальная цена', 'Объем', 'SMA_7', 'SMA_30']
X = data[features]
y = data['Цена закрытия']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Масштабирование данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MAE: {mae}')
print(f'MSE: {mse}')
print(f'R²: {r2}')

# Предсказание на будущую дату
# Например, предсказание на 180 дней вперед
future_date = pd.to_datetime('2023-12-31')
future_data = data[data['Дата'] <= future_date].tail(1)[features]
future_data_scaled = scaler.transform(future_data)
predicted_price = model.predict(future_data_scaled)
print(f'Предсказанная цена на {future_date}: {predicted_price[0]}')