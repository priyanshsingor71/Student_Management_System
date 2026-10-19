students = {}

while True:
    print("STUDENT MANAGEMENT SYSTEM ")
    print("-" * 40)
    print("1. Add student" )
    print("2. View All students")
    print("3. Search student" )
    print("4. Update student" )
    print("5. Delete student" )
    print("6. Exit ")

    option = int(input("Enter your option: "))

    if option == 1:
        roll = input("Enter roll number: ")
        if roll in students:
            print("Student already exists!") 
            
        else:
            name = input("Enter Name: ")
            age = input("Enter Age: ")
            hindi = float(input("Enter Hindi marks: "))
            english = float(input("Enter English marks: "))
            maths = float(input("Enter Maths marks: "))
            science = float(input("Enter Science marks: "))
            computer = float(input("Enter Computer marks: "))
            
            total = hindi + english + maths + science + computer
            percentage = (total)*100/500
            
         
            
            
            students[roll] = {
                    "Name": name,
                    "Age": age,
                    "Hindi": hindi,
                    "English": english,
                    "Maths": maths,
                    "Science": science,
                    "Computer": computer,
                    "Percentage": percentage,
                    "Grade": "A" if percentage >=90 else "B" if percentage >= 80 else "C" if percentage >=70 else "D" if percentage >= 40 else "F"
                }

        print("Student Added Successfully!")
        print("-" * 40)
        
        
    elif option == 2:
        if len(students) == 0:
            print("No records found!")
        
        else:
            print("\nStudent Records")
            print("-" * 40)

            for roll, student_info in students.items():
                print(f"Roll No : {roll}")
                print("-" * 40)
                print(f"Name: {student_info['Name']}")
                print(f"Age: {student_info['Age']}")
                print(f"Percentage: {student_info['Percentage']}")
                print(f"Grade: {student_info['Grade']}")
                print("-" *40)

    elif option == 3:
        roll = input("Enter roll number: ")
        
        if roll in students:
            print("Student record found!")
            print(f"Name: {students[roll]['Name']}")
            print(f"Age: {students[roll]['Age']}")
            print(f"Percentage: {students[roll]['Percentage']}")
            print(f"Grade: {students[roll]['Grade']}")
        else:
            print("Student Not found!")
            
    elif option == 4:
        roll = input("Enter roll number: ")
        
        if roll in students:
            print("Student Found!")
            
            students[roll]['Name'] = input("Enter New Name: ")
            students[roll]['Age'] = input("Enter New Age: ")
            students[roll]['Hindi'] = float(input("Enter New Hindi marks: "))
            students[roll]['English'] = float(input("Enter New English marks:"))
            students[roll]['Maths'] = float(input("Enter New Maths marks:"))
            students[roll]['Science'] = float(input("Enter New Science marks:"))
            students[roll]['Computer'] = float(input("Enter New Computer marks:"))
            
            total = students[roll]['Hindi']+students[roll]['English']+students[roll]['Maths']+students[roll]['Science']+students[roll]['Computer']
            students[roll]['Percentage'] = (total)*100/500
            students[roll]['Grade'] = "A" if students[roll]['Percentage'] >= 90 else "B"if students[roll]['Percentage']>=80 else "C" if students[roll]['Percentage']>=70 else "D" if students[roll]['Percentage']>=40 else "F"
            
            print("Student updated Successfully!")
            print("-" * 40)
            
        else:
            print("Student not found!")
            
    elif option == 5:
        roll = input("Enter roll number: ")
        
        if roll in students:
            del students[roll]
            print("Student Deleted Successfully!")
        
        else:
            print("Student not Found!")
            
            
    elif option == 6:
        print("Thank you!")
        break
    
    else:
        print("Invalid Choice , Try Again!")