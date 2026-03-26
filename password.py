import tkinter as tk
import string

saved_password = None 

#defines the variables for a strong password 
def is_strong_password(password):
    length_ok = len(password) >=10 
    has_upper = any(c.isupper() for c in password) 
    has_lower = any(c.islower() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password) 

    return length_ok and has_upper and has_lower and has_digits and has_special

#stores and checks password. adds scores to determine strength level
def check_password(sv):
    password=sv.get()
    
    if len(password) == 0: #resets screen to blank, so labels don't stay after user resets
        save_stringvar.set("")
        
    length_ok = len(password) >=10
    has_upper = any(c.isupper() for c in password) 
    has_lower = any(c.islower() for c in password) 
    has_digits = any(c.isdigit() for c in password) 
    has_special = any(c in string.punctuation for c in password) 
    
    score = 0
    if length_ok:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digits:
        score += 1
    if has_special:
        score += 1
    
    #tells user if their password is weak, medium, or strong
    if len(password) == 0:
        result_stringvar.set("")
        result_label.config(fg="black")
    elif score <= 2:
        result_stringvar.set("Weak password")
        result_label.config(fg="red")
    elif score <= 4:
        result_stringvar.set("Medium password")
        result_label.config(fg="orange")
    else:
        result_stringvar.set("Strong password")
        result_label.config(fg="green")
    
    #if not strong, specifies what is needed to make password strong
    details = []
    if not length_ok:
        details.append("Needs at least 10 characters")
    if not has_upper:
        details.append("Needs a capital letter")
    if not has_lower:
        details.append("Needs a lowercase letter")
    if not has_digits:
        details.append("Needs a number")
    if not has_special:
        details.append("Needs a special character")
    
    #hides missing requirements when box is empty
    if len(password) == 0:
        rules_stringvar.set("")
    elif len(details) == 0:
        rules_stringvar.set("Meets all requirements")
    else:
        rules_stringvar.set(" and ".join(details))

#hides or shows password based on user preference
def toggle_password():
    if entry.cget("show") == "*":
        entry.config(show="")
        show_button.config(text="Hide password")
    else:
        entry.config(show="*")
        show_button.config(text="Show password")

#stores password and either saves or doesn't save password depending on strength
def save_password(event=None):
    global saved_password
    password = sv.get()
    
    if is_strong_password(password):
        saved_password = password
        save_stringvar.set("Password saved successfully")
        save_label.config(fg="green")
    else:
        save_stringvar.set("Password not saved. Must meet all requirements first.")
        save_label.config(fg="red")

#design basis: controls colours, windows, text settings        
root = tk.Tk()
root.geometry('600x600')
root.configure(bg="white")

frame = tk.Frame(root)
frame.pack()

instruction_label = tk.Label(root, bg='white', text="Type Password Below:")
instruction_label.pack()

result_stringvar = tk.StringVar()
result_label = tk.Label(root, textvariable=result_stringvar, font=("Arial", 14), bg="white")
result_label.pack(pady=10)

rules_stringvar = tk.StringVar()
rules_label = tk.Label(root, textvariable=rules_stringvar, bg="white", justify="left")
rules_label.pack()

save_stringvar = tk.StringVar()
save_label = tk.Label(root, textvariable=save_stringvar, bg="white", font=("Arial", 12))
save_label.pack(pady=10)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: check_password (sv))

entry = tk.Entry(root, textvariable=sv, show="*")
entry.pack()
entry.bind("<Return>", save_password) #Press enter to save

show_button = tk.Button(root, text="Show password", command=toggle_password)
show_button.pack(pady=10)

root.mainloop()
