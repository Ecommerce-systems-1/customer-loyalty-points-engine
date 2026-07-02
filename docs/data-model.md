# Data Model — Customer Loyalty Points Engine

```sql
CREATE TABLE IF NOT EXISTS customers (id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, tier TEXT DEFAULT 'bronze', total_points INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')));
```
