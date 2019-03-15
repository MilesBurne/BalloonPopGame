#Quadratic Module by Miles Burne

#takes (a,b,c) for ax^2 + bx + c
class quadratic_equation():
    
    #initilizer takes a, b and c
    def __init__(self,a,b,c):
        self.quadratic_works = True
        #ax^2 + bx + c
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        #finding the roots of equation
        self.root_1, self.root_2 = self.make_roots()

    #changes a and b
    def change_equation(self,a,b):
        self.a = float(a)
        self.b = float(b)

    #returns whether the equation is valid or not as BOOL
    def get_works(self):
        return(self.quadratic_works)

    #finds and returns the roots of the equation to __init__
    def make_roots(self):
        #quadratic equation = ((-b +- sqrt(b^2 - 4(a)(c))) / 2(a))
        
        #testing for works
        try:
            discriminant = (self.b**2) - 4*(self.a)*(self.c) #b**2 - 4ac
            test_for_error = math.sqrt(discriminant)
            
        #if quadratic errors at discriminant, this function will cease and roots and 'quadratic_works' will be set to'False'
        except:
            self.quadratic_works = False
            return(False, False)

        solution_1 = (((-1*self.b)+(math.sqrt(discriminant)))/(2*self.a)) # -b +- sqrt(b**2 - 4ac)
        solution_2 = (((-1*self.b)-(math.sqrt(discriminant)))/(2*self.a)) #         /2a

        return(solution_1, solution_2)

    #returns the y using equation and input x
    def get_y(self,x):
        #finding each part of equation
        p1 = (self.a)*(x**2)
        p2 = (self.b)*(x)
        p3 = (self.c)
        #finding y
        y = p1+p2+p3
        #output of y
        return(y)

    #returns roots to call
    def get_roots(self):
        return(self.root_1, self.root_2)

        #changes a and b for the equation
    def change_var(self,a,b):
        self.a = float(a)
        self.b = float(b)

    #returns a
    def get_a(self):
        return(self.a)
    
    #returns b
    def get_b(self):
        return(self.b)

    #returns c
    def get_c(self):
        return(self.c)
