# AiPlants
Book Information Extraction and Plant Recommendation System
### Description
This project aims to extract information from books and provide plant recommendations to farmers based on the extracted data. It utilizes various libraries and technologies to achieve this functionality.

The project consists of the following main features:

> Book Information Extraction: The system uses the yargy, pandas, pdfplumber, pytesseract, and pdf2image libraries to extract relevant information from books, such as plant names, descriptions, and other details.

> Plant Recommendation: Based on the extracted book information, the system provides plant recommendations to farmers. It analyzes the data using predefined algorithms and suggests suitable plants for cultivation.

> Telegram Bot Integration: The project integrates with the Telegram platform using the PyTelegramBotAPI library. It allows users to interact with the system through a Telegram bot interface, where they can receive book information, plant recommendations, and perform other related actions.

### Installation
To run this project, you need to install the following libraries using pip:
> yargy, pandas, PyTelegramBotAPI, pdfplumber, pytesseract, pdf2image

You can install these libraries by running the following command:

> pip install yargy pandas PyTelegramBotAPI pdfplumber pytesseract pdf2image

Additionally, make sure you have the necessary dependencies installed for pytesseract to work properly. Refer to the pytesseract documentation for detailed instructions.

### Usage
1. Clone the project repository.
2. Install the required libraries as mentioned in the installation section.
3. Set up the Telegram bot and obtain the bot token from the BotFather.
4. Configure the necessary settings in the project files, such as file paths and API keys.
5. Run the main script to start the Telegram bot and interact with the system.
6. Use the Telegram bot interface to perform book information extraction, receive plant recommendations, and explore other available features.
