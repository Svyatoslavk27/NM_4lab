# Реалізувати алгоритми інтерполяції з вашого варіанту для табличної функції,
#  отриманої з вашої аналітичної функції. Для вашої аналітичної функції 
# на проміжку обрати не менше 15 точок, за якими побудувати табличну функцію.
# У звіті навести всі можливі графіки.

# функція варіант 9) 1/x

# метод Ньютона, природний кубічний сплайн
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def f(x):
    return 1/x

x = np.linspace(1, 5, 15)
y = f(x)

def divided_diff(x, y):
    n = len(x)
    coeffs = np.zeros([n, n])
    coeffs[:, 0] = y
    for j in range(1, n):
        for i in range(n-j):
            coeffs[i, j] = (coeffs[i+1, j-1] - coeffs[i, j-1]) / (x[i+j] - x[i])
    return coeffs[0, :]

def newton_interpolation(x, y, x_new):
    coeffs = divided_diff(x, y)
    n = len(x) - 1
    p = coeffs[n]
    for k in range(1, n+1):
        p = p*(x_new - x[n-k]) + coeffs[n-k]
    return p

f_spline = CubicSpline(x, y, bc_type='natural')

x_new = np.linspace(1, 5, 100)
y_newton = newton_interpolation(x, y, x_new)
y_spline = f_spline(x_new)

error_newton = np.abs(f(x_new) - y_newton)
error_spline = np.abs(f(x_new) - y_spline)

f_spline_der1 = f_spline.derivative(1)
f_spline_der2 = f_spline.derivative(2)

fig, axs = plt.subplots(3, 2, figsize=(15, 15))

axs[0, 0].plot(x, y, 'o', label='Дані')
axs[0, 0].plot(x_new, f(x_new), label='Точна функція')
axs[0, 0].set_title('Точна функція та вузли')
axs[0, 0].legend()
axs[0, 0].grid()

axs[0, 1].plot(x_new, y_newton, label='Метод Ньютона', color='orange')
axs[0, 1].plot(x_new, f(x_new), '--', label='Точна функція', color='gray')
axs[0, 1].set_title('Інтерполяція методом Ньютона')
axs[0, 1].legend()
axs[0, 1].grid()

axs[1, 0].plot(x_new, y_spline, label='Кубічний сплайн', color='green')
axs[1, 0].plot(x_new, f(x_new), '--', label='Точна функція', color='gray')
axs[1, 0].set_title('Кубічний сплайн')
axs[1, 0].legend()
axs[1, 0].grid()

axs[1, 1].plot(x_new, error_newton, label='Похибка Ньютона', color='red')
axs[1, 1].set_title('Похибка методу Ньютона')
axs[1, 1].legend()
axs[1, 1].grid()

axs[2, 0].plot(x_new, error_spline, label='Похибка кубічного сплайну', color='purple')
axs[2, 0].set_title('Похибка кубічного сплайну')
axs[2, 0].legend()
axs[2, 0].grid()

axs[2, 1].plot(x_new, f_spline_der1(x_new), label='Перша похідна', color='blue')
axs[2, 1].plot(x_new, f_spline_der2(x_new), label='Друга похідна', color='brown')
axs[2, 1].set_title('Похідні кубічного сплайну')
axs[2, 1].legend()
axs[2, 1].grid()

plt.tight_layout()
plt.show()
