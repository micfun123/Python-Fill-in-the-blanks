from flask import Flask, request, render_template, session, redirect, url_for
import re
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # For session handling

# Function to remove comments and replace random words with blanks
def remove_comments_and_random_words(code, amount=10):
    # Remove single-line and multi-line comments
    code_no_comments = re.sub(r"(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")", "", code, flags=re.DOTALL)
    code_no_comments = re.sub(r"#.*", "", code_no_comments)

    # Extract words
    words = re.findall(r"\b\w+\b", code_no_comments)
    if len(words) < amount:
        raise ValueError("The code has fewer than 10 words that can be replaced.")

    # Select random words to replace
    random_words = random.sample(words, amount)
    processed_code = code_no_comments

    # Replace each word with a placeholder (e.g., ____)
    for word in random_words:
        processed_code = re.sub(rf"\b{re.escape(word)}\b", "____", processed_code, count=1)

    return processed_code, random_words

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No file selected.", 400

        try:
            # Read the file and process it
            code = uploaded_file.read().decode("utf-8")
            processed_code, original_words = remove_comments_and_random_words(code)

            # Store processed code and original words in session
            session["processed_code"] = processed_code
            session["original_words"] = original_words

            return redirect(url_for("quiz"))

        except Exception as e:
            return str(e), 500

    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    processed_code = session.get("processed_code")
    original_words = session.get("original_words")

    if not processed_code or not original_words:
        return redirect(url_for("index"))

    # If user submits answers
    if request.method == "POST":
        user_answers = request.form.getlist("answer")
        correct_count = 0

        # Compare user answers with original words
        for user_answer, correct_answer in zip(user_answers, original_words):
            if user_answer.strip().lower() == correct_answer.lower():
                correct_count += 1

        score = f"You got {correct_count}/{len(original_words)} correct!"
        return render_template("result.html", score=score)

    # Split code into lines for display
    code_lines = processed_code.split("\n")
    blanks_count = processed_code.count("____")

    return render_template("quiz.html", code_lines=code_lines, blanks_count=blanks_count)

@app.route("/result")
def result():
    score = session.pop("score", None)
    if not score:
        return redirect(url_for("index"))

    return render_template("result.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)
