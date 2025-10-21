# Reddit SEO Agent
Uses your blog posts as grounding for an AI Agent to reply to reddit posts

You will need two sets of API keys to run this agent:

Reddit API Keys: To allow the script to log in and post on your behalf.

Google Gemini API Key: To allow the script to generate comments.

## 1. Reddit API Setup
You need to create a Reddit "app" to get your credentials.

Go to the Reddit Apps Page: Log in to the Reddit account you want to post from, then go to: https://www.reddit.com/prefs/apps/

Create a New App: Scroll to the bottom and click the button that says "are you a developer? create an app...".

Fill Out the Form:

name: My SEO Agent (or any name you want)

type: Select script. This is very important.

description: You can leave this blank.

about url: You can leave this blank.

redirect uri: You must set this to exactly: http://localhost:8080

Save the App: Click the "create app" button.

Get Your Keys: On the next screen, you will see your two keys.

The Client ID is the long string of letters and numbers under the app name.

The Client Secret is the long string labeled secret.

Copy both of these and save them in a temporary text file.

## 2. Google Gemini API Setup
Go to Google AI Studio: Go to https://aistudio.google.com/ and sign in with your Google account.

Get API Key: On the left-hand menu, click "Get API key".

Create New Key: Click the "Create API key in new project" button.

Copy Your Key: A new key will be generated for you. Click the copy icon to copy it to your clipboard.

Copy this key and save it with your Reddit keys.

## 3. Final Project Configuration
Now you will take all the keys you just copied and put them into the project.

The .env File
In your project folder (the same place main.py is), you must have a file named .env. This file holds all your secret keys.

Create the .env file and paste the following text into it:
```
#### Reddit API Credentials
REDDIT_CLIENT_ID=YOUR_CLIENT_ID_HERE
REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
REDDIT_USER_AGENT=My SEO Agent v1.0 by u/your_username
REDDIT_REFRESH_TOKEN=YOUR_REFRESH_TOKEN_GOES_HERE

#### Google Gemini API Key
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

#### Agent Configuration
TARGET_KEYWORD="beginner photography"
YOUR_BLOG_BASE_URL="https://yourwebsite.com/blog/"
Fill in the .env File
REDDIT_CLIENT_ID: Paste the Client ID you got from Reddit here.
REDDIT_CLIENT_SECRET: Paste the Client Secret you got from Reddit here.
REDDIT_USER_AGENT: Change your_username to your actual Reddit username.
GEMINI_API_KEY: Paste the Gemini API key you got from Google AI Studio here.
TARGET_KEYWORD: Change this to the topic you want to search for.
YOUR_BLOG_BASE_URL: Change this to your blog's URL.
```

What about the REDDIT_REFRESH_TOKEN?

You get this last key by running the get_token.py script.

Make sure your REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET are already in the .env file.

Run the check_models.py script to find a valid model name and update main.py.

Run the get_token.py script.

Follow its instructions (it will open your browser).

It will print a Refresh Token in your terminal.

Copy that token and paste it as the value for REDDIT_REFRESH_TOKEN in your .env file.

After you do all these steps, your .env file will be complete, and the main.py script will be ready to run.

## 4.  Add Your Blog Content

This agent works by reading your existing blog posts to generate its helpful comments. You must add your posts as simple text files.

Create the Folder: In your main project folder (the same one as main.py and .env), create a new folder named blog_posts.

Create Your Post Files: Inside the blog_posts/ folder, create a separate .txt file for each blog post you want to use.

Name Your Files: This is important. The name of the file will be used to create the link back to your site. The name should be the "slug" (the part of the URL after your domain).

Example File Name: my-guide-to-cameras.txt

Resulting URL: https://yourwebsite.com/blog/my-guide-to-cameras

Add Content: Copy and paste the full text of your blog post into the .txt file. The script will read this raw text as context for the AI.
