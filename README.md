# ITIS helper
Телеграм бот для студентов **КФУ ИТИС**

## Установка и запуск бота
### 1. Склонировать репозиторий
```shell
git clone https://github.com/MMingazoff/ITIS-helper.git
```
### 2. Переместиться в папку с репозиторием
```shell
cd ITIS-helper
```
### 3. Создать файл с токенами необходимыми для работы бота
  - токен бота
  ```shell
  echo TOKEN = "your token" >> config.py
  ```
  - токен вк (требуется для парсинга мероприятий с пабликов)
    - получите токен [ссылка на гайд](https://dev.vk.com/api/getting-started#%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F)
    - запишите его в файл
    ```shell
    echo ACCESS_TOKEN = "your token" >> config.py
    ```
### 4. Установите зависимости
```shell
pip install -r requirements.txt
```
### 5. Запустите бота
```shell
python bot_telegram.py
```
### 6. Profit
Ваш бот работает!

## Контакты
tg: [_@mf_jstr_](https://t.me/mf_jstr)
