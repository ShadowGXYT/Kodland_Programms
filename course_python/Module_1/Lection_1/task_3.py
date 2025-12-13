print("Hi User")

meme_dict = {
            "CRINGE": "Something strange",
            "LOL": "Something whery funny"
            }
word = input("Please fill in the Word you don't understand (WITH BIG LETTERS!): ")

if word in meme_dict.keys():
    print("Word", word, "means", meme_dict[word])

else:
    print("Not found")
