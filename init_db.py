import sqlite3

# 连接数据库。如果 campus_spend.db 不存在，SQLite 会自动创建
conn = sqlite3.connect("campus_spend.db")

# 创建游标对象，用来执行 SQL 语句
cursor = conn.cursor()

# 如果 expenses 表已经存在，就先删除，方便我们反复测试
cursor.execute("DROP TABLE IF EXISTS expenses")

# 创建消费记录表
cursor.execute("""
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    payment TEXT,
    note TEXT,
    is_necessary INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 插入几条测试数据
cursor.execute("""
INSERT INTO expenses (date, category, amount, payment, note, is_necessary)
VALUES ('2026-05-01', '餐饮', 18.5, '微信', '午饭', 1)
""")

cursor.execute("""
INSERT INTO expenses (date, category, amount, payment, note, is_necessary)
VALUES ('2026-05-01', '学习', 35, '支付宝', '买资料', 1)
""")

cursor.execute("""
INSERT INTO expenses (date, category, amount, payment, note, is_necessary)
VALUES ('2026-05-02', '娱乐', 28, '微信', '奶茶和零食', 0)
""")

# 提交事务，让修改真正保存到数据库
conn.commit()

# 关闭数据库连接
conn.close()

print("数据库初始化完成：campus_spend.db 已创建，expenses 表已生成。")