import aiohttp
import asyncio
from typing import Dict

# ─── 150+ SITES ──────────────────────────────────────────────────
SITES = {
    # Social Media Giants
    "Facebook": "https://facebook.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://instagram.com/{username}",
    "Reddit": "https://reddit.com/user/{username}",
    "Pinterest": "https://pinterest.com/{username}",
    "Tumblr": "https://{username}.tumblr.com",
    "LinkedIn": "https://linkedin.com/in/{username}",
    "YouTube": "https://youtube.com/@{username}",
    "TikTok": "https://tiktok.com/@{username}",
    "Snapchat": "https://snapchat.com/add/{username}",
    "Telegram": "https://t.me/{username}",
    "Discord": "https://discord.com/users/{username}",
    "Twitch": "https://twitch.tv/{username}",
    "VK": "https://vk.com/{username}",
    "Odnoklassniki": "https://ok.ru/profile/{username}",

    # Professional & Dev
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Bitbucket": "https://bitbucket.org/{username}",
    "SourceForge": "https://sourceforge.net/u/{username}",
    "HackerNews": "https://news.ycombinator.com/user?id={username}",
    "StackOverflow": "https://stackoverflow.com/users/{username}",
    "Dev.to": "https://dev.to/{username}",
    "Medium": "https://medium.com/@{username}",
    "Hashnode": "https://hashnode.com/@{username}",
    "WordPress": "https://{username}.wordpress.com",
    "Blogger": "https://{username}.blogspot.com",

    # Coding & Tech
    "LeetCode": "https://leetcode.com/{username}",
    "HackerRank": "https://hackerrank.com/{username}",
    "CodeWars": "https://codewars.com/users/{username}",
    "Exercism": "https://exercism.io/profiles/{username}",
    "TopCoder": "https://topcoder.com/members/{username}",
    "Codeforces": "https://codeforces.com/profile/{username}",
    "AtCoder": "https://atcoder.jp/users/{username}",
    "Kaggle": "https://kaggle.com/{username}",
    "Replit": "https://replit.com/@{username}",
    "CodePen": "https://codepen.io/{username}",
    "Glitch": "https://glitch.com/@{username}",
    "Vercel": "https://vercel.com/{username}",
    "Netlify": "https://netlify.com/{username}",
    "DockerHub": "https://hub.docker.com/u/{username}",
    "PyPI": "https://pypi.org/user/{username}",
    "NPM": "https://npmjs.com/~{username}",
    "RubyGems": "https://rubygems.org/profiles/{username}",

    # Gaming
    "Steam": "https://steamcommunity.com/id/{username}",
    "PlayStation": "https://psnprofiles.com/{username}",
    "Xbox": "https://xboxgamertag.com/{username}",
    "Nintendo": "https://nintendo.com/@{username}",
    "Battle.net": "https://battle.net/{username}",
    "EpicGames": "https://epicgames.com/u/{username}",
    "EA": "https://ea.com/user/{username}",
    "Rockstar": "https://socialclub.rockstargames.com/member/{username}",
    "Minecraft": "https://namemc.com/profile/{username}",
    "Roblox": "https://roblox.com/user/{username}",
    "Mixer": "https://mixer.com/{username}",
    "DLive": "https://dlive.tv/{username}",

    # Music & Audio
    "Spotify": "https://open.spotify.com/user/{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Mixcloud": "https://mixcloud.com/{username}",
    "Last.fm": "https://last.fm/user/{username}",
    "Bandcamp": "https://bandcamp.com/{username}",
    "ReverbNation": "https://reverbnation.com/{username}",
    "Deezer": "https://deezer.com/profile/{username}",
    "Tidal": "https://tidal.com/user/{username}",
    "Splice": "https://splice.com/{username}",
    "Spreaker": "https://spreaker.com/user/{username}",

    # Art & Design
    "Behance": "https://behance.net/{username}",
    "Dribbble": "https://dribbble.com/{username}",
    "Flickr": "https://flickr.com/people/{username}",
    "DeviantArt": "https://deviantart.com/{username}",
    "ArtStation": "https://artstation.com/{username}",
    "Pexels": "https://pexels.com/@{username}",
    "500px": "https://500px.com/{username}",
    "VSCO": "https://vsco.co/{username}",
    "Imgur": "https://imgur.com/user/{username}",
    "Gravatar": "https://gravatar.com/{username}",

    # Video & Streaming
    "Vimeo": "https://vimeo.com/{username}",
    "Dailymotion": "https://dailymotion.com/{username}",
    "Periscope": "https://periscope.tv/{username}",
    "Bigo": "https://bigo.tv/{username}",
    "YouNow": "https://younow.com/{username}",
    "Rumble": "https://rumble.com/user/{username}",
    "Ustream": "https://ustream.tv/channel/{username}",

    # Content & Reading
    "Quora": "https://quora.com/profile/{username}",
    "GoodReads": "https://goodreads.com/{username}",
    "Letterboxd": "https://letterboxd.com/{username}",
    "Anime-Planet": "https://anime-planet.com/users/{username}",
    "MyAnimeList": "https://myanimelist.net/profile/{username}",
    "RateYourMusic": "https://rateyourmusic.com/~{username}",
    "Discogs": "https://discogs.com/user/{username}",
    "Scribd": "https://scribd.com/{username}",
    "Slideshare": "https://slideshare.net/{username}",
    "SpeakerDeck": "https://speakerdeck.com/{username}",

    # Education & Learning
    "KhanAcademy": "https://khanacademy.org/profile/{username}",
    "Duolingo": "https://duolingo.com/profile/{username}",
    "Codecademy": "https://codecademy.com/profiles/{username}",
    "FreeCodeCamp": "https://freecodecamp.org/{username}",
    "Coursera": "https://coursera.org/user/{username}",
    "Udemy": "https://udemy.com/user/{username}",
    "Skillshare": "https://skillshare.com/user/{username}",
    "Pluralsight": "https://pluralsight.com/profile/{username}",
    "Udacity": "https://udacity.com/user/{username}",
    "edX": "https://edx.org/user/{username}",

    # Business & Professional
    "AngelList": "https://angel.co/u/{username}",
    "Crunchbase": "https://crunchbase.com/person/{username}",
    "About.me": "https://about.me/{username}",
    "Keybase": "https://keybase.io/{username}",
    "Mastodon.social": "https://mastodon.social/@{username}",
    "Minds": "https://minds.com/{username}",
    "Gab": "https://gab.com/{username}",
    "Parler": "https://parler.com/{username}",
    "MeWe": "https://mewe.com/i/{username}",

    # Dating & Lifestyle
    "Tinder": "https://tinder.com/@{username}",
    "Bumble": "https://bumble.com/user/{username}",
    "OkCupid": "https://okcupid.com/profile/{username}",
    "Match": "https://match.com/profile/{username}",
    "FetLife": "https://fetlife.com/users/{username}",

    # Travel & Reviews
    "TripAdvisor": "https://tripadvisor.com/members/{username}",
    "Yelp": "https://yelp.com/user_details?userid={username}",
    "Airbnb": "https://airbnb.com/users/show/{username}",
    "Couchsurfing": "https://couchsurfing.com/people/{username}",
    "Meetup": "https://meetup.com/members/{username}",
    "Eventbrite": "https://eventbrite.com/people/{username}",
    "Foursquare": "https://foursquare.com/user/{username}",
    "Swarm": "https://swarmapp.com/user/{username}",

    # Crowdfunding & Commerce
    "ProductHunt": "https://producthunt.com/@{username}",
    "Indiegogo": "https://indiegogo.com/individuals/{username}",
    "Kickstarter": "https://kickstarter.com/profile/{username}",
    "Patreon": "https://patreon.com/{username}",
    "OnlyFans": "https://onlyfans.com/{username}",
    "Substack": "https://substack.com/@{username}",
    "Gumroad": "https://gumroad.com/{username}",
    "Teespring": "https://teespring.com/stores/{username}",
    "Etsy": "https://etsy.com/shop/{username}",
    "Redbubble": "https://redbubble.com/people/{username}",

    # Misc Communities
    "HubPages": "https://hubpages.com/@{username}",
    "Wattpad": "https://wattpad.com/user/{username}",
    "FanFiction": "https://fanfiction.net/u/{username}",
    "ArchiveOfOurOwn": "https://archiveofourown.org/users/{username}",
    "Fandom": "https://fandom.com/u/{username}",
    "Wikia": "https://community.fandom.com/wiki/User:{username}",
    "GitBook": "https://gitbook.com/@{username}",
    "Notion": "https://notion.so/@{username}",
    "Trello": "https://trello.com/{username}",
    "Asana": "https://asana.com/profile/{username}",
    "Slack": "https://slack.com/team/{username}",
    "Zoom": "https://zoom.us/user/{username}",
    "Skype": "https://skype.com/{username}",
    "Guilded": "https://guilded.gg/{username}"
}

