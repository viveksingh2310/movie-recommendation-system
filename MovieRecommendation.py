import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import random

movies_df = pd.read_csv('movies.csv')
movies_df['genres'] = movies_df['genres'].str.replace('|', ',')
movies_df['combined_features'] = movies_df['genres'] + " " + movies_df['title']

class MovieRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        self.movies_df = movies_df

      
        self.title_label = tk.Label(root, text="Enter Movie Title:", font=("Arial", 12), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        self.title_entry = tk.Entry(root, width=60, font=("Arial", 10))
        self.title_entry.pack(pady=5)

        self.recommend_button = tk.Button(root, text="Show Recommendations", command=self.show_recommendations, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.recommend_button.pack(pady=10)

        self.canvas = tk.Canvas(root, bg="#f0f0f0")
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

      
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def get_recommendations(self, title):
        count_matrix = CountVectorizer().fit_transform(self.movies_df['combined_features'])
        cosine_sim = cosine_similarity(count_matrix)
        
        movie_index = self.movies_df[self.movies_df['title'] == title].index[0]
        searched_movie_genres = self.movies_df.loc[movie_index, 'genres']
        
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
        
        same_genre_movies = []
        other_movies = []
        
        for i, _ in sorted_similar_movies:
            if searched_movie_genres in self.movies_df.loc[i, 'genres']:
                same_genre_movies.append(self.movies_df.iloc[i])
            else:
                other_movies.append(self.movies_df.iloc[i])
            
            if len(same_genre_movies) >= 3 and len(other_movies) >= 3:
                break

        return same_genre_movies, other_movies

    def fetch_poster(self, movie_id):
        image_name = f"movie{random.randint(1, 9)}.png"
        try:
            image = Image.open(image_name)
            return image
        except Exception as e:
            print(f"Error fetching poster for {movie_id}: {e}")
            return None

    def display_movie_grid(self, movies, title):
        row, col = 0, 0
        for movie in movies:
  
            card_frame = tk.Frame(self.scrollable_frame, bg="white", bd=2, relief="groove")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    
            poster = self.fetch_poster(movie['title'])
            if poster:
                img = ImageTk.PhotoImage(poster.resize((120, 180)))
                img_label = tk.Label(card_frame, image=img, bg="white")
                img_label.image = img
                img_label.pack(pady=5)

      
            title_label = tk.Label(card_frame, text=movie['title'], font=("Arial", 10, "bold"), wraplength=120, bg="white", justify="center")
            title_label.pack()

            col += 1
            if col == 4:  
                col = 0
                row += 1

    def show_recommendations(self):
        title = self.title_entry.get()
        if title not in self.movies_df['title'].values:
            messagebox.showerror("Error", "Movie not found!")
            return
        
        movie_index = self.movies_df[self.movies_df['title'] == title].index[0]
        movie_details = self.movies_df.loc[movie_index]

    
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

   
        main_movie_label = tk.Label(self.scrollable_frame, text=f"Main Movie: {movie_details['title']}", font=("Arial", 14, "bold"), pady=10, bg="#f0f0f0")
        main_movie_label.grid(row=0, column=0, columnspan=4)

   
        same_genre_movies, other_movies = self.get_recommendations(title)

   
        tk.Label(self.scrollable_frame, text="Movies with Similar Genre:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=1, column=0, columnspan=4, pady=10)
        self.display_movie_grid(same_genre_movies, "Similar Genre")
      
        start_row = len(same_genre_movies) // 4 + 3
        tk.Label(self.scrollable_frame, text="Movies with Other Genres:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=start_row, column=0, columnspan=4, pady=10)
        self.display_movie_grid(other_movies, "Other Genres")

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")

      
        self.username_label = tk.Label(root, text="Username:", font=("Arial", 10))
        self.username_label.pack(pady=5)
        
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)
        
  
        self.password_label = tk.Label(root, text="Password:", font=("Arial", 10))
        self.password_label.pack(pady=5)
        
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack(pady=5)
     
        self.login_button = tk.Button(root, text="Login", command=self.verify_credentials, font=("Arial", 10), bg="#4CAF50", fg="white")
        self.login_button.pack(pady=10)
        
    def verify_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin":
            self.open_movie_recommender()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")
    
    def open_movie_recommender(self):
        self.root.destroy()
        main_app = tk.Tk()
        MovieRecommenderApp(main_app)
        main_app.mainloop()


login_root = tk.Tk()
LoginPage(login_root)
login_root.mainloop()
