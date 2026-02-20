from database import create_connection, create_table
from datetime import datetime
import csv


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_expense():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date = input("Enter date (YYYY-MM-DD): ")

        if not validate_date(date):
            print("❌ Invalid date format! Use YYYY-MM-DD.")
            conn.close()
            return

        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )

        conn.commit()
        print("✅ Expense added successfully!")

    except ValueError:
        print("❌ Invalid amount entered!")

    conn.close()


def view_expenses():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    print("\n===== All Expenses =====")
    print("ID | Amount | Category | Date")
    print("-----------------------------------")

    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    conn.close()


def delete_expense():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        expense_id = int(input("Enter expense ID to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

        if cursor.rowcount == 0:
            print("⚠ No expense found with that ID.")
        else:
            print("🗑 Expense deleted!")

    except ValueError:
        print("❌ Invalid ID entered!")

    conn.close()


def monthly_summary():
    conn = create_connection()
    cursor = conn.cursor()

    month = input("Enter month (YYYY-MM): ")

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE date LIKE ?
    """, (month + "%",))

    total = cursor.fetchone()[0]

    if total:
        print(f"💰 Total expenses for {month}: {total}")
    else:
        print("No expenses found for this month.")

    conn.close()


def category_summary():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()

    print("\n===== Category-wise Summary =====")
    print("Category | Total Amount")
    print("---------------------------")

    for row in rows:
        print(f"{row[0]} | {row[1]}")

    conn.close()


def export_to_csv():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("No data to export.")
        conn.close()
        return

    with open("expenses.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Amount", "Category", "Date"])
        writer.writerows(rows)

    print("📁 Data exported successfully to expenses.csv!")
    conn.close()


def main():
    create_table()

    while True:
        print("\n====== Expense Tracker ======")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary")
        print("5. Category Summary")
        print("6. Export to CSV")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            category_summary()
        elif choice == "6":
            export_to_csv()
        elif choice == "7":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()