# 👥 Gender Classification Tool

A simple web application for classifying names by gender in Excel files. Upload an XLSX file, select a column containing names, and get a new file with gender codes (1 = Male, 2 = Female, ? = Uncertain).

## 🚀 Features

- **📁 File Upload**: Drag & drop or browse Excel files (.xlsx, .xls)
- **📋 Column Selection**: Choose name column from dropdown or type manually
- **🤖 AI-Powered Classification**: Choose between rule-based or OpenAI GPT-3.5 classification
- **🔑 Personal API Keys**: Users enter their own OpenAI API key (credits not shared)
- **📊 Results Summary**: View classification statistics with method used
- **📥 File Download**: Get processed Excel file with gender codes
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd julia-test
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   _Note: This includes OpenAI package for AI-powered classification_

3. **Run the application:**

   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:8080
   ```

## 📖 Usage Guide

### Step 1: Upload Excel File

- Drag and drop your Excel file or click to browse
- Supported formats: `.xlsx`, `.xls`
- Maximum file size: 16MB

### Step 2: Select Name Column

- Choose from available columns in the dropdown
- OR type the column name manually
- Preview the selected column data

### Step 3: Choose Classification Method

- **Rule-Based (Free)**: Uses built-in name database and linguistic patterns
- **AI-Powered (Premium)**: Uses OpenAI GPT-3.5 for higher accuracy
  - Enter your OpenAI API key (get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys))
  - Cost: ~$0.001-0.002 per name (very affordable)
- Click "Classify Names" and wait for processing

### Step 4: Download Results

- Review classification statistics
- Download the processed Excel file
- Start over with a new file if needed

## 🎯 Classification Methods

Choose between two classification approaches:

### 🤖 AI-Powered Classification (Recommended)

- **Technology**: OpenAI GPT-4o Mini
- **Accuracy**: Higher accuracy, especially for:
  - Uncommon or unique names
  - International/non-English names
  - Names with cultural variations
  - Modern or trendy names
- **Cost**: ~$0.001-0.002 per name (your own API credits)
- **Speed**: Slightly slower due to API calls
- **Requirements**: Valid OpenAI API key

### 📚 Rule-Based Classification (Free)

- **Technology**: Built-in name database + linguistic patterns
- **Accuracy**: Good for common English names
- **Cost**: Completely free
- **Speed**: Very fast (offline processing)
- **Database**: 500+ names across multiple cultures

Both methods use the following output codes:

- **1 = Male**: Names identified as male with high confidence
- **2 = Female**: Names identified as female with high confidence
- **? = Uncertain**: Names that are ambiguous, unknown, or empty

### 🔑 How to Get an OpenAI API Key

1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create a free OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add credit to your account (usually $5-10 is plenty)

### Classification Features:

- ✅ Comprehensive name database (English, Spanish, Arabic, French, Italian, Indian, Chinese)
- ✅ Title removal (Dr., Mrs., Ms., etc.)
- ✅ Pattern-based classification (name endings, linguistic rules)
- ✅ AI-powered analysis for complex cases
- ✅ Handles empty/invalid entries gracefully
- ✅ Batch processing for efficiency

## 🗂️ Project Structure

```
julia-test/
├── app.py                 # Flask backend server
├── gender_classifier.py   # AI gender classification logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend JavaScript
├── uploads/              # Temporary file storage (auto-created)
└── outputs/              # Processed files (auto-created)
```

## 🔧 API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload file and get column information
- `POST /process` - Process names and generate output file
- `GET /download/<filename>` - Download processed file

## 🎨 Customization

### Adding New Names

Edit `gender_classifier.py` and add names to the appropriate sets:

- `MALE_NAMES` - for male names
- `FEMALE_NAMES` - for female names
- `AMBIGUOUS_NAMES` - for gender-neutral names

### Modifying Classification Rules

Update the `classify_gender()` function in `gender_classifier.py` to add new classification logic.

### Styling Changes

Modify `static/css/style.css` to customize the appearance.

## 🚀 Production Deployment

For production use:

1. **Set Flask to production mode:**

   ```python
   app.run(debug=False, host='0.0.0.0', port=8080)
   ```

2. **Use a production WSGI server:**

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

3. **Configure file size limits and security as needed**

## 📝 Notes

- Files are temporarily stored during processing and should be cleaned up periodically
- The tool is designed for internal use with trusted Excel files
- Classification accuracy depends on the name database and may vary for uncommon names
- Large files may take longer to process

## 🤝 Support

For issues or questions about this internal tool, please contact the development team.

---

**Gender Classification Codes:**

- 1 = Male 👨
- 2 = Female 👩
- ? = Uncertain ❓
