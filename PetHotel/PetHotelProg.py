import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import tkinter.font as tkfont
from datetime import datetime
import pickle
import hashlib

# Globals:
customer_file = "Database/customers.pkl"
pet_file = "Database/pets.pkl" 
# These must exist in this folder, as it assumes they exist. In a real scenario, they would.
booking_file = "Database/bookings.pkl"
archived_booking_file = "Database/archived_bookings.pkl"
all_rooms = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"] # Global containing all available rooms. In a real scenario, this would be replaced by accurate room names. 
customers = []
pets = []
bookings = []
archived_bookings = []

# Appearance Globals:
prog_colour = "#2E2E2E"
bg_colour = "#2E2E2E"
txt_colour = "#FFFFFF"
system_font = "Arial"
font_size = 12
cust_search_menu = False
pet_search_menu = False
booking_search_menu = False

# Classes for Customer, Pets and Bookings. Important for dictating the format used for the lists. Values each holds are as seen.
class Customer:
    def __init__(self, customer_id, fname, sname, address, postcode, email, phonenum):
        self.id = customer_id
        self.fname = fname
        self.sname = sname
        self.address = address
        self.postcode = postcode
        self.email = email
        self.phonenum = phonenum

class Pet:
    def __init__(self, pet_id, name, age, species, description, diet, add_info):
        self.id = pet_id
        self.name = name
        self.age = age
        self.species = species
        self.description = description
        self.diet = diet
        self.add_info = add_info

class Booking:
    def __init__(self, booking_id, pet_id, customer_id, sdate, edate, dropoff, collect, room):
        self.id = booking_id
        self.pet_id = pet_id
        self.cust_id = customer_id
        self.sdate = sdate
        self.edate = edate
        self.dropoff = dropoff
        self.collect = collect
        self.room = room

# Styling function, which is called for every window to apply the correct style. Important for enforcing user changes from the settings menu. 
def apply_style(window):
    #Uses a base ttk style to fall back on at the start, and edits that.
    style = ttk.Style()
    style.theme_use('clam')

    #The aspects that are configured using the globals edited from the settings menu. Allows for changes to immediately come into effect.
    style.configure("TFrame", background=prog_colour)
    style.configure("TLabel", background=prog_colour, foreground=txt_colour, font=(system_font, font_size))
    style.configure("TButton", background=prog_colour, foreground=txt_colour, font=(system_font, font_size), padding=5)
    style.configure("TEntry", fieldbackground=bg_colour, foreground=txt_colour, font=(system_font, font_size))
    style.configure("TOptionMenu", background=prog_colour, foreground=txt_colour, font=(system_font, font_size))
    style.configure("Error.TLabel", foreground="red", font=("Helvetica", font_size, "bold"))
    style.configure("Edit.TButton", background="#5081e4", font=(system_font, font_size))
    style.configure("Delete.TButton", background="#d15156", font=(system_font, font_size))
    style.configure("TCombobox", fieldbackground=bg_colour, background=prog_colour, foreground=txt_colour, font=(system_font, font_size))
    window.configure(background = bg_colour)

    #Setting the window size to be 75% of the screen, and placing it in the centre. Prevents program from moving around between opening and closing windows.
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width * 0.75)
    window_height = int(screen_height * 0.65)
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2) - 50
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.minsize(800,600) #Prevents window becoming too small

    # Make all rows and columns expand by default
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Print the applied styles, used when I was having difficulty in applying them. Debugging.
    # print(f"Styles applied: prog_colour={prog_colour}, bg_colour={bg_colour}, txt_colour={txt_colour}")

# Function which inserts the logo to any page it is called on. Used both in the Password and Main Menu, but can be used elsewhere if needed in future. 
def insert_image(window):
    try:
        img = tk.PhotoImage(file="logo.png")
    except Exception:
        print("Image failed to load.")
        return # Quit so it doesn't try to do the following.

    img_label = tk.Label(window, image=img)
    img_label.grid(row=0, column=0, padx=20, pady=20)
    img_label.image = img

# Load and Save functions for customers, pets and bookings. Handles scenarios where files do not exist, although this isn't recommended and should never occur under normal use.
def load_pets():
    global pets
    try:
        with open(pet_file, "rb") as file:
            pets = pickle.load(file)
    except (FileNotFoundError, EOFError):
        pets = []

def save_pets():
    with open(pet_file, "wb") as file:
        pickle.dump(pets, file)

def load_customers():
    global customers
    try:
        with open(customer_file, "rb") as file:
            customers = pickle.load(file)
    except (FileNotFoundError, EOFError):
        customers = []

def save_customers():
    with open(customer_file, "wb") as file:
        pickle.dump(customers, file)

def load_bookings():
    global bookings
    try:
        with open(booking_file, "rb") as file:
            bookings = pickle.load(file)
    except (FileNotFoundError, EOFError):
        bookings = []

def save_bookings():
    with open(booking_file, "wb") as file:
        pickle.dump(bookings, file)

def load_archive_bookings():
    global archived_bookings
    try:
        with open(archived_booking_file, "rb") as file:
            archived_bookings = pickle.load(file)
    except (FileNotFoundError, EOFError):
        archived_bookings = []

def save_archive_bookings():
    with open(archived_booking_file, "wb") as file:
        pickle.dump(archived_bookings, file)

# Main Menu. Contains buttons to the other menus. Also loads the relevant lists into memory/program, as each page needs them when creating. 
def mainMenu():
    load_customers()
    load_pets()
    load_bookings()

    mainMenuW = tk.Tk()
    mainMenuW.title("Main Menu")
    apply_style(mainMenuW)
    insert_image(mainMenuW)

    custB = ttk.Button(mainMenuW,text="Customers", command=lambda: openCustMenu(mainMenuW))
    petsB = ttk.Button(mainMenuW,text="Pets", command=lambda: openPetMenu(mainMenuW))
    bookB = ttk.Button(mainMenuW,text="Bookings", command=lambda: openBookMenu(mainMenuW))
    scheduleB = ttk.Button(mainMenuW,text="Schedule", command=lambda: openScheduleMenu(mainMenuW))
    settingsB = ttk.Button(mainMenuW,text="⚙️", command=lambda: openSettingsMenu(mainMenuW)) # Emoticon used for easier recognition and visual design, as went over in design.
    custB.grid(row=1, column=0, ipadx=40, ipady=20, pady=10, padx=10, sticky='ew')
    petsB.grid(row=2, column=0, ipadx=40, ipady=20, pady=10, padx=10, sticky='ew')
    bookB.grid(row=3, column=0, ipadx=40, ipady=20, pady=10, padx=10, sticky='ew')
    scheduleB.grid(row=4, column=0, ipadx=40, ipady=20, pady=10, padx=10, sticky='ew')
    settingsB.grid(row=4, column=1, ipadx=20, ipady=10, padx=20, pady=20, sticky="se") # Sticky controls which side the buttons stay to.
    mainMenuW.mainloop()

