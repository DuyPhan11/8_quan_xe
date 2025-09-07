import tkinter as tk
from tkinter import messagebox
from collections import deque

SBOARD = 8

#Vẽ bàn cờ 2 màu
def draw(btn, r, c):
    if (r+c) %2 == 0:
        btn.config(bg="#EEEEEE", activebackground="#EEEEEE")
    else:
        btn.config(bg="#222831", activebackground= "#222831")

#Sự kiện click của từng btn
def click(r, c):
    board[r][c] = 0 if board[r][c] == 1 else 1
    draw_cell(r, c)
    mess = valid_message()
    information_text.set(mess if mess else "Ready to solve")

#Vẽ quân xe lên một ô cho trước
def draw_cell(r, c):
    btn = cells[r][c]
    btn.config(text="♖" if board[r][c] == 1 else "",
               fg="#00ADB5")
    
#Vẽ các quân xe lên những ô đã được đánh dấu
def draw_cur(cur):
    for r in range(SBOARD):
        for c in range(SBOARD):
            board[r][c] = 0
    for r, c in cur.items():
        board[r][c] = 1
    for r in range(SBOARD):
        for c in range(SBOARD):
            draw_cell(r, c)

#Trả về true và không có tin nhắn nếu không có quân cờ nào vi phạm điều kiện và Falase nếu có quân cờ vi phạm điều kiện
def valid_cells():
    cols_seen = set()
    for r in range(SBOARD):
        count_in_row = sum(board[r])
        if count_in_row > 1:
            return False, f"Row {r+1} has more than 1 rook"
        for c in range(SBOARD):
            if board[r][c] == 1:
                if c in cols_seen:
                    return False, f"Colums {c+1} has more than 1 rook"
                cols_seen.add(c)
    return True, ""


#Trả về tin nhắn như hàm trên nêu vi phạm và số quân xe đã đặt nếu không vi phạm
def valid_message():
    ok, mess = valid_cells()
    if not ok:
        return mess
    used = sum(sum(row) for row in board)
    return f"Rooks used: {used}/8" if used < 8 else "Rooks used: 8/8"
    

#Xóa các quân xe ra khỏi bàn cờ hoặc dừng thuật toán BFS tức thời
def clear():
    global bfs_running, visited, queue
    bfs_running = False
    queue.clear()
    visited.clear()
    for r in range(SBOARD):
        for c in range(SBOARD):
            board[r][c]=0
            draw_cell(r, c)
    information_text.set("Board cleard")

#Lưu một trạng thái của các ô đã được dùng
def state_key(st):
    d, cols = st
    return (tuple(sorted(d.items())), tuple(sorted(cols)))

def start_BFS():

    ok, mess = valid_cells()
    if not ok:
        messagebox.showerror("Invalid: ", mess)
        information_text.set(mess)
        return



    global queue, visited, bfs_running
    bfs_running = True

    queue.clear()
    visited.clear()

    used_rows = {}
    used_cols = set()
    for r in range(SBOARD):
        for c in range(SBOARD):
            if board[r][c] == 1:
                used_rows[r] = c
                used_cols.add(c)
                break

    start_state = (used_rows.copy(), used_cols.copy())
    queue = deque([start_state])
    visited.add(state_key(start_state))

    BFS_step()


def BFS_step():
    global queue, visited, bfs_running
    if not bfs_running:  # nếu đã clear thì dừng luôn
        return
    if not queue:
        information_text.set("No solution")
        return
    
    cur_rows, cur_cols = queue.popleft()
    draw_cur(cur_rows)

    if len(cur_rows) == SBOARD:
        information_text.set("Solution found")
        return
    
    next_row = next_unused_rows(cur_rows)
    for col in range(SBOARD):
        if col not in cur_cols:
            new_cur_rows = cur_rows.copy()
            new_cols = cur_cols.copy()
            new_cur_rows[next_row] = col
            new_cols.add(col)
            key = state_key((new_cur_rows, new_cols))
            if key not in visited:
                visited.add(key)
                queue.append((new_cur_rows, new_cols))

    window.after(100, BFS_step)


def next_unused_rows(used_rows):
    for r in range(SBOARD):
        if r not in used_rows:
            return r
    return None



window = tk.Tk()
window.title("8 Rooks problem solver")

bfs_running = False
queue = deque()
visited = set()
board = [[0 for _ in range(SBOARD)] for _ in range(SBOARD)]
top_frame = tk.Frame(window)
top_frame.pack(padx=10, pady=10)

board_frame = tk.Frame(top_frame)
board_frame.grid(row=0, column=0, columnspan=3)

cells = [] #ma tran 1d chua cac ma tran 1 row btn -> ma tran 2d chua cac btn
for r in range(SBOARD):
    row_btn = []
    for c in range(SBOARD):
        btn = tk.Button(
            board_frame,
            text="",
            width=8,
            height=3,
            font=("IMPACT", 16, 'bold'),
            command=lambda rr=r, cc=c: click(rr, cc)
        )
        btn.grid(row=r,column=c)
        draw(btn, r, c)
        row_btn.append(btn)
    cells.append(row_btn)

information_text = tk.StringVar(value="Click to place or remove rooks")
information_lable = tk.Label(top_frame,textvariable=information_text,font=("Segoe UI Symbol", 16))
information_lable.grid(row=1, column=0, columnspan=3, pady=5)

solver_btn = tk.Button(top_frame, text="Solve by BFS", command=start_BFS)
solver_btn.grid(row=2,column=0,sticky="we")

clear_btn = tk.Button(top_frame,text="Clear Board", command=clear)
clear_btn.grid(row=2, column=1,sticky="we")



window.mainloop()