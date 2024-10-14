
# Stock Scanner



## Overview
This project implements a stock scanner to identify stocks that have reached a lifetime high, used that high as a strong support level, and subsequently experienced significant price appreciation. The scanner analyzes stock data from the last 10 years to determine how often these conditions occur, along with calculating the annual opportunities and the scanner's success rate.
## Features

- Analyzes stocks listed in the provided NSElist.csv file
- Identifies stocks that:
        - Have reached a lifetime high.
        - Used the lifetime high as a support level.
        - Experienced significant price appreciation.
- Generates visualizations for the analyzed stocks.
- Saves results to a CSV file.
- Calculates the success rate and annual opportunities.


## Requirements

    Python 3.x
    numpy
    pandas
    yfinance
    matplotlib

You can install the required packages:

    pip install pandas yfinance numpy matplotlib
## Run Locally

Clone the project

```bash
  git clone https://github.com/juinaik-1/stockmarket-lifetime-high-analysis
```

Go to the project directory

```bash
  cd stockmarket-lifetime-high-analysis
```

Install dependencies

```bash
  pip install pandas yfinance numpy matplotlib
```

Execute the script in python environment

```bash
  python stockfinder.py

```


## Results

- The results will be saved to a file named stock_scanner_results.csv.
- Visualizations for stocks that meet the criteria will be saved as PNG files in the stockraphs directory.
