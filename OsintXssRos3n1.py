import instaloader
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Initialize Instaloader instance
L = instaloader.Instaloader()

# Validate Session ID (ensure it's not empty or too short)
def validate_session(session_id):
    session_id = session_id.strip()
    if len(session_id) < 10:  # Minimal length check for valid session ID
        messagebox.showerror("Invalid Session ID", "Session ID is too short or invalid!")
        return False
    return True

# Login function using Session ID
def login_with_session(username, session_id, result_text):
    if not validate_session(session_id):
        return
    
    try:
        # Manually set the session using the session ID (no need for session file)
        L.context._session.cookies.set("sessionid", session_id)
        print(f"Logged in as {username}")
        messagebox.showinfo("Login Successful", f"Logged in as {username}")
        
        # Proceed to fetch Instagram data
        fetch_instagram_data(username, result_text)

    except Exception as e:
        messagebox.showerror("Session Error", f"Failed to load session: {e}")
        print(f"Error: {e}")

# Function to fetch Instagram data
def fetch_instagram_data(username, result_text):
    try:
        # Fetch the Instagram profile data using instaloader
        profile = instaloader.Profile.from_username(L.context, username)

        # Display profile info
        profile_info = {
            "Username": profile.username,
            "Name": profile.full_name,
            "Bio": profile.biography,
            "Followers": profile.followers,
            "Followings": profile.followees,
            "Profile Picture": profile.profile_pic_url,
            "Is Private": profile.is_private,
            "Is Verified": profile.is_verified,
            "Posts Count": profile.mediacount
        }

        result_text.insert(tk.END, "Profile Info:\n")
        for key, value in profile_info.items():
            result_text.insert(tk.END, f"{key}: {value}\n")

        # Collect and display posts, captions, likes, comments, and hashtags
        result_text.insert(tk.END, "\nPosts Data:\n")
        for post in profile.get_posts():
            result_text.insert(tk.END, f"Post URL: {post.url}\n")
            result_text.insert(tk.END, f"Caption: {post.caption}\n")
            result_text.insert(tk.END, f"Likes: {post.likes}, Comments: {post.comments}\n")
            result_text.insert(tk.END, f"Hashtags: {post.caption_hashtags}\n")
            result_text.insert(tk.END, f"Post Type: {'Video' if post.is_video else 'Photo'}\n")
            result_text.insert(tk.END, f"Date: {post.date_utc}\n\n")

        # Collect and display followers and followings list
        result_text.insert(tk.END, f"\nFollowers ({profile.followers}):\n")
        followers = [follower.username for follower in profile.get_followers()]
        for follower in followers:
            result_text.insert(tk.END, f"- {follower}\n")

        result_text.insert(tk.END, f"\nFollowings ({profile.followees}):\n")
        followings = [following.username for following in profile.get_followees()]
        for following in followings:
            result_text.insert(tk.END, f"- {following}\n")

        # Ask if user wants to fetch followers' details
        fetch_followers = simpledialog.askstring("Fetch Followers' Data", "Do you want to fetch details for followers? (yes/no)").lower()

        if fetch_followers == 'yes':
            result_text.insert(tk.END, "\nFetching Followers' Data:\n")
            fetch_followers_data(followers, result_text)

        # Collect Instagram stories (if any)
        try:
            stories = profile.get_stories()
            result_text.insert(tk.END, "\nInstagram Stories:\n")
            for story in stories:
                result_text.insert(tk.END, f"Story URL: {story.url}, Duration: {story.duration}\n")
        except Exception as e:
            result_text.insert(tk.END, "\nNo stories available.\n")
        
        # Scroll to the bottom of the text widget to show latest content
        result_text.yview(tk.END)

    except Exception as e:
        messagebox.showerror("Data Fetch Error", f"Error fetching Instagram data: {e}")
        print(f"Error: {e}")

# Function to fetch followers' details (email, phone number if available)
def fetch_followers_data(followers, result_text):
    for follower in followers:
        try:
            follower_profile = instaloader.Profile.from_username(L.context, follower)
            result_text.insert(tk.END, f"\nFollower: {follower_profile.username}\n")
            result_text.insert(tk.END, f"Bio: {follower_profile.biography}\n")
            result_text.insert(tk.END, f"Followers: {follower_profile.followers}, Followings: {follower_profile.followees}\n")
            result_text.insert(tk.END, f"Is Verified: {follower_profile.is_verified}\n")
            result_text.insert(tk.END, f"Is Private: {follower_profile.is_private}\n")
            result_text.insert(tk.END, f"Profile Pic URL: {follower_profile.profile_pic_url}\n")

            # Placeholder logic for email and phone (can't directly fetch these from Instagram)
            try:
                email = follower_profile.external_url  # Example placeholder, Instagram API doesn't allow direct access to private emails
                result_text.insert(tk.END, f"Email: {email}\n")
            except:
                result_text.insert(tk.END, f"Email: Not Available\n")

            try:
                result_text.insert(tk.END, f"Phone Number: Not Available\n")  # Phone numbers are not available via the API
            except:
                result_text.insert(tk.END, f"Phone Number: Not Available\n")

        except Exception as e:
            result_text.insert(tk.END, f"Error fetching data for follower {follower}: {e}\n")

# GUI for input and login
def open_gui():
    # Set up root window
    root = tk.Tk()
    root.title("Instagram Session Login")
    root.geometry("800x700")  # Larger window
    
    # Styling for the GUI
    root.configure(bg="#f0f0f0")

    # Username input
    tk.Label(root, text="Instagram Username", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    username_entry = tk.Entry(root, font=("Arial", 12), width=40)
    username_entry.pack(pady=5)

    # Session ID input
    tk.Label(root, text="Session ID", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    session_entry = tk.Entry(root, font=("Arial", 12), width=40)
    session_entry.pack(pady=5)

    # Scrollable Text Area for displaying results
    result_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Arial", 12))
    result_text.pack(padx=10, pady=10)

    # Login button
    def on_login():
        username = username_entry.get()
        session_id = session_entry.get()
        login_with_session(username, session_id, result_text)

    login_button = tk.Button(root, text="Login and Fetch Data", font=("Arial", 12), command=on_login, bg="#4CAF50", fg="white")
    login_button.pack(pady=20)

    # Start GUI
    root.mainloop()

# Run the GUI
open_gui()
