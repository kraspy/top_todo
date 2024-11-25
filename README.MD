```sh
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

crontab -e
* * * * * sudo -u ИмяПользователя /bin/bash -c "source /путь/до/вашего/.venv/bin/activate && /путь/до/вашего/.venv/bin/python /путь/до/проекта/manage.py check_overdue_tasks"

python bot.py
```

- Все ок
- Были сложности с отправкой уведомлений в бота.
- Можно добавить авторизацию, рассылку разным пользователям, а не только захардкоженному.