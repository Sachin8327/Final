class CollegeEnvironment:
    def __init__(self):
        self.seats={"It":120,"Comp":120}
        self.placements={"It":90,"Comp":95}

class Sensor:
    def get_input(self):
        return input("Enter your choice")

class Actuator:
    def show_courses(self):
        print("We offer It and Comp")
    def show_seats(self,course):
        print(environment.seats)
    def confirm_admission(self,course,environment):
        if environment.seats[course]>0:
            environment.seats[course]-=1
            print("Addmision confirmed in ",course)
            print("Remaining seats",environment.seats[course])
        else:
            print("No seats available")

class Simple:
    def __init__(self,actuator,environment):
        self.environment=environment
        self.actuator=actuator
    def act(self,choice):
        if choice=="1":
            self.actuator.show_courses()
        elif choice=="2":
            self.actuator.show_seats(self.environment)
        elif choice=="3":
            print("Admission confirm in it")
        elif choice=="4":
            print("Admission confirm in comp")
        elif choice=="5":
            print("Commp recommended")
        else:
            print("Ivalid choice")

class Model:
    def __init__(self,actuator,environment):
        self.environment=environment
        self.actuator=actuator
        
    def admission(self,course):
        self.actuator.confirm_admission(course,self.environment)

    def recommend(self):
        seats=self.environment.seats
        placements=self.environment.placements
        if seats["It"]==0 and seats["Comp"]==0:
            print("No seats availabel")
        elif seats["It"]==0:
            print("recoomed comp")
        elif seats["Comp"]==0:
            print("recoomed It")
        else:
            comp_score=seats["Comp"]*0.3+placements["Comp"]*0.7
            it_score=seats["It"]*0.3+placements["It"]*0.7
            if comp_score>=it_score:
                print("recommend comp")
            else:
                print("reecommend it")
        
    def act(self,choice):
        if choice=="1":
            self.actuator.show_courses()
        elif choice=="2":
            self.actuator.show_seats(self.environment)
        elif choice=="3":
            self.admission("Comp")
        elif choice=="4":
            self.admission("It")
        elif choice=="5":
            self.recommend()
        else:
            print("INvalid choice")

print("choose model")
print("1.Simple")
print("2.Model")
agent_inp=input("enter your choice")
environment=CollegeEnvironment()
sensor=Sensor()
actuator=Actuator()
if agent_inp=="1":
    agent=Simple(actuator,environment)
elif agent_inp=="2":
    agent=Model(actuator,environment)
else:
    print("Invalid choice")
    exit()

while True:
    print("Menu")
    print("1.courses")
    print("2.Seats")
    print("3.Take comp")
    print("4.Take It")
    print("5.Recommend")
    print("0.exit")
    choice=sensor.get_input()
    if choice=="0":
        print("Thanks")
        break
    agent.act(choice)



