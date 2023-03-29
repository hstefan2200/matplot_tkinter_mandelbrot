import numpy as np
import matplotlib.pyplot as plt
 
d, h = 1000, 600  # pixel density (= image width) and image height
n, r = 100, 500  # number of iterations and escape radius (r > 2)
 
x = np.linspace(0, 2, num=d+1)
y = np.linspace(0, 2 * h / d, num=h+1)
 
A, B = np.meshgrid(x - 1, y - h / d)
C = 2.0 * (A + B * 1j) - 0.5
 
Z = np.zeros_like(C)
S = np.zeros(C.shape)
 
for k in range(n):
    M = abs(Z) < r
    S[M] = S[M] + np.exp(-abs(Z[M]))
    Z[M] = Z[M] ** 2 + C[M]

fig = plt.figure()
ax = fig.subplots()
# plt.imshow(S ** 0.1, cmap=plt.cm.twilight_shifted)
# plt.show()


X, Y = C.real, C.imag
R = 150 * 2 / d  # scaling depends on figsize
 
fig, ax = plt.subplots(figsize=(8, 6))
plt.imshow(S ** 0.1, cmap=plt.cm.twilight_shifted)
plt.show()