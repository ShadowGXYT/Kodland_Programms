vokals = "a, e, i, o, u"

word = input("Please fill in the Word on witch you want to know tha count of vokals (with small Letters): ")

count_vokals = sum(1 for letter in word if letter in vokals)

print("There is/are",count_vokals , "vokals")
