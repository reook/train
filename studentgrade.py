import json
import os
from typing import Dict, Any

class StudentGradeManager:
    """
    学生成绩管理系统（单例模式）
    使用示例：
    >>> manager = StudentGradeManager()
    >>> manager.add_student("001", "张三")
    """
    _instance = None
    DEFAULT_FILE = "students.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students: Dict[str, Dict[str, Any]] = {}
            cls._instance.__load_initial_data()
        return cls._instance

    def __load_initial_data(self):
        """初始化时尝试自动加载数据"""
        if os.path.exists(self.DEFAULT_FILE):
            self.load_from_file()

    def add_student(self, student_id: str, name: str) -> None:
        """
        添加学生信息
        :param student_id: 学生ID（必须唯一）
        :param name: 学生姓名
        """
        if not self.__validate_student_id(student_id):
            return
        if not self.__validate_name(name):
            return

        if student_id in self.students:
            print(f"⚠️ 学生ID {student_id} 已存在！")
        else:
            self.students[student_id] = {
                "name": name.strip(),
                "grades": {},
                "modified": False
            }
            print(f"✅ 学生 {name} (ID: {student_id}) 添加成功！")

    def add_grade(self, student_id: str, subject: str, score: float) -> None:
        """
        录入学科成绩
        :param student_id: 学生ID
        :param subject: 学科名称
        :param score: 分数（0-100）
        """
        if not self.__validate_student(student_id):
            return
        if not self.__validate_subject(subject):
            return
        if not self.__validate_score(score):
            return

        self.students[student_id]["grades"][subject.strip()] = score
        self.students[student_id]["modified"] = True
        print(f"✅ {self.__get_student_name(student_id)} 的 {subject} 成绩录入成功！")

    def get_average(self, student_id: str, subject: str = None) -> float:
        """
        计算平均分
        :param student_id: 学生ID
        :param subject: 指定学科（可选）
        :return: 平均分数
        """
        if not self.__validate_student(student_id):
            return 0.0

        grades = self.students[student_id]["grades"]
        if subject:
            return grades.get(subject, 0.0)
        
        if not grades:
            print(f"⚠️ {self.__get_student_name(student_id)} 尚无成绩！")
            return 0.0
        return sum(grades.values()) / len(grades)

    def show_student(self, student_id: str) -> None:
        """显示学生详细信息"""
        if not self.__validate_student(student_id):
            return

        student = self.students[student_id]
        print(f"\n🔍 学生ID: {student_id}")
        print(f"├── 姓名: {student['name']}")
        print("├── 成绩单：")
        for subject, score in student["grades"].items():
            print(f"│   ├── {subject}: {score}")
        print(f"└── 平均分: {self.get_average(student_id):.1f}\n")

    def save_to_file(self, filename: str = DEFAULT_FILE) -> None:
        """保存数据到JSON文件"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                data = {sid: {**info, "modified": False} 
                       for sid, info in self.students.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 数据已保存到 {filename}")
        except (IOError, TypeError) as e:
            print(f"❌ 保存失败：{str(e)}")

    def load_from_file(self, filename: str = DEFAULT_FILE) -> None:
        """从JSON文件加载数据"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students.update(data)
            print(f"🔃 已从 {filename} 加载数据")
        except FileNotFoundError:
            print(f"❌ 文件 {filename} 不存在")
        except json.JSONDecodeError:
            print(f"❌ 文件 {filename} 格式错误")

    # 验证方法私有化
    def __validate_student_id(self, sid: str) -> bool:
        if not sid.strip():
            print("❌ 学生ID不能为空")
            return False
        if not sid.isalnum():
            print("❌ 学生ID只能包含字母和数字")
            return False
        return True

    def __validate_name(self, name: str) -> bool:
        if len(name.strip()) < 2:
            print("❌ 姓名至少需要2个字符")
            return False
        return True

    def __validate_subject(self, subject: str) -> bool:
        if not subject.strip():
            print("❌ 学科名称不能为空")
            return False
        return True

    def __validate_score(self, score: float) -> bool:
        if not (0 <= score <= 100):
            print("❌ 分数必须在0-100之间")
            return False
        return True

    def __validate_student(self, sid: str) -> bool:
        if sid not in self.students:
            print(f"❌ 学生ID {sid} 不存在")
            return False
        return True

    def __get_student_name(self, sid: str) -> str:
        return self.students[sid]["name"]


if __name__ == "__main__":
    # 测试用例
    manager = StudentGradeManager()
    
    # 添加学生
    manager.add_student("001", "张三")
    manager.add_grade("001", "数学", 85)
    manager.add_grade("001", "物理", 92)
    
    manager.add_student("002", "李四")
    manager.add_grade("002", "数学", 78)
    manager.add_grade("002", "物理", 88)
    
    # 显示信息
    manager.show_student("001")
    print(f"张三的数学成绩：{manager.get_average('001', '数学')}")
    print(f"李四的平均分：{manager.get_average('002'):.1f}")
    
    # 数据持久化
    manager.save_to_file()
    manager.load_from_file()
