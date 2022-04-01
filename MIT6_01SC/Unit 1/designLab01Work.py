#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------
# Skipped, I know how to do this
#def fib(n):
    # Delete the pass statement below and insert your own code
 #   pass

#-----------------------------------------------------------------------------
# Learned some cool stuff from this, I was just getting into python
class V2:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def __str__(self):
        return f"V2[{self.getX()}, {self.getY()}]"

    def __add__(self,other):
        return V2(self.getX() + other.getX(),self.getY()+ other.getY())

    def __mul__(self,scalar):
        return V2(self.getX() * scalar, self.getY() * scalar)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

myVec1 = V2(5.1,6.1)
myVec2 = V2(1,1)

print(myVec1)
print(myVec1+myVec2)
print(myVec1*3.1)

#-----------------------------------------------------------------------------
# This was cool, learnend abt __str__, __call__ etc
class Polynomial:
    def __init__(self,coefficients):
        self.coeffs=coefficients

    def __str__(self):
        return str(self.coeffs)

    def __call__(self,x):
        return self.val(x)

    def __add__(self,other):
        return self.add(other)

    def __mul__(self,other):
        return self.mul(other)

    def coeff(self, i):
        return self.coeffs[-i-1]

    def val(self,x):
        output = 0

        # Horner’s Rule implementation
        for coefficient in self.coeffs:
            output *= x
            output += coefficient
        return output

    def roots(self):
        if len(self.coeffs) == 2: # order 1
            return -self.coeffs[1]/self.coeffs[0]
        elif len(self.coeffs) == 3: # order 2
            a = self.coeffs[0]
            b = self.coeffs[1]
            c = self.coeffs[2]

            root = ((b**2)-(4*a*c))**0.5 # sqrt(b^2-4ac)
            return [(-b + root)/(2*a),(-b - root)/(2*a)] # quadratic equation
        else:
            raise(ValueError,"can't handle polynomials of this degree")


    def add(self, other):
        # determing which if the lists is smallest, to  cap addition step
        if len(self.coeffs) < len(other.coeffs):
            # reverse the list to ease calculations
            smallest = self.coeffs[::-1]
            largest  = other.coeffs[::-1]
        else:
            smallest = other.coeffs[::-1]
            largest  = self.coeffs[::-1]

        # adding values of the two polynomials
        sum = []

        for term, coefficient in enumerate(smallest):
            sum.insert(0,coefficient+largest[term])

        # copying the rest of the values that weren't added together
        sum = largest[len(smallest):len(largest)] + sum
        
        return Polynomial(sum)

    def mul(self,other):
        multipliers   = self.coeffs
        multiplicands = other.coeffs
        output = Polynomial([])
        rows = []

        # column/long multiplication
        for zeros, multiplier in enumerate(reversed(multipliers)):
            cur_row = []
            
            for multiplicand in multiplicands:
                cur_row.append(multiplicand*multiplier)

            #  add the number of 0's necessary for the order of the term
            cur_row += [0 for zero in range(zeros)]
            rows.append(Polynomial(cur_row))

        # combine like terms
        for row in rows:
            output += row
        
        return output
    

p1 = Polynomial([1, 0, 5])
p2 = Polynomial([1,-11,6])
p3 = Polynomial([1,2,3])
p4 = Polynomial([3,2,-1])

print(p3 + p3)
print(p3 * p3)
print(p4(1))
print(p4(-1))
print(p4.roots())