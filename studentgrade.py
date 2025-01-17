import json
import os

# 学生成绩管理系统
class StudentGradeManager:
    def __init__(self):
        self.students = {}  # 用字典存储学生信息，键为学生ID，值为学生信息字典

    def add_student(self, student_id, name):
        """添加学生信息"""
        if student_id in self.students:
            print(f"学生ID {student_id} 已存在！")
        else:
            self.students[student_id] = {"name": name, "grades": []}
            print(f"学生 {name} (ID: {student_id}) 添加成功！")

    def add_grade(self, student_id, grade):
        """录入学生成绩"""
        if student_id not in self.students:
            print(f"学生ID {student_id} 不存在！")
        else:
            self.students[student_id]["grades"].append(grade)
            print(f"学生 {self.students[student_id]['name']} 成绩录入成功！")

    def calculate_average(self, student_id):
        """计算学生平均分"""
        if student_id not in self.students:
            print(f"学生ID {student_id} 不存在！")
        else:
            grades = self.students[student_id]["grades"]
            if not grades:
                print(f"学生 {self.students[student_id]['name']} 尚无成绩！")
            else:
                average = sum(grades) / len(grades)
                print(f"学生 {self.students[student_id]['name']} 的平均成绩为: {average:.2f}")

    def find_student(self, student_id):
        """查找学生信息"""
        if student_id not in self.students:
            print(f"学生ID {student_id} 不存在！")
        else:
            student = self.students[student_id]
            print(f"学生ID: {student_id}, 姓名: {student['name']}, 成绩: {student['grades']}")

    def save_to_file(self, filename="students.json"):
        """将学生信息保存到文件"""
        with open(filename, "w") as file:
            json.dump(self.students, file, indent=4)
        print(f"学生信息已保存到文件 {filename}！")

    def load_from_file(self, filename="students.json"):
        """从文件加载学生信息"""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.students = json.load(file)
            print(f"学生信息已从文件 {filename} 加载！")
        else:
            print(f"文件 {filename} 不存在！")


# 示例使用
if __name__ == "__main__":
    manager = StudentGradeManager()

    # 添加学生
    manager.add_student("001", "张三")
    manager.add_student("002", "李四")

    # 录入成绩
    manager.add_grade("001", 85)
    manager.add_grade("001", 90)
    manager.add_grade("002", 78)
    manager.add_grade("002", 88)

    # 计算平均分
    manager.calculate_average("001")
    manager.calculate_average("002")

    # 查找学生信息
    manager.find_student("001")

    # 保存到文件
    manager.save_to_file()

    # 从文件加载
    manager.load_from_file()
