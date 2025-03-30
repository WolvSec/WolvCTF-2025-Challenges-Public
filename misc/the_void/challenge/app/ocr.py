from PIL import Image
import pytesseract
import sqlite3


def ocr_db(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path), config='--psm 4')
        cleaned = text.strip().replace("\n", "").replace("\"", "'").replace("‘", "'").replace("’", "'").lower()
        # Cleaning up weird OCR things
        con = sqlite3.connect('file:void.db?mode=ro', uri=True)
        cur = con.cursor()
        res = cur.execute("SELECT image, count FROM snacks WHERE name = '" + cleaned + "'")
        return(str(res.fetchall()))
    except sqlite3.Error as e:
        # Print the error message
        return(f"SQLite error occurred: {e}")
    except Exception as e:
        # Handle any other general errors
        return(f"An unexpected error occurred: {e}")
