from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from functions import init_webdriver, get_page_source, extract_names_prices  # Import functions from scraper.py
from bs4 import BeautifulSoup


# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'


def start(update: Update, context: CallbackContext):
    """Send a welcome message."""
    update.message.reply_text('Welcome! Use /search to view products.')


def search(update: Update, context: CallbackContext):
    """Fetch and display the list of products, then prompt for a search."""
    chrome_driver_path = r"C:\Users\User\OneDrive\שולחן העבודה\chromedriver-win64\chromedriver.exe"
    url = "https://shop.hazi-hinam.co.il/catalog/46/%D7%A7%D7%A6%D7%91%D7%99%D7%94/10888/%D7%9E%D7%95%D7%A6%D7%A8%D7%99%20%D7%A2%D7%95%D7%A3"

    driver = init_webdriver(chrome_driver_path)
    html_text = get_page_source(driver, url)
    soup = BeautifulSoup(html_text, 'lxml')

    products = extract_names_prices(soup)

    # Display the list of products
    product_list = "\n".join([f"- {name}" for name in products.keys()])
    update.message.reply_text(f"Available products:\n{product_list}")

    # Store the products dictionary for later use
    context.user_data['products'] = products
    update.message.reply_text("Please type the name of the product you want to search for.")

    driver.quit()


def handle_text(update: Update, context: CallbackContext):
    """Handle user input to search for a product."""
    product_name = update.message.text
    products = context.user_data.get('products', {})

    product_info = products.get(product_name)
    if product_info:
        response = f"Product found: {product_name} - Price: {product_info['price']}, Discount: {product_info['discount']}"
    else:
        response = "Product not found."
    update.message.reply_text(response)


def main():
    """Start the Telegram bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
