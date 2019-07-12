
def inited(func):
    def wrapper(self,*args,**kwargs):
        if not self.driver:
            self.init_chrome()
        return func(self,*args,**kwargs)
    return wrapper