import tkinter as tk
from tkinter import messagebox, scrolledtext
import instaloader

# Function to log in using session ID and username
def login_with_session(username, session_id):
    try:
        # Initialize Instaloader
        L = instaloader.Instaloader()

        # Manually set the session
        L.context._session.cookies.set("sessionid", session_id)  # Directly set session cookie
        L.context.username = username  # Set username in context

        # Verify session by attempting to fetch the profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"Logged in as {profile.username}")
        return L

    except Exception as e:
        messagebox.showerror("Session Error", f"Failed to load session: {e}")
        return None

# Function to fetch Instagram profile information
def fetch_instagram_data(L, username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        data = []
        data.append(f"Username: {profile.username}")
        data.append(f"Full Name: {profile.full_name}")
        data.append(f"Bio: {profile.biography}")
        data.append(f"Followers: {profile.followers}")
        data.append(f"Following: {profile.followees}")
        data.append(f"Posts: {profile.mediacount}")
        data.append(f"Profile Pic: {profile.profile_pic_url}")
        
        # Fetch posts' captions, likes, and comments
        data.append("\nPosts Information:")
        for post in profile.get_posts():
            data.append(f"Caption: {post.caption}")
            data.append(f"Likes: {post.likes}")
            data.append(f"Comments: {post.comments}")
            if len(data) > 15:  # Limit number of posts for now to avoid overload
                break

        return "\n".join(data)
    except Exception as e:
        messagebox.showerror("Fetch Error", f"Error fetching data: {e}")
        return None

# Function to handle the login button press
def on_login():
    username = entry_username.get()
    session_id = entry_session.get()
    
    if not username or not session_id:
        messagebox.showwarning("Input Error", "Please fill both Username and Session ID fields!")
        return
    
    L = login_with_session(username, session_id)
    if L is None:
        return
    
    data = fetch_instagram_data(L, username)
    if data:
        display_data(data)

# Function to display the fetched data in the scrollable text area
def display_data(data):
    # Clear existing data
    text_output.delete(1.0, tk.END)
    
    # Insert the new data
    text_output.insert(tk.END, data)
    text_output.yview(tk.END)  # Auto-scroll to the end

# Create the main GUI window
root = tk.Tk()
root.title("OsintXssRos3n Tool")
root.geometry("600x500")

# Add the title
title_label = tk.Label(root, text="OsintXssRos3n", font=("Arial", 28, "bold"), fg="blue")
title_label.pack(pady=20)

# Add small description below title
desc_label = tk.Label(root, text="~ Tool coded by @xss_ros3n (Aman Shukla)", font=("Arial", 12), fg="gray")
desc_label.pack()

# Add input fields for username and session ID
label_username = tk.Label(root, text="Instagram Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(root, width=40)
entry_username.pack(pady=5)

label_session = tk.Label(root, text="Session ID:")
label_session.pack(pady=5)
entry_session = tk.Entry(root, width=40)
entry_session.pack(pady=5)

# Add login button
login_button = tk.Button(root, text="Login and Fetch Data", command=on_login)
login_button.pack(pady=20)

# Add a scrollable text area to display the results
text_output = scrolledtext.ScrolledText(root, width=70, height=15)
text_output.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
