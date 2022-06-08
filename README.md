# Сервис. Получение картинки-карты с NDVI по geojson.
![](https://github.com/maxzawalo/test_ee_ndvi/blob/main/maps/1654700860467368900.png)

## Установка
- Устанавливаем Google Earth Engine на сервер https://developers.google.com/earth-engine/guides/python_install
- Устанавливаем библиотеки

  pip install uvicorn

  pip install fastapi

  pip install selenium
 
  pip install folium

  pip install pillow


## Запуск сервера
python server.py

## Использование сервиса
- Переходим на https://geojson.io/.
- Выделяем нужную нам область.
- Сохраняем json текст (справа) в файл.
- Переходим по адресу http://127.0.0.1:8000/docs.
- Полученный ранне файл отправляем на сервис и получаем карту в формате png.

Коллекция postman для тестирования ndvi_from_geojson.postman_collection.json
