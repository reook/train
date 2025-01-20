import time
import winsound  # 用于播放提示音（仅限Windows系统）

def pomodoro_timer(work_minutes=25, break_minutes=5, cycles=4):
    print("Pomodoro Timer Started! 🍅")
    
    for cycle in range(cycles):
        print(f"\nCycle {cycle + 1}/{cycles}")
        
        # 专注时间
        print(f"Work for {work_minutes} minutes. Focus! 🎯")
        countdown(work_minutes * 60)
        print("Time's up! Take a break. 🛑")
        play_sound()  # 播放提示音
        
        # 休息时间
        print(f"Break for {break_minutes} minutes. Relax! ☕")
        countdown(break_minutes * 60)
        print("Break is over. Get back to work! ⏰")
        play_sound()  # 播放提示音
    
    print("\nAll cycles completed! Great job! 🎉")

def countdown(seconds):
    """显示倒计时"""
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1

def play_sound():
    """播放提示音"""
    frequency = 1000  # 声音频率
    duration = 1000   # 持续时间（毫秒）
    winsound.Beep(frequency, duration)

def get_user_input(prompt, default_value):
    """获取用户输入，如果输入无效则使用默认值"""
    while True:
        try:
            user_input = input(f"{prompt} (默认: {default_value}): ")
            if user_input.strip() == "":
                return default_value
            return int(user_input)
        except ValueError:
            print("请输入有效的数字！")

if __name__ == "__main__":
    print("Welcome to the Pomodoro Timer! 🍅")
    
    # 获取用户输入
    work_minutes = get_user_input("请输入专注时间（分钟）", 25)
    break_minutes = get_user_input("请输入休息时间（分钟）", 5)
    cycles = get_user_input("请输入循环次数", 4)
    
    # 启动番茄钟
    pomodoro_timer(work_minutes, break_minutes, cycles)
