# Day 6: Data Management

## Today's Goal
Implement features to export and import user data, ensuring data portability and backup capabilities.

## Learning Focus
- Working with CSV and JSON formats in Python.
- File I/O operations for data export and import.
- Handling data validation and error checking during import.

## Fintech Concepts
- **Data Portability**: The ability for users to move their data from one service to another.
- **Data Backup and Recovery**: Ensuring that user data can be saved and restored.
- **Data Validation**: Checking that imported data is in the correct format and meets quality standards.

## Features to Build

### 1. Export Data
- **Flow**:
    1. The user selects "Export Data" from the main menu.
    2. The user is prompted to choose an export format: CSV or JSON.
    3. The application reads all transactions from `transactions.txt` and budgets from `budgets.txt`.
    4. The data is formatted into the chosen format (CSV or JSON).
    5. The formatted data is saved to a file (e.g., `export.csv` or `export.json`) in a new `exports` directory.
    6. A success message is displayed to the user, indicating the location of the exported file.

### 2. Import Data
- **Flow**:
    1. The user selects "Import Data" from the main menu.
    2. The user is prompted to provide the path to the file they want to import.
    3. The application determines the file format (CSV or JSON) based on the file extension.
    4. The application reads the data from the file.
    5. The data is validated to ensure it is in the correct format.
    6. The imported data is appended to the existing `transactions.txt` and `budgets.txt` files.
    7. A success message is displayed to the user, indicating how many transactions and budgets were imported.

## Success Criteria
✅ A new "Data Management" option is available in the main menu.
✅ Users can export their transaction and budget data to CSV and JSON formats.
✅ Users can import data from CSV and JSON files.
✅ The import process includes data validation to prevent errors.
✅ Exported files are saved in a dedicated `exports` directory.
✅ Clear success messages are provided to the user after exporting or importing data.
