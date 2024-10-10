import tkinter as tk
from tkinter.ttk import Label, Style, Notebook, Entry
from leclerc import necklace
from permutations import *
from leclerc import proj_inj
from tilting import tilter

necklace_string = "Given a pair (v,w) with v a maximal length representative of  coset in W^{K}\ W and w >= v" \
                  " there is a positroid variety. The information of v can be given as a k-index and for w\n" \
                  "we take a reduced expression."
tilting_string = "Given a k-index for v (entered as v_1,v_2,v_3,...,v_k) and a reduced expression for w (entered" \
                 " as i_1,i_2,...,i_t) our first tab computes projective injectives. \nFirst it finds the lifts of projective" \
                 "-injectives in Leclerc's category. Then it finds the necklace from S-SB-W. Finally it also computes the " \
                 "two necklaces associated to v^{-1}w. \nThe final tab uses Leclerc's algorithm to compute the lift" \
                 " of a tilting object in his catgorification of the positroid. \nIf you're thinking about a skew-Schubert variety" \
                 " then you can save time by typing iw_1,w_,w_3,...,w_k and then it will use the w associated to" \
                 " this index. \nMake sure not to leave any spaces when entering v and w."


###Defining root
root = tk.Tk()
root.title("Kwivah")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))


### Some variables
k_var = tk.StringVar(root)
n_var = tk.StringVar(root)
v_var = tk.StringVar(root)
w_var = tk.StringVar(root)

### Add necessary tabs
tabControl = Notebook(root)
home_tab = tk.Frame(tabControl)
necklace_tab = tk.Frame(tabControl)
tilting_tab = tk.Frame(tabControl)
tabControl.add(home_tab, text='Home')
tabControl.add(necklace_tab, text = 'Necklaces')
tabControl.add(tilting_tab, text = 'Tilting modules')
tabControl.pack(expand=1, fill="both")

### Insert stylings
style = Style(root)
style.configure('New.TLabel', font = ('Great Vibes', 30))
style.configure('New2.TLabel', font=('Great Vibes', 25))
style.configure('New3.TLabel', font=('Great Vibes', 10))
style.configure('entry.TEntry', padding = [15,0,0,0])


###Home tab:
frame1 = tk.Frame(home_tab, bg = '#ffffff')
frame1.place(relx = 0, rely=0.1, relwidth=1, relheight=0.9)

label = Label(home_tab, text = 'Kwivah', style = 'New.TLabel', background='#0f0f0f', foreground = '#999966')
label.grid()
label.place(relx=0, rely = 0, relwidth=1, relheight=0.1)

def dark_mode():
    frame1.config(bg = '#000000')
    frame2.config(bg = '#000000')
    frame3.config(bg = '#000000')

def light_mode():
    frame1.config(bg = '#fefefe')
    frame2.config(bg = '#fefefe')
    frame3.config(bg = '#fefefe')

btn_dark = tk.Button(home_tab, text = 'Dark Mode', command=dark_mode)
btn_dark.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.2)

btn_light = tk.Button(home_tab, text = 'Light Mode', command=light_mode)
btn_light.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.25)

label2 = Label(frame1, text = "Welcome to Kwivah: \nHow should we use this app?.", style = 'New2.TLabel', background='#999966')
label2.place(relx=0.3, rely = 0.2, relwidth=0.4, relheight=0.2)

label3 = Label(frame1, text = necklace_string, style='New3.TLabel', background='#999966')
label3.place(relx=0.1, rely = 0.45, relwidth= 0.8, relheight=0.1)

label4 = Label(frame1, text = tilting_string, style='New3.TLabel', background='#999966')
label4.place(relx=0.1, rely = 0.6, relwidth= 0.8, relheight=0.2)

###Necklace tab:

frame2 = tk.Frame(necklace_tab, bg = '#ffffff')
frame2.place(relx = 0, rely=0, relwidth=1, relheight=1)

label = Label(necklace_tab, text = 'Kwivah', style = 'New.TLabel', background='#0f0f0f', foreground = '#999966')
label.grid()
label.place(relx=0, rely = 0, relwidth=1, relheight=0.1)

def dark_mode():
    frame1.config(bg='#000000')
    frame2.config(bg = '#000000')
    frame3.config(bg = '#000000')

def light_mode():
    frame1.config(bg='#fefefe')
    frame2.config(bg = '#fefefe')
    frame3.config(bg='#fefefe')

bttn_dark = tk.Button(necklace_tab, text = 'Dark Mode', command=dark_mode)
bttn_dark.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.2)

