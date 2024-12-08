from flask import Flask, request, render_template, Response
import re
import random
import io

app = Flask(__name__)

def remove_comments_and_random_words(input_file, amount=10):
    try:
        # Read the file content
        code = input_file.read().decode("utf-8")

        # Remove single-line comments (`#`) and multi-line comments (`'''` or `"""`)
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

        return code_no_comments

    except ValueError as ve:
        raise ValueError(str(ve))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No file selected.", 400

        try:
            # Process the file content in memory
            processed_code = remove_comments_and_random_words(uploaded_file.stream)

            # Create a response with the processed content, setting it as an attachment
            response = Response(processed_code, mimetype="text/plain", content_type="text")
            response.headers["Content-Disposition"] = "attachment; filename=processed_code.py"
            return response

        except Exception as e:
            return str(e), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
