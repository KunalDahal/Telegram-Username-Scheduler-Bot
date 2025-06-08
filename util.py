import os
from dotenv import load_dotenv
from functools import wraps
from telegram import Update
from motor.motor_asyncio import AsyncIOMotorClient
import random
import asyncio

load_dotenv()

_mongo_client = None
_loop = None

def get_event_loop():
    global _loop
    if _loop is None:
        _loop = asyncio.get_event_loop()
    return _loop

async def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(
            os.getenv("MONGODB_URI"),
            io_loop=get_event_loop()
        )
        try:
            await _mongo_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            raise
    return _mongo_client

async def get_db():
    client = await get_mongo_client()
    return client[os.getenv("DB_NAME")]

async def get_admins_collection():
    db = await get_db()
    return db.admins

async def get_logs_collection():
    db = await get_db()
    return db.logs

async def channels_collection():
    db = await get_db()
    return db.channels

async def get_ses_collection():
    db = await get_db()
    return db.sessions

async def get_channels_coll():
    return await channels_collection()

def init_app(app):
    global application
    application = app

def get_bot_token():
    return os.getenv("BOT_TOKEN")

def is_owner(user_id: int) -> bool:
    owner_id = int(os.getenv("OWNER_ID"))
    return user_id == owner_id

async def is_admin(user_id: int) -> bool:
    """Check if user is either owner or listed in admins collection"""
    if is_owner(user_id):
        return True

    admins_col = await get_admins_collection()
    admin_record = await admins_col.find_one({"user_id": user_id})
    return admin_record is not None

def get_random_audio():
    audio_dir = "audios"
    supported_ext = ['.mp3', '.ogg', '.wav', '.m4a', '.oga']
    
    if not os.path.exists(audio_dir):
        raise FileNotFoundError(f"Audio directory '{audio_dir}' not found")
        
    audio_files = [
        os.path.join(audio_dir, f) 
        for f in os.listdir(audio_dir) 
        if os.path.splitext(f)[1].lower() in supported_ext
    ]
    
    if not audio_files:
        raise FileNotFoundError(f"No audio files found in {audio_dir}")
        
    return random.choice(audio_files)

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context, *args, **kwargs):
        user_id = update.effective_user.id
        is_admin_user = await is_admin(user_id)
        
        if not is_admin_user:
            try:

                audio_path = os.path.join(os.path.dirname(__file__), "audios", "start.mp3")
                await update.message.reply_audio(
                    audio=open(audio_path, 'rb'),
                    caption="Use /help for more info",
                    title="✌︎︎",
                )
            except Exception as e:
                await update.message.reply_text("🚫 Access Denied!")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

application = None

def fancy_text(text: str) -> str:
    fancy_map = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
        "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
    )
    return text.translate(fancy_map)