# ─── COMMON "NOT FOUND" PHRASES ──────────────────────────────────
NOT_FOUND_PHRASES = [
    "not found", "doesn't exist", "no such user", "page not found",
    "sorry", "404", "could not find", "does not exist", "isn't available",
    "user not found", "profile not found", "account not found",
    "this page could not be found", "we couldn't find", "no results found"
]

# ─── SITE CHECKER (async) ────────────────────────────────────────
async def check_site(session: aiohttp.ClientSession, name: str, url: str, username: str) -> Dict:
    full_url = url.format(username=username)
    try:
        # Use GET to fetch content and inspect for error indicators
        async with session.get(full_url, timeout=15, allow_redirects=True, ssl=False) as resp:
            status = resp.status
            if status == 404:
                return {"site": name, "url": full_url, "exists": False, "error": None}
            if status not in (200, 301, 302):
                return {"site": name, "url": full_url, "exists": False, "error": f"HTTP {status}"}
            # For 200, read a portion of the content (up to 4KB)
            try:
                content = await resp.text(encoding='utf-8', errors='ignore')
            except:
                content = ""
            content_lower = content[:4000].lower()
            for phrase in NOT_FOUND_PHRASES:
                if phrase in content_lower:
                    return {"site": name, "url": full_url, "exists": False, "error": "Not found (detected)"}
            # If no error phrases, assume it exists
            return {"site": name, "url": full_url, "exists": True, "error": None}
    except asyncio.TimeoutError:
        return {"site": name, "url": full_url, "exists": False, "error": "Timeout"}
    except Exception as e:
        return {"site": name, "url": full_url, "exists": False, "error": str(e)[:50]}

# ─── MAIN ASYNC SCAN ─────────────────────────────────────────────
async def run_username_scan(username: str) -> Dict:
    connector = aiohttp.TCPConnector(limit=50, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_site(session, name, url_template, username) for name, url_template in SITES.items()]
        results = await asyncio.gather(*tasks)
    found = [r for r in results if r["exists"]]
    return {
        "username": username,
        "total_checked": len(results),
        "found_count": len(found),
        "found_sites": found
    }

# ─── SYNCHRONOUS WRAPPER ─────────────────────────────────────────
def check_username_sync(username: str) -> Dict:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(run_username_scan(username))
    finally:
        loop.close()
