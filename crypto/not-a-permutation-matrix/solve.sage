import sys
sys.path.append("dist")

from base64 import b64encode, b64decode
import re, random
from sage.modules.finite_submodule_iter import FiniteZZsubmodule_iterator
from itertools import product
from functools import reduce

##########################################
########## START From challenge ##########
##########################################

NROUNDS = 10
SEED = int(0xcaffe *3* 0xc0ffee)

# https://people.maths.bris.ac.uk/~matyd/GroupNames/61/Q8s5D4.html
G = PermutationGroup([
    [(1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16),(17,18,19,20),(21,22,23,24),(25,26,27,28),(29,30,31,32)],
    [(1,24,3,22),(2,23,4,21),(5,14,7,16),(6,13,8,15),(9,27,11,25),(10,26,12,28),(17,31,19,29),(18,30,20,32)],
    [(1,5,12,30),(2,6,9,31),(3,7,10,32),(4,8,11,29),(13,25,19,21),(14,26,20,22),(15,27,17,23),(16,28,18,24)],
    [(1,26),(2,27),(3,28),(4,25),(5,14),(6,15),(7,16),(8,13),(9,23),(10,24),(11,21),(12,22),(17,31),(18,32),(19,29),(20,30)]
])
num2e = [*G]
e2num = {y:x for x,y in enumerate(num2e)}
b64encode_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321+/"
b64decode_map = {c:i for i,c in enumerate(b64encode_map)}

def gen_random_mat(seed: int, size: int):
    random.seed(seed)
    return matrix(size, size, random.choices([0,1], k=size*size))

def mat_vec_mul(mat, vec):
    return [reduce(lambda x,y: x*y, (a^b for a,b in zip(vec, m))) for m in mat]

def hash_msg(msg: bytes):
    emsg = b64encode(msg).decode().strip("=")
    sz = len(emsg)
    vec = [num2e[b64decode_map[c]] for c in emsg]
    mat = gen_random_mat(SEED, sz)
    for _ in range(NROUNDS):
        # Since G is non-abelian so this is a pretty good hash function!
        vec = mat_vec_mul(mat, vec)
    return ''.join((b64encode_map[e2num[c]] for c in vec))

ct = "aO3qDbHFoittWTN6MoUYw9CZiC9jdfftFGw1ipES89ugOwk2xCUzDpPdpBWtBP3yarjNOPLXjrMODD"

########################################
########## END From challenge ##########
########################################

def find_generators():
    """
    Find elements a,b,c,d of G such that
    1. All elements of G are uniquely of the form: a^x b^y c^z d^w
    2. a^x b^y c^z d^w |-> ((a, (b, c)), d) exibits an isomorphism
       G -> (C4 × (C4 ⋊ C2)) ⋊ C2
             │     │     │      │
            0th   1st   2nd    3rd - component
    """

    e_ord = {}
    for o,e in ((e.order(), e) for e in num2e):
        if o not in e_ord: e_ord[o] = []
        e_ord[o].append(e)

    for a,b,c,d in product(e_ord[4], e_ord[4], e_ord[2], e_ord[2]):
        if a == b or c == d: continue
        if len(set(a^x * b^y * c^z * d^w for x,y,z,w in product(*map(range, (4,4,2,2))))) != 64: continue
        if b*c != c*b^(-1): continue
        if a*b*a^(-1) != b: continue
        if a*c*a^(-1) != c: continue
        break
    
    return a,b,c,d

a,b,c,d = find_generators()
# Maps elements in G to-and-fro tuple representation. See `find_generators`.
e2tuple = {a^x * b^y * c^z * d^w: (x,y,z,w) for x,y,z,w in product(*map(range, (4,4,2,2)))}
tuple2e = {y:x for x,y in e2tuple.items()}

def cast_vec(vec, dim):
    """
    Cast a vector of elements in G to the `dim`-th
    component. See `find_generators`
    """
    return [e2tuple[c][dim] for c in vec]

