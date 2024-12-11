import tkinter as tk
from tkinter import ttk
import random
import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
from plyer import notification
from tkinter import ttk, messagebox

class WorkWise:
    def __init__(self, root):
        self.root = root
        self.root.geometry("495x700")
        self.root.title("TodoApp")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#222121")

        # Thêm thanh tiến trình ở trên Notebook
        self.progress_frame = tk.Frame(self.root, bg="#222121")
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.pro_label = tk.Label(self.progress_frame, text=f"Lv :", font=("Helvetica", 12), bg="#222121", fg="#ffffff")
        self.pro_label.pack(side=tk.LEFT, padx=5)

        self.progress = ttk.Progressbar(self.progress_frame, length=320, mode="determinate")
        self.progress.pack(side=tk.LEFT, padx=5)
        self.progress["maximum"] = 1
        self.set_button = tk.Button(self.progress_frame, text="Set", command=self.set, width=5, bg="#333333",
                                    fg="#ffffff")
        self.set_button.pack(side=tk.LEFT, padx=5)
        self.get_cur_level()
        # Tùy chỉnh style cho Notebook và các Frame
        style = ttk.Style()
        style.theme_use('clam')  # Sử dụng theme hỗ trợ tùy chỉnh
        style.configure("TNotebook", background="#222121", borderwidth=0)
        style.configure("TNotebook.Tab", background="#444444", foreground="#FFFFFF", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#333333")])
        style.configure("TFrame", background="#222121")

        # Tạo Tab View (Notebook)
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill="both", expand=True)

        # Tạo các tab
        self.create_tabs()
    def get_cur_level(self):
        tasks_conn = sqlite3.connect('setting.db')
        tasks_cursor = tasks_conn.cursor()

        # Fetch current times and history
        tasks_cursor.execute('SELECT times, history FROM setting')
        result = tasks_cursor.fetchone()

        if result:
            current_times, current_history = result

            updated_times = current_times
            self.cur_lev = updated_times // 1

            self.pro_label['text'] = f"Lv {int(self.cur_lev)}:"

            percentage = (updated_times % 1 / 1)

            self.progress['value'] = percentage  # Cập nhật giá trị thanh tiến trình
            self.root.update_idletasks()  # Cập nhật giao diện ngay lập tức

        tasks_conn.close()
        try:

            return
        except:
            messagebox.showerror("Error", f" get_cur_level !!!")
            return

    def set(self):
        try:
            quick_edit_window = tk.Toplevel(self.root)
            quick_edit_window.title("EDIT")
            quick_edit_window.geometry("300x390")
            quick_edit_window.configure(bg="#222121")
            quick_edit_window.attributes('-topmost', True)
            old_word_label = tk.Label(quick_edit_window, text="Current Reward:", fg="#ffffff", bg="#222121")
            old_word_label.pack(padx=10, pady=5)
            old_word_entry = tk.Entry(quick_edit_window)
            old_word_entry.pack(padx=10, pady=5)
            text_area = tk.Text(quick_edit_window, height=9, width=43, font=("Helvetica", 14), fg="#ffffff",
                                bg="#222121", insertbackground="white")
            text_area.pack(padx=10, pady=5)

            def comfirm_word_mean():
                try:
                    new_reward = old_word_entry.get().rstrip(',')
                    self.cursor.execute('UPDATE tasks SET reward = ? WHERE task = ?',
                                        (new_reward, 'original task name',))
                    self.conn.commit()
                    content = text_area.get("1.0", tk.END).strip()
                    conn = sqlite3.connect('setting.db')
                    cursor = conn.cursor()
                    cursor.execute('UPDATE setting SET history = ?',
                                   (content,))
                    conn.commit()
                    conn.close()
                    quick_edit_window.destroy()
                    return
                except:
                    return

            def exporting():
                try:
                    squick_edit_window = tk.Toplevel(self.root)
                    squick_edit_window.title("EDIT")
                    squick_edit_window.geometry("480x460")
                    squick_edit_window.configure(bg="#222121")
                    squick_edit_window.attributes('-topmost', True)
                    group_label = tk.Label(squick_edit_window, text="Export Data", fg="#ffffff", bg="#222121")
                    group_label.pack(padx=10, pady=5)
                    text_area = tk.Text(squick_edit_window, height=16, width=47, font=("Helvetica", 14),
                                        fg="#ffffff",
                                        bg="#222121", insertbackground="white")
                    text_area.pack(padx=10, pady=5)

                    def get():
                        # Fetch tasks from the database
                        self.cursor.execute(
                            'SELECT task, reward, topic, note FROM tasks WHERE task!=? ORDER BY topic',
                            ('original task name',))
                        tasks = self.cursor.fetchall()

                        # Format the tasks and insert them into text_area
                        formatted_text = ""
                        for task, reward, topic, note in tasks:
                            formatted_text += f"Task: {task}\nReward: {reward}\nTopic: {topic}\n<BREAK>\n"

                        return formatted_text

                    def save():
                        squick_edit_window.destroy()
                        return

                    formatted_text = get()
                    text_area.insert(tk.END, formatted_text)
                    ok_button = tk.Button(squick_edit_window, text="OK", command=save, font=("Helvetica", 14))
                    ok_button.pack(padx=3, pady=3)
                    return
                except:
                    return

            text_area.insert(tk.END, self.get_history())

            e_button = tk.Button(quick_edit_window, text="Export", command=exporting, font=("Helvetica", 14))
            e_button.pack(side=tk.RIGHT)

            ok_button = tk.Button(quick_edit_window, text="OK", command=comfirm_word_mean, font=("Helvetica", 14))
            ok_button.pack(side=tk.RIGHT, padx=52)

            return
        except:
            messagebox.showerror("Error", f" set !!!")
            return
    def upgrade_level(self,task_name , masks ):
        # Thêm vào lịch sử và cập nhật tiến trình
        conn = sqlite3.connect('setting.db')
        cursor = conn.cursor()

        # Lấy thông tin hiện tại từ bảng setting
        cursor.execute('SELECT times, history FROM setting')
        result = cursor.fetchone()

        if result:
            current_times, current_history = result
            print("cur_time:", current_times, "cur history:", current_history)
            # Cập nhật lịch sử và số lần hoàn thành
            new_history = current_history + '\n' + f"{task_name}"
            updated_times = current_times + masks
            cursor.execute('''
                                                UPDATE setting
                                                SET times = ?, history = ?
                                            ''', (updated_times, new_history))

            conn.commit()
            self.pro_label['text'] = f"Lv {int(updated_times // 1)}:"
            self.progress['value'] = (updated_times % 1) / 1
            self.root.update_idletasks()
        else:
            print("No data found in the setting table.")

        conn.close()

    def tasks_get_history(self):
        try:
            tasks_conn = sqlite3.connect('setting.db')
            tasks_cursor = tasks_conn.cursor()

            # Fetch current times and history
            tasks_cursor.execute('SELECT times, history FROM setting')
            result = tasks_cursor.fetchone()
            tasks_conn.close()
            if result:
                current_times, current_history = result
                return current_history
        except:
            messagebox.showerror("Error", f" get_history !!!")
            return
    def create_tabs(self):
        # Tab Todos
        self.todo_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.todo_frame, text="Todo")
        self.build_todo_tab()

        # Tab Tasks
        self.tasks_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tasks_frame, text="Tasks")
        self.build_tasks_tab()

        # Tab Goals
        self.goals_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.goals_frame, text="Goals")
        self.build_goals_tab()
        self.root.update_idletasks()
    def build_todo_tab(self):
        def on_drag_start(event):
            """Lưu chỉ số mục được kéo."""
            widget = event.widget
            self.drag_start_index = widget.nearest(event.y)

        def on_drag_motion(event):
            """Làm nổi bật mục đang được kéo."""
            widget = event.widget
            widget.selection_clear(0, tk.END)
            widget.selection_set(widget.nearest(event.y))

        def on_drag_drop(event):
            """Hoán đổi vị trí các mục khi thả chuột."""
            widget = event.widget
            drag_end_index = widget.nearest(event.y)
            if self.drag_start_index != drag_end_index:
                # Lấy dữ liệu từ mục
                item_start = widget.get(self.drag_start_index)
                item_end = widget.get(drag_end_index)
                # Hoán đổi vị trí
                widget.delete(self.drag_start_index)
                widget.insert(self.drag_start_index, item_end)
                widget.delete(drag_end_index)
                widget.insert(drag_end_index, item_start)

        def todo_start_timer():
            try:
                minutes = todo_minutes_entry.get()
                hours = todo_hour_entry.get()
                mins = todo_min_entry.get()
                if minutes.isdigit() and int(minutes) > 0:
                    total_seconds = int(minutes) * 60
                elif hours.isdigit() and mins.isdigit() and int(hours) >= 0 and int(mins) >= 0:
                    now = datetime.now()
                    target_time = now.replace(hour=int(hours), minute=int(mins), second=0, microsecond=0)
                    if target_time < now:
                        target_time += timedelta(days=1)
                    total_seconds = int((target_time - now).total_seconds())
                else:
                    messagebox.showwarning("Warning", "Vui lòng nhập thời gian hợp lệ!")
                    return
                if todo_after_id is not None:
                    self.root.after_cancel(todo_after_id)
                end_time = datetime.now() + timedelta(seconds=total_seconds)
                end_time_str = end_time.strftime('%I:%M %p')
                todo_end_time_label.config(text=f"End Time: {end_time_str}")
                total_minutes, seconds = divmod(total_seconds, 60)
                popup = tk.Toplevel(self.root)
                PopUpTimer(popup, total_minutes, seconds)
            except Exception:
                messagebox.showerror("Error", f"Counter TIMER decrease ")
                return

        def todo_create_table():
            try:
                # Tạo bảng tasks nếu nó chưa tồn tại
                todo_cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        period TEXT NOT NULL, -- Thời gian: sáng, trưa, tối
                        day TEXT NOT NULL, -- Thứ trong tuần: Monday, Tuesday...
                        checkok INTEGER DEFAULT 0
                    )
                ''')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create table: {str(e)}")

        def todo_edit_TKB():
            quick_TKB_window = tk.Toplevel(self.root)
            quick_TKB_window.title("Quản lý thời khóa biểu")
            quick_TKB_window.geometry("800x400")
            quick_TKB_window.configure(bg="#222121")  # , fg="#ffffff", bg="#222121"
            quick_TKB_window.attributes('-topmost', True)
            frame_top = tk.Frame(quick_TKB_window)
            frame_top.pack(pady=10)
            # Entry để nhập công việc
            entry_task = tk.Entry(frame_top, width=30)
            entry_task.grid(row=0, column=0, padx=5)
            # Combobox để chọn buổi
            combo_time = ttk.Combobox(frame_top, values=["Sáng", "Trưa", "Tối"], state="readonly", width=10)
            combo_time.grid(row=0, column=1, padx=5)
            combo_time.set("Sáng")  # Giá trị mặc định
            # Combobox để chọn ngày trong tuần
            combo_day = ttk.Combobox(frame_top,
                                     values=["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"],
                                     state="readonly", width=10)
            combo_day.grid(row=0, column=2, padx=5)
            combo_day.set("Thứ 2")  # Giá trị mặc định

            # Nút "Add"
            def add_task():
                task = entry_task.get()
                time = combo_time.get()
                day = combo_day.get()

                if task and time:
                    # Lưu vào database
                    conn = sqlite3.connect("tododay.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO tasks (task, period, day) VALUES (?, ?, ?)", (task, time, day))
                    conn.commit()
                    conn.close()

                    # Thêm vào Treeview
                    load_data()
                    entry_task.delete(0, tk.END)

            btn_add = tk.Button(frame_top, text="Add", command=add_task)
            btn_add.grid(row=0, column=3, padx=5)

            # Nút "Delete"
            def delete_task():
                selected_item = tree.selection()
                if selected_item:
                    conn = sqlite3.connect("tododay.db")
                    cursor = conn.cursor()

                    for item in selected_item:
                        task_id = tree.item(item)["values"][0]
                        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                        tree.delete(item)

                    conn.commit()
                    conn.close()

            btn_delete = tk.Button(frame_top, text="Delete", command=delete_task)
            btn_delete.grid(row=0, column=4, padx=5)
            # Tạo Treeview với 7 cột
            columns = ["ID", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
            tree = ttk.Treeview(quick_TKB_window, columns=columns, show="headings", height=15)
            tree.pack(fill=tk.BOTH, expand=True)
            # Đặt tiêu đề cột
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100 if col != "ID" else 50)

            # Chức năng load dữ liệu từ database vào Treeview
            def load_data():
                # Xóa các dòng hiện có trong Treeview
                for item in tree.get_children():
                    tree.delete(item)

                # Kết nối với database
                conn = sqlite3.connect("tododay.db")
                cursor = conn.cursor()

                # Tạo bảng nếu chưa tồn tại
                cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    task TEXT NOT NULL,
                                    period TEXT NOT NULL,
                                    day TEXT NOT NULL
                                )''')

                # Lấy dữ liệu từ database và sắp xếp theo ngày + period (Sáng -> Trưa -> Tối)
                cursor.execute('''
                    SELECT * FROM tasks
                    ORDER BY 
                        CASE period 
                            WHEN "Sáng" THEN 1
                            WHEN "Trưa" THEN 2
                            WHEN "Tối" THEN 3
                        END,
                        day
                ''')
                rows = cursor.fetchall()
                conn.close()

                # Chuyển đổi ngày từ tiếng Anh sang tiếng Việt
                day_map = {
                    "Monday": "Thứ 2",
                    "Tuesday": "Thứ 3",
                    "Wednesday": "Thứ 4",
                    "Thursday": "Thứ 5",
                    "Friday": "Thứ 6",
                    "Saturday": "Thứ 7",
                    "Sunday": "Chủ nhật",
                }

                # Duyệt qua từng dòng dữ liệu và chèn vào Treeview
                for row in rows:
                    task_id, task, period, day, checkok = row
                    display_day = day_map.get(day, day)

                    # Chèn vào Treeview
                    col_index = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"].index(
                        display_day) + 1
                    tree.insert("", "end",
                                values=(task_id,) + ("",) * (col_index - 1) + (f"{period}: {task}",) + ("",) * (
                                        7 - col_index))
                self.todo_load_tasks()

            # Tải dữ liệu khi khởi động
            load_data()

            try:
                return
            except:
                messagebox.showerror("Error", f" NOTE !!!")
                return

        def todo_done():
            # Lấy chỉ mục của mục được chọn trong Listbox
            selected_index = self.todo_listbox.curselection()
            if selected_index:
                # Lấy dòng được chọn
                task_name = self.todo_listbox.get(selected_index[0])
                if task_name.startswith("----------") or task_name == "(Không có công việc)" or task_name.startswith(
                        "[X]"):
                    return
                task_name = task_name[5:]
                # Cập nhật cột checkok = 1 trong cơ sở dữ liệu
                todo_conn = sqlite3.connect("tododay.db")
                todo_cursor = todo_conn.cursor()
                todo_cursor.execute('UPDATE tasks SET checkok = 1 WHERE task = ?', (task_name,))
                todo_conn.commit()
                todo_conn.close()

                # Tải lại dữ liệu Listbox
                self.todo_load_tasks()  # Tải lại tasks của Thứ hai
                self.upgrade_level(task_name, 0.16)

            try:

                return
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                return

        def next_day():
            # Tăng chỉ số của ngày hiện tại, quay về 0 nếu vượt quá 6
            self.cur_day_index = (self.cur_day_index + 1) % 7
            self.cur_day = self.weekdays[self.cur_day_index]
            self.todo_load_tasks()
            update_label()

        def back_day():
            # Giảm chỉ số của ngày hiện tại, quay về 6 nếu giảm xuống -1
            self.cur_day_index = (self.cur_day_index - 1) % 7
            self.cur_day = self.weekdays[self.cur_day_index]
            self.todo_load_tasks()
            update_label()

        def get_period():
            # Xác định buổi sáng, trưa, tối dựa trên giờ hiện tại
            now_hour = datetime.now().hour
            if 0 <= now_hour < 12:
                return "Morning"
            elif 12 <= now_hour < 18:
                return "Afternoon"
            else:
                return "Evening"

        def update_label():
            # Cập nhật nội dung của todo_label
            todo_label.config(text=f"{self.cur_day.upper()} {self.cur_period}")

        todo_after_id = None
        todo_conn = sqlite3.connect('tododay.db')
        todo_cursor = todo_conn.cursor()
        todo_create_table()
        # Lấy ngày hiện tại và thứ trong tuần
        today = datetime.now()
        self.weekdays = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        self.cur_day_index = today.weekday()  # Lấy chỉ số của ngày hiện tại
        self.cur_day = self.weekdays[self.cur_day_index]  # Gán ngày hiện tại
        todo_label = ttk.Label(self.todo_frame, text="Danh sách Công Việc hôm nay", font=("Arial", 16),
                               background="#222121", foreground="#FF0000")
        todo_label.pack()
        todo_buttons_frame = tk.Frame(self.todo_frame, bg="#222121")
        todo_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        todo_add_button = tk.Button(todo_buttons_frame, text="TKB Edit", command=todo_edit_TKB, width=12, bg="#333333",
                                    fg="#ffffff")
        todo_add_button.pack(side=tk.LEFT, padx=10)
        todo_edit_button = tk.Button(todo_buttons_frame, text="<", command=back_day, width=12, bg="#333333",
                                     fg="#ffffff")
        todo_edit_button.pack(side=tk.LEFT, padx=10)
        todo_delete_button = tk.Button(todo_buttons_frame, text=">", command=next_day, width=12,
                                       bg="#333333", fg="#ffffff")
        todo_delete_button.pack(side=tk.LEFT, padx=10)
        todo_Done_button = tk.Button(todo_buttons_frame, text="Done", command=todo_done, width=12, bg="#333333",
                                     fg="#ffffff")
        todo_Done_button.pack(side=tk.LEFT, padx=10)
        todo_list_frame = tk.Frame(self.todo_frame, bg="#222121")
        todo_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Tạo Listbox
        todo_label = ttk.Label(todo_list_frame, text="MONDAY Morning", font=("Arial", 16),
                               background="#222121", foreground="#FF0000")
        todo_label.pack()
        self.todo_listbox = tk.Listbox(
            todo_list_frame, font=("Helvetica", 21), bg="#444444", fg="#ffffff",
            selectbackground="#222121", selectforeground="#ffffff"
        )
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Scrollbar
        scrollbar = ttk.Scrollbar(todo_list_frame, orient=tk.VERTICAL, command=self.todo_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.todo_listbox.config(yscrollcommand=scrollbar.set)
        # Gắn sự kiện kéo thả cho Listbox
        self.todo_listbox.bind("<Button-1>", on_drag_start)
        self.todo_listbox.bind("<B1-Motion>", on_drag_motion)
        self.todo_listbox.bind("<ButtonRelease-1>", on_drag_drop)
        todo_timer_frame = tk.Frame(self.todo_frame, bg="#222121")
        todo_timer_frame.pack(fill=tk.X, padx=10, pady=10)
        todo_min_label = tk.Label(todo_timer_frame, text="Min:", font=("Helvetica", 12), bg="#222121", fg="#ffffff")
        todo_min_label.pack(side=tk.LEFT, padx=5)
        todo_minutes_entry = tk.Entry(todo_timer_frame, width=5, font=("Helvetica", 12), bg="#444444", fg="#ffffff")
        todo_minutes_entry.pack(side=tk.LEFT, padx=5)
        todo_ok_button = tk.Button(todo_timer_frame, text="Ok", command=todo_start_timer, width=5, bg="#333333",
                                   fg="#ffffff")
        todo_ok_button.pack(side=tk.LEFT, padx=5)
        todo_hour_entry = tk.Entry(todo_timer_frame, width=5, font=("Helvetica", 12), bg="#444444", fg="#ffffff")
        todo_hour_entry.pack(side=tk.LEFT, padx=5)
        todo_min_entry = tk.Entry(todo_timer_frame, width=5, font=("Helvetica", 12), bg="#444444", fg="#ffffff")
        todo_min_entry.pack(side=tk.LEFT, padx=5)
        todo_end_time_label = tk.Label(todo_timer_frame, font=("Helvetica", 14), bg="#222121", fg="#FF0000")
        todo_end_time_label.pack(side=tk.LEFT, padx=10)
        self.todo_load_tasks()
        self.cur_period = get_period()
        update_label()
    def todo_load_tasks(self):
        # Xóa nội dung cũ trong Listbox
        self.todo_listbox.delete(0, tk.END)

        # Mở kết nối với cơ sở dữ liệu
        todo_conn = sqlite3.connect("tododay.db")
        todo_cursor = todo_conn.cursor()

        # Lấy các task theo ngày và sắp xếp theo buổi
        todo_cursor.execute('''
            SELECT task, period, checkok FROM tasks
            WHERE day = ?
            ORDER BY 
                CASE period 
                    WHEN "Sáng" THEN 1
                    WHEN "Trưa" THEN 2
                    WHEN "Tối" THEN 3
                END
        ''', (self.cur_day,))
        tasks = todo_cursor.fetchall()

        # Đóng kết nối sau khi lấy dữ liệu
        todo_conn.close()

        # Thời gian mô tả
        timee = ["Sáng (7.AM -> 12.AM)", "Trưa (12.AM -> 6.PM)", "Tối (6.PM -> 6.AM)"]
        periods = ["Sáng", "Trưa", "Tối"]

        # Thêm task vào Listbox
        for period, time_desc in zip(periods, timee):
            # Thêm header buổi
            self.todo_listbox.insert(tk.END, f"------------{time_desc}-------------")
            self.todo_listbox.itemconfig(tk.END, {'bg': '#FFFF34', 'fg': '#000000'})

            # Lọc các task theo buổi
            period_tasks = [(task, checkok) for task, task_period, checkok in tasks if task_period == period]

            # Thêm task vào Listbox
            if period_tasks:
                for task, checkok in period_tasks:
                    if checkok == 0:
                        self.todo_listbox.insert(tk.END, f"     {task}")
                    else:
                        self.todo_listbox.insert(tk.END, f"[X] {task}")
            else:
                # Nếu không có task nào, thêm dòng thông báo
                self.todo_listbox.insert(tk.END, "(Không có công việc)")

        # Cập nhật lại Listbox nếu cần
        self.todo_listbox.yview_moveto(1)  # Cuộn xuống cuối cùng (tuỳ chọn)
    def build_tasks_tab(self): # self.tasks_frame

        def tasks_update_progress(current_value, target_value):
            try:
                """Cập nhật giá trị cho ProgressBar dựa trên giá trị hiện tại và mục tiêu"""
                percentage = (current_value / target_value) * 100  # Tính phần trăm tiến trình
                self.progress['value'] = percentage  # Cập nhật giá trị thanh tiến trình
                self.root.update_idletasks()  # Cập nhật giao diện ngay lập tức
            except:
                messagebox.showerror("Error", f" update_progress !!!")
                return
        def tasks_done():
            try:
                selected_item = self.tasks_tree.selection()
                if selected_item:
                    task_name = self.tasks_tree.item(selected_item, 'values')[0]
                    if task_name.startswith("[X]"):
                        task_name = task_name[3:]
                    elif task_name == "----------------TOPIC----------------":
                        return
                    reward = self.tasks_tree.item(selected_item, 'values')[1]
                    tasks_cursor.execute('DELETE FROM tasks WHERE task = ?', (task_name,))
                    tasks_conn.commit()
                    self.tasks_load_tasks()
                    self.upgrade_level(task_name, 0.25)
                return
            except:
                messagebox.showerror("Error", f" done !!!")
                return
        def tasks_get_random_motivational_quote():
            try:
                connn = sqlite3.connect('Database/sentences.db')
                cursorn = connn.cursor()
                cursorn.execute('SELECT sentence FROM sentences')
                quotes = cursorn.fetchall()

                if quotes:
                    # Chọn ngẫu nhiên một câu nói từ database
                    random_quote = random.choice(quotes)
                    return random_quote[0]  # Trả về chỉ câu nói (sentence)
                else:
                    return " 😭🦾😫😥😢😨😢😫🦾"
            except:
                messagebox.showerror("Error", f" get sentences !!!")
                return
        def tasks_clear_selection():
            # Bỏ chọn tất cả các mục trong Treeview
            self.tasks_tree.selection_remove(self.tasks_tree.selection())
        def tasks_get_reward():
            try:
                tasks_cursor.execute('SELECT reward FROM tasks WHERE task = ?', ('original task name',))
                reward = tasks_cursor.fetchall()[0][0]
                if reward:
                    return reward
                else:
                    return ''
            except:
                messagebox.showerror("Error", f" get_reward !!!")
                return
        def tasks_open_note():
            selected_item = self.tasks_tree.selection()
            if selected_item:
                task_name = self.tasks_tree.item(selected_item, 'values')[0]
                if task_name.startswith("[X]"):
                    task_name = task_name[3:]
                elif task_name == "----------------TOPIC----------------":
                    return
                tasks_cursor.execute('SELECT note FROM tasks WHERE task = ?', (task_name,))
                notes = tasks_cursor.fetchall()[0]
                quick_note_window = tk.Toplevel(self.root)
                quick_note_window.title("Note")
                quick_note_window.geometry("400x250")
                quick_note_window.configure(bg="#222121")  # , fg="#ffffff", bg="#222121"
                quick_note_window.attributes('-topmost', True)
                text_area = tk.Text(quick_note_window, height=8, width=43, font=("Helvetica", 14), fg="#ffffff",
                                    bg="#222121", insertbackground="white")
                text_area.pack(padx=10, pady=5)
                def save():
                    content = text_area.get("1.0", tk.END).strip()
                    tasks_cursor.execute('UPDATE tasks SET note = ? WHERE task = ?', (content, task_name,))
                    tasks_conn.commit()
                    quick_note_window.destroy()
                    return
                text_area.insert(tk.END, notes)
                ok_button = tk.Button(quick_note_window, text="Save", command=save, font=("Helvetica", 10))
                ok_button.pack(padx=10, pady=5)
            else:
                tasks_cursor.execute('SELECT note FROM tasks WHERE task = ?', ('original task name',))
                notes = tasks_cursor.fetchall()[0]
                quick_note_window = tk.Toplevel(self.root)
                quick_note_window.title("Note")
                quick_note_window.geometry("400x250")
                quick_note_window.configure(bg="#222121")  # , fg="#ffffff", bg="#222121"
                quick_note_window.attributes('-topmost', True)
                text_area = tk.Text(quick_note_window, height=8, width=43, font=("Helvetica", 14), fg="#ffffff",
                                    bg="#222121", insertbackground="white")
                text_area.pack(padx=10, pady=5)
                def save():
                    content = text_area.get("1.0", tk.END).strip()
                    tasks_cursor.execute('UPDATE tasks SET note = ? WHERE task = ?',
                                   (content, 'original task name',))
                    tasks_conn.commit()
                    quick_note_window.destroy()
                    return
                text_area.insert(tk.END, notes)
                ok_button = tk.Button(quick_note_window, text="Save", command=save, font=("Helvetica", 10))
                ok_button.pack(padx=10, pady=5)
            tasks_clear_selection()
            try:
                return
            except:
                messagebox.showerror("Error", f" NOTE !!!")
                return
        def tasks_edit():
            try:
                selected_item = self.tasks_tree.selection()
                if selected_item:
                    task_name = self.tasks_tree.item(selected_item, 'values')[0]
                    if task_name.startswith("[X]"):
                        task_name = task_name[3:]
                    elif task_name == "----------------TOPIC----------------":
                        old_topic = self.tasks_tree.item(selected_item, 'values')[1]
                        quick_edit_window = tk.Toplevel(self.root)
                        quick_edit_window.title("EDIT")
                        quick_edit_window.geometry("300x150")
                        quick_edit_window.configure(bg="#222121")
                        quick_edit_window.attributes('-topmost', True)
                        old_word_label = tk.Label(quick_edit_window, text="Old task:", fg="#ffffff", bg="#222121")
                        old_word_label.pack(padx=10, pady=5)
                        old_word_entry = tk.Entry(quick_edit_window)
                        old_word_entry.pack(padx=10, pady=5)
                        old_word_entry.insert(0, old_topic)

                        def comfirm_word_mean():
                            new_topic = old_word_entry.get().strip()  # Nhận topic cũ từ input
                            if old_topic != new_topic:
                                # Cập nhật tất cả các bản ghi có topic là old_topic thành topic mới
                                tasks_cursor.execute('UPDATE tasks SET topic = ? WHERE topic = ?',
                                                    (new_topic, old_topic))
                                tasks_conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
                                self.tasks_load_tasks()  # Tải lại các task sau khi cập nhật
                            quick_edit_window.destroy()  # Đóng cửa sổ chỉnh sửa nhanh

                        ok_button = tk.Button(quick_edit_window, text="OK", command=comfirm_word_mean,
                                              font=("Helvetica", 14))
                        ok_button.pack(padx=10, pady=5)
                        return
                    reward = self.tasks_tree.item(selected_item, 'values')[1]
                    quick_edit_window = tk.Toplevel(self.root)
                    quick_edit_window.title("EDIT")
                    quick_edit_window.geometry("300x150")
                    quick_edit_window.configure(bg="#222121")
                    quick_edit_window.attributes('-topmost', True)
                    old_word_label = tk.Label(quick_edit_window, text="Old task:", fg="#ffffff", bg="#222121")
                    old_word_label.pack(padx=10, pady=5)
                    old_word_entry = tk.Entry(quick_edit_window)
                    old_word_entry.pack(padx=10, pady=5)
                    old_mean_label = tk.Label(quick_edit_window, text="Old reward:", fg="#ffffff", bg="#222121")
                    old_mean_label.pack(padx=10, pady=5)
                    old_mean_entry = tk.Entry(quick_edit_window)
                    old_mean_entry.pack(padx=10, pady=5)
                    old_word_entry.insert(0, task_name)
                    old_mean_entry.insert(0, reward)

                    def comfirm_word_mean():
                        new_word = old_word_entry.get()
                        new_mean = old_mean_entry.get()
                        tasks_cursor.execute('UPDATE tasks SET task = ?, reward = ? WHERE task = ?',
                                            (new_word, new_mean, task_name))
                        tasks_conn.commit()
                        self.tasks_load_tasks()
                        quick_edit_window.destroy()

                    ok_button = tk.Button(quick_edit_window, text="OK", command=comfirm_word_mean,
                                          font=("Helvetica", 14))
                    ok_button.pack(padx=10, pady=5)
                tasks_clear_selection()
                return
            except:
                messagebox.showerror("Error", f" EDIT !!!")
                return
        def tasks_print_todo():
            try:
                tasks_cursor.execute('SELECT task, reward, topic FROM tasks WHERE main = 1')
                task = tasks_cursor.fetchall()
                if task:
                    main_task = task[0][0]
                    reward = task[0][1]
                    topic = task[0][2]
                    notification.notify(
                        title=f"{main_task} - {reward} \n------- {topic} -------",
                        message=tasks_get_random_motivational_quote(),
                        timeout=3,
                    )
                    # Lặp lại hàm này sau 7 phút (7*60*1000 milliseconds = 420000 ms)
                self.root.after(420000, tasks_print_todo)
            except:
                messagebox.showerror("Error", f" NOTIFY Main task !!!")
                return
        def tasks_create_table():
            # Tạo bảng task nếu nó chưa tồn tại
            tasks_cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS tasks (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        task TEXT NOT NULL,
                                        main INTEGER DEFAULT 0,
                                        note TEXT DEFAULT '',
                                        reward TEXT DEFAULT '',
                                        topic TEXT DEFAULT 'none'
                                    )
                                ''')
            tasks_cursor.execute('SELECT COUNT(*) FROM tasks')
            task_count = tasks_cursor.fetchone()[0]

            if task_count == 0:
                # Thêm task với giá trị mặc định
                tasks_cursor.execute('''
                                INSERT INTO tasks (task, main, note, reward)
                                VALUES (?, ?, ?, ?)
                            ''', ('original task name', 0, '', ''))
            tasks_conn.commit()
            try:
                return
            except:
                messagebox.showerror("Error", f" create table db !!!")
                return
        def tasks_add_task():
            task = tasks_entry.get()
            topic = self.tasks_combobox.get()
            if task:
                reward = random.choice(tasks_get_reward().split(','))
                print("task:", task, "reward:", reward, "topic:", topic)
                tasks_cursor.execute('INSERT INTO tasks (task, reward, topic) VALUES (?, ?, ?)',
                               (task, reward, topic))
                tasks_conn.commit()
                self.tasks_tree.insert("", "end", values=(task, reward))
                tasks_entry.delete(0, tk.END)
                self.tasks_combobox.set("none")
                self.tasks_load_tasks()
            tasks_clear_selection()

            try:
                return
            except:
                messagebox.showerror("Error", f"ADD TASK !!!")
                return
        def tasks_add_task_event(event):
            tasks_add_task()
        def tasks_open_task():
            try:
                cup = tk.Toplevel(self.root)
                CountTimer(cup)
            except:
                messagebox.showerror("Error", f"OPEN init timer !!!")
                return
        def tasks_choose_main():
            try:
                selected_item = self.tasks_tree.selection()
                if selected_item:
                    task_name = self.tasks_tree.item(selected_item, 'values')[0]
                    tasks_cursor.execute('UPDATE tasks SET main = 0')
                    tasks_cursor.execute('UPDATE tasks SET main = 1 WHERE task = ?', (task_name,))
                    tasks_conn.commit()
                    self.tasks_load_tasks()
                    self.goals_load_tasks()
                return
            except:
                messagebox.showerror("Error", f" Main Task !!!")
                return
        def tasks_delete_task():
            try:
                # self.get_selected_task()
                selected_item = self.tasks_tree.selection()
                if selected_item:
                    for item in selected_item:
                        task_name = self.tasks_tree.item(item, 'values')[0]
                        if task_name.startswith("[X]"):
                            task_name = task_name[3:]
                        elif task_name == "----------------TOPIC----------------":
                            return
                        tasks_cursor.execute('DELETE FROM tasks WHERE task = ?', (task_name,))
                        tasks_conn.commit()
                        self.tasks_tree.delete(item)
                    self.tasks_load_tasks()
            except:
                messagebox.showerror("Error", f" Delete !!!")
                return
        def ___del__():
            # Đóng kết nối cơ sở dữ liệu khi ứng dụng kết thúc
            tasks_conn.close()

        tasks_after_id = None
        tasks_conn = sqlite3.connect('todolist.db')
        tasks_cursor = tasks_conn.cursor()
        tasks_create_table()
        tasks_label = ttk.Label(self.tasks_frame, text="Danh sách Nhiệm Vụ hôm nay", font=("Arial", 16), background="#222121", foreground="#CCCC00")
        tasks_label.pack()
        tasks_entry_frame = tk.Frame(self.tasks_frame, bg="#222121")
        tasks_entry_frame.pack(fill=tk.X, padx=10, pady=2)
        tasks_entry = tk.Entry(tasks_entry_frame, width=16, font=("Helvetica", 16, 'bold'), bg="#444444",
                              fg="#ffffff",
                              insertbackground="#ffffff")
        tasks_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.tasks_combobox = ttk.Combobox(tasks_entry_frame, width=10, font=("Helvetica", 16, 'bold'), state="readonly")
        self.tasks_combobox.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
        self.tasks_combobox.set("none")
        tasks_entry.bind('<Return>', tasks_add_task_event)

        tasks_style = ttk.Style()
        tasks_style.theme_use("clam")
        tasks_style.configure("Treeview",background="#444444",foreground="#ffffff",fieldbackground="#444444",bordercolor="#222121", )
        tasks_style.configure("Treeview.Heading",background="#333333",foreground="#ffffff",relief="flat")
        tasks_style.map('mystyle.Treeview',background=[('selected', '#222121')],foreground=[('selected', '#ffffff')])
        tasks_tree_frame = tk.Frame(self.tasks_frame, bg="#222121")
        tasks_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tasks_tree = ttk.Treeview(tasks_tree_frame, columns=("Task", "Reward"), show="headings", height=8,style="mystyle.Treeview")
        self.tasks_tree.heading("Task", text="Task Name")
        self.tasks_tree.heading("Reward", text="Reward")
        self.tasks_tree.column("Task", width=160, anchor='center')
        self.tasks_tree.column("Reward", width=70, anchor='center')
        scrollbar = ttk.Scrollbar(tasks_tree_frame, orient=tk.VERTICAL, command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        self.tasks_load_tasks()

        tasks_buttons_frame = tk.Frame(self.tasks_frame, bg="#222121")
        tasks_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        tasks_add_button = tk.Button(tasks_buttons_frame, text="Add", command=tasks_add_task, width=8, bg="#333333",
                                     fg="#ffffff")
        tasks_add_button.pack(side=tk.LEFT, padx=7)
        tasks_open_button = tk.Button(tasks_buttons_frame, text="Note", command=tasks_open_note, width=8, bg="#333333",
                                      fg="#ffffff")
        tasks_open_button.pack(side=tk.LEFT, padx=7)
        tasks_Done_button = tk.Button(tasks_buttons_frame, text="Done", command=tasks_done, width=8, bg="#333333",
                                      fg="#ffffff")
        tasks_Done_button.pack(side=tk.RIGHT, padx=7)
        tasks_edit_button = tk.Button(tasks_buttons_frame, text="Edit", command=tasks_edit, width=8, bg="#333333",
                                      fg="#ffffff")
        tasks_edit_button.pack(side=tk.RIGHT, padx=7)
        tasks_main_button = tk.Button(tasks_buttons_frame, text="Main", command=tasks_choose_main, width=8,
                                      bg="#333333", fg="#ffffff")
        tasks_main_button.pack(side=tk.RIGHT, padx=7)
        tasks_delete_button = tk.Button(tasks_buttons_frame, text="Delete", command=tasks_delete_task, width=8,
                                        bg="#333333", fg="#ffffff")
        tasks_delete_button.pack(side=tk.RIGHT, padx=7)

        #tasks_open_task()  # mở đếm tăng dần
        #tasks_print_todo()  # bắt đầu hiện thông báo
    def tasks_load_tasks(self):
        try:
            # Xóa tất cả các dòng hiện có trong Treeview
            for item in self.tasks_tree.get_children():
                self.tasks_tree.delete(item)
            self.topic = []
            # Load tasks từ cơ sở dữ liệu và hiển thị trong Listbox
            tasks_conn = sqlite3.connect('todolist.db')
            tasks_cursor = tasks_conn.cursor()
            tasks_cursor.execute('SELECT main, task, reward, topic FROM tasks WHERE task!=? ORDER  BY topic',
                                 ('original task name',))
            tasks = tasks_cursor.fetchall()

            cur_topic = 'nonádasdasde'
            # Đăng ký thẻ với màu nền vàng
            self.tasks_tree.tag_configure('black', background='black')
            for main, task, reward, topic in tasks:

                if topic != cur_topic:
                    self.topic.append(topic)
                    self.tasks_tree.insert("", "end", values=("----------------TOPIC----------------", topic),
                                      tags=('black',))
                    cur_topic = topic
                if task == "example_task":
                    continue
                if not main:
                    self.tasks_tree.insert("", "end", values=(f"{task}", reward))
                else:
                    self.tasks_tree.insert("", "end", values=(f"[X]{task}", reward))

            self.tasks_combobox['values'] = self.topic
            tasks_conn.close()
            return
        except Exception:
            messagebox.showerror("Error", f"Counter TIMER decrease ")
            return
    def goals_load_tasks(self):
        try:
            goals_conn = sqlite3.connect('todolist.db')
            goals_cursor = goals_conn.cursor()
            # Xóa tất cả các mục hiện có trong Listbox
            self.goals_listbox.delete(0, tk.END)

            #                 # Load tasks từ cơ sở dữ liệu và hiển thị trong Listbox
            goals_cursor.execute(
                '''
                SELECT main, topic 
                FROM tasks 
                GROUP BY topic 
                ORDER BY main DESC, topic ASC
                '''
            )
            goals = goals_cursor.fetchall()

            # Cập nhật Listbox với dữ liệu mới
            for main, goal in goals:
                self.goals_listbox.insert(tk.END, f"{goal}")
            goals_conn.close()
        except Exception as e:
            # Hiển thị thông báo lỗi nếu có
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
    def build_goals_tab(self):
        def goals_add_task():
            goals = goals_entry.get().strip()
            if task:
                goals_cursor.execute('INSERT INTO tasks (task, reward, topic) VALUES (?, ?, ?)',
                                     ('example_task', 'example_reward', goals))
                goals_conn.commit()
                goals_entry.delete(0, tk.END)
                self.goals_load_tasks()
                self.tasks_load_tasks()
            goals_clear_selection()
            try:
                return
            except:
                messagebox.showerror("Error", f"ADD TASK !!!")
                return

        def goals_edit():
            try:
                selected_item = self.goals_listbox.curselection()
                if selected_item:
                    task_name = self.goals_listbox.get(selected_item[0])
                    quick_edit_window = tk.Toplevel(self.root)
                    quick_edit_window.title("EDIT")
                    quick_edit_window.geometry("300x150")
                    quick_edit_window.configure(bg="#222121")
                    quick_edit_window.attributes('-topmost', True)
                    old_word_label = tk.Label(quick_edit_window, text="Old task:", fg="#ffffff", bg="#222121")
                    old_word_label.pack(padx=10, pady=5)
                    old_word_entry = tk.Entry(quick_edit_window)
                    old_word_entry.pack(padx=10, pady=5)
                    old_word_entry.insert(0, task_name)

                    def comfirm_word_mean():
                        new_word = old_word_entry.get()
                        goals_cursor.execute('UPDATE tasks SET topic=? WHERE topic = ?',
                                             (new_word, task_name))
                        goals_conn.commit()
                        self.goals_load_tasks()
                        quick_edit_window.destroy()

                    ok_button = tk.Button(quick_edit_window, text="OK", command=comfirm_word_mean,
                                          font=("Helvetica", 14))
                    ok_button.pack(padx=10, pady=5)
                goals_clear_selection()
                return
            except:
                messagebox.showerror("Error", f" EDIT !!!")
                return

        def goals_clear_selection():
            # Bỏ chọn tất cả các mục trong Listbox
            self.goals_listbox.selection_clear(0, tk.END)

        def on_drag_start(event):
            """Lưu chỉ số mục được kéo."""
            widget = event.widget
            self.drag_start_index = widget.nearest(event.y)

        def on_drag_motion(event):
            """Làm nổi bật mục đang được kéo."""
            widget = event.widget
            widget.selection_clear(0, tk.END)
            widget.selection_set(widget.nearest(event.y))

        def on_drag_drop(event):
            """Hoán đổi vị trí các mục khi thả chuột."""
            widget = event.widget
            drag_end_index = widget.nearest(event.y)
            if self.drag_start_index != drag_end_index:
                # Lấy dữ liệu từ mục
                item_start = widget.get(self.drag_start_index)
                item_end = widget.get(drag_end_index)
                # Hoán đổi vị trí
                widget.delete(self.drag_start_index)
                widget.insert(self.drag_start_index, item_end)
                widget.delete(drag_end_index)
                widget.insert(drag_end_index, item_start)

        def goals_done():
            try:
                # Lấy mục đã chọn trong Listbox
                selected_index = self.goals_listbox.curselection()
                if selected_index:
                    task_name = self.goals_listbox.get(selected_index[0])
                    goals_cursor.execute('DELETE FROM tasks WHERE topic = ?', (task_name,))
                    goals_conn.commit()
                    self.goals_load_tasks()
                    self.tasks_load_tasks()
                    self.upgrade_level(task_name, 0.7)
                else:
                    messagebox.showinfo("Info", "No task selected.")
                return
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                return

        def goals_delete():
            try:
                selected_index = self.goals_listbox.curselection()
                if selected_index:
                    task_name = self.goals_listbox.get(selected_index[0])
                    goals_cursor.execute('DELETE FROM tasks WHERE topic = ?', (task_name,))
                    goals_conn.commit()
                    self.goals_load_tasks()
                    self.tasks_load_tasks()
            except:
                messagebox.showerror("Error", f" Delete !!!")
                return

        def goals_open_note():
            selected_item = self.goals_listbox.curselection()
            if selected_item:
                task_name = self.goals_listbox.get(selected_item[0])
                goals_cursor.execute('SELECT note FROM tasks WHERE topic = ?', (task_name,))
                notes = goals_cursor.fetchall()[0]
                quick_note_window = tk.Toplevel(self.root)
                quick_note_window.title("Note")
                quick_note_window.geometry("400x250")
                quick_note_window.configure(bg="#222121")  # , fg="#ffffff", bg="#222121"
                quick_note_window.attributes('-topmost', True)
                text_area = tk.Text(quick_note_window, height=8, width=43, font=("Helvetica", 14), fg="#ffffff",
                                    bg="#222121", insertbackground="white")
                text_area.pack(padx=10, pady=5)

                def save():
                    content = text_area.get("1.0", tk.END).strip()
                    goals_cursor.execute('UPDATE tasks SET note = ? WHERE topic = ?', (content, task_name,))
                    goals_conn.commit()
                    quick_note_window.destroy()
                    return

                text_area.insert(tk.END, notes)
                ok_button = tk.Button(quick_note_window, text="Save", command=save, font=("Helvetica", 10))
                ok_button.pack(padx=10, pady=5)
            goals_clear_selection()
            try:
                return
            except:
                messagebox.showerror("Error", f" NOTE !!!")
                return

        goals_conn = sqlite3.connect('todolist.db')
        goals_cursor = goals_conn.cursor()
        goals_label = ttk.Label(self.goals_frame, text="Danh sách Mục Tiêu hôm nay", font=("Arial", 16),
                                background="#222121", foreground="#0000FF")
        goals_label.pack()
        goals_list_frame = tk.Frame(self.goals_frame, bg="#222121")
        goals_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Tạo Listbox
        self.goals_listbox = tk.Listbox(
            goals_list_frame, font=("Helvetica", 21), bg="#444444", fg="#ffffff",
            selectbackground="#222121", selectforeground="#ffffff"
        )
        self.goals_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Scrollbar
        scrollbar = ttk.Scrollbar(goals_list_frame, orient=tk.VERTICAL, command=self.goals_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.goals_listbox.config(yscrollcommand=scrollbar.set)
        # Gắn sự kiện kéo thả cho Listbox
        self.goals_listbox.bind("<Button-1>", on_drag_start)
        self.goals_listbox.bind("<B1-Motion>", on_drag_motion)
        self.goals_listbox.bind("<ButtonRelease-1>", on_drag_drop)
        # Thêm dữ liệu mẫu vào Listbox
        tasks = [("Goal 1"), ("Goal 2"), ("Goal 3")]
        for task in tasks:
            self.goals_listbox.insert(tk.END, f"{task}")

        goals_entry_frame = tk.Frame(self.goals_frame, bg="#222121")
        goals_entry_frame.pack(fill=tk.X, padx=10, pady=2)
        goals_entry = tk.Entry(goals_entry_frame, width=16, font=("Helvetica", 16, 'bold'), bg="#444444",
                               fg="#ffffff", insertbackground="#ffffff")
        goals_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        goals_add_button = tk.Button(goals_entry_frame, text="Add", command=goals_add_task, width=4, bg="#333333",
                                     fg="#ffffff")
        goals_add_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=7)
        goals_buttons_frame = tk.Frame(self.goals_frame, bg="#222121")
        goals_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        goals_open_button = tk.Button(goals_buttons_frame, text="Note", command=goals_open_note, width=12, bg="#333333",
                                      fg="#ffffff")
        goals_open_button.pack(side=tk.LEFT, padx=10)
        goals_done_button = tk.Button(goals_buttons_frame, text="Done", command=goals_done, width=12, bg="#333333",
                                      fg="#ffffff")
        goals_done_button.pack(side=tk.LEFT, padx=10)
        goals_edit_button = tk.Button(goals_buttons_frame, text="Edit", command=goals_edit, width=12, bg="#333333",
                                      fg="#ffffff")
        goals_edit_button.pack(side=tk.LEFT, padx=10)
        goals_delete_button = tk.Button(goals_buttons_frame, text="Delete", command=goals_delete, width=12,
                                        bg="#333333", fg="#ffffff")
        goals_delete_button.pack(side=tk.LEFT, padx=10)
        self.goals_load_tasks()


##OK Popup Counter decrease
class PopUpTimer:
    def __init__(self, root, minutes, seconds):
        print("PopUpTimer")
        self.root = root
        self.minutes = minutes
        self.seconds = seconds

        self.root.title("")
        self.root.overrideredirect(1)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#222121")
        screen_width = self.root.winfo_screenwidth()
        window_width = 300  # Thay đổi giá trị này thành chiều rộng thực tế của cửa sổ của bạn
        x_position = (screen_width // 2) - (window_width // 2)

        # Đặt cửa sổ ở trên cùng và giữa
        self.root.geometry(f"+{x_position + 160}+0")

        # Cho phép di chuyển cửa sổ
        self.root.bind("<B1-Motion>", self.move_window)

        # Nhãn hiển thị thời gian đếm ngược
        self.label = tk.Label(self.root, text=f"{self.minutes:02d}:{self.seconds:02d}", font=("Helvetica", 20),
                              bg="#222121", fg="#FF0000")
        self.label.pack()
        self.close_button = tk.Button(self.root, text="X", command=self.root.destroy, bg="#444444", fg="#ffffff", bd=0)
        self.close_button.pack(side=tk.TOP)
        # Nút để đóng cửa sổ

        # Đặt cửa sổ trong suốt và trên cùng
        self.root.attributes('-transparentcolor', '#222121')
        self.root.attributes('-alpha', 0.7)

        # Bắt đầu đếm ngược
        self.update_timer()

    def update_timer(self):
        if self.minutes > 0 or self.seconds > 0:
            if self.seconds == 0:
                self.minutes -= 1
                self.seconds = 59
            else:
                self.seconds -= 1

            self.label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")

            # Cập nhật mỗi giây
            self.root.after(1000, self.update_timer)
        else:
            self.timer_finished()
            notification.notify(
                title="Time's Up!",
                message="Đă Hết Thời gian Đếm ngược !!!!!!!",
                timeout=7,
            )

    def timer_finished(self):
        self.label.config(text="Time's up!")
        self.root.attributes('-alpha', 1.0)  # Làm cửa sổ hoàn toàn hiện diện khi hết thời gian

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

#Open Popup Counter increase
class CountTimer:
    def __init__(self, root):
        print("CountTimer")
        self.root = root
        self.minutes = 0
        self.seconds = 0

        self.root.title("")
        self.root.overrideredirect(1)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#222121")
        screen_width = self.root.winfo_screenwidth()
        window_width = 300  # Thay đổi giá trị này thành chiều rộng thực tế của cửa sổ của bạn
        x_position = (screen_width // 2) - (window_width // 2)

        # Đặt cửa sổ ở trên cùng và giữa
        self.root.geometry(f"+{x_position}+0")

        # Cho phép di chuyển cửa sổ
        self.root.bind("<B1-Motion>", self.move_window)

        # Nhãn hiển thị thời gian
        self.label = tk.Label(self.root, text=f"{self.minutes:02d}:{self.seconds:02d}", font=("Helvetica", 20),
                              bg="#222121", fg="#FFFF33")
        self.label.pack()

        # Nút đóng cửa sổ
        self.close_button = tk.Button(self.root, text="X", command=self.root.destroy, bg="#444444", fg="#ffffff", bd=0)
        self.close_button.pack(side=tk.TOP)

        # Đặt cửa sổ trong suốt và trên cùng
        self.root.attributes('-transparentcolor', '#222121')
        self.root.attributes('-alpha', 0.7)

        # Bắt đầu đếm thời gian
        self.update_timer()

    def update_timer(self):
        # Tăng thời gian
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0

        # Cập nhật nhãn
        self.label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")

        # Cập nhật mỗi giây
        self.root.after(1000, self.update_timer)

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkWise(root)
    root.mainloop()
