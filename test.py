class Foo:
    def bar1(self):
        print(1)
    def bar2(self,n):
        print(n)

def call_method(o, name):
    return getattr(o, name)()


f = Foo()
method_to_call = getattr(f, 'bar2')
result=method_to_call(3)