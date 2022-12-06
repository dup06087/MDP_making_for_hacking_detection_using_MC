import random
import pandas as pd
import numpy as np
random.seed(1001)


number_of_User_PCs = 100
number_of_attack_property = 20
iteration_per_User_PC = 100
gamma = 0.9

### 파일에서 공격 방식 가져오기 시작
file_path = "./transition_probability.txt"

with open(file_path) as f:
    lines = f.readlines()

lines = [line.rstrip('\n') for line in lines]
print(lines)

## 파일에서 공격 방식 가져오기 끝

### Environment State 만들기 시작
class States:
    def __init__(self):
        self.defense_lst = lines
        self.State = [("ON" if random.randint(0,2) == 1 else "OFF") for _ in range(len(self.defense_lst))] ### 여기 변경!!!
        self.transition_prob_lst = [0 for _ in range(number_of_attack_property)]
        self.initial_policy = [0.25 for _ in range(number_of_attack_property)]
        self.value_funct_lst =  [0 for _ in range(number_of_attack_property)]
        self.Reward_lst = [0 for _ in range(number_of_attack_property)]

User_PCs = [States() for _ in range(number_of_User_PCs)]

print(len(States().defense_lst))

print("for문으로 defense 생성 확인  0 : ", User_PCs[0].defense_lst)

print("for문으로 State 생성 확인  0 : ", User_PCs[0].State)

print("for문으로 transition_prob_lst 생성 확인  0 : ", User_PCs[0].transition_prob_lst)

## Environment State 만들기 끝

### Transition Probability 만들기 및 생성 시작

def transition_probability():
    for PC_num in range(len(User_PCs)):
        for state_num in range(len(User_PCs[PC_num].State)):
            if User_PCs[PC_num].State[state_num] == "ON":
                User_PCs[PC_num].transition_prob_lst[state_num // 4] += 1

    print("transition_prob 생성 확인 :", User_PCs[0].transition_prob_lst)

transition_probability()

# Transition_prob 5개씩 해서 normalization
for PC_num in range(len(User_PCs)):
    transition_prob_sum0 = 0
    transition_prob_sum1 = 0
    transition_prob_sum2 = 0
    transition_prob_sum3 = 0

    for transition_prob_num in range(len(User_PCs[PC_num].transition_prob_lst)):
        if transition_prob_num < 5:
            transition_prob_sum0 += User_PCs[PC_num].transition_prob_lst[transition_prob_num]

        elif transition_prob_num < 10:
            transition_prob_sum1 += User_PCs[PC_num].transition_prob_lst[transition_prob_num]

        elif transition_prob_num < 15:
            transition_prob_sum2 += User_PCs[PC_num].transition_prob_lst[transition_prob_num]

        elif transition_prob_num < 20:
            transition_prob_sum3 += User_PCs[PC_num].transition_prob_lst[transition_prob_num]

    # print("???", transition_prob_num)
    # print("여기" , transition_prob_sum2)
    # print("tran")

    for transition_prob_num in range(len(User_PCs[PC_num].transition_prob_lst)):
        if transition_prob_num < 5:
            try:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = User_PCs[PC_num].transition_prob_lst[transition_prob_num] / transition_prob_sum0
            except:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] =0.25

        elif transition_prob_num < 10:
            try:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = User_PCs[PC_num].transition_prob_lst[transition_prob_num] / transition_prob_sum1
            except:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = 0.25
        elif transition_prob_num < 15:
            try:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = User_PCs[PC_num].transition_prob_lst[transition_prob_num] / transition_prob_sum2
            except:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = 0.25

        elif transition_prob_num < 20:
            try:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = User_PCs[PC_num].transition_prob_lst[transition_prob_num] / transition_prob_sum3
            except:
                User_PCs[PC_num].transition_prob_lst[transition_prob_num] = 0.25

print("regularization 확인 0", User_PCs[0].transition_prob_lst)

## Transition Probability 만들기 생성 끝

### 공격 수행 및 리워드 산출 시작

Reward_lst = [[0 for _ in range(5)] for i in range(4)] ## attack way개수

