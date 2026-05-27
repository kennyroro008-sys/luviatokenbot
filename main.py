import logging
import os
import io
from dotenv import load_dotenv
import qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from the .env file
load_dotenv()

# Get the bot token from the environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file. Please add it.")

# Enable logging to see what your bot is doing
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# LUVIA Token Information
PROJECT_INFO = {
    "name": "🚀 LUVIA TOKEN",
    "status": "🔥 PRESALE ACTIVE 🔥",
    "description": "LUVIA is an innovative cryptocurrency project built on the blockchain, offering unique utilities and real-world applications.",
    "website": "https://www.LUVIA.exchange",
    "telegram": "https://t.me/luviatoken",
    "twitter": "https://twitter.com/LUVIA_Token",  # Update with actual Twitter handle if different
    "telegram_members": "500+",
    "twitter_followers": "803+",
    "presale_info": "The project is currently in its presale phase! Join early to secure your tokens at the best price."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with LUVIA Token information when /start command is issued."""
    user = update.effective_user
    
    # Create welcome message
    welcome_message = f"""
🌟 *WELCOME TO {PROJECT_INFO['name']}* 🌟

{PROJECT_INFO['description']}

📊 *PROJECT STATUS*
{PROJECT_INFO['status']}

💰 *PRESALE INFORMATION*
{PROJECT_INFO['presale_info']}

👥 *COMMUNITY GROWTH*
• Telegram: {PROJECT_INFO['telegram_members']} members
• Twitter: {PROJECT_INFO['twitter_followers']} followers

🔗 *OFFICIAL LINKS*
• Website: {PROJECT_INFO['website']}
• Telegram Channel: {PROJECT_INFO['telegram']}
• Twitter Page: {PROJECT_INFO['twitter']}

💡 *HOW TO USE ME*
• Ask me anything about LUVIA Token
• Send me any text to generate a QR code
• Use /help to see all commands

*Don't miss out on the presale opportunity!* 🚀
"""
    
    # Create inline keyboard buttons
    keyboard = [
        [
            InlineKeyboardButton("🌐 Website", url=PROJECT_INFO['website']),
            InlineKeyboardButton("💬 Telegram", url=PROJECT_INFO['telegram'])
        ],
        [
            InlineKeyboardButton("🐦 Twitter", url=PROJECT_INFO['twitter']),
            InlineKeyboardButton("📊 Presale Info", callback_data="presale_info")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message with available commands."""
    help_text = """
🤖 *LUVIA Token Bot Commands*

/start - Display project information and links
/help - Show this help message
/presale - Get detailed presale information
/stats - View current community statistics
/website - Get the official website link
/telegram - Join our Telegram community
/twitter - Follow us on Twitter
/qr [text] - Generate QR code from text (or just send any text)

*Quick Tips:*
• Just ask me questions like "What is LUVIA?" or "How to buy?"
• Send me any text or URL to convert it into a QR code
• Click the buttons below for quick access to important links

*Stay connected and don't miss the presale!* 🚀
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def presale_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send detailed presale information."""
    presale_text = """
💰 *LUVIA TOKEN PRESALE DETAILS* 💰

✅ *PRESALE STATUS: ACTIVE*
The project is currently in its presale phase!

📈 *WHY JOIN PRESALE?*
• Get tokens at the lowest possible price
• Early investor bonuses
• First access to platform features
• Higher potential returns

👥 *COMMUNITY STRENGTH*
• Telegram: 500+ active members
• Twitter: 803+ followers and growing

🔗 *USEFUL LINKS*
• Website: https://www.LUVIA.exchange
• Telegram: https://t.me/luviatoken
• Twitter: @LUVIA_Token

⚠️ *IMPORTANT*
Always verify links and never share your private keys. Official links are listed above.

*Secure your spot in the LUVIA ecosystem today!* 🚀
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 Visit Website", url=PROJECT_INFO['website']),
            InlineKeyboardButton("💬 Join Telegram", url=PROJECT_INFO['telegram'])
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(presale_text, parse_mode='Markdown', reply_markup=reply_markup)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current community statistics."""
    stats_text = f"""
📊 *LUVIA TOKEN COMMUNITY STATISTICS* 📊

👥 *TELEGRAM*
• Members: {PROJECT_INFO['telegram_members']}
• Channel: @luviatoken
• Status: Growing daily!

🐦 *TWITTER (X)*
• Followers: {PROJECT_INFO['twitter_followers']}+
• Handle: @LUVIA_Token
• Engagement: High community interaction

🌐 *WEBSITE TRAFFIC*
• Daily visitors: Growing steadily
• Presale interest: Strong

📈 *PROJECT MILESTONES*
✅ Website launched
✅ Smart contract deployed
✅ Presale started
🎯 1,000 Telegram members (upcoming)
🎯 2,000 Twitter followers (upcoming)
🎯 Exchange listing (post-presale)

*Join our growing community!* 🚀
"""
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send website link."""
    keyboard = [[InlineKeyboardButton("🌐 Visit LUVIA.exchange", url=PROJECT_INFO['website'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🌐 *Official LUVIA Token Website*\n{PROJECT_INFO['website']}\n\nClick the button below to visit our website!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def telegram_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send Telegram channel link."""
    keyboard = [[InlineKeyboardButton("💬 Join Telegram Channel", url=PROJECT_INFO['telegram'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"💬 *Join LUVIA Token Telegram Community*\n{PROJECT_INFO['telegram']}\n\n{PROJECT_INFO['telegram_members']}+ active members waiting for you!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def twitter_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send Twitter page link."""
    keyboard = [[InlineKeyboardButton("🐦 Follow on Twitter", url=PROJECT_INFO['twitter'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🐦 *Follow LUVIA Token on Twitter*\n{PROJECT_INFO['twitter']}\n\n{PROJECT_INFO['twitter_followers']}+ followers and growing!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user questions about LUVIA Token."""
    text = update.message.text.lower()
    
    # Question patterns and responses
    if any(word in text for word in ['what is luvia', 'what is luvia token', 'about luvia']):
        response = f"""
🌟 *About LUVIA Token* 🌟

LUVIA is an innovative cryptocurrency project designed to provide real-world utility and value to its holders.

*Key Features:*
• Built on secure blockchain technology
• Community-driven development
• Real-world applications
• Transparent team and operations

*Current Status:* {PROJECT_INFO['status']}

*Learn more:* {PROJECT_INFO['website']}
"""
        await update.message.reply_text(response, parse_mode='Markdown')
    
    elif any(word in text for word in ['presale', 'buy', 'purchase', 'invest']):
        keyboard = [[InlineKeyboardButton("💰 Join Presale", url=PROJECT_INFO['website'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🔥 *LUVIA Token Presale is LIVE!* 🔥\n\n{PROJECT_INFO['presale_info']}\n\nVisit our website to participate in the presale!",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif any(word in text for word in ['price', 'cost', 'value']):
        await update.message.reply_text(
            f"💰 *LUVIA Token Pricing* 💰\n\n"
            f"Presale price information is available on our official website.\n\n"
            f"🌐 Check {PROJECT_INFO['website']} for current presale rates and bonus structures.\n\n"
            f"Join early to get the best prices! 🚀"
        )
    
    elif any(word in text for word in ['telegram', 'group', 'channel']):
        keyboard = [[InlineKeyboardButton("💬 Join Telegram", url=PROJECT_INFO['telegram'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"📱 *Join our Telegram Community!*\n\n"
            f"Current members: {PROJECT_INFO['telegram_members']}+\n"
            f"Link: {PROJECT_INFO['telegram']}\n\n"
            f"Get news, updates, and support from the team!",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif any(word in text for word in ['twitter', 'x', 'social media']):
        keyboard = [[InlineKeyboardButton("🐦 Follow on Twitter", url=PROJECT_INFO['twitter'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🐦 *Follow us on Twitter/X!*\n\n"
            f"Followers: {PROJECT_INFO['twitter_followers']}+\n"
            f"Handle: @LUVIA_Token\n\n"
            f"Stay updated with the latest announcements!",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    elif any(word in text for word in ['roadmap', 'future', 'plan']):
        await update.message.reply_text(
            f"🗺️ *LUVIA Token Roadmap* 🗺️\n\n"
            f"*Phase 1 - Current (Presale)*\n"
            f"✅ Website Launch\n"
            f"✅ Smart Contract Deployment\n"
            f"✅ Presale Initiation\n"
            f"✅ Community Building\n\n"
            f"*Phase 2 (Coming Soon)*\n"
            f"• Exchange Listings\n"
            f"• Marketing Campaigns\n"
            f"• Strategic Partnerships\n\n"
            f"*Phase 3 (Future)*\n"
            f"• Platform Development\n"
            f"• Ecosystem Expansion\n"
            f"• Real-world Utility\n\n"
            f"Visit {PROJECT_INFO['website']} for detailed roadmap! 🚀"
        )
    
    else:
        # If not a question about LUVIA, offer QR code generation
        await generate_qr(update, context)

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a QR code from the user's text message (kept as utility feature)."""
    text_to_encode = update.message.text
    
    if not text_to_encode:
        return

    # Let the user know we're working on it
    processing_msg = await update.message.reply_text("🔲 Generating QR code...")

    try:
        # Create the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text_to_encode)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image to a bytes buffer (in-memory file)
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        bio.seek(0)
        
        # Send the image back to the user
        await update.message.reply_photo(
            photo=bio, 
            caption=f"✅ QR code generated for your text!\n\n💡 *Want to learn about LUVIA Token?* Use /start"
        )
        
        # Delete the "processing" message
        await processing_msg.delete()

    except Exception as e:
        logger.error(f"Error generating QR: {e}")
        await processing_msg.edit_text("❌ Sorry, an error occurred. Please try again or use /help for available commands.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "presale_info":
        await presale_info(update, context)
    elif query.data == "help":
        await help_command(update, context)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("presale", presale_info))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("website", website_command))
    application.add_handler(CommandHandler("telegram", telegram_command))
    application.add_handler(CommandHandler("twitter", twitter_command))

    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_questions))
    
    # Register callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the Bot using polling
    logger.info("LUVIA Token Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
