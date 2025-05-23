# Приложение для загрузки моделей и чата

Это приложение на Python, созданное с использованием Tkinter, предназначенное для загрузки трансформерных моделей машинного обучения с Hugging Face и взаимодействия с ними через интерфейс чата.

## Возможности
- Загрузка трансформерных моделей с Hugging Face по имени модели (например, `gpt2`).
- Выбор папки для сохранения и управления загруженными моделями.
- Отображение списка доступных моделей в выбранной папке.
- Общение с выбранной моделью через текстовый интерфейс чата.
- Индикатор прогресса и отображение расчетного времени загрузки модели.

## Требования
Для работы приложения необходимо установить Python (рекомендуется версия 3.7 или выше). Требуются следующие библиотеки:

### Необходимые библиотеки
- `tkinter`: Для создания графического интерфейса (обычно включена в стандартную установку Python).
- `transformers`: Для загрузки и взаимодействия с моделями Hugging Face.
- `huggingface_hub`: Для скачивания моделей с Hugging Face.
- `humanize`: Для форматирования времени в удобочитаемый вид.
- `threading`: Для выполнения загрузки моделей в отдельном потоке (включена в стандартную библиотеку Python).
- `os`: Для работы с файловой системой (включена в стандартную библиотеку Python).
- `time`: Для расчета времени загрузки (включена в стандартную библиотеку Python).

### Установка библиотек
Установите необходимые библиотеки с помощью `pip`:
```bash
pip install transformers huggingface_hub humanize
```
### рекомендую
Установить :
```bash
pip install torch
```


## Установка и запуск
1. Убедитесь, что Python и все необходимые библиотеки установлены.
2. Сохраните файлы приложения (`main.py`, `ui.py`, `model_handler.py`, `chat.py`) в одной директории.
3. Запустите приложение, выполнив команду:
   ```bash
   python main.py
   ```

## Принцип работы
1. **Интерфейс загрузки модели**:
   - Введите имя модели (например, `gpt2`) в поле ввода.
   - Выберите папку для сохранения модели с помощью кнопки "Выберите папку для установки".
   - Нажмите "Скачать модель" для начала загрузки. Прогресс отображается в индикаторе, а расчетное время — в текстовом поле.
   - Список загруженных моделей отображается в списке ниже.

2. **Проверка существующих моделей**:
   - При выборе папки приложение проверяет наличие моделей (папок с файлом `config.json`) и загружает их в список.
   - Модели, которые не удалось загрузить, игнорируются с выводом ошибки в консоль.

3. **Чат с моделью**:
   - Выберите модель из списка и нажмите "Начать чат с моделью".
   - Введите сообщение в поле ввода и нажмите "Отправить" или клавишу Enter.
   - Ответ модели отображается в окне чата (сообщения пользователя — синим, ответы бота — зеленым, ошибки — красным).
   - Нажмите "Вернуться", чтобы вернуться к главному интерфейсу.

## Структура кода
- `main.py`: Основной файл, инициализирующий приложение и связывающий компоненты.
- `ui.py`: Отвечает за создание и управление графическим интерфейсом (главное окно и окно чата).
- `model_handler.py`: Обрабатывает выбор папки, загрузку моделей и управление списком моделей.
- `chat.py`: Реализует функционал чата, включая отправку сообщений и отображение ответов.

## Замечания
- Загрузка моделей выполняется в отдельном потоке, чтобы не блокировать интерфейс.
- Для корректной работы чата модель должна быть совместима с `AutoModelForCausalLM` и `AutoTokenizer` из библиотеки `transformers`.
- Если модель не имеет токена паддинга, используется токен конца последовательности (`eos_token`).
