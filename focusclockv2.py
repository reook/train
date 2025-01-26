import time
import sys
import platform
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from pathlib import Path
import threading

try:
    import winsound
except ImportError:
    winsound = None

try:
    from playsound import playsound
except ImportError:
    playsound = None

class PomodoroTimer:
    """
    高级番茄工作法计时器
    功能亮点：
    - 实时统计和可视化
    - 自动保存和加载配置
    - 任务目标跟踪
    - 多线程提示音
    - 跨平台支持
    - 详细日志记录
    """
    CONFIG_FILE = "pomodoro_config.json"
    DEFAULT_SETTINGS = {
        "work_mins": 25,
        "break_mins": 5,
        "long_break_mins": 15,
        "cycles": 4,
        "target_hours": 8,
        "sound_enabled": True,
        "notifications": True
    }

    def __init__(self):
        self.running = False
        self.start_time: Optional[datetime] = None
        self.session_data: List[Dict] = []
        self.config = self._load_config()
        self.current_task: Optional[str] = None
        self.total_worked = timedelta()
        self.lock = threading.Lock()

    def start(self, task: Optional[str] = None):
        """启动计时器"""
        self.current_task = task
        self._show_welcome_message()
        
        try:
            while self.total_worked < timedelta(hours=self.config["target_hours"]):
                self._run_session()
                if not self._ask_to_continue():
                    break
        except KeyboardInterrupt:
            self._handle_interrupt()
        finally:
            self._save_session_data()
            self._show_summary()
            self._save_config()

    def _run_session(self):
        """执行一个完整的工作周期"""
        for cycle in range(1, self.config["cycles"] + 1):
            if not self.running:
                break
            
            # 工作阶段
            self._start_phase("工作", cycle, self.config["work_mins"])
            self._play_async_sound("work_end")
            
            # 休息阶段
            if cycle < self.config["cycles"]:
                duration = (self.config["long_break_mins"] if cycle % 4 == 0 
                           else self.config["break_mins"])
                self._start_phase("休息", cycle, duration)
                self._play_async_sound("break_end")

    def _start_phase(self, phase_type: str, cycle_num: int, duration_mins: int):
        """执行单个阶段"""
        self.start_time = datetime.now()
        phase_data = {
            "type": phase_type,
            "cycle": cycle_num,
            "duration": duration_mins,
            "start": self.start_time,
            "task": self.current_task
        }
        
        print(f"\n⏳ [{self.start_time:%H:%M}] 开始 {phase_type} #{cycle_num} "
              f"({duration_mins} 分钟)")
        
        self._countdown(duration_mins * 60, phase_type)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        phase_data.update({
            "end": end_time,
            "actual_duration": duration.total_seconds()
        })
        
        with self.lock:
            self.session_data.append(phase_data)
            if phase_type == "工作":
                self.total_worked += duration

    def _countdown(self, seconds: int, label: str):
        """带实时统计的倒计时"""
        start = time.time()
        last_update = start
        
        try:
            while seconds > 0 and self.running:
                current = time.time()
                if current - last_update >= 1:
                    self._display_progress(seconds, label)
                    last_update = current
                    seconds -= 1
                time.sleep(0.1)
        except KeyboardInterrupt:
            self._handle_interrupt()

    def _display_progress(self, seconds: int, label: str):
        """显示进度信息"""
        mins, secs = divmod(seconds, 60)
        progress = 1 - (seconds / (self.config["work_mins"] * 60))
        
        stats = (f"\r{label}中 [{self._progress_bar(progress)}] "
                f"{mins:02d}:{secs:02d} | "
                f"今日工作: {self._format_duration(self.total_worked)} | "
                f"目标: {self.config['target_hours']}小时")
        
        sys.stdout.write(stats)
        sys.stdout.flush()

    def _progress_bar(self, progress: float) -> str:
        """生成进度条"""
        bar_length = 30
        filled = int(bar_length * progress)
        return '█' * filled + '░' * (bar_length - filled)

    def _play_async_sound(self, sound_type: str):
        """异步播放提示音"""
        if not self.config["sound_enabled"]:
            return
        
        sound_map = {
            "work_end": (2000, 800),
            "break_end": (1000, 800)
        }
        
        def play():
            if playsound:
                try:
                    playsound('alert.mp3')
                except Exception:
                    self._fallback_beep(sound_map[sound_type])
            elif winsound:
                winsound.Beep(*sound_map[sound_type])
            else:
                print("\a")
        
        threading.Thread(target=play, daemon=True).start()

    # 其他辅助方法保持不变...

    def _load_config(self) -> Dict:
        """加载配置文件"""
        config_path = Path(self.CONFIG_FILE)
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return {**self.DEFAULT_SETTINGS, **json.load(f)}
            except Exception:
                print("⚠️ 配置文件损坏，使用默认设置")
        return self.DEFAULT_SETTINGS

    def _save_config(self):
        """保存当前配置"""
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def _save_session_data(self):
        """保存会话数据"""
        data_path = Path("pomodoro_sessions.json")
        existing_data = []
        if data_path.exists():
            with open(data_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(existing_data + self.session_data, f, indent=2)

    def _format_duration(self, duration: timedelta) -> str:
        """格式化时间显示"""
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # 其他方法保持不变...

if __name__ == "__main__":
    timer = PomodoroTimer()
    timer.start("项目开发")
