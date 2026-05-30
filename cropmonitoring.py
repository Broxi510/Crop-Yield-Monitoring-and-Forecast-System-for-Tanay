import mysql.connector
import matplotlib.pyplot as plt

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jaydenkyle202124",
        database="crop_monitoring"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    print("Connected DB:", cursor.fetchall())

except mysql.connector.Error as err:
    print("Connection failed:", err)
    exit()

def add_record():
    print("\n--- Add Record ---")
    name = input("Farmer Name: ")
    barangay = input("Barangay: ")
    crop = input("Crop Type: ")

    try:
        area = float(input("Area (hectares): "))
        yield_amt = float(input("Yield (tons): "))
    except ValueError:
        print("Invalid input!")
        return

    yield_per_hectare = yield_amt / area if area != 0 else 0

    sql = """INSERT INTO records 
             (name, barangay, crop, area, yield_amt, yield_per_hectare)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    cursor.execute(sql, (name, barangay, crop, area, yield_amt, yield_per_hectare))
    conn.commit()

    print("Saved!")

def view_records():
    print("\n--- Records ---")
    cursor.execute("SELECT * FROM records")
    data = cursor.fetchall()

    if not data:
        print("No records found.")
        return

    for i, r in enumerate(data, 1):
        print(f"{i}. {r[1]} | {r[2]} | {r[3]} | {r[5]} tons (ID: {r[0]})")

def show_chart():
    cursor.execute("SELECT crop, SUM(yield_amt) FROM records GROUP BY crop")
    data = cursor.fetchall()

    if not data:
        print("No data for chart")
        return

    crops = [row[0] for row in data]
    yields = [row[1] for row in data]

    plt.bar(crops, yields)
    plt.title("Total Yield per Crop")
    plt.xlabel("Crop")
    plt.ylabel("Yield (tons)")
    plt.show()

def view_analytics():
    print("\n--- Analytics & Forecast ---")

    cursor.execute("""
        SELECT 
            crop,
            SUM(yield_amt),
            SUM(area),
            COUNT(*)
        FROM records
        GROUP BY crop
    """)

    data = cursor.fetchall()

    if not data:
        print("No data available.")
        return

    for row in data:
        crop = row[0]
        total_yield = row[1]
        total_area = row[2]
        count = row[3]

        avg_yield = total_yield / count if count != 0 else 0
        yield_per_hectare = total_yield / total_area if total_area != 0 else 0

        print(f"\nCrop: {crop}")
        print(f"  - Total Yield: {total_yield:.2f} tons")
        print(f"  - Average Yield: {avg_yield:.2f} tons")
        print(f"  - Yield per Hectare: {yield_per_hectare:.2f} tons/ha")
        print(f"  - Forecast (next season): {avg_yield:.2f} tons")

def delete_record():
    print("\n--- Delete Record ---")
    view_records()

    try:
        record_id = int(input("Enter ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    sql = "DELETE FROM records WHERE id = %s"
    cursor.execute(sql, (record_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Record deleted!")
        reset_ids()
    else:
        print("No record found with that ID.")

def reset_ids():
    cursor.execute("SET @num = 0")
    cursor.execute("""
        UPDATE records 
        SET id = (@num := @num + 1)
        ORDER BY id
    """)
    cursor.execute("ALTER TABLE records AUTO_INCREMENT = 1")
    conn.commit()

def main():
    while True:
        print("\n=== Crop Monitoring System ===")
        print("1. Add Record")
        print("2. View Records")
        print("3. Show Chart")
        print("4. Analytics & Forecast")
        print("5. Delete Record")
        print("6. Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            show_chart()
        elif choice == "4":
            view_analytics()
        elif choice == "5":
            delete_record()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()