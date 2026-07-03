class Students:
    def _init_(self,student_id,name,age,grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = age


    def to_dict(self):
        return{
            "student_id": "self.student_id",
            "name": "self.name",
            "age": self.age,
            "grade": self.grade
        }    