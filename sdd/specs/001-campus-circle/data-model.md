# Data model and invariants

Accounts(id INTEGER primary key, username TEXT unique COLLATE NOCASE, name TEXT, salt TEXT, password_hash TEXT). Required fields NOT NULL. ASCII username validation precedes insertion; uniqueness is also enforced in the database. A failed registration transaction must leave no new row.

Sessions(token TEXT primary key, csrf TEXT, user_id INTEGER nullable foreign key Accounts, expires REAL). A guest has user_id NULL. A valid authenticated session has an existing account and expires greater than current wall time. Transitions: absent/expired -> guest; guest/authenticated + valid login/registration -> new authenticated token, old token deleted; logout -> token deleted; next GET -> guest. Sessions are isolated across cookie jars.

Posts(id INTEGER primary key, user_id INTEGER foreign key Accounts, body TEXT, created TEXT). body length 1–500 after trimming; no NUL characters. The username and display name are joined from the account. Newest-first ordering uses id, avoiding equal-timestamp ambiguity. UTC timestamp is ISO 8601. No seeded users/posts.

Database contexts commit on success, roll back on error, and always close. All variable SQL values use parameters. Application data lives under ignored data/ directories.
