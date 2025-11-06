import aiosqlite

DB_PATH = "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_code TEXT,
                latitude REAL,
                longitude REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()

async def add_user(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (tg_id,))
        await db.commit()

async def get_user_id(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else None

async def add_tag(tg_id: int, tag_code: str):
    user_id = await get_user_id(tg_id)
    if not user_id:
        await add_user(tg_id)
        user_id = await get_user_id(tg_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO tags (user_id, tag_code) VALUES (?, ?)", (user_id, tag_code))
        await db.commit()

async def get_tags(tg_id: int):
    user_id = await get_user_id(tg_id)
    if not user_id:
        return []
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT tag_code FROM tags WHERE user_id = ?", (user_id,)) as cur:
            return [row[0] for row in await cur.fetchall()]
async def add_location(tag_code: str, lat: float, lon: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO locations (tag_code, latitude, longitude) VALUES (?, ?, ?)",
            (tag_code, lat, lon)
        )
        await db.commit()

async def get_last_location(tag_code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT latitude, longitude, timestamp
            FROM locations
            WHERE tag_code = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (tag_code,)) as cur:
            return await cur.fetchone()

async def get_location_history(tag_code: str, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT latitude, longitude, timestamp
            FROM locations
            WHERE tag_code = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (tag_code, limit)) as cur:
            return await cur.fetchall()
