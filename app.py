import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("campus_spend.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()

    # 查询所有消费记录
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC, id DESC"
    ).fetchall()

    # 统计总消费金额和消费记录数量
    total_result = conn.execute(
        "SELECT SUM(amount) AS total_amount, COUNT(*) AS total_count FROM expenses"
    ).fetchone()

    # 统计必要消费总额
    necessary_result = conn.execute(
        "SELECT SUM(amount) AS necessary_amount FROM expenses WHERE is_necessary = 1"
    ).fetchone()

    # 统计非必要消费总额
    unnecessary_result = conn.execute(
        "SELECT SUM(amount) AS unnecessary_amount FROM expenses WHERE is_necessary = 0"
    ).fetchone()

    # 按消费分类统计金额
    category_stats = conn.execute(
        """
        SELECT category, SUM(amount) AS category_total
        FROM expenses
        GROUP BY category
        ORDER BY category_total DESC
        """
    ).fetchall()

    conn.close()

    total_amount = total_result["total_amount"] or 0
    total_count = total_result["total_count"] or 0
    necessary_amount = necessary_result["necessary_amount"] or 0
    unnecessary_amount = unnecessary_result["unnecessary_amount"] or 0

    # ECharts 饼图需要的数据格式：
    # [
    #   {"name": "餐饮", "value": 120.5},
    #   {"name": "学习", "value": 35}
    # ]
    category_chart_data = [
        {
            "name": item["category"],
            "value": item["category_total"]
        }
        for item in category_stats
    ]

    return render_template(
        "index.html",
        expenses=expenses,
        total_amount=total_amount,
        total_count=total_count,
        necessary_amount=necessary_amount,
        unnecessary_amount=unnecessary_amount,
        category_stats=category_stats,
        category_chart_data=category_chart_data
    )


@app.route("/add", methods=("GET", "POST"))
def add_expense():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = request.form["amount"]
        payment = request.form["payment"]
        note = request.form["note"]
        is_necessary = request.form["is_necessary"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO expenses (date, category, amount, payment, note, is_necessary)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date, category, amount, payment, note, is_necessary)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:expense_id>", methods=("POST",))
def delete_expense(expense_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:expense_id>", methods=("GET", "POST"))
def edit_expense(expense_id):
    conn = get_db_connection()

    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = request.form["amount"]
        payment = request.form["payment"]
        note = request.form["note"]
        is_necessary = request.form["is_necessary"]

        conn.execute(
            """
            UPDATE expenses
            SET date = ?, category = ?, amount = ?, payment = ?, note = ?, is_necessary = ?
            WHERE id = ?
            """,
            (date, category, amount, payment, note, is_necessary, expense_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()

    return render_template("edit.html", expense=expense)


if __name__ == "__main__":
    app.run(debug=True)