from permutations import simple_to_perm, flip, long_2, inv, niave_expression, index_to_perm
from tilting import tilt_alg_gls
from present import list_to_profile, mat_to_list_conv
from leclerc import epsilon, proj_inj, necklace, width_set
import tkinter as tk
from tkinter import font
from app_build import kwivah_application





# def main(w_expression: list[int], v: list[int], k: int, n: int, Projective_Injective = False, Tilting = False, Necklace = False, Galashin_Lam = False) -> None:
#     """Given a reduced expression for w and a k-index v giving rise to a Grassmannian
#     Richardson variety in Gr(k,n+1) we return useful information about the categorifications.
#
#      In particular Projective_Injective = True produces the projective-injective objects
#      in Leclerc's category.
#
#      Tilting = True performs an algorithm found in Leclerc's paper giving rise to a cluster tilting object in Leclerc's
#      category.
#
#      Necklace = True returns the list of modules which projects down onto Leclerc's projective injectives under the
#      functor pi_v. The name necklace is a slight abuse of naming.
#
#      Galashin_Lam = True uses a slightly different convention as described in the paper 'Positroid varieties and
#      cluster algebras'. When Galashin_Lam = True we convert their permutations to the Leclerc conventions and perform any computations there."""
#     if Necklace:
#         Projective_Injective = True
#     if Galashin_Lam:
#         hold = v.copy()
#         v = sorted(inv(flip(simple_to_perm(w_expression[::-1], n + 1), n + 1))[:k])
#         w_expression = niave_expression(flip(simple_to_perm(hold[::-1],n + 1), n+1), n+1)
#     if Projective_Injective:
#         v_expression = niave_expression(long_2(index_to_perm(v, n+1), k), n+1)
#         pi = proj_inj(v_expression, w_expression, n+1)
#         if Necklace:
#             widths = width_set(w_expression, k, n+1)
#             print(necklace(pi, v, widths))
#     if Tilting:
#         print('First we produce the cluster-tilting object in C_w \n')
#         tilt_alg_gls(w_expression, n)
#         print('Each summand must then be quotiented by a maximal submodule which is a factor of the following module:')
#         v_adapt = niave_expression(long_2(index_to_perm(v, n+1), k), n+1)
#         counter = []
#         for j in epsilon(v_adapt,n):
#             counter.append(mat_to_list_conv(j))
#         for j in counter:
#             list_to_profile(j, counter.index(j) + 1, print_filt=True)



# w_expression =  niave_expression(long_2(index_to_perm([3,6], 6), 2), 6)
# v = [1,3]
# v = [4,3,2,1,4,3,2,7,6,5,4,3,8,6,4,10,9,8,7,6,5,11,10,9,8,7]
# w_expression = [4,3,2,1,5,4,3,2,7,6,5,4,3,8,7,6,5,4,10,9,8,7,6,5,11,10,9,8,7,6]
# k = 6
# n = 11
# Projective_Injective = False
# Tilting = False
# Necklace = True
# Galashin_Lam = True



if __name__ == '__main__':
    kwivah_application()





