# Customer Menu. Must move start and end positions around, as only 10 entries of the list are shown at once, using the next and previous buttons. Requires the list to be refreshed each time. 
def custMenu():
    custMenuW = tk.Tk()
    custMenuW.title("Customers")
    apply_style(custMenuW)

    load_customers()
    start = 0
    end = 10

    # Recieves either -1 or 1 to go forward or backwards. 
    def changePage(pn):
        nonlocal start, end

        # Change the start and end correctly and in a simpler way.
        newstart = start + (pn * 10)
        newend = newstart + 10

        # Prevents errors by quitting before it can go out of bounds.
        if newstart >= len(customers):  
            return 
        if newstart < 0:
            return

        start = newstart
        end = newend
        update_cust()  # Updates list after changing pages. 

    def update_cust(fname=None, sname=None, address=None, postcode=None, email=None, phonenum=None): 
        # = None allows for having nothing passed in or passing them in. Useful for when no search is given.
        # Moved to menu. Used to be outside function. Lets me call update inside of it. 
        def delete_customers(index):
            cust_index = customers.index(results_customers[index])
            confirm = messagebox.askyesno("Delete Customer", f"Are you sure you want to delete {customers[cust_index].fname} {customers[cust_index].sname}?")
            if confirm:
                del customers[cust_index]
                save_customers()
                messagebox.showinfo("Deleted", "Customer was deleted successfully.")
                update_cust()

        resultFrame.grid(row=0, column=0, rowspan=10, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Clear any previous results
        for widget in resultFrame.winfo_children(): # Having a frame makes this easier, since I can just destroy everything attached to one. 
            widget.destroy()

        filtered_customers = []

        # Linear search through each customer and see if they match
        for customer in customers:
            match = True  # Fail condition

            # Manually check each search term (and case-insensitive)
            if fname and (fname.lower() not in customer.fname.lower()):
                match = False
            if sname and (sname.lower() not in customer.sname.lower()):
                match = False
            if address and (address.lower() not in customer.address.lower()):
                match = False
            if postcode and (postcode.lower() not in customer.postcode.lower()):
                match = False
            if email and (email.lower() not in customer.email.lower()):
                match = False
            if phonenum and (phonenum not in customer.phonenum):
                match = False

            # If the customer matches all conditions, add them to the filtered list to be shown
            if match:
                filtered_customers.append(customer)

        # If no search terms are provided, show all customers
        if not (fname or sname or address or postcode or email or phonenum):
            filtered_customers = customers

        # Splice the list to show only 10 entries at a time
        results_customers = filtered_customers[start:end]  # Now applies to both normal and filtered results

        # Display the filtered customers (split up if necessary)
        for i, customer in enumerate(results_customers): 
            # Enumerate returns something as separate objects. Here, it returns the filtered customers as objects with their own indexes, so I can show them.
            customerL = ttk.Label(resultFrame, text=f"{customer.fname} {customer.sname}") # Shows first and last name on page.
            customerL.grid(row=i, column=0, pady=2, padx=10, sticky="w")
            resultFrame.columnconfigure(1, weight=1)

            # Buttons for editing and deleting. Idx here keeps track of the i to use later if clicked on, as an index of that customer to be passed around. 
            custEditB = ttk.Button(resultFrame, text="∆", style="Edit.TButton", command=lambda idx=i: editCustomer(idx, custMenuW))
            custEditB.grid(row=i, column=2, sticky="e")
            custDelB = ttk.Button(resultFrame, text="➖", style="Delete.TButton", command=lambda idx=i: delete_customers(idx))
            custDelB.grid(row=i, column=3, sticky="e", padx=10, pady=10)

        # Disabled buttons if the end of the list is reached, so nothing unexpected happens. 
        if start > 0:
            prevB.config(state=tk.NORMAL) # Tk states must be capitialised.
        else:
            prevB.config(state=tk.DISABLED)

        if end < len(filtered_customers):
            nextB.config(state=tk.NORMAL)
        else:
            nextB.config(state=tk.DISABLED)

    # Search menu which pops up in the corner after pressing the search button.
    def searchMenu():
        global cust_search_menu

        if cust_search_menu == False: # Global not ideal, but using alternative would have been too difficult and time consuming. Global unimportant so not very bad, and am unlikely to name a variable this name. 
            searchFrame.grid(row=0, column=5, rowspan=7, padx=10, pady=10)
            searchLab = ttk.Label(searchFrame, text="Search Options")
            fnameLab = ttk.Label(searchFrame, text="First Name: ")
            fnameEntry = ttk.Entry(searchFrame)
            snameLab = ttk.Label(searchFrame, text="Surname: ")
            snameEntry = ttk.Entry(searchFrame)
            addressLab = ttk.Label(searchFrame, text="Address: ")
            addressEntry = ttk.Entry(searchFrame)
            postcodeLab = ttk.Label(searchFrame, text="Postcode: ")
            postcodeEntry = ttk.Entry(searchFrame)
            emailLab = ttk.Label(searchFrame, text="Email: ")
            emailEntry = ttk.Entry(searchFrame)
            phonenumLab = ttk.Label(searchFrame, text="Phone Number: ")
            phonenumEntry = ttk.Entry(searchFrame)
            searchButton = ttk.Button(searchFrame, text="🔍", command = lambda: update_cust(fnameEntry.get().strip(), snameEntry.get().strip(), addressEntry.get().strip(), postcodeEntry.get().strip(), emailEntry.get().strip(), phonenumEntry.get().strip()))
            # Sends what you put into the entries, to search the list by in the update function. 
            searchLab.grid(row=0, column=0, columnspan=2, pady=5)
            fnameLab.grid(row=1, column=0, sticky="ne", padx=5)
            snameLab.grid(row=2, column=0, sticky="ne", padx=5)
            addressLab.grid(row=3, column=0, sticky="ne", padx=5)
            postcodeLab.grid(row=4, column=0, sticky="ne", padx=5)
            emailLab.grid(row=5, column=0, sticky="ne", padx=5)
            phonenumLab.grid(row=6, column=0, sticky="ne", padx=5)

            fnameEntry.grid(row=1, column=1, padx=5)
            snameEntry.grid(row=2, column=1, padx=5)
            addressEntry.grid(row=3, column=1, padx=5)
            postcodeEntry.grid(row=4, column=1, padx=5)
            emailEntry.grid(row=5, column=1, padx=5)
            phonenumEntry.grid(row=6, column=1, padx=5)
            searchButton.grid(row=7, column=1, padx=5)
            cust_search_menu = True # Toggles the menu being active or not, using said global.
        else:
            searchFrame.grid_forget()
            cust_search_menu = False

    # Frames are defined here but gridded/made visible when needed. Allows for better control over them. 
    searchFrame = ttk.Frame(custMenuW, padding="10", relief="solid", borderwidth=2)
    resultFrame = ttk.Frame(custMenuW, padding="10", relief="solid", borderwidth=2)
    searchcustB = ttk.Button(custMenuW, text="Search", command=lambda: searchMenu())
    addcustB = ttk.Button(custMenuW, text="Add Customer",command=lambda: addCustomer(custMenuW))
    mainmenuB = ttk.Button(custMenuW, text="Return",command=lambda: openMainMenu(custMenuW))
    prevB = ttk.Button(custMenuW, text = "◀", command= lambda: changePage(-1)) # Lets me go back and forth between pages using one function.
    prevB.grid(row = 11, column = 0, sticky="w", padx=10, pady=10)
    nextB = ttk.Button(custMenuW, text = "▶", command= lambda: changePage(1))
    nextB.grid(row = 11, column = 2, sticky="e", padx=10, pady=10)

    searchcustB.grid(row = 0, column = 3, sticky="nsew", padx=10, pady=10), addcustB.grid(row = 12, column = 0, pady = 10, padx = 10, sticky="nsew"), mainmenuB.grid(row = 12, column = 1, pady = 10, padx = 10, sticky="nsew")
    update_cust()
    custMenuW.mainloop()

# Pets Menu. Must move start and end positions around, as only 10 entries of the list are shown at once, using the next and previous buttons. Requires the list to be refreshed each time. 
def petMenu():
    petMenuW = tk.Tk()
    petMenuW.title("Pets")
    apply_style(petMenuW)

    load_pets()
    start = 0
    end = 10

    # Receives either -1 or 1 to go forward or backwards.
    def changePage(pn):
        nonlocal start, end

        # Change the start and end correctly and simpler.
        newstart = start + (pn * 10)
        newend = newstart + 10

        # Prevents errors by quitting before it can go out of bounds
        if newstart >= len(pets):
            return
        if newstart < 0:
            return

        start = newstart
        end = newend
        update_pet()  # Updates list after changing pages.

    def update_pet(name=None, species=None, age=None):
        def delete_pets(index):
            pet_index = pets.index(results_pets[index])
            confirm = messagebox.askyesno("Delete Pet", f"Are you sure you want to delete {pets[pet_index].name} {pets[pet_index].species}?")
            if confirm:
                del pets[pet_index]
                save_pets()
                messagebox.showinfo("Deleted", "Pet was deleted successfully.")
                update_pet()
        # = None allows for having nothing passed in, and passing them in. Useful for when no search is given.
        resultFrame.grid(row=0, column=0, rowspan=10, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Clear any previous results
        for widget in resultFrame.winfo_children():  # Having a frame makes this easier, since I can just destroy everything attached to one.
            widget.destroy()

        filtered_pets = []

        # Linear search through each pet and see if they match
        for pet in pets:
            match = True  # Fail condition

            # Manually check each search term (and case-insensitive)
            if name and (name.lower() not in pet.name.lower()):
                match = False
            if species and (species.lower() not in pet.species.lower()):
                match = False
            if age and (age != pet.age):
                match = False

            # If the pet matches all conditions, add them to the filtered list to be shown
            if match:
                filtered_pets.append(pet)

        # If no search terms are provided, show all pets
        if not (name or species or age):
            filtered_pets = pets

        # Splice the list to show only 10 entries at a time
        results_pets = filtered_pets[start:end]  # Now applies to both normal and filtered results

        # Display the filtered pets (split up if necessary)
        for i, pet in enumerate(results_pets):
            # Enumerate returns something as separate objects. Here, it returns the filtered pets as objects with their own indexes, so I can show them.
            petL = ttk.Label(resultFrame, text=f"{pet.name} ({pet.species})")
            petL.grid(row=i, column=0, pady=2, padx=10, sticky="w")

            resultFrame.columnconfigure(1, weight=1)

            # Buttons for editing and deleting. Idx here keeps track of the i to use later if clicked on, as an index of that pet to be passed around.
            petEditB = ttk.Button(resultFrame, text="∆", style="Edit.TButton", command=lambda idx=i: editPet(idx, petMenuW))
            petEditB.grid(row=i, column=2, sticky="e")
            petDelB = ttk.Button(resultFrame, text="➖", style="Delete.TButton", command=lambda idx=i: delete_pets(idx))
            petDelB.grid(row=i, column=3, sticky="e", padx=10, pady=10)

        # Disabled buttons if the end of the list is reached, so nothing unexpected happens.
        if start > 0:
            prevB.config(state=tk.NORMAL)
        else:
            prevB.config(state=tk.DISABLED)

        if end < len(filtered_pets):
            nextB.config(state=tk.NORMAL)
        else:
            nextB.config(state=tk.DISABLED)

    # Search menu which pops up in the corner after pressing the search button.
    def searchPetsMenu():
        global pet_search_menu

        if not pet_search_menu:
            searchFrame.grid(row=0, column=5, rowspan=7, padx=10, pady=10)
            searchLab = ttk.Label(searchFrame, text="Search Options")
            nameLab = ttk.Label(searchFrame, text="Name: ")
            nameEntry = ttk.Entry(searchFrame)
            speciesLab = ttk.Label(searchFrame, text="Species: ")
            speciesEntry = ttk.Entry(searchFrame)
            ageLab = ttk.Label(searchFrame, text="Age: ")
            ageEntry = ttk.Entry(searchFrame)
            searchButton = ttk.Button(searchFrame, text="🔍", command=lambda: update_pet(nameEntry.get().strip(), speciesEntry.get().strip(), ageEntry.get().strip()))
            # Sends what you put into the entries, to search the list by in the update function.
            searchLab.grid(row=0, column=0, columnspan=2, pady=5)
            nameLab.grid(row=1, column=0, sticky="ne", padx=5)
            speciesLab.grid(row=2, column=0, sticky="ne", padx=5)
            ageLab.grid(row=3, column=0, sticky="ne", padx=5)

            nameEntry.grid(row=1, column=1, padx=5)
            speciesEntry.grid(row=2, column=1, padx=5)
            ageEntry.grid(row=3, column=1, padx=5)
            searchButton.grid(row=4, column=1, padx=5)
            pet_search_menu = True  # Toggles the menu being active or not, using global, like the customer one.
        else:
            searchFrame.grid_forget()
            pet_search_menu = False

    # Frame and button creation and grid. Same reason as customer.
    searchFrame = ttk.Frame(petMenuW, padding="10", relief="solid", borderwidth=2)
    resultFrame = ttk.Frame(petMenuW, padding="10", relief="solid", borderwidth=2)
    searchpetB = ttk.Button(petMenuW, text="Search", command=lambda: searchPetsMenu())
    addpetB = ttk.Button(petMenuW, text="Add Pet", command=lambda: addPet(petMenuW))
    mainmenuB = ttk.Button(petMenuW, text="Return", command=lambda: openMainMenu(petMenuW))
    prevB = ttk.Button(petMenuW, text="◀", command=lambda: changePage(-1))
    nextB = ttk.Button(petMenuW, text="▶", command=lambda: changePage(1))

    prevB.grid(row=11, column=0, sticky="w", padx=10, pady=10)
    nextB.grid(row=11, column=2, sticky="e", padx=10, pady=10)
    searchpetB.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)
    addpetB.grid(row=12, column=0, pady=10, padx=10, sticky="nsew")
    mainmenuB.grid(row=12, column=1, pady=10, padx=10, sticky="nsew")

    update_pet()
    petMenuW.mainloop()

# These functions handle changing windows. Sub-windows are handled by Toplevel, but the "main" menus for each part of the program are their own Tk windows. They accept a former window and then send to the window the function is named after, allowing for closing and reopening wherever inside the program.
def openCustMenu(lastWindow):
    lastWindow.destroy()
    custMenu()

def openBookMenu(lastWindow):
    lastWindow.destroy()
    bookMenu()

def openPetMenu(lastWindow):
    lastWindow.destroy()
    petMenu()

def openMainMenu(lastWindow):
    lastWindow.destroy()
    mainMenu()
    
def openSettingsMenu(lastWindow):
    lastWindow.destroy()
    settings()

def openScheduleMenu(lastWindow):
    lastWindow.destroy()
    schedule()

# Customer validation, used by Add and Edit Customer pages. When editing, an id is passed in, but when creating a new entry, it is not needed. It also takes the window name and error labels, in order to output the correct errors to the correct window.  
def validateCustomer(fname, sname, address, postcode, email, phonenum, editing, fnameError, snameError, addressError, postcodeError, emailError, phonenumError, window, cust_id=None):
        # Creates customer object and appends it to the customer list, running save_ afterwards to save to file immediately. Success message is shown purely for users benefit, since it doesn't control anything.
        def submitCustomer(fname, sname, address, postcode, email, phonenum, window):
            customer_id = len(customers) + 1
            new_customer = Customer(
                customer_id,
                fname,
                sname,
                address,
                postcode,
                email,
                phonenum
            )
            customers.append(new_customer)
            save_customers()
            messagebox.showinfo("Success", "Customer added successfully")
            window.destroy()
        
        # Edits pre-existing customer object, running save afterwards to save to file immediately. Same reason for success message.
        def modifyCustomer(fname, sname, address, postcode, email, phonenum, cust_id, window):
            customers[cust_id].fname = fname
            customers[cust_id].sname = sname
            customers[cust_id].address = address
            customers[cust_id].postcode = postcode
            customers[cust_id].email = email
            customers[cust_id].phonenum = phonenum
            
            save_customers()
            messagebox.showinfo("Success", "Customer modified successfully")
            window.destroy()
            
        # Resets errors after running again, removing errors that no longer apply. Without this, errors would still persist even when no longer needed. 
        valid_failed = False
        Error_Message = ""
        fnameError.config(text="")
        snameError.config(text="")
        addressError.config(text="")
        postcodeError.config(text="")
        emailError.config(text="")
        phonenumError.config(text="")
        
        # Validation for each customer field, starting with presence. Due to elifs, the first error going down is the one used. I've attempted ordered them based on importance, although the next applicable error would be shown after one is fixed regardless.
        if not fname:
            valid_failed = True
            Error_Message += "First name required.\n"
            fnameError.config(text="Required.")
        elif len(fname) > 30:
            valid_failed = True
            Error_Message += "First name too long (over 30 characters).\n"
            fnameError.config(text="Over 30 characters.")
        elif not (fname.isalpha()):
            valid_failed = True
            Error_Message += "First name must contain only letters.\n"
            fnameError.config(text="Only letters.")

        if not sname:
            valid_failed = True
            Error_Message += "Surname required.\n"
            snameError.config(text="Required.")
        elif len(sname) > 30:
            valid_failed = True
            Error_Message += "Surname too long (over 30 characters).\n"
            snameError.config(text="Over 30 characters.")
        elif not (sname.isalpha()):
            valid_failed = True
            Error_Message += "Surname must contain only letters.\n"
            snameError.config(text="Only letters.")

        if not address:
            valid_failed = True
            Error_Message += "Address required.\n"
            addressError.config(text="Required.")
        elif len(address) >= 100:
           valid_failed = True
           Error_Message += "Address should not exceed 100 characters.\n"
           addressError.config(text="Should not exceed 100 characters.")
        elif len(address) < 5:
            valid_failed = True
            Error_Message += "Address must exceed 5 characters.\n"
            addressError.config(text="Must exceed 5 characters.")

        # Strict format check on the postcode. Format must match example exactly in regards to letters and numbers. 
        if not postcode:
            valid_failed = True
            Error_Message += "Postcode required.\n"
            postcodeError.config(text="Required.")
        else:
            try:
                if not ((postcode[0].isalpha() and postcode[1].isalpha() and postcode[6].isalpha() and postcode[7].isalpha() and postcode[2].isnumeric() and postcode[3].isnumeric() and postcode[5].isnumeric())) or (len(postcode)!=8):
                    valid_failed = True
                    Error_Message += "Postcode does not match format LL00 0LL.\n"
                    postcodeError.config(text="Does not match format LL00 0LL.")
            except Exception as error:
                valid_failed = True
                Error_Message += "Postcode does not match format LL00 0LL.\n"
                postcodeError.config(text="Does not match format LL00 0LL.")
        
        # Without internet connection, there is no way to check an email is valid. Checking its contents is the best solution, and this splits it in half to check for an @ and a "." for domain afterwards.
        # I've used "." since checking .co.uk or .com felt needlessly restricting, I don't know the types of emails being provided.     
        if not email:
            valid_failed = True
            Error_Message += "Email required.\n"
            emailError.config(text="Required.")
        elif not "@" in email:
            valid_failed = True
            Error_Message += "Email must contain an @.\n"
            emailError.config(text="Must contain an @.")
        else:
            start, domain = email.split("@", 1)
            if not "." in domain:
                valid_failed = True
                Error_Message += "Email must contain a domain.\n"
                emailError.config(text="Must contain a domain.")

        # Phone number validation. Forcing UK standard was counter productive, as customers might go abroad, so not enforcing that is more useful to the business. 
        if not phonenum:
            valid_failed = True
            Error_Message += "Phone number required.\n"
            phonenumError.config(text="Required.")
        elif not len(phonenum) == 11:
            valid_failed = True
            Error_Message += "Phone number must be 11 digits.\n"
            phonenumError.config(text="Must be 11 digits.")
        elif not phonenum.isdigit():
            valid_failed = True
            Error_Message += "Phone number must be only digits.\n"
            phonenumError.config(text="Only digits.")

        # Depending on passed in boolean, the function either attempts to create a new customer or edit an existing one. Assumes cust_ID would be passed in when editing, so its important to ensure all edit functions pass one in. Other variables are always passed in.
        # Allowed me to combine the validation function, which used to be two separate ones.
        if valid_failed == False and editing == False:
            submitCustomer(fname, sname, address, postcode, email, phonenum, window)
        elif valid_failed == False and editing == True:
            modifyCustomer(fname, sname, address, postcode, email, phonenum, cust_id, window)
        else:
            messagebox.showerror("Fail", Error_Message)

# Adding a customer window. Needs window to be topleveled to. 
def addCustomer(window):
    addCustW = tk.Toplevel(window)  # Use Toplevel instead of Tk makes styling work. It does not work as a new window for uncertain reasons, so Toplevel made more sense. 
    addCustW.title("Add Customer")
    apply_style(addCustW)
    addCustW.geometry("350x600")
    addCustW.minsize(350, 600)

    # Input fields and labels
    addCustFrame = ttk.Frame(addCustW, padding="10")
    addCustFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    fnameLab = ttk.Label(addCustFrame, text="First Name: ")
    fnameEntry = ttk.Entry(addCustFrame, style="TEntry")
    fnameError = ttk.Label(addCustFrame, text="", style="Error.TLabel")
    snameLab = ttk.Label(addCustFrame, text="Surname: ")
    snameEntry = ttk.Entry(addCustFrame)
    snameError = ttk.Label(addCustFrame, text="", style="Error.TLabel")
    addressLab = ttk.Label(addCustFrame, text="Address: ")
    addressEntry = ttk.Entry(addCustFrame)
    addressError = ttk.Label(addCustFrame, text="", style="Error.TLabel")
    postcodeLab = ttk.Label(addCustFrame, text="Postcode: ")
    postcodeEntry = ttk.Entry(addCustFrame)
    postcodeError = ttk.Label(addCustFrame, text="", style="Error.TLabel")
    emailLab = ttk.Label(addCustFrame, text="Email: ")
    emailEntry = ttk.Entry(addCustFrame)
    emailError = ttk.Label(addCustFrame, text="", style="Error.TLabel")
    phonenumLab = ttk.Label(addCustFrame, text="Phone Number: ")
    phonenumEntry = ttk.Entry(addCustFrame)
    phonenumError = ttk.Label(addCustFrame, text="", style="Error.TLabel")

    # Buttons for submitting. Very long parameters so I've indented it. Required to pass in the error labels, so they can be updated.
    addcustsubmit = ttk.Button(addCustFrame, text="Submit", command=lambda: validateCustomer(
            fnameEntry.get().strip(), snameEntry.get().strip(), addressEntry.get().strip(),
            postcodeEntry.get().strip(), emailEntry.get().strip(), phonenumEntry.get().strip(),
            False, fnameError, snameError, addressError, postcodeError, emailError, phonenumError, addCustW))
    cancelcustsubmit = ttk.Button(addCustFrame, text="Cancel", command=addCustW.destroy)

    # Place input fields and labels in the grid. Padding = 5 is better here, less empty space.
    fnameLab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    fnameEntry.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    fnameError.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    snameLab.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    snameEntry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    snameError.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    addressLab.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
    addressEntry.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
    addressError.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    postcodeLab.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
    postcodeEntry.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
    postcodeError.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    emailLab.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)
    emailEntry.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
    emailError.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    phonenumLab.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)
    phonenumEntry.grid(row=10, column=1, sticky="nsew", padx=5, pady=5)
    phonenumError.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # Place buttons at the bottom with columnspan 2, makes them long.
    addcustsubmit.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
    cancelcustsubmit.grid(row=13, column=0, columnspan=2, pady=10, sticky="nsew")

    addCustW.mainloop()

