import tkinter as tk
from tkinter.ttk import Label, Style, Notebook, Entry
from tkinter import messagebox
from leclerc import necklace
from permutations import *
from leclerc import proj_inj, width_set

necklace_string = "Necklace:\nIn the Necklace tab we take a k-index and permutation w and produce a list " \
                  "of rank one modules whose projection under pi_v gives Leclerc's projective\n injective modules."
tilting_string = "Tilting:\nGiven v and w we perform steps of a algorithm contained in Leclerc's paper\n " \
                 "'Cluster structures on strata of flag varieties' to help describe a cluster \n" \
                 "tilting object in his category C_{v,w}."


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
tilting = tk.Frame(tabControl)
tabControl.add(home_tab, text='Home')
tabControl.add(necklace_tab, text = 'Necklaces')
tabControl.add(tilting, text = 'Tilting modules')
tabControl.pack(expand=1, fill="both")

### Insert stylings
style = Style(root)
style.configure('New.TLabel', font = ('Great Vibes', 30))
style.configure('New2.TLabel', font=('Great Vibes', 25))
style.configure('New3.TLabel', font=('Great Vibes', 10))
style.configure('entry.TEntry', padding = [15,0,0,0])


###Home tab:
frame1 = tk.Frame(home_tab, bg = '#ffffff')
frame1.place(relx = 0, rely=0, relwidth=1, relheight=1)

label = Label(home_tab, text = 'Kwivah', style = 'New.TLabel', background='#0f0f0f', foreground = '#999966')
label.grid()
label.place(relx=0, rely = 0, relwidth=1, relheight=0.1)

def dark_mode():
    frame1.config(bg = '#000000')

def light_mode():
    frame1.config(bg = '#fefefe')

btn_dark = tk.Button(home_tab, text = 'Dark Mode', command=dark_mode, width= 10, height = 1)
btn_dark.place(x = 25, y = 120)

btn_light = tk.Button(home_tab, text = 'Light Mode', command=light_mode, width = 10, height = 1)
btn_light.place(x = 25, y=145)

label2 = Label(frame1, text = "Welcome to Kwivah: \nLet's have a look at what we can do in here.", style = 'New2.TLabel', background='#999966')
label2.place(relx=0.3, rely = 0.2, relwidth=0.4, relheight=0.1)

label3 = Label(frame1, text = necklace_string, style='New3.TLabel', background='#999966')
label3.place(relx=0.25, rely = 0.4, relwidth= 0.5, relheight=0.05)

def necklace_display():
    messagebox.showinfo(title = 'Necklace info', message=necklace.__doc__)

display_more = tk.Button(home_tab, text='Tell me more!', command=necklace_display, width = 15, height = 1)
display_more.place(x = 1450, y = 430)


###Necklace tab:

frame2 = tk.Frame(necklace_tab, bg = '#ffffff')
frame2.place(relx = 0, rely=0, relwidth=1, relheight=1)

label = Label(necklace_tab, text = 'Kwivah', style = 'New.TLabel', background='#0f0f0f', foreground = '#999966')
label.grid()
label.place(relx=0, rely = 0, relwidth=1, relheight=0.1)

def dark_mode():
    frame2.config(bg = '#000000')

def light_mode():
    frame2.config(bg = '#fefefe')

bttn_dark = tk.Button(necklace_tab, text = 'Dark Mode', command=dark_mode, width= 10, height = 1)
bttn_dark.place(x = 25, y = 120)

bttn_light = tk.Button(necklace_tab, text = 'Light Mode', command=light_mode, width = 10, height = 1)
bttn_light.place(x = 25, y=145)

Grassmannian_description = Label(necklace_tab, text='We are in Gr(k,n). Enter k,n:', style='New3.TLabel', background='#999966')
Grassmannian_description.place(relx=0.3, rely = 0.2, relwidth=0.09, relheight=0.03)

k_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=k_var)
k_entry.place(relx=0.4, rely = 0.2, relwidth=0.05, relheight=0.03)

n_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=n_var)
n_entry.place(relx=0.45, rely = 0.2, relwidth=0.05, relheight=0.03)

V_description = Label(necklace_tab, text='Enter the k-index v', style='New3.TLabel', background='#999966')
V_description.place(relx=0.3, rely = 0.25, relwidth=0.09, relheight=0.03)

v_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=v_var)
v_entry.place(relx=0.4, rely = 0.25, relwidth=0.05, relheight=0.03)

W_description = Label(necklace_tab, text='Enter a simple filtration for w', style='New3.TLabel', background='#999966')
W_description.place(relx=0.3, rely = 0.3, relwidth=0.09, relheight=0.03)

w_entry = Entry(necklace_tab, width = 3, style='entry.TEntry', textvariable=w_var)
w_entry.place(relx=0.4, rely = 0.3, relwidth=0.2, relheight=0.03)

GL_go = tk.Label(necklace_tab, bg = '#ff0000')
GL_go.place(x = 400, y = 145, width = 20, height = 20)

L_go = tk.Label(necklace_tab, bg = '#009900')
L_go.place(x = 400, y = 180, width = 20, height = 20)


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


def Help():
    messagebox.showinfo(title = "What's going on?", message="In Leclerc's convention, a Grassmannian positroid"
                                                            " corresponds to a pair (v,w) with v = w^{K}_0 u and w greater"
                                                            " than or equal to v. In Galashin and Lam's convention they"
                                                            " use pairs (v,w) where w is a minimal length"
                                                            " representative for a coset W/W^{K}. Our standard is Leclerc's "
                                                            " but if you want to use Galashin and Lam's then just enter a simple "
                                                            " filtration for v,w and make sure your convention 'button' is set"
                                                            " to Galashin Lam.")

GL = tk.Button(necklace_tab, text = 'Galashin Lam', command=GalshinLam, width = 10, height = 1)
GL.place(x = 300, y=145)

L = tk.Button(necklace_tab, text = 'Leclerc', command=Leclerc, width = 10, height = 1)
L.place(x = 300, y=180)

Help = tk.Button(necklace_tab, text = 'What?', command=Help, width = 10, height = 1)
Help.place(x = 300, y=215)

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
    w_expression = string_to_list(w_var.get())
    v = string_to_list(v_var.get())
    if Galashin_Lam:
        hold = v.copy()
        v = sorted(inv(flip(simple_to_perm(w_expression, n), n))[:k])
        w_expression = niave_expression(flip(simple_to_perm(hold, n), n), n)
    v_expression = niave_expression(long_2(index_to_perm(v, n), k), n)
    pi = proj_inj(v_expression, w_expression, n,show = False)
    widths = width_set(w_expression, k, n)
    J = necklace(pi, v, widths)
    out = ''
    p = [f'M_{i}    ' for i in J]
    for i in list(set(p)):
        out += i
    out += f'( quotiented by M_{v})'
    txt = tk.Text(necklace_tab)
    txt.place(relx = 0, rely = 0.6, relwidth= 0.9, relheight=0.25)
    txt.insert(tk.END, out)



compute = tk.Button(necklace_tab, text = 'Give me my modules', command=display_necklace, width = 10, height = 1)
compute.place(relx=0.6, rely = 0.3, relwidth=0.2, relheight=0.03)



### Tilting tab:





def kwivah_application():
    root.mainloop()