class attack:
    def __init__(self, User_PC_num):
        self.User_PC_num = User_PC_num
        self.attack_Initial_Access = ["attack_way0-0", "attack_way0-1","attack_way0-2","attack_way0-3","attack_way0-4"]
        self.attack_Execution = ["attack_way1-0", "attack_way1-1","attack_way1-2","attack_way1-3","attack_way1-4"]
        self.attack_Defense_Evasion = ["attack_way2-0", "attack_way2-1","attack_way2-2","attack_way2-3","attack_way2-4"]
        self.attack_Command_and_Control = ["attack_way3-0", "attack_way3-1","attack_way3-2","attack_way3-3","attack_way3-4"]
        self.attack_way = [self.attack_Initial_Access, self.attack_Execution, self.attack_Defense_Evasion, self.attack_Command_and_Control]

    def Attack(self):

        self.iteration_counter = 0
        self.inner_Reward_lst = [0 for _ in range(number_of_attack_property)]
        self.attack_ways = []

        current_step = 0

        while self.iteration_counter < iteration_per_User_PC:
            current_step = 0
            while True:

                self.Reward = 0

                current_step += 1


                ## step별로 attack방식에 대한 index와 attack 이름 뽑기
                selected_attack_way_index = random.choices(range(len(self.attack_way[current_step-1])), weights=User_PCs[self.User_PC_num].initial_policy[(current_step-1) * 5: current_step *5]) #list형
                for i in range(len(selected_attack_way_index)):
                    selected_attack_way_index = selected_attack_way_index[i]
                selected_attack_way = self.attack_way[current_step-1][selected_attack_way_index]

                threshold_value = random.random()
                if (User_PCs[self.User_PC_num].transition_prob_lst[5 * (current_step-1) + selected_attack_way_index]  < threshold_value):
                    # self.Reward += 0
                    # print("hacked")
                    self.inner_Reward_lst[5 * (current_step-1) + selected_attack_way_index] += 0

                    User_PCs[self.User_PC_num].Reward_lst = self.inner_Reward_lst
                    self.attack_ways.append((current_step, selected_attack_way_index, selected_attack_way,
                                             User_PCs[self.User_PC_num].Reward_lst[
                                                 5 * (current_step - 1) + selected_attack_way_index]))


                elif (User_PCs[self.User_PC_num].transition_prob_lst[5 * (current_step - 1) + selected_attack_way_index]  >= threshold_value):
                    # print("hacking failed : ", selected_attack_way)
                    self.inner_Reward_lst[5 * (current_step - 1) + selected_attack_way_index] -= 1

                    User_PCs[self.User_PC_num].Reward_lst = self.inner_Reward_lst

                    self.attack_ways.append((current_step, selected_attack_way_index, selected_attack_way,
                                             User_PCs[self.User_PC_num].Reward_lst[
                                                 5 * (current_step - 1) + selected_attack_way_index]))
                    current_step -= 1

                else:
                    print("error")

                # print(current_step)

                ## 한 PC 내에서의 Value Function 산출 > value iteration
                #제일 마지막 공격먼저 V(s) 측정

                ### MC 방식 도전 안되면 버리는 부분 시작
                G_t_lst = []
                if current_step >= 4:
                    self.iteration_counter +=1

                    #반복문 함수로
                    for i in range(len(self.attack_ways)):
                        valufunction_index = (self.attack_ways[i][0] - 1) * 5 + self.attack_ways[i][1]

                        j = 1
                        j_list = []
                        while i + j < len(self.attack_ways):
                            j_list.append(j)
                            j += 1
                        G_t = User_PCs[self.User_PC_num].Reward_lst[valufunction_index]
                        for k in range(len(j_list)):
                            G_t += (gamma ** (k+1)) * User_PCs[self.User_PC_num].Reward_lst[(self.attack_ways[k+1][0] - 1) * 5 + self.attack_ways[k+1][1]]
                        G_t_lst.append(G_t)
                        # print(G_t_lst)

                    for i in range(len(self.attack_ways)):
                        valufunction_index = (self.attack_ways[i][0] - 1) * 5 + self.attack_ways[i][1]

                        User_PCs[self.User_PC_num].value_funct_lst[valufunction_index] = User_PCs[self.User_PC_num].value_funct_lst[valufunction_index] + \
                            1 / self.iteration_counter * (G_t_lst[i])

                        # print("inner value function : ", User_PCs[self.User_PC_num].value_funct_lst)

                    print("value function : ", User_PCs[self.User_PC_num].value_funct_lst)
                    break




        # print("끝 : ",  self.User_PC_num)
            ## MC 방식 도전 안되면 버리는 부분 끝


attack_lst = [attack(i) for i in range(number_of_User_PCs)]

for i in range(len(attack_lst)):
    attack_lst[i].Attack()
    # print(attack_lst[i].attack_ways, attack_lst[i].Reward, User_PCs[i].Reward_lst)

np_value_func_array = []
for i in range(len(User_PCs)):
    np_value_func_array.append(np.array(User_PCs[i].value_funct_lst))


np_value_func_array = np.array((np_value_func_array))

Avg_Value_function = np_value_func_array.mean(axis=0)

Avg_Value_function = Avg_Value_function.reshape(4,5).transpose()

optimal_policy = [attack(0).attack_Initial_Access[Avg_Value_function.argmax(axis = 0)[0]],
                    attack(0).attack_Execution[Avg_Value_function.argmax(axis = 0)[1]],
                    attack(0).attack_Defense_Evasion[Avg_Value_function.argmax(axis = 0)[2]],
                    attack(0).attack_Command_and_Control[Avg_Value_function.argmax(axis = 0)[3]]
                  ]

print(optimal_policy)