# Adding a customer window. Needs window to be topleveled to. 
def editCustomer(cust_id, window):
    editCustW = tk.Toplevel(window)
    editCustW.title("Edit Customer")
    apply_style(editCustW)
    editCustW.geometry("350x600")
    editCustW.minsize(350, 600)

    # Input fields and labels
    editCustFrame = ttk.Frame(editCustW, padding="10")
    editCustFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    fnameLab = ttk.Label(editCustFrame, text="First Name: ")
    fnameEntry = ttk.Entry(editCustFrame)
    fnameError = ttk.Label(editCustFrame, text="", style="Error.TLabel")
    snameLab = ttk.Label(editCustFrame, text="Surname: ")
    snameEntry = ttk.Entry(editCustFrame)
    snameError = ttk.Label(editCustFrame, text="", style="Error.TLabel")
    addressLab = ttk.Label(editCustFrame, text="Address: ")
    addressEntry = ttk.Entry(editCustFrame)
    addressError = ttk.Label(editCustFrame, text="", style="Error.TLabel")
    postcodeLab = ttk.Label(editCustFrame, text="Postcode: ")
    postcodeEntry = ttk.Entry(editCustFrame)
    postcodeError = ttk.Label(editCustFrame, text="", style="Error.TLabel")
    emailLab = ttk.Label(editCustFrame, text="Email: ")
    emailEntry = ttk.Entry(editCustFrame)
    emailError = ttk.Label(editCustFrame, text="", style="Error.TLabel")
    phonenumLab = ttk.Label(editCustFrame, text="Phone Number: ")
    phonenumEntry = ttk.Entry(editCustFrame)
    phonenumError = ttk.Label(editCustFrame, text="", style="Error.TLabel")

    # Pre-fill fields with existing customer data
    fnameEntry.insert(0, customers[cust_id].fname)
    snameEntry.insert(0, customers[cust_id].sname)
    addressEntry.insert(0, customers[cust_id].address)
    postcodeEntry.insert(0, customers[cust_id].postcode)
    emailEntry.insert(0, customers[cust_id].email)
    phonenumEntry.insert(0, customers[cust_id].phonenum)

    # Buttons for submitting. Same reason as previous.
    editcustsubmit = ttk.Button(editCustFrame, text="Submit", command=lambda: validateCustomer(
        fnameEntry.get().strip(), snameEntry.get().strip(), addressEntry.get().strip(),
        postcodeEntry.get().strip(), emailEntry.get().strip(), phonenumEntry.get().strip(),
        True, fnameError, snameError, addressError, postcodeError, emailError, phonenumError, editCustW, cust_id))
    canceleditcustsubmit = ttk.Button(editCustFrame, text="Cancel", command=editCustW.destroy)

    # Place input fields and labels in the grid
    fnameLab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    fnameEntry.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    fnameError.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    snameLab.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    snameEntry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    snameError.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    addressLab.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
    addressEntry.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
    addressError.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    postcodeLab.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
    postcodeEntry.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
    postcodeError.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    emailLab.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)
    emailEntry.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
    emailError.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    phonenumLab.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)
    phonenumEntry.grid(row=10, column=1, sticky="nsew", padx=5, pady=5)
    phonenumError.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # Place buttons at the bottom with columnspan 2
    editcustsubmit.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
    canceleditcustsubmit.grid(row=13, column=0, columnspan=2, pady=10, sticky="nsew")

    editCustW.mainloop()

