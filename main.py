import asyncio
import sqlite3

import aiohttp
from itertools import cycle
from datetime import datetime
import aiofiles

from config.info import \
    db, \
    users_file as u_f, \
    proxies_file as p_f, \
    log_file as l_f


class ProxyAssigner:
    def __init__(self, db_file=db, users_file=u_f, proxies_file=p_f, log_file=l_f):
        self.users_file = users_file
        self.proxies_file = proxies_file
        self.log_file = log_file
        self.db_file = db_file
        self.users = []
        self.proxies = []

    def create_table(self):
        """Создание таблицы в базе данных, если она не существует"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                proxy TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()


    def load_users(self):
        """Загрузка пользователей из файла"""
        with open(self.users_file, 'r') as f:
            for line in f:
                email, password = line.strip().split(':')
                self.users.append(email)

    def load_proxies(self):
        """Загрузка прокси из файла"""
        with open(self.proxies_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 4:
                    ip, port, username, password = parts
                    self.proxies.append({
                        'ip': ip,
                        'port': port,
                        'username': username,
                        'password': password
                    })
                else:
                    pass

    async def is_proxy_valid(self, session, proxy):
        """Проверка прокси на валидность через API"""
        proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
        try:
            async with session.get('http://api.ipify.org', proxy=proxy_url, timeout=5) as response:
                return response.status == 200
        except Exception:
            return False

    def assign_proxy(self, email, proxy):
        """Назначение валидного прокси пользователю"""
        return {'email': email, 'proxy': f"{proxy['ip']}:{proxy['port']}"}

    async def log_assignment(self, assignment):
        """Логирование связки email + IP в файл и базу данных"""
        log_entry = f"{datetime.now()} - {assignment['email']} assigned to {assignment['proxy']}"
        print(f"\033[92m{log_entry}\033[0m")

        # Логируем в файл
        async with aiofiles.open(self.log_file, 'a') as f:
            await f.write(log_entry + "\n")

        # Логируем в базу данных
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO proxy_assignments (email, proxy)
            VALUES (?, ?)
        ''', (assignment['email'], assignment['proxy']))
        conn.commit()
        conn.close()

    async def process_user(self, email, proxy_pool):
        """Функция для обработки одного пользователя"""
        async with aiohttp.ClientSession() as session:
            for proxy in proxy_pool:
                if await self.is_proxy_valid(session, proxy):
                    assignment = self.assign_proxy(email, proxy)
                    await self.log_assignment(assignment)
                    break
            await asyncio.sleep(10)  # Задержка в 10 секунд

    async def run(self):
        """Основная асинхронная функция для запуска"""
        self.load_users()
        self.load_proxies()

        # Создаем таблицу перед началом обработки
        self.create_table()

        proxy_pool = cycle(self.proxies) # Создаем циклический итератор по прокси
        while True:
            tasks = []
            # Обрабатываем до 4 пользователей, но не больше чем есть в self.users
            self.users = self.users[::-1]
            for _ in range(min(4, len(self.users))): # Выбираем минимальное количество
                tasks.append(self.process_user(self.users.pop(), proxy_pool))
            await asyncio.gather(*tasks)

            print('\033[91m--------------------\033[0m')

            if len(self.users) == 0: # Если пользователи закончились, загружаем их снова
                print(f"\033[91m\nВсе пользователи обработаны, начинаем заново...\n\033[0m")
                self.load_users()  # Загружаем пользователей снова


if __name__ == "__main__":
    proxy_assigner = ProxyAssigner()
    asyncio.run(proxy_assigner.run())
