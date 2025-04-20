import instaloader
import tkinter as tk
from tkinter import messagebox
import time

# Instaloader instance
L = instaloader.Instaloader()

# Validate Session ID (check length and spaces)
def validate_session(session_id):
    session_id = session_id.strip()  # Remove leading/trailing spaces
    if len(session_id) < 10:  # Minimal length check for valid session ID
        messagebox.showerror("Invalid Session ID", "Session ID is too short or invalid!")
        return False
    return True

# Login function using Session ID
def login_with_session(username, session_id):
    if not validate_session(session_id):  # Validate session before login
        return
    try:
        # Set session cookie manually
        L.context._session.cookies.set("sessionid", session_id)
        print(f"Logged in as {username}")
        messagebox.showinfo("Login Successful", f"Logged in as {username}")
        # Proceed to fetch Instagram data
        fetch_instagram_data(username)
    except Exception as e:
        messagebox.showerror("Session Error", f"Failed to load session: {e}")

# Function to fetch all Instagram data
def fetch_instagram_data(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Fetch Profile Info
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
        
        print("Profile Info:")
        for key, value in profile_info.items():
            print(f"{key}: {value}")

        # Collect Posts, Comments, Likes, Captions
        posts_data = []
        for post in profile.get_posts():
            post_info = {
                "Post URL": post.url,
                "Caption": post.caption,
                "Likes": post.likes,
                "Comments": post.comments,
                "Hashtags": post.caption_hashtags,
                "Post Type": "Video" if post.is_video else "Photo",
                "Date": post.date_utc
            }
            posts_data.append(post_info)
            print(f"Post: {post.url}")
            print(f"Caption: {post.caption}")
            print(f"Likes: {post.likes}, Comments: {post.comments}")
            print(f"Hashtags: {post.caption_hashtags}")
            print(f"Date: {post.date_utc}")
        
        # Fetch Followers and Followings List
        followers = [follower.username for follower in profile.get_followers()]
        followings = [following.username for following in profile.get_followees()]
        
        print(f"\nFollowers ({len(followers)}):")
        for follower in followers:
            print(f"- {follower}")
        
        print(f"\nFollowings ({len(followings)}):")
        for following in followings:
            print(f"- {following}")
        
        # Collect Instagram Stories (if any)
        stories_data = []
        try:
            stories = profile.get_stories()
            for story in stories:
                story_info = {
                    "Story URL": story.url,
                    "Duration": story.duration,
                    "Type": "Photo" if not story.is_video else "Video"
                }
                stories_data.append(story_info)
                print(f"Story URL: {story.url}, Duration: {story.duration}")
        except Exception as e:
            print("No stories available.")

        # Show gathered data in GUI
        messagebox.showinfo("Instagram Data", f"Username: {profile.username}\nFollowers: {profile.followers}\nFollowings: {profile.followees}\nPosts Count: {profile.mediacount}")

    except Exception as e:
        messagebox.showerror("Data Fetch Error", f"Error fetching Instagram data: {e}")

# GUI code for input and login
def open_gui():
    root = tk.Tk()
    root.title("Instagram Session Login")

    # Username input
    tk.Label(root, text="Instagram Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    # Session ID input
    tk.Label(root, text="Session ID").pack()
    session_entry = tk.Entry(root)
    session_entry.pack()

    # Login button
    def on_login():
        username = username_entry.get()
        session_id = session_entry.get()
        login_with_session(username, session_id)

    login_button = tk.Button(root, text="Login", command=on_login)
    login_button.pack()

    # Start GUI
    root.mainloop()

# Run the GUI
open_gui()