# Pet validation, used by Add and Edit Pet pages. When editing, an id is passed in, but when creating a new entry, it is not needed. It also takes the window name and error labels, in order to output the correct errors to the correct window.  
def validatePet(name, age, species, description, diet, add_info, editing, nameError, ageError, speciesError, descriptionError, dietError, add_infoError, window, pet_id=None):
    # Creates a new pet object and appends it to the pets list. Saves to file right after.
    def submitPet(name, age, species, description, diet, add_info, window):
        pet_id = len(pets) + 1
        new_pet = Pet(
            pet_id,
            name.strip(),
            age.strip(),
            species.strip(),
            description.strip(),
            diet.strip(),
            add_info.strip()
        )
        pets.append(new_pet)
        save_pets()
        messagebox.showinfo("Success", "Pet added successfully")
        window.destroy()

    # Modifies an existing pet object. Saves immediately to file.
    def modifyPet(name, age, species, description, diet, add_info, pet_id, window):
        pets[pet_id].name = name
        pets[pet_id].age = age
        pets[pet_id].species = species
        pets[pet_id].description = description
        pets[pet_id].diet = diet
        pets[pet_id].add_info = add_info

        save_pets()
        messagebox.showinfo("Success", "Pet modified successfully")
        window.destroy()

    # Resets errors after running again, removing errors that no longer apply. Without this, errors would still persist even when no longer needed. 
    valid_failed = False
    Error_Message = ""
    nameError.config(text="")
    ageError.config(text="")
    speciesError.config(text="")
    descriptionError.config(text="")
    dietError.config(text="")
    add_infoError.config(text="")

    # Validate Name
    if not name:
        valid_failed = True
        Error_Message += "Name required.\n"
        nameError.config(text="Required.")
    elif len(name) > 30:
        valid_failed = True
        Error_Message += "Name too long (over 30 characters).\n"
        nameError.config(text="Over 30 characters.")
    elif not name.isalpha():
        valid_failed = True
        Error_Message += "Name must contain only letters.\n"
        nameError.config(text="Only letters.")

    # Validate Age
    if not age:
        valid_failed = True
        Error_Message += "Age required.\n"
        ageError.config(text="Required.")
    else:
        try:
            age_int = int(age)
            if age_int < 0 or age_int > 200:
                valid_failed = True
                Error_Message += "Age must be between 0 and 200.\n"
                ageError.config(text="Must be 0-200.")
        except ValueError:
            valid_failed = True
            Error_Message += "Age must be a number.\n"
            ageError.config(text="Only numbers.")

    # Validate Species
    if not species:
        valid_failed = True
        Error_Message += "Species required.\n"
        speciesError.config(text="Required.")
    elif len(species) > 30:
        valid_failed = True
        Error_Message += "Species too long (over 30 characters).\n"
        speciesError.config(text="Over 30 characters.")
    elif not species.isalpha():
        valid_failed = True
        Error_Message += "Species must contain only letters.\n"
        speciesError.config(text="Only letters.")

    # Validate Description
    if not description:
        valid_failed = True
        Error_Message += "Description required.\n"
        descriptionError.config(text="Required.")
    elif len(description) > 200:
        valid_failed = True
        Error_Message += "Description too long (over 200 characters).\n"
        descriptionError.config(text="Over 200 characters.")

    # Validate Diet
    if not diet:
        valid_failed = True
        Error_Message += "Diet required.\n"
        dietError.config(text="Required.")
    elif len(diet) > 30:
        valid_failed = True
        Error_Message += "Diet too long (over 30 characters).\n"
        dietError.config(text="Over 30 characters.")
    elif not diet.isalpha():
        valid_failed = True
        Error_Message += "Diet must contain only letters.\n"
        dietError.config(text="Only letters.")

    # Validate the Additional Information
    if len(add_info) > 500:
        valid_failed = True
        Error_Message += "Additional Information too long (over 500 characters).\n"
        add_infoError.config(text="Over 500 characters.")

    # Depending on the editing variable, either create a new pet or modify an existing one.
    if not valid_failed:
        if editing:
            modifyPet(name, age, species, description, diet, add_info, pet_id, window)
        else:
            submitPet(name, age, species, description, diet, add_info, window)
    else:
        # Show error message if validation fails.
        messagebox.showerror("Validation Error", Error_Message)

# Adding a pet window. Needs window to be topleveled to. Standard labels, buttons, layouts.
def addPet(window):
    addPetW = tk.Toplevel(window)
    addPetW.title("Add Pet")
    apply_style(addPetW)
    addPetW.geometry("400x600")
    addPetW.minsize(400, 600)

    addPetFrame = ttk.Frame(addPetW, padding="10")
    addPetFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    nameLab = ttk.Label(addPetFrame, text="Name: ")
    nameEntry = ttk.Entry(addPetFrame)
    nameError = ttk.Label(addPetFrame, text="", style="Error.TLabel")
    ageLab = ttk.Label(addPetFrame, text="Age: ")
    ageEntry = ttk.Entry(addPetFrame)
    ageError = ttk.Label(addPetFrame, text="", style="Error.TLabel")
    speciesLab = ttk.Label(addPetFrame, text="Species: ")
    speciesEntry = ttk.Entry(addPetFrame)
    speciesError = ttk.Label(addPetFrame, text="", style="Error.TLabel")
    descriptionLab = ttk.Label(addPetFrame, text="Description: ")
    descriptionEntry = ttk.Entry(addPetFrame)
    descriptionError = ttk.Label(addPetFrame, text="", style="Error.TLabel")
    dietLab = ttk.Label(addPetFrame, text="Diet: ")
    dietEntry = ttk.Entry(addPetFrame)
    dietError = ttk.Label(addPetFrame, text="", style="Error.TLabel")
    add_infoLab = ttk.Label(addPetFrame, text="Additional Information: ")
    add_infoEntry = ttk.Entry(addPetFrame)
    add_infoError = ttk.Label(addPetFrame, text="", style="Error.TLabel")

    addpetsubmit = ttk.Button(addPetFrame, text="Submit", command=lambda: validatePet(
        nameEntry.get().strip(), ageEntry.get().strip(), speciesEntry.get().strip(),
        descriptionEntry.get().strip(), dietEntry.get().strip(), add_infoEntry.get().strip(), False, nameError, ageError, speciesError, descriptionError, dietError, add_infoError, addPetW))
    cancelpetsubmit = ttk.Button(addPetFrame, text="Cancel", command=addPetW.destroy)

    nameLab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    nameEntry.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    nameError.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    ageLab.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    ageEntry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    ageError.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    speciesLab.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
    speciesEntry.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
    speciesError.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    descriptionLab.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
    descriptionEntry.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
    descriptionError.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    dietLab.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)
    dietEntry.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
    dietError.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    add_infoLab.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)
    add_infoEntry.grid(row=10, column=1, sticky="nsew", padx=5, pady=5)
    add_infoError.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    addpetsubmit.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
    cancelpetsubmit.grid(row=13, column=0, columnspan=2, pady=10, sticky="nsew")

    addPetW.mainloop()

