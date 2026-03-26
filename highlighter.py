import tkinter as tk
import re # pattern matching to find keywords in text

# keywords to flag and highlight
keywords = ["one party", "terminate", "termination", "fee", "fees", 
            "renewal", "automatic", "limitation", "ownership"]

root = tk.Tk()
root.geometry('500x450')

title = tk.Label(root, text="Paste your terms and conditions below:")
title.pack() # puts title at the top

# text box
text_box = tk.Text(root, wrap=tk.WORD, height=10)
text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# text wraps at the end of the text box and is spaced along the outside

# highlight style
text_box.tag_config("highlight", background="yellow")

def highlight_text():
    # clears previous highlights
    text_box.tag_remove("highlight", "1.0", tk.END)
    # gets all text from box
    content = text_box.get("1.0", tk.END)

    for word in keywords:
        pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
        # matches word regardless of capital case

        # finds every occurance of the word and highlights
        for match in pattern.finditer(content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            text_box.tag_add("highlight", start, end)

# button to highlight
highlight_button = tk.Button(root, text="Highlight Keywords", command=highlight_text)
highlight_button.pack(pady=5)

root.mainloop()
