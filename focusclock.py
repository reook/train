import time
import sys
import platform
from datetime import datetime
from typing import Optional

try:
    import winsound  # Windows系统使用
except ImportError:
    winsound = None

try:
    from playsound import playsound  # 跨平台音频播放
except ImportError:
    playsound = None

class PomodoroTimer:
    """
    番茄工作法计时器（支持跨平台）
    功能：
    - 可自定义工作时间/休息时间/循环次数
    - 声音和视觉提示
    - 实时进度显示
    - 使用统计日志
    - 支持中断恢复
    """
    def __init__(self):
        self.running = False
        self.start_time: Optional[datetime] = None
        self.log = []

    def start(self, work_mins=25, break_mins=5, cycles=4):
        """启动番茄钟"""
        self._validate_inputs(work_mins, break_mins, cycles)
        self.running = True
        
        print("\n🍅 番茄工作法计时器启动！")
        print(f"参数设置：工作时间 {work_mins} 分钟 | 休息时间 {break_mins} 分钟 | 总循环 {cycles} 次\n")
        
        try:
            for cycle in range(cycles):
                self._start_cycle(cycle+1, cycles, work_mins, break_mins)
        except KeyboardInterrupt:
            self._handle_interrupt()
        finally:
            self._save_session_log()
            print("\n📊 本次工作统计：")
            for entry in self.log:
                print(f"- {entry}")

    def _start_cycle(self, current_cycle, total_cycles, work_mins, break_mins):
        """执行单个循环"""
        # 工作阶段
        self._start_phase("工作", current_cycle, work_mins)
        self._play_alert("work_end")
        
        # 休息阶段（最后一个循环不休息）
        if current_cycle < total_cycles:
            self._start_phase("休息", current_cycle, break_mins)
            self._play_alert("break_end")

    def _start_phase(self, phase_type, cycle_num, duration_mins):
        """执行单个阶段"""
        self.start_time = datetime.now()
        phase_info = f"{phase_type} #{cycle_num} | 时长: {duration_mins} 分钟"
        self.log.append(f"{phase_info} | 开始时间: {self.start_time:%H:%M}")
        
        print(f"\n⏳ [{self.start_time:%H:%M}] 开始 {phase_info}")
        self._countdown(duration_mins * 60, phase_type)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.log[-1] += f" | 结束时间: {end_time:%H:%M} | 实际用时: {duration}"

    def _countdown(self, seconds, label):
        """带实时进度条的倒计时"""
        total_seconds = seconds
        start = time.time()
        
        try:
            while seconds > 0 and self.running:
                self._print_progress(seconds, total_seconds, label)
                time.sleep(1)
                seconds = total_seconds - int(time.time() - start)
        except KeyboardInterrupt:
            self._handle_interrupt()

    def _print_progress(self, remaining, total, label):
        """显示进度条和剩余时间"""
        mins, secs = divmod(remaining, 60)
        progress = 1 - (remaining / total)
        bar_length = 30
        filled = int(bar_length * progress)
        
        progress_bar = '█' * filled + '░' * (bar_length - filled)
        time_display = f"{mins:02d}:{secs:02d}"
        
        sys.stdout.write(
            f"\r{label}中 [{progress_bar}] {time_display} "
            f"{progress*100:.1f}%   "
        )
        sys.stdout.flush()

    def _play_alert(self, alert_type):
        """播放系统提示音"""
        sounds = {
            "work_end": (2000, 800),
            "break_end": (1000, 800)
        }
        print("\n" + "🔔" * 3 + " 时间到！" + "🔔" * 3)
        
        # 跨平台声音提示
        if playsound:
            try:
                playsound('alert.mp3')  # 需要准备音频文件
            except Exception as e:
                self._fallback_beep(sounds[alert_type])
        elif winsound:
            winsound.Beep(*sounds[alert_type])
        else:
            print("\a")  # 系统默认提示音

    def _fallback_beep(self, params):
        """备用蜂鸣方案"""
        if winsound:
            winsound.Beep(*params)
        else:
            print("\a")

    def _validate_inputs(self, *values):
        """验证输入参数"""
        for val, max_val in zip(values, (180, 60, 20)):
            if not isinstance(val, int) or val <= 0:
                raise ValueError("输入必须为正整数")
            if val > max_val:
                raise ValueError(f"输入值不能超过 {max_val}")

    def _handle_interrupt(self):
        """处理中断事件"""
        self.running = False
        print("\n\n⚠️  检测到中断，正在保存当前进度...")
        self._save_session_log()
        sys.exit(0)

    def _save_session_log(self):
        """保存会话日志"""
        with open("pomodoro.log", "a", encoding="utf-8") as f:
            f.write("\n".join(self.log) + "\n")

def get_valid_input(prompt: str, default: int, max_val: int) -> int:
    """获取并验证用户输入"""
    while True:
        try:
            input_str = input(f"{prompt} (默认 {default}, 最大 {max_val}): ")
            value = int(input_str) if input_str else default
            if 0 < value <= max_val:
                return value
            print(f"请输入 1-{max_val} 之间的整数")
        except ValueError:
            print("请输入有效数字")

if __name__ == "__main__":
    timer = PomodoroTimer()
    
    print("""\n=== 番茄工作法计时器 ===
    使用说明：
    1. 按 Ctrl+C 可随时中断
    2. 日志自动保存到 pomodoro.log
    3. 推荐准备 alert.mp3 文件用于提示音
    """)
    
    # 获取用户输入
    work_mins = get_valid_input("工作时间（分钟）", 25, 180)
    break_mins = get_valid_input("休息时间（分钟）", 5, 60)
    cycles = get_valid_input("循环次数", 4, 20)
    
    # 启动计时器
    timer.start(work_mins, break_mins, cycles)
