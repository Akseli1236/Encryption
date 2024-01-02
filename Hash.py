import hashlib


def compute_sha256_hash(filename):
    # Initialize SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Read and update hash string value in blocks of 4K
    with open(filename, "rb") as file:
        while True:
            data = file.read(4096)  # Read 4K at a time
            if not data:
                break
            sha256_hash.update(data)

    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

def verify_integrity(filename, expected_hash):
    # Compute the hash of the file
    computed_hash = compute_sha256_hash(filename)

    # Verify if the computed hash matches the expected hash
    if computed_hash == expected_hash:
        print("File integrity verified. The hashes match.\n")
    else:
        print("File integrity verification failed. The hashes do not match.\n")

if __name__ == "__main__":
    # Generate the sample text file

    # Compute the SHA-256 hash of the file
    computed_hash = compute_sha256_hash("text.txt")
    f = open("text.txt", "r")
    text = f.read()
    print("Input text: \n", text, "\n")
    print("SHA-256 Hash:", computed_hash)

    # Verify the integrity of the file using the computed hash
    verify_integrity("text.txt", computed_hash)
    text = text.replace("M", "A", 1)
    with open("text.txt", 'w') as file:
        file.write(text)
    new_hash = compute_sha256_hash("text.txt")
    print(text, "\n")
    print("SHA-256 Hash:", new_hash)
    verify_integrity("text.txt", computed_hash)


