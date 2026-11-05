rules=[(("And",["fever","cough"]),"flu"),
       (("And",["flu","body pain"]),"see doctor"),
       (("Or",["sneez","running nose"]),"cold"),
       (("And",[("Or",["fever","flu"]),"sneez"]),"infection")
      ]
facts=["fever","cough","body pain"]
print(facts)
def show_condition(condition):
    if isinstance(condition,str):
        return condition
    operator,parts=condition
    return "("+(" "+operator+" ").join(show_condition(part) for part in parts)+")"

for condition,conclusion in rules:
    print("IF",show_condition(condition),"THEN",conclusion)

def condition_is_true(condition,known):
    if isinstance(condition,str):
        return condition in known
    operator,parts=condition
    if operator=="And":
        return all(condition_is_true(part,known) for part in parts)
    elif operator=="Or":
        return any(condition_is_true(part,known) for part in parts)

def forward(goal,rules,facts):
    changed=True
    known=list(facts)
    while changed:
        changed=False
        for condition,conclusion in rules:
            if condition_is_true(condition,known) and conclusion not in known:   ###known ata hai naki rules
                known.append(conclusion)
                print("IF",show_condition(condition) ,"THEN", conclusion)
                changed=False
    print(known)
    return goal in known

print(forward("see doctor",rules,facts))

def proved_condition(condition,rules,facts,checking):
    if isinstance(condition,str):
        return backward(condition,rules,facts,checking)
    operator,parts=condition
    if operator=="And":
        return all(proved_condition(part,rules,facts,checking) for part in parts)
    elif operator=="Or":
        return any(proved_condition(part,rules,facts,checking) for part in parts)
    else:
        return False

def backward(goal,rules,facts,checking=None):
    if checking is None:
        checking=set()

        ###these two lines dekh lena 
    if goal in facts:
        print("Fact",goal)
        return True
    if goal in checking:
        return False

    checking=checking|{goal} ## don't forget this 
    for condition,conclusion in rules:
        if conclusion==goal:
            print("we need to prove",goal,"we check",show_condition(condition))
            if proved_condition(condition,rules,facts,checking):
                return True
    return False

print(backward("see doctor",rules,facts))























while True:

    print("\n------ EXPERT SYSTEM ------")
    print("1. Car Expert System")
    print("2. Disease Expert System")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:

        print("\n--- Car Expert System ---")

        print("1. Forward Chaining")
        print("2. Backward Chaining")

        ch = int(input("Enter choice: "))

        goal = input("Enter goal: ")

        if ch == 1:
            result = forward(goal, rules_car, facts_car)

        elif ch == 2:
            result = backward(goal, rules_car, facts_car)

        else:
            print("Invalid choice")
            continue

        if result:
            print("Goal is proved")
        else:
            print("Goal is not proved")

    elif choice == 2:

        print("\n--- Disease Expert System ---")

        print("1. Forward Chaining")
        print("2. Backward Chaining")

        ch = int(input("Enter choice: "))

        goal = input("Enter goal: ")

        if ch == 1:
            result = forward(goal, rules_disease, facts_disease)

        elif ch == 2:
            result = backward(goal, rules_disease, facts_disease)

        else:
            print("Invalid choice")
            continue

        if result:
            print("Goal is proved")
        else:
            print("Goal is not proved")

    elif choice == 3:

        print("Exiting...")
        break

    else:
        print("Invalid choice")