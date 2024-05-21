import pandas as pd

# config_file_name = 'C:\\prot_nf_auto\\bin\\MM_scenario_config.xlsx'
# config_file = pd.ExcelFile(config_file_name, engine='openpyxl')

# config_sheet_name = config_file.sheet_names
# # print(config_sheet_name)

# sub_sheet_list = []
# for sub_sheet in config_sheet_name:
#     if 'SUB' in sub_sheet:
#         print(sub_sheet)
#         # sub_sheet_list = []
#         sub_sheet_list.append(sub_sheet)
# print(sub_sheet_list)

# a = 1
# b = 2

# ab = []
# ab.append(a)
# ab.append(b)
# print(ab)




class MyStack3(list):
    def push(self, item):
        self.append(item)


mystack = MyStack3()
mystack.push(1)
mystack.push(2)
mystack.push(3)
mystack.push(4)
mystack.push(5)
print(mystack)
print(mystack.pop())
print(mystack.pop())
for item in mystack:
    print(item)
print(mystack[1:])