import numpy as np


# x -> vector contains x1 , x2 and x3 consequently
# a,b,c -> coefficients from user input
def func(x, a, b, c):
    return abs(a) * (1 - x[0]) ** 2 + abs(b) * (x[1] - x[0] ** 2) ** 2 + abs(c) * (x[2] - x[1] ** 2) ** 2


# grad -> [∂x1,∂x2,∂x3]
def gradient(x, a, b, c):
    grad = np.zeros(3, dtype=np.longdouble)  # initializing a numpy array with zeros.
    grad[0] = -2 * abs(a) * (1 - x[0]) - 4 * abs(b) * x[0] * (x[1] - x[0] ** 2)  # mathematical equation to compute ∂x1
    grad[1] = 2 * abs(b) * (x[1] - x[0] ** 2) - 4 * abs(c) * x[1] * (x[2] - x[1] ** 2)  # ∂x2
    grad[2] = 2 * abs(c) * (x[2] - x[1] ** 2)  # ∂x3
    return grad


# alpha -> learning rate
# tol -> threshold to check convergence
# max_iter -> maximum number of iterations till convergence
def gradient_descent(a, b, c, x_init=None, alpha=1e-3, tol=1e-3, max_iter=100000):
    if x_init is None:  # if X parameter isn't given.
        x_init = np.random.uniform(low=-10, high=10, size=3)  # randomly selecting the starting points for x1,x2,x3
    x = x_init.copy()
    for i in range(max_iter):
        grad = gradient(x, a, b, c)
        if np.linalg.norm(np.abs(grad)) < tol:  # checking if the magnitude of gradient vector is less than tol
            print("Breaking the loop at iteration ", i)
            break  # f(x) converged to the minimum, there is no need to continue optimizing
        x -= alpha * grad  # x1 = x1 - alpha*∂x1 , x2 = x2 - alpha*∂x2 , x3 = x3 - alpha∂dx3
        old_grad = grad
    return x, func(x, a, b, c)


# parameters: a, b, c, alpha and max_iter will be asked to user:
a = float(input("Enter a value for parameter a: "))
b = float(input("Enter a value for parameter b: "))
c = float(input("Enter a value for parameter c: "))
alpha = float(input("Enter a value for alpha: "))
max_iter = int(input("Enter a value for max_iter: "))

x_star, f_x_star = gradient_descent(a, b, c, alpha=alpha, max_iter=max_iter)

print("Minimum point x*: ", x_star)
print("Minimum value f(x*): ", f_x_star)
