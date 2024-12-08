from flask import Flask, request, render_template, send_file
import re
import random
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def remove_comments_and_random_words(input_file, output_file, amount=10):
    try:
        with open(input_file, "r") as file:
            code = file.read()

        # Remove single-line comments (`#`) and multi-line comments (`'''` or `"""`)
        # Handle multi-line comments
        code_no_comments = re.sub(
            r'(\'\'\'(.*?)\'\'\'|"""(.*?)""")', "", code, flags=re.DOTALL
        )
        # Handle single-line comments
        code_no_comments = re.sub(r"#.*", "", code_no_comments)

        # Extract words from the code
        words = re.findall(r"\b\w+\b", code_no_comments)

        # Ensure there are enough words to replace
        if len(words) < amount:
            raise ValueError("The code has fewer than 10 words that can be replaced.")

        # Randomly replace words
        random_words = random.sample(words, amount)
        for word in random_words:
            code_no_comments = re.sub(
                rf"\b{re.escape(word)}\b", "_", code_no_comments, count=1
            )

        # Write processed code to the output file
        with open(output_file, "w") as file:
            file.write(code_no_comments)

    except FileNotFoundError:
        raise FileNotFoundError("The specified input file does not exist.")
    except ValueError as ve:
        raise ValueError(str(ve))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No file selected.", 400

        # Save the uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_path)

        # Define the output path
        output_path = os.path.join(
            PROCESSED_FOLDER, f"processed_{uploaded_file.filename}"
        )

        try:
            # Process the file
            remove_comments_and_random_words(input_path, output_path)
            #remove the input file
            os.remove(input_path)
            return send_file(output_path, as_attachment=True)

        except Exception as e:
            return str(e), 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
