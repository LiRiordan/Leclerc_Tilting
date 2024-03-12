# Leclerc_Tilting

In "Cluster structures on strata of flag varieties", Leclerc describes (section 4.8) how to construct a cluster tilting object in his categorification of Richardsons. 

The data of a Richardson variety is determined by a pair of permutations v, w in S_m with v =< w in the Bruhat order. If v = w_{0}^{K} u where W^{K} is a parabolic associated to the Grassmannian Gr(k,m) 
and u is in W^{K}\W then the Richardson variety lives in the Grassmannian Gr(k,m). To v we associate the k-index given by u([1,2,3,...,k]). After picking a reduced expression for w and fixing n = m - 1 we perform his algorithm. 
It first produces a cluster tilting object in the Schubert associated to w. It then produces a second module such that the cluster tilting object desired is the quotient of that in the Schubert by its maximal submodule which is a factor module of the second (see the paper for details). We produce these two modules algorithmically and may at a later date attempt to perform the quotient via algorithm. 
