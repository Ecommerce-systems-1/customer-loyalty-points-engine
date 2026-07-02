import uuid
import aiosqlite
from typing import List, Dict, Any

class Database:
    def __init__(self, path: str = '/data/11_customer_loyalty_points_engine.db'):
        self.path = path
        self._conn = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute('PRAGMA journal_mode=WAL')
        await self._conn.executescript('''
            CREATE TABLE IF NOT EXISTS customers (id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, tier TEXT DEFAULT 'bronze', total_points INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')));
            CREATE TABLE IF NOT EXISTS points_transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT NOT NULL, amount INTEGER NOT NULL, transaction_type TEXT NOT NULL, description TEXT, created_at TEXT DEFAULT (datetime('now')));
        ''')
        await self._conn.commit()

    async def close(self):
        if self._conn:
            await self._conn.close()