def my_hash(vec):
    """
    Like `hash_msg but without the base64 part`
    """
    sz = len(vec)
    mat = gen_random_mat(SEED, sz)
    for _ in range(NROUNDS):
        vec = mat_vec_mul(mat, vec)
    return vec

def modq_kernel(matx, q):
    """
    Solves for the kernel of `matx` which is a matrix
    with elements in ZZ/`q`ZZ
    """
    # From: https://ask.sagemath.org/question/49365/computing-the-mod-q-kernel-of-a-matrix-for-q-composite/
    source_dim = matx.ncols()
    target_dim = matx.nrows()
    domain = ZZ^source_dim / (q * ZZ^source_dim)
    codomain = ZZ^target_dim / (q * ZZ^target_dim)
    phi = domain.hom([codomain(matx.columns()[i]) for i in range(source_dim)])
    
    full_kernel = matrix([domain(b) for b in phi.kernel()]).T

    pivot_cols = full_kernel.echelon_form().pivots()
    reduced_kernel = matrix(full_kernel.columns()[i] for i in pivot_cols)
    return reduced_kernel.change_ring(Zmod(q))

def matq_solve_right_all(mat, vec, q):
    """
    Solves for all vectors u such that
    `mat * u = vec`, where we are working
    in ZZ/`q`ZZ.
    """
    v = mat.solve_right(vec)
    if is_prime(q):
        return [v + k for k in mat.right_kernel()]
    kernel = modq_kernel(mat, q)
    print(f"Kernel has {kernel.nrows()} rows")
    if kernel.nrows() > 8: raise Exception(f"Too many solutions, regen challenge")
    if kernel.nrows() == 0: return [v]
    unique_v = set(tuple(v + k) for k in FiniteZZsubmodule_iterator([*kernel]))
    return list(vector(Zmod(q), v) for v in unique_v)


sz = len(ct)
ct_vec = [num2e[b64decode_map[c]] for c in ct]

# By working in the quotient G -> G/(C4 × (C4 ⋊ C2)),
# isomorphic to C2,
# find all possible 3rd component of the flag.

ct_vec_3 = vector(Zmod(2), cast_vec(ct_vec, 3))
mat_3 = gen_random_mat(SEED, sz).change_ring(Zmod(2))^NROUNDS
pos_pt_3s = matq_solve_right_all(mat_3, ct_vec_3, 2)

