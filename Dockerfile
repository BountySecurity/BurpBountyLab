FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libxml2-dev libxslt-dev curl dnsutils iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create fake /etc/passwd for path traversal
RUN cp /etc/passwd /etc/passwd.bak

# Create fake win.ini for Windows path traversal simulation
RUN mkdir -p /app/fake_windows && \
    printf '[fonts]\r\n; for 16-bit app support\r\n[extensions]\r\n[mci extensions]\r\n[files]\r\n[Mail]\r\nMAPI=1\r\n' > /app/fake_windows/win.ini

# Create fake .git directory
RUN mkdir -p /app/static/.git/refs/heads && \
    echo 'ref: refs/heads/main' > /app/static/.git/HEAD && \
    printf '[core]\n\trepositoryformatversion = 0\n\tfileversion = 0\n\tbare = false\n' > /app/static/.git/config && \
    echo 'abc123def456' > /app/static/.git/refs/heads/main

# Create fake .svn directory
RUN mkdir -p /app/static/.svn && \
    printf '10\ndir\n123\nurl=https://svn.example.com/repo\ncommitted-date=2024-01-01T00:00:00Z\n' > /app/static/.svn/entries

# Init the SQLite database
RUN python -c "import sqlite3; \
    conn = sqlite3.connect('/app/vuln.db'); \
    c = conn.cursor(); \
    c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, role TEXT)'); \
    c.execute(\"INSERT INTO users VALUES (1, 'admin', 'admin@example.com', 'admin123', 'admin')\"); \
    c.execute(\"INSERT INTO users VALUES (2, 'john', 'john@example.com', 'password', 'user')\"); \
    c.execute(\"INSERT INTO users VALUES (3, 'jane', 'jane@example.com', 'secret', 'user')\"); \
    c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, category TEXT)'); \
    c.execute(\"INSERT INTO products VALUES (1, 'Laptop', 999.99, 'electronics')\"); \
    c.execute(\"INSERT INTO products VALUES (2, 'Phone', 499.99, 'electronics')\"); \
    c.execute(\"INSERT INTO products VALUES (3, 'Book', 19.99, 'education')\"); \
    conn.commit(); conn.close()"

EXPOSE 8088

CMD ["gunicorn", "--bind", "0.0.0.0:8088", "--workers", "4", "--threads", "4", "--timeout", "30", "app:app"]
