# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (optional, Railway will override with dashboard values)
# ENV BOT_TOKEN=your-telegram-bot-token-here
# ENV ADMIN_ID=8158960738

# Start the bot
CMD ["python", "telegram_bot.py"]
