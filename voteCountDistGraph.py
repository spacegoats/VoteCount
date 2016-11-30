import praw
import matplotlib.pyplot as plt
import numpy as np

# median deviation filter
# taken from the internet, remember that
def is_outlier(points, thresh=5):
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation
    print("Median threshold is: ", med_abs_deviation)
    return modified_z_score > thresh

# reddit credential bullshit
my_client_id = "ChicYmXzPyjIMQ"
my_client_secret = "QW7E4td2L7iaOwi5-FOeyFMjcTE"
my_user_agent = "Baby Scraping Bot"
my_username = "procedural_goat"
my_password = "Denali1783"

# gathers "reddit" for later use lol
reddit = praw.Reddit(user_agent = my_user_agent,
                        client_id = my_client_id,
                        client_secret = my_client_secret,
                        username = my_username,
                        password = my_password)

# get ID from user and save submission from ID
subID = input("What is the submission ID of the post you want to search?: ")
submission = reddit.submission(id=subID)
print("Submission title: ",     submission.title)  # Output: the title of the submission

scoreList = [] # holds all score values
count = 0

# currrently only iterates through the 1st 500 comments listed
# need to add functionality to "press" more comments.
submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
    scoreList.append(comment.score)
    if comment.score > 0 and comment.score < 6:
        count += 1

print (len(scoreList), "comments recorded.")
print (submission.num_comments, "total comments.")

# ------------------------------------------------------------------------
# convert array to score array
plotArray = [0]*19

numpyScoreList = np.array(scoreList)
filtered = numpyScoreList[~is_outlier(numpyScoreList)]

#find largest num in scoreArray
scoreMax = np.amax(numpyScoreList)
scoreMin = np.amin(numpyScoreList)
filteredScoreMax = np.amax(filtered)
filteredScoreMin = np.amin(filtered)
increment = 1
filteredIncrement = 1

print("The max is: ", scoreMax)
print("The min is: ", scoreMin)

# increment logic
if (scoreMax - scoreMin) > 500:
    increment = 10
    # increment = abs(scoreMax / scoreMin)/2
    print(increment)

if (filteredScoreMax - filteredScoreMin) > 25:
    print(filteredScoreMax - filteredScoreMin, "filtered difference.")
    filteredincrement = 3
    print(filteredIncrement)

# ------------------------------------------
# Histogram Graph Creation
# plt.hist(data, bins=range(min(data), max(data) + binwidth, binwidth))

fig, (ax1,ax2) = plt.subplots(nrows=2)
fig.savefig('whatever.png', facecolor=fig.get_facecolor(), align="left", edgecolor='none')

plt.tight_layout()

ax1.hist(numpyScoreList,
        bins=np.arange(scoreMin, scoreMax+increment, increment),
        align="left",
        edgecolor = "none")
ax1.set_title('Reddit Submission Comment Score Distribution')

ax2.hist(filtered,
        bins=np.arange(filteredScoreMin, filteredScoreMax+filteredIncrement, filteredIncrement),
        edgecolor = "none")
ax2.set_title('NO OUTLIERS: Reddit Submission Comment Score Distribution')

# plt.title("Reddit Submission Comment Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("# of comments")
plt.show()
