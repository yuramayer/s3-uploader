# 📁 S3 File Uploader

This script uploads a **file** or a **folder** to **Yandex S3 Cloud bucket**

## ✅ Requirements

- Python 3.7+
- AWS S3 access
- `.env` file with your credentials

## 📦 Installation

1. Clone the repo or copy the files.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ `.env` File Setup

Create a .env file in the same folder as main.py, and add this:

```ini
CLOUD_S3_ID_KEY=your_s3_access_key
CLOUD_S3_SECRET_KEY=your_s3_secret_key
BUCKET_NAME=your_bucket_name
```

## 🚀 How to Use

Run the script with a path to a file or folder:

```bash
python main.py
```

It will ask you to enter a file or folder path.

- If you give a **file** – it uploads that file.

- If you give a **folder** – it uploads all files inside it recursively.

*👉 Supports relative and absolute paths!*

-----

Need help? Open an issue 😉
