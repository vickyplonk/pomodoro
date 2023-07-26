from tkinter import *
import math

work = 25
short_break = 5
long_break = 15
timer = None
reps = 0
timer_running = False
remaining_time = 0

def reset():
    global reps, timer_running, remaining_time
    reps = 0
    timer_running = False
    remaining_time = 0
    timer_label["text"] = "Timer"
    canvas.itemconfig(timer_text, text="00:00")
    root.after_cancel(timer)

def toggle_timer():
    global reps,timer_running, remaining_time
    if not timer_running:
        work_sec = work * 60
        short_break_sec = short_break * 60
        long_break_sec = long_break * 60
        if not remaining_time:
            reps += 1

        if reps % 8 == 0:
            count_down(long_break_sec)
            timer_label.config(text="Long Break", fg="#8ABD91")
            root.bell()
        elif reps % 2 == 0:
            count_down(short_break_sec)
            timer_label.config(text="Break", fg="#ffd0cd")
            root.bell()
        else:
            if remaining_time:
                count_down(remaining_time)
                remaining_time = 0  # Reset remaining_time after resuming
            else:
                count_down(work_sec)
                timer_label.config(text="Work!", fg="#8ABD91")
                root.bell()

        timer_running = True
        start_button.config(text="Pause")
    else:
        root.after_cancel(timer)
        timer_running = False
        remaining_time = get_remaining_time()
        start_button.config(text="Start")

def get_remaining_time():
    current_time = canvas.itemcget(timer_text, 'text')
    current_time = current_time.split(':')
    return int(current_time[0]) * 60 + int(current_time[1])

def count_down(count):
    global timer, timer_running
    timer_running = True
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = root.after(1000, count_down, count - 1)
    else:
        timer_running = False
        toggle_timer()  # Start the next timer if timer completes

background = "#fff2ca"
font = "Comfortaa"
root = Tk()
root.title("Pomodoro Timer")
root.config(padx=30, pady=30, bg=background)
root.iconbitmap("tomatocat.ico")

canvas = Canvas(width=450, height=450, bg=background, highlightthickness=0)
tomato_img = PhotoImage(file="tomatoes.png")
canvas.create_image(215,225, image=tomato_img)
timer_text = canvas.create_text(230, 190, text="00:00", fill="white", font=(font, 35, "bold"))
canvas.grid(column=1, row=1)

timer_label = Label(text="Pomodoro Timer", font=(font, 50, "bold"), bg=background, fg="#8ABD91")
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", font=(font, 15, "bold"), highlightthickness=0, command=toggle_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", font=(font, 15, "bold"), command=reset, highlightthickness=0)
reset_button.grid(column=2, row=2)

root.mainloop()
