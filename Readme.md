# Automated Faculty Publication Summary Generator

This web application allows users to analyze and visualize publication data for scholars based on their Google Scholar profiles. Users can upload an Excel file containing author information, and the application will generate various outputs including publication statistics, graphs, and BibTeX entries.

## Features

- Excel file upload for author information
- Date range selection for publication analysis
- Generation of publication statistics per subject
- Interactive bar graph visualization of publication counts
- BibTeX output for easy citation management
- Excel output with detailed publication information

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/scholar-publication-analyzer.git
   cd scholar-publication-analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Upload an Excel file containing author information (columns should include 'author', 'authorID', and 'subject').

4. Select the date range for analysis (optional).

5. Submit the form to generate the analysis.

6. View the results, including the graph, and download Excel or BibTeX outputs as needed.

## Requirements

This project requires Python 3.7+ and the following main packages:

- Flask
- pandas
- matplotlib
- requests
- openpyxl
- xlsxwriter

For a complete list of dependencies, please refer to the `requirements.txt` file.

## Configuration

- The application uses the SerpAPI for fetching Google Scholar data. Make sure to replace the API key in the `get_data` function with your own SerpAPI key.
- The maximum file upload size is set to 16MB. You can adjust this in the `app.config['MAX_CONTENT_LENGTH']` setting.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
