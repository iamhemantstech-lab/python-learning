username = "developer"

def func():
    username = "designer"
    print("inside func username" , username)

func()

print("global username" , username)



# =========================== closure =========================
def parent(num):
    def child(c):
        return c ** num
    return child


res = parent(2)
res2 = parent(3)
print(res(5))
print(res2(5))