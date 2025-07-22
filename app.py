import mysql.connector
import tkinter as tk 
from tkinter import messagebox
from datetime import date

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@data",
    database="hotel_db"
)

cursor=db.cursor()

def add_room():
    room_type=entry_room_type.get()
    price=entry_price.get()
    if room_type and price:
        cursor.execute("Insert into rooms(room_type, price, is_available) values (%s, %s, TRUE)", (room_type, price))
        db.commit()
        messagebox.showinfo("Success", "room Added successfully")
        entry_room_type.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "please fill all fields")
        
def view_rooms():
    cursor.execute("select * from rooms where is_available=TRUE")
    rooms=cursor.fetchall()
    display_text="Available Rooms:\n\n"
    for room in rooms:
        display_text+=f"Room ID: {room[0]}, Type: {room[1]}, Price:{room[2]}\n"
    messagebox.showinfo("Available Rooms", display_text)
    

def book_room():
    try:
        name=entry_guest_name.get()
        contact=entry_contact.get()
        room_id=entry_room_id.get()
        checkin=entry_checkin.get()
        checkout=entry_checkout.get()
        if name and contact and room_id and checkin and checkout:
            cursor.execute("select is_available from rooms where room_id=%s", (room_id,))
            result=cursor.fetchone()
            if result and result[0]:
                cursor.execute("Insert into guests(name, contact, check_in, check_out, room_id) values (%s, %s, %s, %s, %s)",(name, contact, checkin, checkout, room_id))
                cursor.execute("update rooms set is_available= false where room_id=%s", (room_id,))
                db.commit()
                messagebox.showinfo("Success"," Room booked successfully")
            else:
                messagebox.showerror("Unavilable", "selected Room is not available")
        else:
            messagebox.showerror("Error", "Please fill all fields")
    except ValueError:
        messagebox.showerror("Error", "Room ID must be a number")

    finally:            
        entry_guest_name.delete(0, tk.END)
        entry_contact.delete(0, tk.END)
        entry_room_id.delete(0, tk.END)
        entry_checkin.delete(0, tk.END)
        entry_checkout.delete(0, tk.END)
        
        
def view_guests():
    cursor.execute("select guest_id, name,contact, check_in, check_out, room_id from guests")
    guests=cursor.fetchall()
    if guests:
        display_text="Guest Details:\n\n"
        for guest in guests:
            display_text+=f"Guest ID: {guest[0]}, Name: {guest[1]}, contact: {guest[2]}, check_in: {guest[3]}, check-out: {guest[4]}, Room ID: {guest[5]}\n"
        messagebox.showinfo("Guests", display_text)
    else:
        messagebox.showinfo("Guests", "No guests found")

def modify_booking():
    try:
        guest_id=entry_modify_guest_id.get()
        new_contact=entry_new_contact.get()
        new_checkout=entry_new_checkout.get()
        if guest_id and (new_contact or new_checkout):
            if new_contact:
                cursor.execute("update guests set contact=%s where guest_id=%s", (new_contact, guest_id))
            if new_checkout:
                cursor.execute("update guests set check_out=%s where guest_id=%s", (new_checkout, guest_id))
            db.commit()
            messagebox.showinfo("success", "Booking Modified Successfully")
        else:
            messagebox.showerror("Error", "Please provide Guest ID and at least one fiels to update")

    finally:
        entry_modify_guest_id.delete(0, tk.END)
        entry_new_contact.delete(0, tk.END)
        entry_new_checkout.delete(0, tk.END)



def cancel_booking():
    try:
        guest_id=entry_cancel_guest_id.get()
        if guest_id:
            cursor.execute("select room_id from guests where guest_id=%s", (guest_id, ))
            result=cursor.fetchone()
            if result:
                room_id=result[0] 
                cursor.execute("update rooms set is_available=TRUE where room_id=%s", (room_id, ))
                db.commit()
                messagebox.showinfo("Success", "Booking Cancelled and Room Available Now")
            else:
                messagebox.showerror("Error", "Guest ID not found") 
        else:
            messagebox.showerror("Error", "Please Enter a Guest ID")
    finally:
        entry_cancel_guest_id.delete(0, tk.END)
          
        
root=tk.Tk()
root.title("Hotel Room Reservation System")
root.geometry("600x700")

tk.Label(root, text="Add Room").pack()
tk.Label(root, text="Room Type").pack()
entry_room_type=tk.Entry(root)
entry_room_type.pack()

tk.Label(root, text="Price").pack()
entry_price=tk.Entry(root)
entry_price.pack()

tk.Button(root, text="Add Room", command=add_room).pack(pady=5)

tk.Button(root, text="View Available Rooms", command=view_rooms).pack(pady=5)

tk.Label(root, text="\nBook Room").pack()
tk.Label(root, text="Guest Name").pack()
entry_guest_name=tk.Entry(root)
entry_guest_name.pack()

tk.Label(root, text="Contact").pack()
entry_contact=tk.Entry(root)
entry_contact.pack()

tk.Label(root, text="Room ID").pack()
entry_room_id=tk.Entry(root)
entry_room_id.pack()

tk.Label(root, text="Check-in Date(YYYY-MM-DD)").pack()
entry_checkin=tk.Entry(root)
entry_checkin.pack()

tk.Label(root, text="Check-out Date(YYYY-MM-DD)").pack()
entry_checkout=tk.Entry(root)
entry_checkout.pack()

tk.Button(root, text="Book Room", command=book_room).pack(pady=5)

tk.Button(root, text="View Guest Details", command=view_guests).pack(pady=5)

tk.Label(root, text="\nModify Booking").pack()
tk.Label(root, text="Guest ID").pack()
entry_modify_guest_id=tk.Entry(root)
entry_modify_guest_id.pack()

tk.Label(root, text="New Contact (optional)").pack()
entry_new_contact=tk.Entry(root)
entry_new_contact.pack()

tk.Label(root, text="New check-out Date(YYYY-MM-DD, optional)").pack()
entry_new_checkout=tk.Entry(root)
entry_new_checkout.pack()

tk.Button(root, text="Modify Booking", command=modify_booking).pack(pady=5)

tk.Label(root, text="\nCancel Booking").pack()
tk.Label(root, text="Guest ID").pack()
entry_cancel_guest_id=tk.Entry(root)
entry_cancel_guest_id.pack()

tk.Button(root, text="cancel Booking", command=cancel_booking).pack(pady=5)

root.mainloop()

            
        


