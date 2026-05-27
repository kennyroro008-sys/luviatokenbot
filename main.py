import logging
import os
import io
from dotenv import load_dotenv
import qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Load environment variables
load_dotenv()

# Get bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found. Please add it to environment variables.")

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# LUVIA Token Information
WEBSITE = "https://www.LUVIA.exchange"
TELEGRAM_CHANNEL = "https://t.me/luviatoken"
TWITTER_PAGE = "https://twitter.com/LUVIA_Token"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is used"""
    user = update.effective_user
    
    message = f"""🚀 *WELCOME TO LUVIA TOKEN* 🚀

Hey {user.first_name}! Thanks for joining the LUVIA community!

📊 *PROJECT STATUS: PRESALE ACTIVE* 📊

LUVIA is an innovative cryptocurrency project built on the blockchain with real-world utilities.

💰 *PRESALE INFORMATION*
• The project is currently in PRESALE phase
• Join early to get the best prices
• Limited tokens available

👥 *COMMUNITY GROWTH*
• Telegram: 500+ members
• Twitter: 803+ followers

🔗 *OFFICIAL LINKS*
• Website: {WEBSITE}
• Telegram: {TELEGRAM_CHANNEL}
• Twitter: {TWITTER_PAGE}

💡 *COMMANDS*
/presale - Presale details
/stats - Community statistics
/links - All official links
/help - Show all commands

*Don't miss out on this opportunity!* 🚀
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 Website", url=WEBSITE),
            InlineKeyboardButton("💬 Telegram", url=TELEGRAM_CHANNEL)
        ],
        [
            InlineKeyboardButton("🐦 Twitter", url=TWITTER_PAGE),
            InlineKeyboardButton("💰 Presale Info", callback_data="presale")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def presale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send presale information"""
    message = f"""💰 *LUVIA TOKEN PRESALE* 💰

✅ *STATUS: ACTIVE & LIVE*

The LUVIA Token presale is currently happening!

🎯 *WHY JOIN PRESALE?*
• Lowest possible entry price
• Early investor bonuses
• First access to ecosystem
• Higher potential returns

📈 *COMMUNITY GROWTH*
• Telegram: 500+ members
• Twitter: 803+ followers
• Growing daily!

🔗 *JOIN PRESALE*
Visit our website to participate:
{WEBSITE}

⚠️ *IMPORTANT*
Always use official links only. Never share your private keys.

*Secure your LUVIA tokens today!* 🚀
"""
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Join Presale", url=WEBSITE),
            InlineKeyboardButton("💬 Ask Questions", url=TELEGRAM_CHANNEL)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show community statistics"""
    message = f"""📊 *LUVIA TOKEN STATISTICS* 📊

👥 *TELEGRAM COMMUNITY*
• Members: 500+
• Channel: @luviatoken
• Status: Growing rapidly

🐦 *TWITTER (X)*
• Followers: 803+
• Handle: @LUVIA_Token
• Engagement: High

🌐 *WEBSITE*
• URL: {WEBSITE}
• Status: Live

📈 *PRESALE PROGRESS*
• Phase: Early stage
• Opportunity: Active
• Next milestone: 1,000 Telegram members

🎯 *UPCOMING MILESTONES*
✅ Website launched
✅ Presale started
📌 1,000 Telegram members
📌 2,000 Twitter followers
📌 Exchange listing

*Join our growing community!* 🚀
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send all official links"""
    message = f"""🔗 *LUVIA TOKEN OFFICIAL LINKS* 🔗

🌐 *WEBSITE*
{WEBSITE}

💬 *TELEGRAM CHANNEL*
{TELEGRAM_CHANNEL}
(500+ members)

🐦 *TWITTER (X)*
{TWITTER_PAGE}
(803+ followers)

📊 *PRESALE*
Visit website for presale access

⚠️ *WARNING*
These are the ONLY official links. Beware of scams!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 Website", url=WEBSITE),
            InlineKeyboardButton("💬 Telegram", url=TELEGRAM_CHANNEL)
        ],
        [
            InlineKeyboardButton("🐦 Twitter", url=TWITTER_PAGE)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    message = f"""🤖 *LUVIA Token Bot Commands*

/start - Show project information
/presale - Get presale details
/stats - View community statistics
/links - All official links
/help - Show this help message

💡 *QR CODE FEATURE*
Just send me any text or URL and I'll convert it to a QR code!

📢 *PROJECT INFO*
• Presale is ACTIVE
• 500+ Telegram members
• 803+ Twitter followers
• Website: {WEBSITE}

*Need help? Join our Telegram community:* {TELEGRAM_CHANNEL}
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate QR code from text message"""
    text = update.message.text
    
    # Don't generate QR for commands
    if text.startswith('/'):
        return
    
    processing_msg = await update.message.reply_text("🔲 Generating QR code...")
    
    try:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to memory
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        bio.seek(0)
        
        # Send QR code
        await update.message.reply_photo(
            photo=bio,
            caption=f"✅ QR code generated!\n\n💡 Try /start to learn about LUVIA Token presale!"
        )
        
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"QR Error: {e}")
        await processing_msg.edit_text("❌ Failed to generate QR code. Please try again.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "presale":
        # Create a new message instead of editing
        message = f"""💰 *LUVIA TOKEN PRESALE* 💰

✅ *STATUS: ACTIVE & LIVE*

The LUVIA Token presale is currently happening!

🎯 *WHY JOIN PRESALE?*
• Lowest possible entry price
• Early investor bonuses
• First access to ecosystem

🔗 *JOIN PRESALE*
Visit our website to participate:
{WEBSITE}

*Secure your LUVIA tokens today!* 🚀
"""
        keyboard = [[InlineKeyboardButton("💰 Join Presale", url=WEBSITE)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("presale", presale_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("links", links_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler for QR codes (handles all non-command text messages)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))
    
    # Add callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    logger.info("LUVIA Token Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
