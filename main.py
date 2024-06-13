import csv
from tkinter import *
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

gui_root = Tk()
#weitht and height of frame
gui_root.geometry("450x600")
gui_root.minsize(325,500)
gui_root.maxsize(500,900)

# gui design
gui_root.title("Movie recommended system")
photo = PhotoImage(file = "1.png")
pic = Label(image = photo, padx = 5, pady =95)
pic.pack()
txt =Label(text = "Please Select Movie Name From ComboBox", font = "lucid 15 " ,padx = 5, pady =5)
txt.pack()
#gui input
#loading data in combo box from csv file
with open('F:\year3\AI\development\movie_data.csv', encoding= 'utf-8-sig') as csvfile:
	reader = csv.DictReader(csvfile)
	counts = 0
	mlist = []
	for row in reader:
		counts = counts +1
		mlist.append(row['original_title'])
		if counts>4000:
			break

movieList = StringVar()
movieList.set("Avatar")
menues = OptionMenu(gui_root, movieList, *mlist)
menues.pack()
#method to perform action for a button
def MovieRecommended():
    res = ""+movieList.get()

    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]
    def get_index_from_title(title):
        return df[df.title == title]["index"].values[0]

    # Read CSV File
    df = pd.read_csv("F:\year3\AI\development\movie_data.csv")
    #Select Features
    features = ['keywords', 'cast', 'genres', 'director']

    #  Create a column in DF known as dataframe which combines all selected features
    for feature in features:
        df[feature] = df[feature].fillna('')

    def combine_features(row):
        try:
            return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
        except:
            print("Error:", row)
    df["combined_features"] = df.apply(combine_features, axis=1)

    # Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    # Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix)
    movie_user_likes = res

    # Get index of this movie from its title
    movie_index = get_index_from_title(movie_user_likes)

    similar_movies = list(enumerate(cosine_sim[movie_index]))

    # Get a list of similar movies in descending order of similarity score
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    # Print titles of first 10 movies
    recommendMovie = ""
    i = 0
    for element in sorted_similar_movies:
        recommendMovie +="\n  "+ get_title_from_index(element[0])
        i = i + 1
        if i > 10:
            break
    result.configure(text = recommendMovie, padx = 5, )
# Create a Button and call the method
btn = Button(gui_root, text='Recommend me !', bd='5', fg = "green",command=MovieRecommended)
# Set the position of button on the top of window.
btn.pack(side='top')

#display result
result =Label(text = "", font = "lucid 10 " ,padx = -5, pady =15)
result.pack()

gui_root.mainloop()
