import random
q = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
def qwe():
    w = int(input("длина пороля: "))
    pas = ""
    for i in range(w):
        pas += random.choice(q)
    print(pas)
# qwe()
qwe()
# # for i in range(6):
# #     print("*" * i)
# def my_print(x):
#     print("*" * (len(x) + 2))
#     print("*" + x + "*")
#     print("*" * (len(x) + 2))
# my_print("")
# def d__d(x):
#     f_list = []
#     f_r = 0
#     for i in range(1, x + 1):
#         f_list.append(i)
#     for i in range(len(f_list)):
#         f_r = f_r + f_list[i]
#     return(f_r)
# n = int(input(""))
# print(d__d(n))




