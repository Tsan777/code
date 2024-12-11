import sqlite3


def create_setting_table():
    # Kết nối tới database setting.db
    conn = sqlite3.connect('setting.db')
    cursor = conn.cursor()

    # Tạo bảng setting với cột times là INTEGER và history là TEXT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS setting (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            times INTEGER DEFAULT 0,
            history TEXT DEFAULT '',
            todo TEXT DEFAULT '',
            task TEXT DEFAULT '',
            goal  TEXT DEFAULT ''
        )
    ''')

    # Kiểm tra xem bảng có bản ghi nào chưa, nếu chưa thì thêm bản ghi mặc định
    cursor.execute('SELECT COUNT(*) FROM setting')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO setting (times, history) VALUES (?, ?)', (0, ''))
        conn.commit()

    # Đóng kết nối
    conn.close()


# Gọi hàm tạo bảng
create_setting_table()
