from app_build import kwivah_application
from tilting import tilt_alg_gls
from present import list_to_array
from homological import submodules, quotients, max_quotient
import numpy as np

# if __name__ == '__main__':
#     kwivah_application()


t = [np.array([[1],[1],[1]]), np.array([[0,1],[1,1]])]

l = [np.array([[1],[1],[0]]), np.array([[1,0,0]])]

for j in max_quotient(l, t):
    print(j)


# v = np.array([[1,1],[1,1]])
# v[:1,:2] = 0
# print(v)












