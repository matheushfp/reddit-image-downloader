# Reddit Image Downloader

A Python script to download images from Reddit (Reddit image scraper) using PRAW.<br>
The script download static images like JPG and PNG from users and subreddits.

## How to run the code
1. Download the libraries to run the code with `pip install -r requirements.txt`
2. Create a Reddit account [here](https://www.reddit.com/register/)
3. Create an app in Reddit [here](https://reddit.com/prefs/apps/)
4. Put a name of your choice and `http://localhost` in redirect uri
5. Get your client_id and client_secret<br>

| Creating an app  | Getting Credentials |
| ------------- | ------------- |
| <img width="250" height="150" alt="Creating an app" src="https://user-images.githubusercontent.com/72332090/131933617-f9ee6245-69ca-4e07-8af7-414cb15823b6.png">  | <img width="250" height="250" alt="Getting Credentials" src="https://user-images.githubusercontent.com/72332090/131933713-322740ea-61bb-4f8f-867a-a44086ddc49e.png">  |

5. Open the code with an editor and put your credentials here (line 12)<br>You can leave user_agent as it is, or change to something like 'bot v1'
```
reddit = praw.Reddit(
    client_id='XXXXXXXXXXXXXXX',
    client_secret='XXXXXXXXXXXXXXX',
    user_agent='XXXXXXXXXXXXXXX',
)
```

6. Run the script

## Additional Information
You can download images from more than one user or more than one subreddit, depending the option you choose<br>
If you want to download images from more than one subreddit you can put the subreddits names separated by spaces, the same works for users.<br>

Example:<br>
Subreddits names: `cats dogpictures wallpaper`

You may receive less images than the number you put in posts to search, because not every post have images.
