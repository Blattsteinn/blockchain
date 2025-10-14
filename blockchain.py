import hash

if __name__ == "__main__":
    user_input: int

    while True:
        word = input("Enter the word you want to hash: ")
        hash_received = hash.hash_function(word)
        print(f"Word: {word[:20]}, hash: {hash_received}")