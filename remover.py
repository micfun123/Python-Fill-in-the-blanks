import re
import random

def remove_comments_and_random_words(input_file, output_file,amount = 10):
    try:
        with open(input_file, 'r') as file:
            code = file.read()

        # Remove single-line comments (`#`) and multi-line comments (`'''` or `"""`)
        # Handle multi-line comments
        code_no_comments = re.sub(r'(\'\'\'(.*?)\'\'\'|"""(.*?)""")', '', code, flags=re.DOTALL)
        # Handle single-line comments
        code_no_comments = re.sub(r'#.*', '', code_no_comments)

        # Extract words from the code
        words = re.findall(r'\b\w+\b', code_no_comments)

        # Ensure there are at least 10 words
        if len(words) < amount:
            raise ValueError("The code has fewer than 10 words that can be replaced.")

        
        random_words = random.sample(words, 10)
        for word in random_words:
            code_no_comments = re.sub(rf'\b{re.escape(word)}\b', '_', code_no_comments, count=1)

      
        with open(output_file, 'w') as file:
            file.write(code_no_comments)

        print(f"Processed code written to {output_file}")

    except FileNotFoundError:
        print("The specified input file does not exist.")
    except ValueError as ve:
        print(ve)


if __name__ == "__main__":
    input_file = "in.py" 
    output_file = "out.py"
    remove_comments_and_random_words(input_file, output_file)