# Editing a pet window. Needs window to be topleveled to. 
def editPet(pet_id, window):
    editPetW = tk.Toplevel(window)
    editPetW.title("Edit Pet")
    apply_style(editPetW)
    editPetW.geometry("400x600")
    editPetW.minsize(400, 600)

    editPetFrame = ttk.Frame(editPetW, padding="10")
    editPetFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    nameLab = ttk.Label(editPetFrame, text="Name: ")
    nameEntry = ttk.Entry(editPetFrame)
    nameError = ttk.Label(editPetFrame, text="", style="Error.TLabel")
    ageLab = ttk.Label(editPetFrame, text="Age: ")
    ageEntry = ttk.Entry(editPetFrame)
    ageError = ttk.Label(editPetFrame, text="", style="Error.TLabel")
    speciesLab = ttk.Label(editPetFrame, text="Species: ")
    speciesEntry = ttk.Entry(editPetFrame)
    speciesError = ttk.Label(editPetFrame, text="", style="Error.TLabel")
    descriptionLab = ttk.Label(editPetFrame, text="Description: ")
    descriptionEntry = ttk.Entry(editPetFrame)
    descriptionError = ttk.Label(editPetFrame, text="", style="Error.TLabel")
    dietLab = ttk.Label(editPetFrame, text="Diet: ")
    dietEntry = ttk.Entry(editPetFrame)
    dietError = ttk.Label(editPetFrame, text="", style="Error.TLabel")
    add_infoLab = ttk.Label(editPetFrame, text="Additional Information: ")
    add_infoEntry = ttk.Entry(editPetFrame)
    add_infoError = ttk.Label(editPetFrame, text="", style="Error.TLabel")

    nameEntry.insert(0, pets[pet_id].name)
    ageEntry.insert(0, pets[pet_id].age)
    speciesEntry.insert(0, pets[pet_id].species)
    descriptionEntry.insert(0, pets[pet_id].description)
    dietEntry.insert(0, pets[pet_id].diet)
    add_infoEntry.insert(0, pets[pet_id].add_info)

    # Buttons for submitting, requires error labels as well. 
    editpetsubmit = ttk.Button(editPetFrame, text="Submit", command=lambda: validatePet(
        nameEntry.get().strip(), ageEntry.get().strip(), speciesEntry.get().strip(),
        descriptionEntry.get().strip(), dietEntry.get().strip(), add_infoEntry.get().strip(), True, nameError, ageError, speciesError, descriptionError, dietError, add_infoError, editPetW, pet_id))
    canceleditpetsubmit = ttk.Button(editPetFrame, text="Cancel", command=editPetW.destroy)

    nameLab.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    nameEntry.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    nameError.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    ageLab.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    ageEntry.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
    ageError.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    speciesLab.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
    speciesEntry.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
    speciesError.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    descriptionLab.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
    descriptionEntry.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
    descriptionError.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    dietLab.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)
    dietEntry.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
    dietError.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    add_infoLab.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)
    add_infoEntry.grid(row=10, column=1, sticky="nsew", padx=5, pady=5)
    add_infoError.grid(row=11, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    editpetsubmit.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
    canceleditpetsubmit.grid(row=13, column=0, columnspan=2, pady=10, sticky="nsew")

    editPetW.mainloop()

# Opens a calendar widget for date selection. Falls back to manual entry if tkcalendar is unavailable.
def open_calendar(entry):
    try:
        from tkcalendar import Calendar  # Import tkcalendar
        calendar_available = True  # Set to True if tkcalendar is available
    except ImportError:
        calendar_available = False  # Fallback if tkcalendar is not installed
    # print(calendar_available)
    
    def select_date(entry, date_entry):
        try:
            # print(f"Date_entry: {date_entry}")  # Print the date value. For debugging.
            # Validate and format the date to DD/MM/YYYY
            if calendar_available:
                # Calendar returns MM/DD/YYYY, so convert it to DD/MM/YYYY
                formatted_date = datetime.strptime(date_entry, "%m/%d/%y").strftime("%d/%m/%Y") 
                # Lowercase y is for 2 digit year, which calendar returns as. Will error if in Y. Requires convertion to YYYY.
            else:
                # Manual entry is expected in DD/MM/YYYY format
                formatted_date = date_entry
            #print(f"Formatted date: {formatted_date}")  # Debugging. Print the formatted date
            # Insert the formatted date into the entry field
            entry.delete(0, tk.END)
            entry.insert(0, formatted_date)
            calW.destroy()
        except ValueError: # Catches error if the date is not in the correct format, a validation method that applys to both manual and calendar.
            messagebox.showerror("Date Invalid", "Please enter a valid date in DD/MM/YYYY format.") 

    today = datetime.today()

    if calendar_available:
        # Create a calendar picker window
        calW = tk.Toplevel()
        calW.title("Select Date")
        apply_style(calW)
        calW.geometry("300x300")
        calW.minsize(300, 300)

        # Create the calendar widget
        cal = Calendar(calW, selectmode="day", year=today.year, month=today.month, day=today.day)
        cal.pack(pady=10)

        # Button to select the date from the calendar
        ttk.Button(calW, text="Select", command=lambda: select_date(entry, cal.get_date())).pack(pady=10)
    else:
        # Fallback manual entry window
        calW = tk.Toplevel()
        calW.title("No Calendar Available")
        apply_style(calW)
        calW.geometry("300x300")
        calW.minsize(300, 300)

        # Manual date entry
        entry_label = ttk.Label(calW, text="Enter Date (DD/MM/YYYY):")
        entry_label.pack(pady=10)
        date_entry = ttk.Entry(calW)
        date_entry.pack(pady=10)
        date_entry.insert(0, today.strftime("%d/%m/%Y"))

        # Button to validate and insert the manually entered date
        select_button = ttk.Button(calW, text="Select", command=lambda: select_date(entry, date_entry.get().strip()))
        select_button.pack(pady=10)

# Booking validation, used by Add and Edit booking pages. When editing, an id is passed in, but when creating a new entry, it is not needed. It also takes the window name and error labels, in order to output the correct errors to the correct window.  
def validateBooking(customer_id, pet_id, sdate, edate, dropoff, collect, room, customerError, petError, roomError, sdateError, edateError, dropoffError, collectError, window, editing=False, booking_id=None):
    # Creates a new booking object and appends it to the bookings list. Saves immediately to file.
    def createBooking(customer_id, pet_id, sdate, edate, dropoff, collect, room, window):
        booking_id = len(bookings) + 1
        new_booking = Booking(
            booking_id,
            pet_id,
            customer_id,
            sdate,
            edate,
            dropoff,
            collect,
            room
        )
        bookings.append(new_booking)
        save_bookings()
        messagebox.showinfo("Success", "Booking created successfully.")
        window.destroy()

    # Modifies an existing booking object. Saves immediately to file.
    def modifyBooking(customer_id, pet_id, sdate, edate, dropoff, collect, room, booking_id, window):
        bookings[booking_id].cust_id = customer_id
        bookings[booking_id].pet_id = pet_id
        bookings[booking_id].sdate = sdate
        bookings[booking_id].edate = edate
        bookings[booking_id].dropoff = dropoff
        bookings[booking_id].collect = collect
        bookings[booking_id].room = room

        save_bookings()
        messagebox.showinfo("Success", "Booking modified successfully.")
        window.destroy()

    # Reset errors before validation, so they do not persist. 
    valid_failed = False
    Error_Message = ""
    roomError.config(text="")
    customerError.config(text="")
    petError.config(text="")
    sdateError.config(text="")
    edateError.config(text="")
    dropoffError.config(text="")
    collectError.config(text="")

    # Ensures the room, pet and customer are selected.
    if room == "Select a Room":
        valid_failed = True
        Error_Message += "Room selection required.\n"
        roomError.config(text="Required.")

    if customer_id == "Select a Customer":
        valid_failed = True
        Error_Message += "Customer selection required.\n"
        customerError.config(text="Required.")
    
    if pet_id == "Select a Pet":
        valid_failed = True
        Error_Message += "Pet selection required.\n"
        petError.config(text="Required.")

    # Validate Start Date. Ensures it is not in the past and is in the correct format.
    if not sdate:
        valid_failed = True
        Error_Message += "A Start Date is required.\n"
        sdateError.config(text="Required.")
    else:
        try:
            start_date = datetime.strptime(sdate, "%d/%m/%Y").date() # For some reason, theres no strpdate, so this is nessessary. 
            # print(start_date) Debugging.
            if start_date < datetime.now().date():
                valid_failed = True
                Error_Message += "Start Date cannot be in the past.\n"
                sdateError.config(text="Cannot be in the past.")
        except ValueError:
            valid_failed = True
            Error_Message += "Invalid Start Date format.\n"
            sdateError.config(text="Invalid format.")

    # Validate End Date. Ensures it is after the Start Date and not in the past.
    if not edate:
        valid_failed = True
        Error_Message += "An End Date is required.\n"
        edateError.config(text="Required.")
    else:
        try:
            end_date = datetime.strptime(edate, "%d/%m/%Y").date() 
            if end_date <= start_date:
                valid_failed = True
                Error_Message += "End Date must be after Start Date.\n"
                edateError.config(text="Must be after Start Date.")
            elif end_date < datetime.now().date():
                valid_failed = True
                Error_Message += "End Date cannot be in the past.\n"
                edateError.config(text="Cannot be in the past.")
        except ValueError:
            valid_failed = True
            Error_Message += "Invalid End Date format.\n"
            edateError.config(text="Invalid format.")

    # Validate Dropoff Time. Ensures it's provided.
    if not dropoff.strip(":"):
        valid_failed = True
        Error_Message += "Drop off time required.\n"
        dropoffError.config(text="Required.")

    # Validate Collection Time. Ensures it's provided.
    if not collect.strip(":"):
        valid_failed = True
        Error_Message += "Collection time required.\n"
        collectError.config(text="Required.")

    customer_id = customer_id.split("} ")[-1].split(",")[-1].strip() # Earlier, the names got attached to the entry, so the customer can see them. This removes them.
    pet_id = pet_id.split("} ")[-1].split(",")[-1].strip() 
    # Debugging.
    # print(customer_id)
    # print(pet_id)

    # If validation passes, either create or modify the booking based on the editing flag.
    if not valid_failed:
        if editing:
            modifyBooking(int(customer_id)-1, int(pet_id)-1, sdate, edate, dropoff, collect, room, booking_id, window)
        else:
            createBooking(int(customer_id)-1, int(pet_id)-1, sdate, edate, dropoff, collect, room, window)
    else:
        # Show error message if validation fails.
        messagebox.showerror("Validation Error", Error_Message)

# Adds a new booking. Opens a new window for booking creation.
def submitBooking(window):    
    addBookW = tk.Toplevel(window)
    addBookW.title("Create Booking")
    apply_style(addBookW)
    addBookW.geometry("500x700")
    addBookW.minsize(500, 700)
    
    addBookFrame = ttk.Frame(addBookW, padding="10")
    addBookFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            
    # Lists all unbooked rooms, using the all_rooms global. 
    def unbooked_rooms():
        free_rooms = ["Select a Room"] # Default option
        for room in all_rooms:
            if room not in [booking.room for booking in bookings]: # Gets rooms that arent booked, from a list of all rooms.
                free_rooms.append(room)
        return free_rooms

    def cust_ids():
        customer_ids = []
        customer_ids.append("Select a Customer")
        for customer in customers:
            customer_ids.append((f"{customer.fname} {customer.sname}", customer.id))
        return customer_ids
    
    def pet_ids():
        pet_ids = []
        pet_ids.append("Select a Pet")
        for pet in pets:
            pet_ids.append((f"{pet.name} {pet.species}", pet.id))
        return pet_ids

    # Retrieve available rooms, customers, and pets for the booking.
    free_rooms = unbooked_rooms()
    customer_ids = cust_ids()
    pets_ids = pet_ids()

    # Check if there are no available rooms, customers, or pets and show appropriate error messages.
    if not free_rooms:
        addBookW.destroy()
        messagebox.showerror("No Rooms Available", "All rooms are currently booked.")
        return

    if not customers:
        addBookW.destroy()
        messagebox.showerror("No Customers", "Please add a customer before booking.")
        return
    
    if not pets:
        addBookW.destroy()
        messagebox.showerror("No Pets", "Please add a pet before booking.")
        return

    # Create dropdowns and input fields for booking details.
    room_var = tk.StringVar(addBookW)
    room_var.set("Select a Room")
    
    selected_customer = tk.StringVar(addBookW)
    selected_customer.set("Select a Customer")  # Default option

    selected_pet = tk.StringVar(addBookW)
    selected_pet.set("Select a Pet")
    
    custIDLab = ttk.Label(addBookFrame, text="Customer: ")
    custIDDrop = ttk.OptionMenu(addBookFrame, selected_customer, *customer_ids)
    custIDLab.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    custIDDrop.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    customerError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    customerError.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    petIDLab = ttk.Label(addBookFrame, text="Pet: ")
    petIDDrop = ttk.OptionMenu(addBookFrame, selected_pet, *pets_ids)
    petIDLab.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
    petIDDrop.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
    petError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    petError.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    sdateLab = ttk.Label(addBookFrame, text="Start Date: ")
    sdateEntry = ttk.Entry(addBookFrame, width=15)
    sdateButton = ttk.Button(addBookFrame, text="Pick a Date", command= lambda: open_calendar(sdateEntry))
    sdateLab.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
    sdateEntry.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
    sdateButton.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)
    sdateError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    sdateError.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    edateLab = ttk.Label(addBookFrame, text="End Date: ")
    edateEntry = ttk.Entry(addBookFrame, width=15)
    edateButton = ttk.Button(addBookFrame, text="Pick a Date", command= lambda: open_calendar(edateEntry))
    edateLab.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
    edateEntry.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
    edateButton.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)
    edateError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    edateError.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    dropoffLab = ttk.Label(addBookFrame, text="Dropoff Time: ")
    dropoffHour = ttk.Spinbox(addBookFrame, from_=0, to=23, width=2, format="%02.0f")
    dropoffMinute = ttk.Spinbox(addBookFrame, from_=0, to=59, width=2, format="%02.0f") # Digits for hours and minutes.
    dropoffLab.grid(row=9, column=0, sticky="nsew", padx=5, pady=5)
    dropoffHour.grid(row=9, column=1, sticky="nsew", padx=5, pady=5)
    dropoffMinute.grid(row=9, column=2, sticky="nsew", padx=5, pady=5)
    dropoffError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    dropoffError.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    collectLab = ttk.Label(addBookFrame, text="Collection Time: ")
    collectHour = ttk.Spinbox(addBookFrame, from_=0, to=23, width=2, format="%02.0f")
    collectMinute = ttk.Spinbox(addBookFrame, from_=0, to=59, width=2, format="%02.0f")
    collectLab.grid(row=11, column=0, sticky="nsew", padx=5, pady=5)
    collectHour.grid(row=11, column=1, sticky="nsew", padx=5, pady=5)
    collectMinute.grid(row=11, column=2, sticky="nsew", padx=5, pady=5)
    collectError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    collectError.grid(row=12, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    roomLab = ttk.Label(addBookFrame, text="Room: ")
    roomDrop = ttk.OptionMenu(addBookFrame, room_var, *free_rooms)
    roomLab.grid(row=13, column=0, sticky="nsew", padx=5, pady=5)
    roomDrop.grid(row=13, column=1, sticky="nsew", padx=5, pady=5)
    roomError = ttk.Label(addBookFrame, text="", style="Error.TLabel")
    roomError.grid(row=14, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # Submit button to validate and create the booking.
    addbooksubmit = ttk.Button(addBookFrame, text="Submit", command=lambda: validateBooking(selected_customer.get().strip(), selected_pet.get().strip(), sdateEntry.get().strip(), edateEntry.get().strip(), f"{dropoffHour.get()}:{dropoffMinute.get()}", f"{collectHour.get()}:{collectMinute.get()}", room_var.get(), customerError, petError, roomError, sdateError, edateError, dropoffError, collectError, addBookW))
    addbooksubmit.grid(row=15, column=0, columnspan=3, pady=10, sticky="nsew")
    # Cancel button to close the booking window without saving.
    cancelbooksubmit = ttk.Button(addBookFrame, text="Cancel", command=addBookW.destroy)
    cancelbooksubmit.grid(row=16, column=0, columnspan=3, pady=10, sticky="nsew")

    # Start the booking creation window.
    addBookW.mainloop()

# Lets user edit an existing booking. Opens a pre-filled window for editing.
def editBooking(book_id, window):  
    editBookW = tk.Toplevel(window)
    editBookW.title("Edit Booking")
    apply_style(editBookW)
    editBookW.geometry("500x700")
    editBookW.minsize(500, 700)

    editBookFrame = ttk.Frame(editBookW, padding="10")
    editBookFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Lists all unbooked rooms, using the all_rooms global.
    def unbooked_rooms():
        free_rooms = ["Select a Room"] # Default option
        for room in all_rooms:
            if room not in [booking.room for booking in bookings]:
                free_rooms.append(room)
        return free_rooms

    def cust_ids():
        customer_ids = []
        customer_ids.append("Select a Customer")
        for customer in customers:
            customer_ids.append((f"{customer.fname} {customer.sname}", customer.id))
        return customer_ids
    
    def pet_ids():
        pet_ids = []
        pet_ids.append("Select a Pet")
        for pet in pets:
            pet_ids.append((f"{pet.name} {pet.species}", pet.id))
        return pet_ids

    # Retrieve available rooms, customers, and pets for the booking.
    free_rooms = unbooked_rooms()
    customer_ids = cust_ids()
    pets_ids = pet_ids()

    # Check if there are no available rooms, customers, or pets and show appropriate error messages.
    if not free_rooms:
        editBookW.destroy()
        messagebox.showerror("No Rooms Available", "All rooms are currently booked.")
        return

    if not customers:
        editBookW.destroy()
        messagebox.showerror("No Customers", "Please add a customer before booking.")
        return
    
    if not pets:
        editBookW.destroy()
        messagebox.showerror("No Pets", "Please add a pet before booking.")
        return

    # Create dropdowns and input fields for booking details, pre-filled with booking data.
    room_var = tk.StringVar(editBookW)
    room_var.set(bookings[book_id].room)  # Pre-fill
    
    selected_customer = tk.StringVar(editBookW)
    selected_customer.set(bookings[book_id].cust_id)

    selected_pet = tk.StringVar(editBookW)
    selected_pet.set(bookings[book_id].pet_id)
        
    custIDLab = ttk.Label(editBookFrame, text="Customer: ")
    custIDDrop = ttk.OptionMenu(editBookFrame, selected_customer, *customer_ids)
    custIDLab.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    custIDDrop.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    customerError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    customerError.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    petIDLab = ttk.Label(editBookFrame, text="Pet: ")
    petIDDrop = ttk.OptionMenu(editBookFrame, selected_pet, *pets_ids)
    petIDLab.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
    petIDDrop.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
    petError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    petError.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    sdateLab = ttk.Label(editBookFrame, text="Start Date: ")
    sdateEntry = ttk.Entry(editBookFrame, width=15)
    sdateEntry.insert(0, bookings[book_id].sdate)
    sdateButton = ttk.Button(editBookFrame, text="Pick a Date", command= lambda: open_calendar(sdateEntry))
    sdateLab.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
    sdateEntry.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
    sdateButton.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)
    sdateError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    sdateError.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    edateLab = ttk.Label(editBookFrame, text="End Date: ")
    edateEntry = ttk.Entry(editBookFrame, width=15)
    edateEntry.insert(0, bookings[book_id].edate)
    edateButton = ttk.Button(editBookFrame, text="Pick a Date", command= lambda: open_calendar(edateEntry))
    edateLab.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
    edateEntry.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
    edateButton.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)
    edateError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    edateError.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    dropoffLab = ttk.Label(editBookFrame, text="Dropoff Time: ")
    dropoffHour = ttk.Spinbox(editBookFrame, from_=0, to=23, width=2, format="%02.0f")
    dropoffMinute = ttk.Spinbox(editBookFrame, from_=0, to=59, width=2, format="%02.0f")
    dropoffLab.grid(row=9, column=0, sticky="nsew", padx=5, pady=5)
    dropoffHour.grid(row=9, column=1, sticky="nsew", padx=5, pady=5)
    dropoffMinute.grid(row=9, column=2, sticky="nsew", padx=5, pady=5)
    dropoffError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    dropoffError.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    dropoffHour.insert(0, bookings[book_id].dropoff.split(":")[0])
    dropoffMinute.insert(0, bookings[book_id].dropoff.split(":")[1])

    collectLab = ttk.Label(editBookFrame, text="Collection Time: ")
    collectHour = ttk.Spinbox(editBookFrame, from_=0, to=23, width=2, format="%02.0f")
    collectMinute = ttk.Spinbox(editBookFrame, from_=0, to=59, width=2, format="%02.0f")
    collectLab.grid(row=11, column=0, sticky="nsew", padx=5, pady=5)
    collectHour.grid(row=11, column=1, sticky="nsew", padx=5, pady=5)
    collectMinute.grid(row=11, column=2, sticky="nsew", padx=5, pady=5)
    collectError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    collectError.grid(row=12, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    collectHour.insert(0, bookings[book_id].collect.split(":")[0])
    collectMinute.insert(0, bookings[book_id].collect.split(":")[1])

    roomLab = ttk.Label(editBookFrame, text="Room: ")
    roomDrop = ttk.OptionMenu(editBookFrame, room_var, *free_rooms)
    roomLab.grid(row=13, column=0, sticky="nsew", padx=5, pady=5)
    roomDrop.grid(row=13, column=1, sticky="nsew", padx=5, pady=5)
    roomError = ttk.Label(editBookFrame, text="", style="Error.TLabel")
    roomError.grid(row=14, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # Submit button to validate and modify the booking.
    addbooksubmit = ttk.Button(editBookFrame, text="Submit", command=lambda: validateBooking(selected_customer.get().strip(), selected_pet.get().strip(), sdateEntry.get().strip(), edateEntry.get().strip(), f"{dropoffHour.get()}:{dropoffMinute.get()}", f"{collectHour.get()}:{collectMinute.get()}", room_var.get(), customerError, petError, roomError, sdateError, edateError, dropoffError, collectError, editBookW, True, book_id))
    addbooksubmit.grid(row=15, column=0, columnspan=3, pady=10, sticky="nsew")
    # Cancel button to close the booking editing window without editing anything.
    cancelbooksubmit = ttk.Button(editBookFrame, text="Cancel", command=editBookW.destroy)
    cancelbooksubmit.grid(row=16, column=0, columnspan=3, pady=10, sticky="nsew")

    # Start the booking editing window.
    editBookW.mainloop()

# Booking Menu, where the user can view, edit, and archive bookings.
def bookMenu():
    bookMenuW = tk.Tk()
    bookMenuW.title("Bookings")
    apply_style(bookMenuW)

    load_bookings()
    load_archive_bookings()
    start = 0
    end = 10

    # Viewing, which creates a simple page out of the id that gets passed in. Also a Toplevel.
    def view_booking(window, idx, archived=False):
        viewBookW = tk.Toplevel(window)
        viewBookW.title("View Booking")
        apply_style(viewBookW)
        viewBookW.geometry("300x400")
        viewBookW.minsize(300, 400)

        # Select the appropriate booking list using the boolean. 
        if archived:
            booking = archived_bookings[idx]
        else:
            booking = bookings[idx]

        # Debugging prints. 
        # print(f"Booking Data: {vars(booking)}")

        # Ensure cust_id and pet_id are integers before accessing the lists, and then accessing the lists. 
        cust_id = int(booking.cust_id)
        pet_id = int(booking.pet_id)
        customer = customers[cust_id]
        pet = pets[pet_id]

        # UI Labels for Booking Details
        viewBookFrame = ttk.Frame(viewBookW, padding="10", relief="solid", borderwidth=2)
        viewBookFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        bookDetails = ttk.Label(viewBookFrame, text="Booking Details", font=(system_font, font_size + 4, "bold"))
        bookDetails.grid(row=0, column=0, columnspan=2, pady=10)

        # Nothing to enter, so no entries. Just labels.
        bookCustIDLab = ttk.Label(viewBookFrame, text="Customer:")
        bookCustID = ttk.Label(viewBookFrame, text=f"{customer.fname} {customer.sname}")
        bookPetIDLab = ttk.Label(viewBookFrame, text="Pet:")
        bookPetID = ttk.Label(viewBookFrame, text=f"{pet.name} ({pet.species})")
        bookSdateLab = ttk.Label(viewBookFrame, text="Start Date:")
        bookSdate = ttk.Label(viewBookFrame, text=booking.sdate)
        bookEdateLab = ttk.Label(viewBookFrame, text="End Date:")
        bookEdate = ttk.Label(viewBookFrame, text=booking.edate)
        bookDropLab = ttk.Label(viewBookFrame, text="Dropoff Time:")
        bookDrop = ttk.Label(viewBookFrame, text=booking.dropoff)
        bookCollectLab = ttk.Label(viewBookFrame, text="Collection Time:")
        bookCollect = ttk.Label(viewBookFrame, text=booking.collect)
        bookRoomLab = ttk.Label(viewBookFrame, text="Room:")
        bookRoom = ttk.Label(viewBookFrame, text=booking.room)

        bookCustIDLab.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        bookCustID.grid(row=1, column=1, sticky="w")
        bookPetIDLab.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        bookPetID.grid(row=2, column=1, sticky="w")
        bookSdateLab.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        bookSdate.grid(row=3, column=1, sticky="w")
        bookEdateLab.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        bookEdate.grid(row=4, column=1, sticky="w")
        bookDropLab.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        bookDrop.grid(row=5, column=1, sticky="w")
        bookCollectLab.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        bookCollect.grid(row=6, column=1, sticky="w")
        bookRoomLab.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        bookRoom.grid(row=7, column=1, sticky="w")

        # Close Button
        returnB = ttk.Button(viewBookW, text="Close", command=viewBookW.destroy)
        returnB.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Recieves either -1 or 1 to go forward or backwards. 
    def changePage(pn):
        nonlocal start, end

        # Change the start and end correctly.
        newstart = start + (pn * 10)
        newend = newstart + 10

        # Prevents errors by quitting before it can go out of bounds
        if newstart >= len(bookings):  
            return 
        if newstart < 0:
            return

        start = newstart
        end = newend
        update_bookings()  # Updates list after changing pages. 

    # Unique function to bookings, allowing for archival and unarchiving as the archived bookings are their own list for clarity and easier management.
    def archive_booking(index):
        confirm = messagebox.askyesno("Archive Booking", f"Are you sure you want to archive this booking? It can be retrieved later.")
        if confirm:
            archived_bookings.append(bookings[index])
            del bookings[index]
            save_bookings()
            save_archive_bookings()
            messagebox.showinfo("Archived", "Booking was moved successfully.")
            update_bookings()

    def update_bookings(room=None, sdate=None, edate=None):
        def delete_booking(index):
            book_index = bookings.index(results_bookings[index])
            confirm = messagebox.askyesno("Delete Booking", f"Are you sure you want to delete this booking?")
            if confirm:
                del bookings[book_index]
                save_bookings()
                messagebox.showinfo("Deleted", "Booking was deleted successfully.")
                update_bookings()
        resultFrame.grid(row=0, column=0, rowspan=10, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Clear previous results
        for widget in resultFrame.winfo_children():
            widget.destroy()

        filtered_bookings = []

        # Linear search through each booking. Same logic as the rest. 
        for booking in bookings:
            match = True
            if room and (room.lower() not in booking.room.lower()):
                match = False
            if sdate and (sdate != booking.sdate):
                match = False
            if edate and (edate != booking.edate):
                match = False

            if match:
                filtered_bookings.append(booking)

        if not (room or sdate or edate):
            filtered_bookings = bookings

        results_bookings = filtered_bookings[start:end]

        for i, booking in enumerate(results_bookings):
            bookingL = ttk.Label(resultFrame, text=f"{booking.room} {booking.sdate} - {booking.edate}")
            bookingL.grid(row=i, column=0, pady=10, padx=10)

            resultFrame.columnconfigure(1, weight=1)

            bookingEditB = ttk.Button(resultFrame, text="∆", style="Edit.TButton", command=lambda idx=i: editBooking(idx, bookMenuW))
            bookingEditB.grid(row=i, column=2, sticky="e", padx=5, pady=10)
            bookingArchiveB = ttk.Button(resultFrame, text="📦", style="Edit.TButton", command=lambda idx=i: archive_booking(idx))
            bookingArchiveB.grid(row=i, column=3, sticky="e", padx=5, pady=10)
            bookingViewB = ttk.Button(resultFrame, text="👁‍🗨", style="Delete.TButton", command=lambda idx=i: view_booking(bookMenuW,idx))
            bookingViewB.grid(row=i, column=4, sticky="e", padx=5, pady=10)
            bookingDelB = ttk.Button(resultFrame, text="➖", style="Delete.TButton", command=lambda idx=i: delete_booking(idx))
            bookingDelB.grid(row=i, column=5, sticky="e", padx=5, pady=10)

        if start > 0:
            prevB.config(state=tk.NORMAL)
        else:
            prevB.config(state=tk.DISABLED)

        if end < len(filtered_bookings):
            nextB.config(state=tk.NORMAL)
        else:
            nextB.config(state=tk.DISABLED)
    
    def archiveBookings():
        archivedBW = tk.Toplevel(bookMenuW)
        archivedBW.title("Archived Bookings")
        apply_style(archivedBW)
        archivedBW.geometry("600x800")

        archiveFrame = ttk.Frame(archivedBW, padding="10", relief="solid", borderwidth=2)
        archiveFrame.grid(row=0, column=0, rowspan=10, columnspan=3, padx=10, pady=10, sticky="nsew")

        start = 0
        end = 10

        # Split them up as they can only be accessed from different locations. Needed access to update_archive
        def unarchive_booking(index):
            confirm = messagebox.askyesno("Unarchive Booking", f"Are you sure you want to restore this booking? It can be archived again later.")
            if confirm:
                bookings.append(archived_bookings[index])
                del archived_bookings[index]
                save_bookings()
                save_archive_bookings()
                messagebox.showinfo("Restored", "Booking was moved successfully.")
                update_bookings()
                update_archive_display()

        def update_archive_display():
            nonlocal start, end

            # Clear previous results
            for widget in archiveFrame.winfo_children():
                widget.destroy()

            for i, booking in enumerate(archived_bookings[start:end]):
                archiveFrame.columnconfigure(1, weight=1)
                arcbookL = ttk.Label(archiveFrame, text=f"{booking.sdate} - {booking.edate} --- Room: {booking.room}")
                arcbookL.grid(row=i, column=0, pady=10, padx=10)

                bookViewB = ttk.Button(archiveFrame, text="👁‍🗨", style="Edit.TButton", command=lambda idx=start + i: view_booking(archivedBW, idx, archived=True))
                bookViewB.grid(row=i, column=1, sticky="e", padx=5, pady=10)

                bookUnarcB = ttk.Button(archiveFrame, text="📦", style="Delete.TButton", command=lambda idx=start + i: unarchive_booking(idx))
                bookUnarcB.grid(row=i, column=2, sticky="e", padx=5, pady=10)

            # List buttons. Same logic as before.
            if start > 0:
                prevB.config(state=tk.NORMAL)
            else:
                prevB.config(state=tk.DISABLED)

            if end < len(archived_bookings):
                nextB.config(state=tk.NORMAL)
            else:
                nextB.config(state=tk.DISABLED)

        def changePage(pn):
            nonlocal start, end

            # Change the start and end correctly.
            newstart = start + (pn * 10)
            newend = newstart + 10

            # Prevents errors by quitting before it can go out of bounds
            if newstart >= len(archived_bookings):
                return
            if newstart < 0:
                return

            start = newstart
            end = newend
            update_archive_display()  # Updates list after changing pages.

        prevB = ttk.Button(archivedBW, text="◀", command=lambda: changePage(-1))
        nextB = ttk.Button(archivedBW, text="▶", command=lambda: changePage(1))

        prevB.grid(row=11, column=0, pady=10, padx=5, sticky="w")
        nextB.grid(row=11, column=2, pady=10, padx=5, sticky="e")

        returnB = ttk.Button(archivedBW, text="Return", command=archivedBW.destroy)
        returnB.grid(row=12, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        update_archive_display()

    def searchBookingsMenu():
        global booking_search_menu

        if not booking_search_menu:
            searchFrame.grid(row=0, column=5, rowspan=7, padx=10, pady=10)
            searchLab = ttk.Label(searchFrame, text="Search Options")
            roomLab = ttk.Label(searchFrame, text="Room: ")
            roomEntry = ttk.Entry(searchFrame)
            sdateLab = ttk.Label(searchFrame, text="Start Date: ")
            sdateEntry = ttk.Entry(searchFrame)
            edateLab = ttk.Label(searchFrame, text="End Date: ")
            edateEntry = ttk.Entry(searchFrame)
            searchButton = ttk.Button(searchFrame, text="Search", command=lambda: update_bookings(roomEntry.get().strip(), sdateEntry.get().strip(), edateEntry.get().strip()))

            searchLab.grid(row=0, column=0, columnspan=2, pady=5)
            roomLab.grid(row=1, column=0, sticky="ne", padx=5)
            sdateLab.grid(row=2, column=0, sticky="ne", padx=5)
            edateLab.grid(row=3, column=0, sticky="ne", padx=5)

            roomEntry.grid(row=1, column=1, padx=5)
            sdateEntry.grid(row=2, column=1, padx=5)
            edateEntry.grid(row=3, column=1, padx=5)
            searchButton.grid(row=4, column=1, padx=5)
            booking_search_menu = True
        else:
            searchFrame.grid_forget()
            booking_search_menu = False

    searchFrame = ttk.Frame(bookMenuW, padding="10", relief="solid", borderwidth=2)
    resultFrame = ttk.Frame(bookMenuW, padding="10", relief="solid", borderwidth=2)
    searchbookB = ttk.Button(bookMenuW, text="Search", command=lambda: searchBookingsMenu())
    addbookB = ttk.Button(bookMenuW, text="Create Booking",command=lambda: submitBooking(bookMenuW))
    viewArcBookB = ttk.Button(bookMenuW, text="View Archives",command=lambda: archiveBookings())
    mainmenuB = ttk.Button(bookMenuW, text="Return",command=lambda: openMainMenu(bookMenuW))
    prevB = ttk.Button(bookMenuW, text="◀", command=lambda: changePage(-1))
    nextB = ttk.Button(bookMenuW, text="▶", command=lambda: changePage(1))

    prevB.grid(row=11, column=0, sticky="w", padx=10, pady=10)
    nextB.grid(row=11, column=2, sticky="e", padx=10, pady=10)
    searchbookB.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)
    addbookB.grid(row=12, column=0, pady=5, padx=5, sticky="nsew")
    viewArcBookB.grid(row=12, column=1, pady=5, padx=5, sticky="nsew")
    mainmenuB.grid(row=12, column=2, pady=5, padx=5, sticky="nsew")

    update_bookings()
    bookMenuW.mainloop()

# Schedule/Timetable to show bookings visually.
def schedule():
    scheduleW = tk.Tk()
    scheduleW.title("Schedule")
    apply_style(scheduleW)
    scheduleW.geometry("1200x750")

    def get_month_days(month):
        # Returns the number of days in the given month
        if month.month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month.month in [4, 6, 9, 11]:
            return 30
        elif month.month == 2: 
            # Simplistic leap year checking, best option without being too complex. Had to learn to take the /400 rule into account.
            if (month.year % 4 == 0 and month.year % 100 != 0) or (month.year % 400 == 0):
                return 29
            else:
                return 28

    def update_schedule():
        # Updates the schedule display for the current month
        monthLab.config(text=month.strftime("%B %Y"))

        # Display all rooms, using the room number as the label and the rooms global. Did not need separate frames, due to borderwidth.
        for i in range(len(all_rooms)):
            roomNumLab = ttk.Label(scheduleFrame, text=all_rooms[i], borderwidth=10, relief="solid")
            roomNumLab.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")

        # Display bookings for the current month
        for i in range(len(bookings)):
            # Set start_day and end_day to handle non use cases.
            start_day = None
            end_day = None
            start_date = datetime.strptime(bookings[i].sdate, "%d/%m/%Y")
            end_date = datetime.strptime(bookings[i].edate, "%d/%m/%Y")

            # Adjust start_date and end_date to fit within the current month
            if start_date.month == month.month and start_date.year == month.year:
                # Booking starts in the current month
                start_day = start_date.day
            elif start_date < month:
                # Booking starts before the current month
                start_day = 1

            if end_date.month == month.month and end_date.year == month.year:
                # Booking ends in the current month
                end_day = end_date.day
            elif end_date > month:
                # Booking ends after the current month
                end_day = get_month_days(month)

            # Check if start_day and end_day are both set before trying to display the booking
            if start_day is not None and end_day is not None:
                room = all_rooms.index(bookings[i].room)

                # Display the booking
                #print(int(bookings[i].pet_id))
                #print(pets[int(bookings[i].pet_id)].name)
                #print(f"Booking: {pets[int(bookings[i].pet_id)].name} / Start: {start_day}, End: {end_day} / Columnspan: {end_day - start_day}") # Debugging print, lets me see what its using for the label.
                
                bookingLab = ttk.Label(scheduleFrame, text=f"{pets[int(bookings[i].pet_id)].name}", background="Red", padding=5, borderwidth=2, relief="solid")
                bookingLab.grid(row=room+1, column=start_day+1, columnspan=end_day - start_day + 1, sticky="ew")

    def change_month(forward=None): 
        # Allows calling the function without changing the active month, which is needed to start it.
        nonlocal month

        if forward:
            new_month = month.month + 1
        elif forward == False:
            new_month = month.month - 1
        else:
            new_month = month.month

        if new_month > 12:
            new_month = 1
            year = month.year + 1
        elif new_month < 1:
            new_month = 12
            year = month.year - 1
        else:
            year = month.year
        
        month = month.replace(month=new_month, year=year)

        for widget in scheduleFrame.winfo_children():
            widget.destroy()

        for i in range(get_month_days(month) + 1):  # Ensure all days are accounted for
            scheduleFrame.columnconfigure(i, weight=1)

        for i in range(get_month_days(month)):
            dayLab = ttk.Label(scheduleFrame, text=i + 1)
            dayLab.grid(row=0, column=i + 2, padx=5, pady=5, sticky="nsew")

        update_schedule()

    # Gets the first day of the current month
    month = datetime.today().replace(day=1)

    # Header frame for navigation and month display
    headerFrame = ttk.Frame(scheduleW, padding="5", relief="solid", borderwidth=2)
    headerFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Configuring grid for headerFrame
    headerFrame.columnconfigure(0, weight=1)
    headerFrame.columnconfigure(1, weight=1)
    headerFrame.columnconfigure(2, weight=1) 
    headerFrame.columnconfigure(3, weight=1) 

    prevB = ttk.Button(headerFrame, text="◀", command=lambda: change_month(False))
    monthLab = ttk.Label(headerFrame, text="", font=(system_font, font_size + 4, "bold"))
    returnB = ttk.Button(headerFrame, text="Return", command=lambda: openMainMenu(scheduleW))
    nextB = ttk.Button(headerFrame, text="▶", command=lambda: change_month(True))

    prevB.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    monthLab.grid(row=0, column=1, pady=5, padx=5, sticky="e")
    returnB.grid(row=0, column=2, padx=5, pady=5, sticky="w") 
    nextB.grid(row=0, column=3, padx=5, pady=5, sticky="e")

    # Frame for displaying days, rooms and the actual bookings.
    scheduleFrame = ttk.Frame(scheduleW, padding="10", relief="solid", borderwidth=2)
    scheduleFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # These are responsible for forcing the amount of space the frames take, so the header frame isn't too large for example (which is what will happen if they are removed)
    scheduleW.rowconfigure(0, weight=1)
    scheduleW.rowconfigure(1, weight=1)
    scheduleW.rowconfigure(2, weight=10)
    scheduleW.columnconfigure(0, weight=1)

    update_schedule()
    change_month() # Month function to display the days.
    scheduleW.mainloop()
             
# Password Menu, which is the first page that the user will see. Takes input password, hashing and compares to existing password in text file.
def passwordMenu():
    def passCheck():
        password = pwentry.get()
        with open("Database/passwords.txt", "r") as f:
            validPw1 = f.readline().strip()
            validPw2 = f.readline().strip()

        global accessLevel
        # Hashing
        bpassword = password.encode("utf-8")
        sha256 = hashlib.sha256()
        sha256.update(bpassword)
        password_hash = sha256.hexdigest()
        
        # Depending on the password entered, the access level will be set to 0 or 1, which is read when the .txt is opened.
        if password_hash == validPw1:
            accessLevel = 0
            pwMenuW.destroy()
            mainMenu()
            
        elif password_hash == validPw2:
            accessLevel = 1
            pwMenuW.destroy()
            mainMenu()
    
        else:
            messagebox.showerror("Error", "Incorrect Password!")
            pwerrorlab.config(text="Incorrect Password!")
            pwentry.delete(0, tk.END) 
            # Deletes the entry box so the user can try again, in most cases the user will want to retype the password again as they cannot see it, so this is a user experience feature.  

    pwMenuW = tk.Tk()
    pwMenuW.title("Password")
    apply_style(pwMenuW)
    pwMenuW.geometry("500x600")
    pwMenuW.minsize(500, 600)
    
    # Image/Logo for aesthetics.
    insert_image(pwMenuW)
    pwlab = ttk.Label(pwMenuW, text="Password:")
    pwentry = ttk.Entry(pwMenuW, show="*")
    pwsubmit = ttk.Button(pwMenuW, text="Submit", command=passCheck)
    pwerrorlab = ttk.Label(pwMenuW, text="", style="Error.TLabel")

    pwlab.grid(row=1, column=0, pady=10, padx=10, sticky="nsew"), pwentry.grid(row=2, column=0, pady=10, padx=10, ipady=10, sticky="nsew"), pwsubmit.grid(row=4, column=0, pady=10, padx=10, sticky="nsew"), pwerrorlab.grid(row=3, column=0, pady=10, sticky="nsew") 
    pwMenuW.mainloop()

# Settings Menu, which allows the user to change the font, font size and colours of the program.
def settings():
    settingsMenuW = tk.Tk()
    settingsMenuW.title("Settings")
    apply_style(settingsMenuW)
    settingsMenuW.geometry("500x600")
    settingsMenuW.minsize(500, 600)

    # Makes use of tkfont to get the fonts available on the system.
    def get_fonts():
        fonts = tkfont.families()
        available_fonts = [] 
        for font in fonts:
            available_fonts.append(font)
        return available_fonts

    def set_fonts(font, size):
        global system_font, font_size
        if size > 30:  # Enforce size limit
            size = 30
        system_font = font
        font_size = size
        apply_style(settingsMenuW)

    # Functions to change colours, which are saved to different globals but make use of the same colour chooser.
    def choose_progcolour():
        global prog_colour
        colour = colorchooser.askcolor(title = "Choose colour")[1]
        prog_colour = colour
        apply_style(settingsMenuW)

    def choose_bgcolour():
        global bg_colour
        colour = colorchooser.askcolor(title = "Choose colour")[1]
        bg_colour = colour
        apply_style(settingsMenuW)

    def choose_txtcolour():
        global txt_colour
        colour = colorchooser.askcolor(title = "Choose colour")[1]
        txt_colour = colour
        apply_style(settingsMenuW)
    
    # This is used to change the password, and is only available to owners from the hidden button.
    def passwChange():          
        def validatePassw(passw, adminpassw=None):
            def changePassw(hashed_password, hashed_adminpassword=None):
                with open("Database/passwords.txt", "r") as f:
                    lines = f.readlines()

                if len(lines) < 2: # I had issues with the writing as the txt could accidentally have less than 2 lines, so this will create them if needed.
                    lines.append("\n")

                lines[0] = hashed_password + "\n"
                if hashed_adminpassword is not None:  
                    lines[1] = hashed_adminpassword + "\n"

                with open("Database/passwords.txt", "w") as f:
                    f.writelines(lines)
                messagebox.showinfo("Success", "Password(s) changed successfully.")
                pwtop.destroy()

            valid_failed = False
            Error_Message = ""
            passwError.config(text="")
            adminpasswError.config(text="")
            
            # Password validation for both passwords
            if not passw:
                valid_failed = True
                Error_Message += "Password required.\n"
                passwError.config(text="Required.")
            if len(passw) < 6:
                valid_failed = True
                Error_Message += "Password must be over 6 characters"
                passwError.config(text="Must be over 6 characters")
            if not any(char.isdigit() for char in passw): # Ensures that the password has at least 1 number in it.
                valid_failed = True
                Error_Message += "Password must contain at least 1 number"
                passwError.config(text="Must contain at least a number")

            if adminpassw:
                if len(adminpassw) < 6:
                    valid_failed = True
                    Error_Message += "Admin Password must be over 6 characters"
                    adminpasswError.config(text="Must be over 6 characters")
                if not any(char.isdigit() for char in adminpassw):
                    valid_failed = True
                    Error_Message += "Admin Password must contain at least 1 number"
                    adminpasswError.config(text="Must contain at least a number")

            # This is the hashing part. 
            if valid_failed:
                messagebox.showerror("Password Error", Error_Message)
            else:
                bpassw = passw.encode("utf-8")
                sha256 = hashlib.sha256()
                sha256.update(bpassw)
                passw_hash = sha256.hexdigest()

                if adminpassw:
                    bapassw = adminpassw.encode("utf-8")
                    sha256 = hashlib.sha256()  
                    sha256.update(bapassw)
                    adminpassw_hash = sha256.hexdigest()
                    changePassw(passw_hash, adminpassw_hash)  
                else:
                    changePassw(passw_hash)  

        pwtop = tk.Toplevel(settingsMenuW)
        pwtop.title("Change Password")
        apply_style(pwtop)
        pwtop.geometry("300x300")
        pwtop.minsize(300, 300)

        passwLabel = ttk.Label(pwtop, text="Password")
        passwLabel.pack()
        passwEntry = ttk.Entry(pwtop)
        passwEntry.pack()
        passwError = ttk.Label(pwtop, text="", style="Error.TLabel")
        passwError.pack()
        
        adminpasswLabel = ttk.Label(pwtop, text="Admin Password")
        adminpasswLabel.pack()
        adminpasswEntry = ttk.Entry(pwtop)
        adminpasswEntry.pack()
        adminpasswError = ttk.Label(pwtop, text="This will be left unchanged if empty", style="Error.TLabel")
        adminpasswError.pack()

        passwEntry.insert(0, "123456") 
        # Default placeholder password. If a password change for this user isn't rquired, you can just close the page, however the admin password change is optional.
        changeB = ttk.Button(pwtop, text="Change", command=lambda: validatePassw(passwEntry.get().strip(), adminpasswEntry.get().strip()))
        changeB.pack()
        cancelB = ttk.Button(pwtop, text="Cancel", command=lambda: pwtop.destroy())
        cancelB.pack()

    size_var = tk.IntVar(value=font_size)
    font_var = tk.StringVar(value="Arial")
    
    settingsFrame = ttk.Frame(settingsMenuW, padding="10", relief="solid", borderwidth=2)
    fontLabel = ttk.Label(settingsFrame, text="Font:")
    fontDrop = ttk.Combobox(settingsFrame, textvariable=font_var, values=get_fonts(), state="readonly")
    fontSizeSpinbox = ttk.Spinbox(settingsFrame, from_=4, to=30, increment=1, textvariable=size_var)
    # Shows button if access level is 1. This is the only way to access the password change menu, and it requires the right access level.    
    if accessLevel == 1:
        pwchange = ttk.Button(settingsFrame, text="Change Passwords", command=passwChange)
        pwchange.grid(row=0, column=1)

    colourBgB = ttk.Button(settingsFrame, text = "Change Background Colour", command = choose_bgcolour)
    colourProgB = ttk.Button(settingsFrame, text = "Change Program Colour", command = choose_progcolour)
    colourTextB = ttk.Button(settingsFrame, text = "Change Text Colour", command = choose_txtcolour)
    changeB = ttk.Button(settingsFrame, text = "Change", command = lambda: set_fonts(font_var.get(), size_var.get()))
    closeB = ttk.Button(settingsFrame, text = "Close", command = lambda: openMainMenu(settingsMenuW))

    settingsFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    fontLabel.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    fontDrop.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    fontSizeSpinbox.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    changeB.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    colourBgB.grid(row=4, column=1, padx=5, pady=10, sticky="nsew")
    colourProgB.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
    colourTextB.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
    closeB.grid(row=8, column=1, padx=5, pady=5, sticky="nsew")
    
passwordMenu()