print("No. possible 3rd component:", len(pos_pt_3s), end="\n\n")
for pt_vec_3 in pos_pt_3s:
    
    # By commutating with (known) 3rd component,
    # and working in the quotient
    # (C4 × (C4 ⋊ C2)) -> (C4 × (C4 ⋊ C2))/C4/C4,
    # isomorphic to C2,
    # find all possible 2nd component of the flag.

    mat = []
    for j in range(sz):
        v = [tuple2e[(0,0,int(i==j),b)] for i,b in enumerate(pt_vec_3)]
        v = cast_vec(my_hash(v), 2)
        mat.append(v)
    mat = matrix(Zmod(2), mat).T

    known = my_hash([tuple2e[(0,0,0,b)] for b in pt_vec_3])
    diff = [a * b^(-1) for a,b in zip(ct_vec, known)]
    diff = vector(Zmod(2), cast_vec(diff, 2))
    pos_pt_2s = matq_solve_right_all(mat, diff, 2)

    print(f"Assuming 3rd component is: {''.join(map(str, pt_vec_3))},\n"
           "No. possible 2nd component:", len(pos_pt_2s), end="\n\n")
    for pt_vec_2 in pos_pt_2s:
        
        # By commutating with (known) 3rd component,
        # and working in the quotient
        # (C4 × (C4 ⋊ C2)) -> (C4 × (C4 ⋊ C2))/C4,
        # and commutating with (known) 2nd component,
        # we can work in C4 to
        # find all possible 1st component of the flag.

        mat = []
        for j in range(sz):
            v = [tuple2e[(0, int(i==j), *v)] 
                 for i, v
                 in enumerate(zip(pt_vec_2, pt_vec_3))]
            v = cast_vec(my_hash(v), 1)
            mat.append(v)
        mat = matrix(Zmod(4), mat).T

        known = my_hash([tuple2e[(0, 0, *v)] for v in zip(pt_vec_2, pt_vec_3)])
        diff = [a * b^(-1) for a,b in zip(ct_vec, known)]
        diff = vector(Zmod(4), cast_vec(diff, 1))
        pos_pt_1s = matq_solve_right_all(mat, diff, 4)
        
        # Since `matq_solve_right_all` is super slow when
        # the modulus isn't prime, we can optimize by filtering out
        # possible 1st component of the flag since we know
        # the flag has to start with `grey{`.
        
        knownflag_b64 = b64encode(b"grey{")[:6].decode()
        possible_pt_vec_1_values_first_6 = [
            set((tuple2e[(x,0,0,0)]
                * num2e[b64decode_map[c]]
                * tuple2e[(0,0,0,b3)] 
                * tuple2e[(0,0,b2,0)] for x in range(4))
               ) 
            - set((tuple2e[(0,x,0,0)] for x in range(4)))
            for c,b2,b3
            in zip(knownflag_b64, pt_vec_2, pt_vec_3)]
        possible_pt_vec_1_values_first_6 = [
            set([e2tuple[x][1] for x in c]) 
            for c in possible_pt_vec_1_values_first_6]

        pos_pt_1s = filter(
            lambda s: all(a in b for a,b in zip(s, possible_pt_vec_1_values_first_6)),
            pos_pt_1s)
        pos_pt_1s = list(pos_pt_1s)

        print(f"Assuming 3rd component is: {''.join(map(str, pt_vec_3))},\n"
              f"Assuming 2nd component is: {''.join(map(str, pt_vec_2))},\n"
               "No. possible 1st component:", len(pos_pt_1s), end="\n\n")
        for pt_vec_1 in pos_pt_1s:
            
            # By commutating with (known) 3rd component,
            # and working in the quotient
            # (C4 × (C4 ⋊ C2)) -> (C4 × (C4 ⋊ C2))/(C4 ⋊ C2),
            # isomorphic to C4,
            # find all possible 1st component of the flag.

            mat = []
            for j in range(sz):
                v = [tuple2e[(int(i==j), *v)] 
                    for i, v
                    in enumerate(zip(pt_vec_1, pt_vec_2, pt_vec_3))]
                v = cast_vec(my_hash(v), 0)
                mat.append(v)
            mat = matrix(Zmod(4), mat).T

            known1 = my_hash([tuple2e[(0,0,0,b3)] for b3 in pt_vec_3])
            known2 = my_hash([tuple2e[(0,*v,0)] for v in zip(pt_vec_1, pt_vec_2)])
            diff = [a * b^(-1) * c^(-1) for a,b,c in zip(ct_vec, known1, known2)]
            diff = vector(Zmod(4), cast_vec(diff, 0))
            pos_pt_0s = matq_solve_right_all(mat, diff, 4)
            
            print(f"Assuming 3rd component is: {''.join(map(str, pt_vec_3))},\n"
                  f"Assuming 2nd component is: {''.join(map(str, pt_vec_2))},\n"
                  f"Assuming 1st component is: {''.join(map(str, pt_vec_1))},\n"
                   "No. possible 0th component:", len(pos_pt_0s), end="\n\n")
            for pt_vec_0 in pos_pt_0s:
                
                # Finally, with all 4 components,
                # we can check if the components we have found
                # is actually the flag.

                b64_flag = ''.join(
                    b64encode_map[e2num[a^x * b^y * c^z * d^w]]
                    for x,y,z,w in zip(pt_vec_0, pt_vec_1, pt_vec_2, pt_vec_3)
                )
                print(f"Found Base64:", b64_flag)
                try: decoded = b64decode(b64_flag + "="*2, validate=False).decode()
                except: continue
                if not re.match(r"^grey\{.+\}$", decoded): continue

                print("Possible flag:", decoded)


