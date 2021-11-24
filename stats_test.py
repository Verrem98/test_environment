import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

mu = 100
std = 15

x = np.linspace(50, 150)

nv = stats.norm(loc=mu, scale=std)
y = nv.pdf(x)

plt.figure(figsize=(10,5), dpi=80)
plt.plot(x,y)
plt.show()

print(nv.cdf(110)-nv.cdf(120))


y = 13