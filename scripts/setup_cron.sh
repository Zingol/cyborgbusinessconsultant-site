#!/bin/bash
# Setup cron job for weekly blog post generation
# Run this script once to set up the automation

echo "Setting up weekly blog post automation..."

# Make the Python script executable
chmod +x /Users/zingo/Documents/SITI_WEB/cyborgbusinessconsultant-site/scripts/weekly_blog_generator.py

# Create cron job entry
SCRIPT_PATH="/Users/zingo/Documents/SITI_WEB/cyborgbusinessconsultant-site/scripts/weekly_blog_generator.py"
LOG_PATH="/Users/zingo/Documents/SITI_WEB/cyborgbusinessconsultant-site/scripts/blog_generator.log"

# Cron job: Every Monday at 8:00 AM
CRON_ENTRY="0 8 * * 1 cd /Users/zingo && /usr/bin/python3 $SCRIPT_PATH >> $LOG_PATH 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job installed successfully!"
echo "📅 Will run every Monday at 8:00 AM"
echo "📄 Logs will be saved to: $LOG_PATH"
echo ""
echo "To verify cron job:"
echo "crontab -l"
echo ""
echo "To test manually:"
echo "python3 $SCRIPT_PATH"
echo ""
echo "To remove cron job:"
echo "crontab -e  # then delete the line"