bttn_light = tk.Button(necklace_tab, text = 'Light Mode', command=light_mode)
bttn_light.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.25)

Grassmannian_description = Label(necklace_tab, text='We are in Gr(k,n). Enter k,n:', style='New3.TLabel', background='#999966')
Grassmannian_description.place(relx=0.25, rely = 0.2, relwidth=0.15, relheight=0.03)

k_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=k_var)
k_entry.place(relx=0.4, rely = 0.2, relwidth=0.05, relheight=0.03)

n_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=n_var)
n_entry.place(relx=0.45, rely = 0.2, relwidth=0.05, relheight=0.03)

V_description = Label(necklace_tab, text='Enter the k-index v', style='New3.TLabel', background='#999966')
V_description.place(relx=0.25, rely = 0.25, relwidth=0.15, relheight=0.03)

v_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=v_var)
v_entry.place(relx=0.4, rely = 0.25, relwidth=0.05, relheight=0.03)

W_description = Label(necklace_tab, text='Enter reduced expression for w', style='New3.TLabel', background='#999966')
W_description.place(relx=0.25, rely = 0.3, relwidth=0.15, relheight=0.03)

w_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=w_var)
w_entry.place(relx=0.4, rely = 0.3, relwidth=0.2, relheight=0.03)

GL_go = tk.Label(necklace_tab, bg = '#ff0000')
GL_go.place(relwidth = 0.05, relheight=0.05, relx = 0.15, rely = 0.3)

L_go = tk.Label(necklace_tab, bg = '#009900')
L_go.place(relwidth = 0.05, relheight=0.05, relx = 0.15, rely = 0.35)


Galashin_Lam = False

def GalshinLam():
    global Galashin_Lam
    Galashin_Lam = True
    GL_go.config(bg = '#009900')
    L_go.config(bg = '#ff0000')

def Leclerc():
    global Galashin_Lam
    Galashin_Lam = False
    GL_go.config(bg='#ff0000')
    L_go.config(bg='#009900')

GL = tk.Button(necklace_tab, text = 'Galashin Lam', command=GalshinLam)
GL.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.3)

L = tk.Button(necklace_tab, text = 'Leclerc', command=Leclerc)
L.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.35)

def string_to_num(s: str) -> int:
    t=0
    for j in range(len(s)):
        t+= int(s[::-1][j])*(10**j)
    return t

def string_to_list(s: str) -> list[int]:
    return [int(j) for j in s.split(',')]


def display_necklace():
    k = string_to_num(k_var.get())
    n = string_to_num(n_var.get())
    if w_var.get()[0].upper() == 'I':
        w =  string_to_list(w_var.get()[1:])
        w_expression = niave_expression(long_2(index_to_perm(w, n), k), n)
    else:
        w_expression = string_to_list(w_var.get())
    v = string_to_list(v_var.get())
    if Galashin_Lam:
        hold = v.copy()
        v = sorted(inv(flip(inv(simple_to_perm(w_expression, n)), n))[:k])
        w_expression = niave_expression(flip(inv(simple_to_perm(hold, n)), n), n)
    v_expression = niave_expression(long_2(index_to_perm(v, n), k), n)
    pi = proj_inj(v_expression, w_expression, n,show = False)
    J = necklace(pi, v)
    out = "The lift of Leclerc's projective injectives gives: \n"
    p = [f'M_{i}    ' for i in J]
    for i in sorted(list(set(p))):
        out += i
    out += f'( quotiented by M_{v})'

    w = simple_to_perm(w_expression, n)
    v_perm = simple_to_perm(v_expression, n)

    out += "\n \nSerhiyenko, Sherman-Bennett and Williams give the necklace:\n"
    ssbw = s_sb_w(v, v_perm, w, n)
    f =  [f'M_{i}    ' for i in ssbw]
    for i in sorted(list(set(f))):
        out += i

    out += "\n \nThe standard necklace associated to (v,w) gives:\n"
    ne = perm_necklace(v, v_perm, w, n)
    r = [f'M_{i}    ' for i in ne]
    for i in sorted(list(set(r))):
        out += i

    out += "\n \nThe opposite necklace for (v,w) gives:\n"
    ne1 = perm_necklace(v, v_perm, w, n, flip = True)
    t = [f'M_{i}    ' for i in ne1]
    for i in sorted(list(set(t))):
        out += i

    m = matroid(ne)

    out += "\n \nThe postroid associated to the standard necklace is:\n"
    P = [a for a in m if all([weakly_seperated(a,b) for b in ne])]
    post = [f'M_{i}    ' for i in P]
    for i in sorted(list(set(post))):
        out += i

    out += "\n \nThe GI positroid associated to the opposite necklace is:\n"
    H = opp(matroid)(ne1)
    V = [a for a in H if all([weakly_seperated(a, b) for b in ne1])]
    opost = [f'M_{i}    ' for i in V]
    for i in sorted(list(set(opost))):
        out += i



    txt = tk.Text(necklace_tab)
    txt.place(relx = 0, rely = 0.4, relwidth= 0.9, relheight=0.6)
    txt.insert(tk.END, out)



