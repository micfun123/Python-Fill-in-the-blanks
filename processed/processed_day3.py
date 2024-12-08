_ = open("in.txt", "r")
input_data = input_data.read()

total = 0

_ = 0
previose_num = 0

status = True

check_flase = "don't()"
check_do = "do()"


for _ in range(0,_(input_data),_):

    

    _ input_data[_] == "d":
        if input_data[i+1] == "o":
            if input_data[i+2] == "(" and input_data[i+3] == ")":
                status = True
                _("do() flag _ on")
            else:
                if input_data[i+2] == "_" and input_data[i+3] == "'" and input_data[i+4] == "t" and input_data[i+5] == "(" and input_data[i+6] == ")":
                    status = False
                    print("don't() flag is on")




    if status == True:
        if input_data[i] == ",":
            previose_num = current_num
            current_num = 0
        elif input_data[i] == "(":
            previose_num = 0
            current_num = 0
        elif input_data[i] == ")":
            print(current_num,previose_num)

            backcheck = len(str(previose_num)) + len(str(current_num))
            print(input_data[i - backcheck -5],input_data[i - backcheck-4],input_data[i - backcheck-3])

            if input_data[i - backcheck -5] == "m" and input_data[i - backcheck-4] == "u" and input_data[i - backcheck-3] == "l":
                total += current_num * previose_num
                previose_num = 0
                current_num = 0
        elif input_data[i].isnumeric():
            current_num = current_num * 10 + int(input_data[i])
        
       


print(f"The total is {total}")