import re
import discord

from tweety.types import Tweet


def is_match_type(tweet: Tweet, enable_type: str):
    tweet_type = 0 if tweet.is_retweet else 1 if tweet.is_quoted else -1
    return tweet_type == -1 or enable_type[tweet_type] == '1'


def is_match_media_type(tweet: Tweet, media_type: str):
    return media_type == '11' or (media_type == '10' and len(tweet.media) == 0) or (media_type == '01' and len(tweet.media) > 0)


def is_match_text_filter(tweet: Tweet, text_filter: str):
    """Check if the tweet text contains the filter string (case-insensitive).
    If text_filter is None or empty, return True (no filtering)."""
    if not text_filter:
        return True
    
    # Get the tweet text - handle both original tweets and retweets
    tweet_text = tweet.text if tweet.text else ""
    
    # Case-insensitive search
    return text_filter.lower() in tweet_text.lower()


def replace_emoji(match: re.Match, guild: discord.Guild):
    emoji_name = match.group(1)
    emoji = discord.utils.get(guild.emojis, name=emoji_name)
    return str(emoji) if emoji else match.group(0)
