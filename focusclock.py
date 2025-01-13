import time

def pomodoro_timer(work_minutes=25, break_minutes=5, cycles=4):
    for cycle in range(cycles):
        print(f"Cycle {cycle + 1}/{cycles}")
        
        # 专注时间
        print(f"Work for {work_minutes} minutes. Focus!")
        time.sleep(work_minutes * 60)
        print("Time's up! Take a break.")
        
        # 休息时间
        print(f"Break for {break_minutes} minutes. Relax!")
        time.sleep(break_minutes * 60)
        print("Break is over. Get back to work!")
    
    print("All cycles completed! Great job!")

if __name__ == "__main__":
    pomodoro_timer()
