# main.py

import os
import praw
import time
from dotenv import load_dotenv

# --- Import Google Gemini library ---
import google.generativeai as genai

# --- CONFIGURATION ---
# Load environment variables from the .env file
load_dotenv()

# Reddit API Credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_REFRESH_TOKEN = os.getenv("REDDIT_REFRESH_TOKEN")

# --- Configure Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Agent Settings
TARGET_KEYWORD = os.getenv("TARGET_KEYWORD")
YOUR_BLOG_BASE_URL = os.getenv("YOUR_BLOG_BASE_URL")
BLOG_POSTS_DIR = "blog_posts"
COMMENTED_LOG_FILE = "commented_posts.log"
HOT_POST_LIMIT = 10 

# --- HELPER FUNCTIONS ---

def load_blog_posts():
    """
    Loads all blog posts from the 'blog_posts' directory into memory.
    Returns a dictionary where keys are filenames (slugs) and values are the content.
    """
    blog_data = {}
    print(f"Loading blog posts from '{BLOG_POSTS_DIR}'...")
    for filename in os.listdir(BLOG_POSTS_DIR):
        if filename.endswith(".txt"):
            slug = os.path.splitext(filename)[0]
            with open(os.path.join(BLOG_POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                blog_data[slug] = f.read()
    print(f"Loaded {len(blog_data)} blog posts.")
    return blog_data

def find_best_blog_post_match(post_title, blog_data):
    """
    Finds the most relevant blog post based on the Reddit post's title.
    """
    post_title_words = set(post_title.lower().split())
    best_match_slug = None
    max_overlap = 0

    for slug, content in blog_data.items():
        slug_words = set(slug.replace('-', ' ').lower().split())
        overlap = len(post_title_words.intersection(slug_words))
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_match_slug = slug

    return best_match_slug

# --- UPDATED: This function now uses Gemini ---
def generate_comment(post_title, blog_content):
    """
    Uses Google's Gemini to generate a helpful comment based on the blog post.
    """
    print("Generating AI comment with Gemini...")
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = f"""
        A Reddit user has created a post titled: "{post_title}".
        
        Based on the following article text, write a helpful and insightful comment that adds value to the discussion.
        The comment should be written in a conversational, friendly tone, as if a real person is helping out.
        Do NOT sound like a marketing bot. Be genuinely helpful.
        Start the comment naturally without introducing yourself or the article.
        
        Article text:
        ---
        {blog_content[:4000]} 
        ---
        
        Generate only the comment text.
        """
        
        # Generate the content
        response = model.generate_content(prompt)
        
        # Extract the text from the response
        comment_text = response.text.strip()
        return comment_text
        
    except Exception as e:
        print(f"Error generating comment with Gemini: {e}")
        return None

def load_commented_posts():
    """
    Loads the set of post IDs that have already been commented on.
    """
    if not os.path.exists(COMMENTED_LOG_FILE):
        return set()
    with open(COMMENTED_LOG_FILE, 'r') as f:
        return set(line.strip() for line in f)

def log_commented_post(post_id):
    """
    Adds a post ID to the log file to avoid commenting again.
    """
    with open(COMMENTED_LOG_FILE, 'a') as f:
        f.write(post_id + '\n')

# --- MAIN AGENT LOGIC ---

def main():
    """
    The main function to run the Reddit SEO Agent.
    """
    print("--- Reddit SEO Agent Initializing ---")
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            refresh_token=REDDIT_REFRESH_TOKEN,
        )
        print(f"Successfully authenticated as Reddit user: {reddit.user.me()}")
    except Exception as e:
        print(f"Failed to authenticate with Reddit: {e}")
        print("Please ensure your REFRESH_TOKEN is correct in the .env file.")
        return

    blog_data = load_blog_posts()
    commented_posts = load_commented_posts()
    
    if not blog_data:
        print("No blog posts found. Please add .txt files to the 'blog_posts' directory.")
        return

    print(f"\nSearching for posts related to keyword: '{TARGET_KEYWORD}'")

    try:
        for subreddit in reddit.subreddits.search(TARGET_KEYWORD, limit=5):
            print(f"\nScanning subreddit: r/{subreddit.display_name}")
            
            for post in subreddit.hot(limit=HOT_POST_LIMIT):
                if TARGET_KEYWORD in post.title.lower() and post.id not in commented_posts and not post.archived:
                    print(f"\nFound a relevant post: '{post.title}' (ID: {post.id})")
                    
                    best_match_slug = find_best_blog_post_match(post.title, blog_data)
                    
                    if best_match_slug:
                        print(f"Best blog post match: '{best_match_slug}.txt'")
                        blog_content = blog_data[best_match_slug]
                        
                        ai_comment = generate_comment(post.title, blog_content)
                        
                        if ai_comment:
                            blog_link = YOUR_BLOG_BASE_URL + best_match_slug
                            full_comment = f"{ai_comment}\n\n---\n*For more details, you can check out this guide: [{best_match_slug.replace('-', ' ').title()}]({blog_link})*"
                            
                            print("--- PREVIEW OF COMMENT ---")
                            print(full_comment)
                            print("--------------------------")
                            
                            try:
                                post.reply(full_comment)
                                print("Successfully posted comment!")
                                log_commented_post(post.id)
                                print("Waiting for 10 minutes before next action...")
                                time.sleep(600) 
                            except Exception as e:
                                print(f"Failed to post comment: {e}")

                        else:
                            print("Could not generate a comment.")
                    else:
                        print("No relevant blog post found for this title.")
                    
                    log_commented_post(post.id)
            
    except Exception as e:
        print(f"An error occurred while scanning subreddits: {e}")

    print("\n--- Agent has finished its run ---")

if __name__ == "__main__":
    main()