compute = tk.Button(necklace_tab, text = 'Give me my modules', command=display_necklace, width = 10, height = 1)
compute.place(relx=0.6, rely = 0.3, relwidth=0.2, relheight=0.03)



### Tilting tab:


frame3 = tk.Frame(tilting_tab, bg = '#ffffff')
frame3.place(relx = 0, rely=0, relwidth=1, relheight=1)

label = Label(tilting_tab, text = 'Kwivah', style = 'New.TLabel', background='#0f0f0f', foreground = '#999966')
label.grid()
label.place(relx=0, rely = 0, relwidth=1, relheight=0.1)

def dark_mode():
    frame1.config(bg = '#000000')
    frame2.config(bg = '#000000')
    frame3.config(bg = '#000000')

def light_mode():
    frame1.config(bg = '#fefefe')
    frame2.config(bg = '#fefefe')
    frame3.config(bg = '#fefefe')

buttn_dark = tk.Button(tilting_tab, text = 'Dark Mode', command=dark_mode, width= 10, height = 1)
buttn_dark.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.2)

buttn_light = tk.Button(tilting_tab, text = 'Light Mode', command=light_mode, width = 10, height = 1)
buttn_light.place(relwidth = 0.1, relheight=0.05, relx = 0.05, rely = 0.25)

Grassmannian1_description = Label(tilting_tab, text='We are in Gr(k,n). Enter k,n:', style='New3.TLabel', background='#999966')
Grassmannian1_description.place(relx=0.25, rely = 0.2, relwidth=0.15, relheight=0.03)

k1_entry = Entry(tilting_tab, width = 3, style='entry.TEntry', textvariable=k_var)
k1_entry.place(relx=0.4, rely = 0.2, relwidth=0.05, relheight=0.03)

n1_entry = Entry(tilting_tab, width = 3, style='entry.TEntry', textvariable=n_var)
n1_entry.place(relx=0.45, rely = 0.2, relwidth=0.05, relheight=0.03)

V1_description = Label(tilting_tab, text='Enter the k-index v', style='New3.TLabel', background='#999966')
V1_description.place(relx=0.25, rely = 0.25, relwidth=0.15, relheight=0.03)

v1_entry = Entry(tilting_tab, width = 3, style='entry.TEntry', textvariable=v_var)
v1_entry.place(relx=0.4, rely = 0.25, relwidth=0.05, relheight=0.03)

W1_description = Label(tilting_tab, text='Enter reduced expression for w', style='New3.TLabel', background='#999966')
W1_description.place(relx=0.25, rely = 0.3, relwidth=0.15, relheight=0.03)

w1_entry = Entry(tilting_tab, width = 3, style='entry.TEntry', textvariable=w_var)
w1_entry.place(relx=0.4, rely = 0.3, relwidth=0.2, relheight=0.03)


def display_tilting():
    k = string_to_num(k_var.get())
    n = string_to_num(n_var.get())
    if w_var.get()[0].upper() == 'I':
        w = string_to_list(w_var.get()[1:])
        w_expression = niave_expression(long_2(index_to_perm(w, n), k), n)
    else:
        w_expression = string_to_list(w_var.get())
    v = string_to_list(v_var.get())
    J = tilter(v, w_expression, k, n)
    out = f"Leclerc's tilting algorithm for this choice of reduced expression for w gives us: \n \n "
    p = [f'M_{i}    ' for i in J]
    for i in sorted(list(set(p))):
        out += i
    out += f'(quotiented by M_{v})'
    txt = tk.Text(tilting_tab)
    txt.place(relx = 0, rely = 0.4, relwidth= 0.9, relheight=0.6)
    txt.insert(tk.END, out)



compute = tk.Button(tilting_tab, text = 'Give me my tilting modules', command=display_tilting, width = 10, height = 1)
compute.place(relx=0.6, rely = 0.3, relwidth=0.2, relheight=0.03)



def kwivah_application():
    root.mainloop()