# No. possible 3rd component: 2
# 
# Assuming 3rd component is: 000011001001000101001110010110000010011101111011100000110110001111011000000110,
# No. possible 2nd component: 2
# 
# Kernel has 3 rows
# Assuming 3rd component is: 000011001001000101001110010110000010011101111011100000110110001111011000000110,
# Assuming 2nd component is: 010111101010010000011110001011010000011000011010110000010101000010001011011010,
# No. possible 1st component: 1
# 
# Kernel has 3 rows
# Assuming 3rd component is: 000011001001000101001110010110000010011101111011100000110110001111011000000110,
# Assuming 2nd component is: 010111101010010000011110001011010000011000011010110000010101000010001011011010,
# Assuming 1st component is: 131232113220100022303201322230012222003032230000303012213203120132202221022230,
# No. possible 0th component: 4
# 
# Found Base64: K4J8eW/KeH8iIyBhFmOzfURJNl9mcwA2HFmHARfiPkkfTAQhfzNBJGmZOXi4LGiucmGgXE92D07keC
# Found Base64: J3I9eW2IcH8hLyAhHkMydXRKOk9mdyB1FEkEDSchMkleSCQidzMCJFkbMWg6JEgudmEjXG91B80kfA
# Found Base64: I3I0eW1JdH8gKyAhGlNycWRLPk9mdzB1EElFCTdgNkleSDQjczMDJElaNWh5IFhudmFiXH91A79kfB
# Found Base64: L4J7eW+LfH8jJyBhEnPzeVRIMl9mcxA2GFnGBQejOkkfTBQgezNAJHnYPXj3KHjucmHhXF92C98keD
# Kernel has 3 rows
# Assuming 3rd component is: 000011001001000101001110010110000010011101111011100000110110001111011000000110,
# Assuming 2nd component is: 110011010011110011110011101010011011100110011111010101101110111010111111100011,
# No. possible 1st component: 0
# 
# Assuming 3rd component is: 100111110000100110100011110111001001100011111110000101001101110111101100111111,
# No. possible 2nd component: 2
# 
# Kernel has 3 rows
# Assuming 3rd component is: 100111110000100110100011110111001001100011111110000101001101110111101100111111,
# Assuming 2nd component is: 010111101010010000011110001011010000011000011010110000010101000010001011011010,
# No. possible 1st component: 0
# 
# Kernel has 3 rows
# Assuming 3rd component is: 100111110000100110100011110111001001100011111110000101001101110111101100111111,
# Assuming 2nd component is: 110011010011110011110011101010011011100110011111010101101110111010111111100011,
# No. possible 1st component: 1
# 
# Kernel has 3 rows
# Assuming 3rd component is: 100111110000100110100011110111001001100011111110000101001101110111101100111111,
# Assuming 2nd component is: 110011010011110011110011101010011011100110011111010101101110111010111111100011,
# Assuming 1st component is: 131232113220100022303201322230012222003032230000303012213203120132202221022230,
# No. possible 0th component: 4
# 
# Found Base64: b4JmfXvaPH8zYyAhV8eyPFRZdl9nchA2WE7XQAPyfklfSRQxPzMRIW8IfXyqaXzudnXwWU91SlnlfT
# Found Base64: Z3JleXtZMG8wbzAhX0dyNHRael9ncjB1UF9USDMwcllfTTRzNzNSIV9KdWxpYUxvdmVzWW91QnllfQ
# Possible flag: grey{Y0o0o0!_Gr4tZz_gr0uP_TH30rY_M4s73R!_JuliaLovesYouBye}
# Found Base64: Y3JkeXsYNG8xazAhW9cyMGRbfl9nciB1VF0VTCNxdllfTSRyMzNTIU0LcWwoZVwvdmUyWX91RmklfR
# Found Base64: a4JnfXubOH8yZyAhU7fyOERYcl9ncgA2XE8WRBOzeklfSQQwOzMQIX7JeXzrbWyudnWxWV91TkmlfS
