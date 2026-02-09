import re
import discord

from tweety.types import Tweet


def is_match_type(tweet: Tweet, enable_type: str):
    tweet_type = 0 if tweet.is_retweet else 1 if tweet.is_quoted else -1
    return tweet_type == -1 or enable_type[tweet_type] == '1'


def is_match_media_type(tweet: Tweet, media_type: str):
    return media_type == '11' or (media_type == '10' and len(tweet.media) == 0) or (media_type == '01' and len(tweet.media) > 0)


def is_match_text_filter(tweet: Tweet, text_filter: str):
    """Check if the tweet text contains any of the filter strings as whole words (case-insensitive).
    Supports multiple filters separated by commas (match any).
    If text_filter is None or empty, return True (no filtering)."""
    if not text_filter:
        return True
    
    # Get the tweet text - handle both original tweets and retweets
    tweet_text = tweet.text if tweet.text else ""
    
    # Split by comma to support multiple filters (match any)
    filters = [f.strip() for f in text_filter.split(',') if f.strip()]
    
    # Check if any filter matches
    for filter_word in filters:
        # Handle hashtags and special characters - match as whole words
        # For hashtags like #Stream, we want to match #Stream but not #Streaming
        escaped_filter = re.escape(filter_word)
        
        # Use word boundary only after the text, and ensure we're not in the middle of a word
        # This pattern matches if the filter appears and is followed by a non-word character or end of string
        pattern = r'(?<![#\w])' + escaped_filter + r'(?![#\w])'
        if re.search(pattern, tweet_text, re.IGNORECASE):
            return True
    
    return False


def replace_emoji(match: re.Match, guild: discord.Guild):
    emoji_name = match.group(1)
    emoji = discord.utils.get(guild.emojis, name=emoji_name)
    return str(emoji) if emoji else match.group(0)
