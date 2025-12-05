import json
import os
import asyncio

# Local JSON file to store user data
DB_FILE = "database/users.json"

class Database:
    def __init__(self, uri=None, database_name=None):
        # uri and database_name are kept for compatibility with the existing init signature
        self.db_file = DB_FILE
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)
        self.lock = asyncio.Lock()

    def _load(self):
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    async def add_user(self, id, name):
        async with self.lock:
            data = self._load()
            if str(id) not in data:
                data[str(id)] = {
                    "id": id,
                    "name": name,
                    "session": None,
                    "api_id": None,
                    "api_hash": None
                }
                self._save(data)

    async def is_user_exist(self, id):
        data = self._load()
        return str(id) in data

    async def total_users_count(self):
        data = self._load()
        return len(data)

    async def get_all_users(self):
        data = self._load()
        # Return an async generator to satisfy 'async for' loops in the bot code
        async def async_gen():
            for user in data.values():
                yield user
        return async_gen()

    async def delete_user(self, user_id):
        async with self.lock:
            data = self._load()
            if str(user_id) in data:
                del data[str(user_id)]
                self._save(data)

    async def set_session(self, id, session):
        async with self.lock:
            data = self._load()
            if str(id) in data:
                data[str(id)]['session'] = session
                self._save(data)

    async def get_session(self, id):
        data = self._load()
        return data.get(str(id), {}).get('session')

    async def set_api_id(self, id, api_id):
        async with self.lock:
            data = self._load()
            if str(id) in data:
                data[str(id)]['api_id'] = api_id
                self._save(data)

    async def get_api_id(self, id):
        data = self._load()
        return data.get(str(id), {}).get('api_id')

    async def set_api_hash(self, id, api_hash):
        async with self.lock:
            data = self._load()
            if str(id) in data:
                data[str(id)]['api_hash'] = api_hash
                self._save(data)

    async def get_api_hash(self, id):
        data = self._load()
        return data.get(str(id), {}).get('api_hash')

# Initialize the database instance (arguments are ignored)
db = Database("dummy_uri", "dummy_name")
