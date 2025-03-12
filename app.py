from flask import Flask, request, render_template, session, redirect, url_for
import re
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # For session handling

# Function to remove comments and replace random words with blanks
def remove_comments_and_random_words(input_file, amount=10):
    try:
        # Read the file content
        code = input_file.read().decode("utf-8")

        # Remove single-line comments (`#`) and multi-line comments (`'''` or `"""`)
        code_no_comments = re.sub(
            r"(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")", "", code, flags=re.DOTALL
        )
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
                rf"\b{re.escape(word)}\b", "____", code_no_comments, count=1
            )

        return code_no_comments, random_words

    except ValueError as ve:
        raise ValueError(str(ve))




@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Clear the session to avoid old data conflicts
        session.clear()

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No file selected.", 400

        try:
            processed_code, original_words = remove_comments_and_random_words(uploaded_file.stream)

            # Store data in session for use in quiz
            session["processed_code"] = processed_code
            session["original_words"] = original_words

            return redirect(url_for("quiz"))

        except Exception as e:
            return str(e), 500

    return render_template("index.html")


    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    processed_code = session.get("processed_code")
    original_words = session.get("original_words")

    if not processed_code or not original_words:
        return redirect(url_for("index"))

    if request.method == "POST":
        user_answers = request.form.getlist("answer")
        correct_count = 0

        # Compare user answers with original words (strip whitespace + ignore case)
        for user_answer, correct_answer in zip(user_answers, original_words):
            if user_answer.strip().lower() == correct_answer.strip().lower():
                correct_count += 1

        # Store the score in session so it can be accessed on the result page
        session["score"] = f"You got {correct_count}/{len(original_words)} correct!"

        return redirect(url_for("result"))

    code_lines = processed_code.split("\n")

    return render_template("quiz.html", code_lines=code_lines)


@app.route("/result")
def result():
    score = session.get("score")
    if not score:
        return redirect(url_for("index"))

    return render_template("result.html", score=score)

if __name__ == "__main__":
    app.run(debug=True, port=5501)
