import sqlite3
from contextlib import contextmanager
from .config import DB_PATH

SCHEMA = '''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS participants (
 id TEXT PRIMARY KEY, consent_version TEXT NOT NULL, consented_at TEXT NOT NULL,
 gender_identity TEXT NOT NULL, target_gender TEXT NOT NULL,
 age_band TEXT NOT NULL, area TEXT NOT NULL, role TEXT NOT NULL,
 required_json TEXT NOT NULL, preferred_json TEXT NOT NULL,
 availability_json TEXT NOT NULL, portrait_opt_in INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS survey_responses (
 id INTEGER PRIMARY KEY AUTOINCREMENT, participant_id TEXT NOT NULL,
 participation_intent INTEGER NOT NULL, payment_intent INTEGER NOT NULL,
 price_plan TEXT NOT NULL, usability_score INTEGER NOT NULL,
 comment TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL,
 FOREIGN KEY(participant_id) REFERENCES participants(id)
);
CREATE TABLE IF NOT EXISTS portrait_trials (
 id INTEGER PRIMARY KEY AUTOINCREMENT, participant_id TEXT NOT NULL,
 attempt INTEGER NOT NULL, provider TEXT NOT NULL, status TEXT NOT NULL,
 approved INTEGER, rejection_reason TEXT, asset_ref TEXT,
 created_at TEXT NOT NULL, deleted_at TEXT,
 FOREIGN KEY(participant_id) REFERENCES participants(id)
);
CREATE TABLE IF NOT EXISTS simulation_runs (
 id TEXT PRIMARY KEY, created_at TEXT NOT NULL, rule_version TEXT NOT NULL,
 applications INTEGER NOT NULL, assigned INTEGER NOT NULL,
 groups_json TEXT NOT NULL, metrics_json TEXT NOT NULL
);
'''

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
        conn.commit()

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
