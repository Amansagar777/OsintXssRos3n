import tkinter as tk
from tkinter import messagebox, scrolledtext
import instaloader
import pyperclip
import threading

# Create instaloader instance
L = instaloader.Instaloader()

# GUI function
def start_gui():
    def paste_session():
        session_entry.delete(0, tk.END)
        session_entry.insert(0, pyperclip.paste())

    def validate_session(session_id):
        session_id = session_id.strip()
        return len(session_id) > 10

    def gather_data():
        username = target_entry.get().strip()
        session_id = session_entry.get().strip()

        if not username or not validate_session(session_id):
            messagebox.showerror("Input Error", "Please enter valid target username and session ID.")
            return

        try:
            # Clear any existing session
            L.close()
            L.context._session.cookies.clear()
            L.context._session.cookies.set("sessionid", session_id, domain=".instagram.com")
            profile = instaloader.Profile.from_username(L.context, username)
            
            info = f"Username: {profile.username}\n"
            info += f"Full Name: {profile.full_name}\n"
            info += f"Bio: {profile.biography}\n"
            info += f"Profile Pic URL: {profile.profile_pic_url}\n"
            info += f"Followers: {profile.followers}\n"
            info += f"Following: {profile.followees}\n"
            info += f"Posts: {profile.mediacount}\n"
            joined_date = getattr(profile, "date_joined", "Not Available")
            info += f"Joined: {joined_date}\n"

            print("\n[INFO] Target Profile Data:")
            print(info)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, info + "\n\nFetching Posts...\n")

            posts_data = ""
            for post in profile.get_posts():
                posts_data += f"Post URL: https://www.instagram.com/p/{post.shortcode}/\n"
                posts_data += f"Caption: {post.caption[:100] if post.caption else 'No Caption'}\n"
                posts_data += f"Likes: {post.likes}, Comments: {post.comments}\n\n"

            print("[INFO] Posts:\n" + posts_data)
            output_text.insert(tk.END, posts_data)

            if messagebox.askyesno("Followers Info", "Do you want to fetch followers' info?"):
                followers_data = ""
                for follower in profile.get_followers():
                    followers_data += f"Username: {follower.username}, Full Name: {follower.full_name}\n"
                print("[INFO] Followers:\n" + followers_data)
                output_text.insert(tk.END, "\nFollowers:\n" + followers_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    root = tk.Tk()
    root.title("Osint Xss Ros3n")
    root.geometry("800x600")
    root.configure(bg="#1a1a1a")

    header = tk.Label(root, text="Osint Xss Ros3n", font=("Helvetica", 24, "bold"), fg="white", bg="#1a1a1a")
    header.pack(pady=10)
    subheader = tk.Label(root, text="~ tool coded by @xss_ros3n (Aman Shukla)", font=("Courier", 12), fg="gray", bg="#1a1a1a")
    subheader.pack()

    input_frame = tk.Frame(root, bg="#1a1a1a")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Target Username:", fg="white", bg="#1a1a1a").grid(row=0, column=0, padx=5, pady=5)
    target_entry = tk.Entry(input_frame, width=30)
    target_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Session ID:", fg="white", bg="#1a1a1a").grid(row=1, column=0, padx=5, pady=5)
    session_entry = tk.Entry(input_frame, width=30)
    session_entry.grid(row=1, column=1, padx=5, pady=5)
    paste_btn = tk.Button(input_frame, text="Paste", command=paste_session)
    paste_btn.grid(row=1, column=2, padx=5)

    start_btn = tk.Button(root, text="Start OSINT", command=lambda: threading.Thread(target=gather_data).start(), bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    start_btn.pack(pady=10)

    output_text = scrolledtext.ScrolledText(root, width=95, height=20, wrap=tk.WORD, font=("Courier", 10))
    output_text.pack(padx=10, pady=10)

    root.mainloop()

# Run the GUI
if __name__ == '__main__':
    start_gui()
