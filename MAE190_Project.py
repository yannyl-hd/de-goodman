from tkinter import *
from tkinter import ttk
import json
import math

# -----------------------MATERIALS ------------------------------------
f = open('ASTM.json')
astm_data = json.load(f)
f.close()

material_options = []

for i in astm_data['ASTM']:
    aisi_number = i['AISI']
    if 'HR' in i:
        material_options.append(f"AISI {aisi_number} HR")
    if 'CD' in i:
        material_options.append(f"AISI {aisi_number} CD")

reliability_options = [50, 90, 95, 99, 99.9, 99.99, 99.999, 99.9999 ]


#-------------------------------GUI STUFF------------------------------
root = Tk()
root.title("Shaft Dimension Design")
select_material = StringVar()
select_material.set(material_options[0])
frm =ttk.Frame(root,padding=15)
style = ttk.Style()
style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
style.configure("notice.Label", font=("Arial", 8), foreground="red")
style.configure("result.Label", font =("Arial", 8, "bold"))

diameter_result = StringVar()
diameter_result.set("The minimum diameter is -- inches.")
large_diam = StringVar()
large_diam.set("The larger diameter D is -- inches")


def getStrength():
    selected = select_material.get()
    parts = selected.split()
    aisi = parts[1] 
    condition = parts[2]

    for material in astm_data['ASTM']:
        if material['AISI'] == aisi and condition in material:
            tensile = material[condition][0]['Tensile Strength']
            yields = material[condition][0]['Yield Strength']
            return tensile, yields, condition
        
select_reliability = StringVar()
select_reliability.set(reliability_options[0])

def getReliability():
    selected = select_reliability.get()
    return selected


usergroup = ttk.LabelFrame(root, text ='Material Properties:', style = "TLabelframe")
usergroup.grid(column =0, row =0, padx=10, pady =10, sticky="nswe")

actingforcesgroup =ttk.LabelFrame(root, text ='Acting Forces:', style = "TLabelframe")
actingforcesgroup.grid(column = 1, row = 0, padx=10, pady =10, sticky="nswe")

ratiogroup = ttk.LabelFrame(root, text ='Diameter Relations:', style = "TLabelframe")
ratiogroup.grid(column = 2, row = 0, padx=10, pady =10, sticky="nswe")

buttongroup =  ttk.LabelFrame(root, text = 'Results:')
buttongroup.grid(column = 0, row = 1, padx=10, pady =10, sticky="ew", columnspan= 3)


#Material Combobox
ttk.Label(usergroup, text="AISI Material type:").grid(column =0, row = 0)
material_combobox = ttk.Combobox(usergroup, textvariable=select_material, values=material_options)
material_combobox.grid(column=0, row=1, padx =10, pady=10) 
material_combobox.current(0)
material_combobox.bind('<<ComboboxSelected>>', lambda event: getStrength())  

#Material Reliability
ttk.Label(usergroup, text="Reliability (%):").grid(column = 0, row =2)
reliability_combobox =ttk.Combobox(usergroup, textvariable=select_reliability, values= reliability_options)
reliability_combobox.grid(column=0, row=3, padx =10, pady=10)
reliability_combobox.current(0)
reliability_combobox.bind('<<ComboboxSelected>>', lambda event: getReliability())

#Mean Torsion
ttk.Label(actingforcesgroup, text="Mean Torsion (lbin):").grid(column=2, row = 0,padx=10)
tm = StringVar()
Tm = ttk.Entry(actingforcesgroup, textvariable=tm).grid(column=2, row =1, padx=15, pady = 10)

#Alternating Torsion
ttk.Label(actingforcesgroup, text = "Alternating Torsion (lbin):").grid(column=2,row=2,padx=10)
ta = StringVar()
Ta = ttk.Entry(actingforcesgroup,textvariable=ta).grid(column=2, row=3, pady=10)

#Mean Moment
ttk.Label(actingforcesgroup, text ="Mean Moment (lbin):").grid(column =2, row = 4)
mm = StringVar()
Mm = ttk.Entry(actingforcesgroup, textvariable= mm).grid(column = 2, row = 5, pady=10)

#Alternating Moment
ttk.Label(actingforcesgroup, text ="Alternating Moment (lbin):").grid(column =2, row = 6)
ma = StringVar()
Mm = ttk.Entry(actingforcesgroup, textvariable= ma).grid(column = 2, row = 7, pady=10)

#Factor of Safety
ttk.Label(usergroup, text ="Factor of Safety:").grid(column = 0, row = 4)
fos = StringVar()
FoS =ttk.Entry(usergroup, textvariable= fos).grid(column = 0, row = 5,pady=10)

#D/d ratio
ttk.Label(ratiogroup, text ="D/d Ratio: ").grid(column = 0, row = 0)
dd = StringVar(value="1.2")
Dd =ttk.Entry(ratiogroup, textvariable= dd).grid(column = 0, row = 1,pady=10, padx= 10)

#r/d ratio
ttk.Label(ratiogroup, text ="Fillet Radius Ratio (r/d): ").grid(column = 0, row = 2)
rd = StringVar(value="0.1")
Rd =ttk.Entry(ratiogroup, textvariable= rd).grid(column = 0, row = 3,pady=10, padx= 10)

ttk.Label(ratiogroup, text = "NOTE: Please only use D/d", style = "notice.Label").grid(column =0, row = 4)
ttk.Label(ratiogroup, text = "values between 2 - 1.09", style = "notice.Label").grid(column =0, row = 5)

