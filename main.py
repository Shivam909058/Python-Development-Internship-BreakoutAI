from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any

app = FastAPI()

# Configuring CORS for proper connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

def clean_numeric_values(value: Any) -> Any:
    """Clean numeric values for JSON serialization."""
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, (np.int64, np.int32)):
        return int(value)
    if isinstance(value, (np.float64, np.float32)):
        if np.isinf(value) or np.isnan(value):
            return None
        return float(value)
    return value

def get_options_data(ticker_symbol: str) -> pd.DataFrame:
    """Fetch options data for the specified stock ticker."""
    try:
        stock = yf.Ticker(ticker_symbol)
        options_dates = stock.options
        
        if not options_dates:
            return pd.DataFrame()
            
        exp_date = options_dates[0]
        option_chain = stock.option_chain(exp_date)
        
        calls = option_chain.calls.assign(option_type='call')
        puts = option_chain.puts.assign(option_type='put')
        
        # Select only necessary columns to avoid serialization issues
        columns_to_keep = [
            'strike', 'bid', 'ask', 'volume', 'openInterest', 
            'impliedVolatility', 'inTheMoney', 'option_type'
        ]
        
        options_data = pd.concat([
            calls[columns_to_keep], 
            puts[columns_to_keep]
        ], ignore_index=True)
        
        return options_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching options data: {str(e)}")

def calculate_margin_and_premium(options_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate margin and premium for the options."""
    try:
        # Margin calculation
        options_df['margin_required'] = options_df.apply(
            lambda row: row['strike'] * (0.20 if row['option_type'] == 'call' else 0.10),
            axis=1
        )
        
        # Premium calculation
        options_df['premium_earned'] = options_df['bid'] * 100
        
        # Return on margin (with safety checks)
        options_df['return_on_margin'] = options_df.apply(
            lambda row: (row['premium_earned'] / row['margin_required'] * 100) 
            if row['margin_required'] > 0 else 0,
            axis=1
        )
        
        return options_df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating margins: {str(e)}")

@app.get("/get_options/{ticker}")
async def get_options(ticker: str) -> Dict[str, Any]:
    try:
        options_data = get_options_data(ticker)
        
        if options_data.empty:
            raise HTTPException(status_code=404, detail=f"No options data available for {ticker}")
        
        options_with_calculations = calculate_margin_and_premium(options_data)
        
        # Convert DataFrame to dict and clean values
        result_data = []
        for record in options_with_calculations.to_dict(orient="records"):
            cleaned_record = {k: clean_numeric_values(v) for k, v in record.items()}
            result_data.append(cleaned_record)
        
        return {
            "success": True,
            "data": result_data
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))