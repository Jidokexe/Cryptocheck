# Описание
Этот проект представляет собой систему для проверки цифровых подписей документов, которая использует базу данных PostgreSQL для хранения данных документов и их подписей, а также SMTP и IMAP для обработки электронной почты. Скрипт проверяет подписи документов, отправляет результаты проверки по электронной почте и обрабатывает входящие сообщения с документами.

# Основные функции
- Подключение к базе данных: Функция connect_db() устанавливает соединение с базой данных PostgreSQL, в которой хранятся документы, их подписи и открытые ключи пользователей.
  
- Проверка цифровой подписи: Функция verify_signature(document_data, signature, public_key) использует библиотеку cryptography для проверки подлинности цифровой подписи документа с использованием открытого ключа.

- Проверка подписи документа: Функция check_document_signature(document_id) извлекает данные документа, его подпись и открытый ключ из базы данных и проверяет подпись документа.

- Отправка электронной почты: Функция send_email(to_email, subject, body, attachment) отправляет электронное письмо с указанным телом и вложением (в случае необходимости), используя SMTP.

- Проверка входящих электронных писем: Функция check_incoming_emails() считывает непрочитанные сообщения в почтовом ящике и проверяет вложенные PDF-документы на наличие действительных цифровых подписей, отправляя отчет о результатах проверки обратно отправителю.

# Установка
Для установки необходим Python 3 и библиотеки, указанные в requirements.txt, а также база данных postgesql. Установите их с помощью следующей команды:
pip install -r requirements.txt


# Настройка
Не забудьте настроить параметры подключения к базе данных и электронной почте в скрипте перед использованием. Замените следующие значения:

- dbname, user, password в функции connect_db().
- your_email@example.com и your_password в функции send_email() и check_incoming_emails().
- SMTP и IMAP-серверы (например, smtp.example.com, imap.example.com) соответствующими значениями для вашего почтового провайдера.

# Запуск
Чтобы запустить систему проверки документов, выполните следующую команду:
python3 Cryptocheck.py


# Функциональность и особенности
- Код читаем и понятен: Каждая функция имеет четко определенную задачу, что делает проект упорядоченным и легким для дальнейшего расширения.
  
- Криптографическая безопасность: Проект использует библиотеку cryptography для надежной проверки цифровых подписей, гарантируя безопасность данных.

- Интеграция с электронной почтой: Проект включает функции отправки и получения электронных писем, что позволяет пользователям получать результаты проверки документов в реальном времени.

- Расширяемость: Проект может быть легко адаптирован для работы с другими типами документов или расширен новыми функциями по запросу.


# Контактная информация
Email: IvanilovVM22@st.ithub.ru Telegram: @Jidok_exe

Email: KhaydukovDO22@st.ithub.ru Telegram: @coldy01
