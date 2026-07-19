import asyncio
try:
    from holehe import check_email
except ImportError:
    import holehe
    check_email = holehe.check_email

async def run_holehe_async(email):
    # rest of code
