# Options Trading Data API

## Overview

This project is a Python-based API developed using FastAPI that retrieves options trading data for specified stock tickers. The API fetches option chain data, calculates margin requirements, and computes premiums earned for options contracts. The project is designed to assist users in analyzing options trading data in the context of Indian financial markets.

## Features

- Fetches options data for a specified stock ticker using the `yfinance` library.
- Calculates margin required and premium earned for each option.
- Provides a RESTful API endpoint to access the options data.
- Implements error handling for robust data retrieval and processing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shivam909058/options-trading-api.git
   cd options-trading-api
Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

pip install fastapi uvicorn yfinance pandas
Usage
Start the FastAPI server:

uvicorn main:app --reload
Access the API documentation at http://127.0.0.1:8000/docs.

Use the following endpoint to fetch options data:

GET /get_options/{ticker}
Replace {ticker} with the stock ticker symbol (e.g., AAPL for Apple Inc.).

Example Request
GET http://127.0.0.1:8000/get_options/AAPL
Example Response
{
    "options_data": [
        {
            "strike_price": 150,
            "side": "CE",
            "bid": 5.0,
            "ask": 5.5,
            "margin_required": 5000,
            "premium_earned": 500
        },
        {
            "strike_price": 140,
            "side": "PE",
            "bid": 3.0,
            "ask": 3.5,
            "margin_required": 3000,
            "premium_earned": 300
        }
    ]
}
Error Handling
The API includes error handling to manage issues such as:

Invalid ticker symbols
Network errors during data retrieval
Calculation errors
AI Assistance
Throughout the development of this project, AI tools such as ChatGPT were utilized for:

Generating code snippets for data retrieval and calculations.
Clarifying financial concepts related to options trading.
Debugging and improving code structure.
Testing
To ensure the functionality of the API, consider implementing unit tests using pytest. This will help validate the correctness of the data retrieval and calculations.

Contribution
Contributions are welcome! If you have suggestions for improvements or additional features, please feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License.

Contact
For any inquiries, please contact [shivamatvit@gmail.com].

