from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from other.ss import (
    API_HASH,
    API_ID,
    api_hash,
    api_id,
    cancel,
    phone_number,
    PASSWORD,
    PHONE_NUMBER,
    password,
    CODE,
    code,
    start 
)
from list.track import setup_track_handlers
from util import get_bot_token, init_app, get_mongo_client
import other.start as other_start
import other.help as help
import channel.add_channel as add_channel
import channel.remove_channel as remove_channel
import admin.add_admin as add_admin
import admin.remove_admin as remove_admin
import channel.remove_owner as remove_owner
import channel.add_owner as add_owner
from list import list_all_channels
import logging
import asyncio
import sys
import platform
from client.scheduler import process_table, remove_process,start_scheduler
from other import log

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = None

async def health_check():
    while True:
        await asyncio.sleep(60)

        if not application.running:
            await shutdown("HealthCheckFailure")
            await main()
            
async def shutdown(signal_name):
    logging.info(f"Received {signal_name}, stopping all tasks...")

    for owner_id in list(process_table.keys()):
        await remove_process(owner_id)
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)  
    

    if application and application.running:
        await application.stop()
        await application.updater.stop()
        await application.shutdown()
    
    sys.exit(0)

async def main():
    global application
    await get_mongo_client()

    application = (
        Application.builder()
        .token(get_bot_token())
        .post_init(init_app)
        .build()
    )

    conv = ConversationHandler(
        entry_points=[CommandHandler('ses_string', start)],
        states={
            API_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, api_id)],
            API_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, api_hash)],
            PHONE_NUMBER: [
                MessageHandler(filters.CONTACT | filters.TEXT, phone_number)
            ],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, code)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    handlers = [
        CommandHandler("start", other_start.start),
        CommandHandler("help", help.help),
        CommandHandler("add_ch", add_channel.add_channel),
        CommandHandler("remove_ch", remove_channel.remove_channel),
        CommandHandler("add_admin", add_admin.add_admin),
        CommandHandler("remove_admin", remove_admin.remove_admin),
        CommandHandler("remove_ses", remove_owner.remove_owner),
        CommandHandler("add_ses", add_owner.add_owner),
        log.get_log_handler(),
        conv
    ]
    
    handlers.extend(list_all_channels.lists())
    setup_track_handlers(application)
    for handler in handlers:
        application.add_handler(handler)
    await start_scheduler()
    logging.info("Bot starting with scheduler integration...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown("KeyboardInterrupt"))
    finally:
        loop.close()