#------------------ Code to find Min Diameter ---------------------------------------------------------------------
def calculate_diameter():
    # Get the material strength and reliability
    tensile_strength, yield_strength, material_condition = getStrength()  # Unpack the tuple returned by getStrength
    reliability = float(getReliability())  # Convert reliability to float for calculations

    # Get the values from the Entry widgets
    try:
        tmean = float(tm.get()) if tm.get() else 0.0
        talt = float(ta.get()) if ta.get() else 0.0
        mmean = float(mm.get()) if mm.get() else 0.0
        malt = float(ma.get()) if ma.get() else 0.0
        fas = float(fos.get()) if fos.get() else 0.0
        d_d_ratio = float(dd.get()) if dd.get() else 0.0
        r_d_ratio = float(rd.get()) if rd.get() else 0.0
    except ValueError:
        print("Please enter valid numbers")
        return  # Exit the function if there's a ValueError


    print(f"Tensile Strength: {tensile_strength}, Yield Strength: {yield_strength}, Reliability: {reliability}, Condition: {material_condition}")

    #INITIAL CALCULATION OF d
    Se_prime = 0.5*tensile_strength
    Sut = tensile_strength

    if material_condition == "HR":
        ka = 14.4*(tensile_strength)**-0.718
    elif material_condition == "CD":
        ka = 2.7*(tensile_strength)**-0.265
    
    kb = 0.85

    if reliability == 50.0:
        ke = 1
    elif reliability == 90.0:
        ke = 0.897
    elif reliability == 95.0:
        ke = 0.868
    elif reliability == 99.0:
        ke = 0.814
    elif reliability == 99.9:
        ke = 0.753
    elif reliability == 99.99:
        ke = 0.702
    elif reliability == 99.999:
        ke = 0.659
    elif reliability == 99.9999:
        ke = 0.620

    Se = ka*kb*ke*Se_prime
    kt = 0.97098*(r_d_ratio)**-0.21796
    kts = 0.83425*(r_d_ratio)**-0.21542

    #FINDING Kt VALUE
    Ddb = [2,1.5,1.2,1.1,1.07]
    Ab = [0.90879, 0.93836, 0.97098, 0.95120, 0.97527]
    bb = [-0.28598, -0.25759, -0.21796, -0.23757, -0.20958]

    Ddt = [2, 1.33, 1.2, 1.09]
    At = [ 0.86331, 0.84897, 0.83425, 0.90337]
    bt = [-0.23865, -0.23161, -0.21649, -0.12692]

    count = 0
    for i in Ddb:
        if i <= d_d_ratio:
            x0 = i
            break
        count += 1  
    
    y0 = Ab[count]
    x1 = Ddb[count - 1]
    y1 = Ab[count -1]
    x = d_d_ratio
    y0b = bb[count]
    y1b = bb[count-1]

    a = y0 + ((x-x0)*(y1-y0))/(x1 - x0)
    b = y0b + ((x-x0)*(y1b-y0b))/(x1 - x0)
    kt = a*r_d_ratio**b                           # <---- KT VALUE

    count = 0
    for i in Ddt:
        if i <= d_d_ratio:
            x0 = i
            break
        count += 1  
    
    y0 = At[count]
    x1 = Ddt[count - 1]
    y1 = At[count -1]
    x = d_d_ratio
    y0b = bt[count]
    y1b = bt[count-1]

    at = y0 + ((x-x0)*(y1-y0))/(x1 - x0)
    btt = y0b + ((x-x0)*(y1b-y0b))/(x1 - x0)
    kts = at*r_d_ratio**btt                         # <--- KTS VALUE
    
    Kf = kt
    Kfs = kts

    d = (((16*fas)/math.pi)*((1/(Se*(10**3))*(4*(Kf*malt)**2 + 3*(Kfs*talt)**2)**0.5 + (1/(tensile_strength**3))*(4*(Kf*mmean)**2 + 3*(Kfs*tmean)**2)**0.5)))**(1/3)
    a_bending = (0.246 - 3.08*(10**-3)*Sut + 1.51*(10**-5)*(Sut**2) - 2.67*(10**-8)*(Sut**3))
    a_torsion = (0.190 - 2.51*(10**-3)*Sut + 1.53*(10**-5)*(Sut**2) - 2.67*(10**-8)*(Sut**3))
    
    conv =1
    while conv >= 0.01:
        kb = (d/0.3)**(-0.107)
        r = r_d_ratio*d
        q = 1/(1+(a_bending)/math.sqrt(r))
        qs = 1/(1+(a_torsion)/math.sqrt(r))
        Kf = 1 + q*(kt - 1)
        Kfs = 1 + qs*(kts - 1)
        Se = Se_prime*ka*kb*ke
        do = d
        d = (((16*fas)/math.pi)*((1/(Se*(10**3))*(4*(Kf*malt)**2 + 3*(Kfs*talt)**2)**0.5 + (1/(tensile_strength**3))*(4*(Kf*mmean)**2 + 3*(Kfs*tmean)**2)**0.5)))**(1/3)
        conv = abs(d - do)/d

    result_D = d*d_d_ratio
    fillet_r = r_d_ratio*d

    #CHECK FOR YIELDING

    diameter_result.set(f"The minimum diameter is {d:.2f} inches.")
    large_diam.set(f"The larger diameter D is {result_D:.2f} inches with a fillet radius of {fillet_r:.2f}.")


#------------------------------------- DISPLAY RESULTS------------------------------------------
ttk.Button(ratiogroup, text = "Calculate",  command=calculate_diameter).grid(column = 0, row = 6, pady = 20, padx = 10)

ttk.Label(buttongroup, textvariable= diameter_result, style = "result.Label").grid( column=1, row= 4, padx = 5)
ttk.Label(buttongroup, textvariable= large_diam).grid( column=1, row= 5, padx = 10)
root.mainloop()



