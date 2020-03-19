class A:

    def a(self, t: int)->int:
        return 1

    def a(self, i: float)->float:
        return 1.0

a=A()
print(a.a(t=1))
print(a.a(1.1))