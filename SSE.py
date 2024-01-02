import os
import hashlib
import string

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sqlite3
import time
import random

from Crypto.Util.Padding import pad, unpad

output_directory = 'Jotain'

# Ensure the output directory exists or create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Generate and save 25 text files with random content and varying sizes
for i in range(0, 4):
    # Define the file name
    file_name = os.path.join(output_directory, f"file_{i}.txt")

    # Generate random text content with a random length (between 1 and 1000 characters)
    # random_text = ' '.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1, 100)))
    random_text = "apina mies karhu kahvi keppi hattu maila stick motor"
    # Save the content to the file
    with open(file_name, 'w') as file_enc:
        file_enc.write(random_text)

    print(f"Created {file_name} with {len(random_text)} characters.")

kske = get_random_bytes(16)

# Function to compute the SHA-256 hash of a word
def compute_sha256_hash(word):
    sha256 = hashlib.sha256()
    sha256.update(word.encode('utf-8'))
    return sha256.hexdigest()


# Function to encrypt data with AES
def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return ciphertext, cipher.iv  # Return both ciphertext and IV


def decrypt_aes(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad(decrypted_data, AES.block_size).decode('utf-8')


# Specify the folder where .txt files are located
folder_path = 'Jotain'

# Generate an AES key for file encryption (KSKE)
# 128-bit key
iv = 0
execution_times = []
total_combined_size = 0
# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
deletedFile = [];

table_names = ['sse_csp_keywords', 'sse_keywords']

# Clean each table
for table_name in table_names:
    cursor.execute(f"DELETE FROM {table_name}")
    cursor.execute(
        f"UPDATE sqlite_sequence SET seq=1 WHERE name='{table_name}'")
    print(f"All data in {table_name} has been deleted.")

# Commit the changes
conn.commit()

num_files = 0
sse_keyword_numfiles = 0
num_search = 0
sse_keyword_numsearch = 0
# For each .txt file in the folder
for filename in os.listdir(folder_path):

    if filename.endswith('.txt'):

        file_path = os.path.join(folder_path, filename)
        file_size = os.path.getsize(file_path)
        total_combined_size += file_size

        start_time = time.time()
        file_name = os.path.join(output_directory,
                                 f"file_{num_files}_encrypted.bin")

        with open(file_path, 'r') as infile:
            file_content = infile.read()

        # Encrypt the file using KSKE
        encrypted_data, iv = encrypt_aes(file_content, kske)

        with open(file_name, 'wb') as outfile:
            outfile.write(iv)
            outfile.write(encrypted_data)

        # Initialize counters

        # Split the file content into words
        words = file_content.split()

        for word in words:
            # Compute SHA-256 hash of the word as the keyword
            keyword = compute_sha256_hash(word)

            # Initialize counters for the keyword

            # Compute keyword key (Kw)
            keyword_key = hashlib.sha256(
                (keyword + str(num_search)).encode('utf-8')).hexdigest()

            # Compute csp_keywords_address
            csp_keywords_address = hashlib.sha256(
                (keyword_key + str(num_files)).encode('utf-8')).hexdigest()

            # Encrypt filename and num_files with KSKE as csp_keyvalue
            csp_keyvalue, iv = encrypt_aes(filename + str(num_files), kske)

            # Insert values into the tables
            cursor.execute(
                "INSERT INTO sse_csp_keywords (csp_keywords_address, csp_keyvalue) VALUES (?, ?)",
                (csp_keywords_address, csp_keyvalue + iv))

            cursor.execute(
                "INSERT INTO sse_keywords (sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch) VALUES (NULL, ?, ?, ?)",
                (keyword, sse_keyword_numfiles, sse_keyword_numsearch))

        sse_keyword_numfiles = sse_keyword_numfiles + 1
        num_files += 1

        # Commit the changes to the database
        conn.commit()

        # Delete the original .txt file
        deletedFile.append(filename);
        os.remove(file_path)

        cursor.execute("SELECT * FROM sse_csp_keywords;")
        csp_keywords_data = cursor.fetchall()

        # Display the content of 'sse_keywords' table
        cursor.execute("SELECT * FROM sse_keywords;")
        sse_keywords_data = cursor.fetchall()

        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append((filename, execution_time))

# Close the database connection

print("Contents of sse_csp_keywords:")
for row in csp_keywords_data:
    print(row)

print("\nContents of sse_keywords:")
for row in sse_keywords_data:
    print(row)

print(deletedFile)
total_time = 0
for filename, execution_time in execution_times:
    print(f"Time taken to process {filename}: {execution_time:.2f} seconds")
    total_time += execution_time

# Print the total combined size of test files
print(
    f"Total combined size of test files: {total_combined_size / (1024 * 1024):.2f} MB\n Total time: {total_time:.2f} seconds")
while (True):
    execution_times_2 = []
    search_word = input("Enter the word you wish to search for: ")
    start_time = time.time()
    if (search_word == 'exit'):
        break
    search_hash = compute_sha256_hash(search_word)

    cursor.execute(
        "SELECT sse_keyword_numfiles, sse_keyword_numsearch FROM sse_keywords WHERE sse_keyword = ?",
        (search_hash,))
    result_1 = cursor.fetchall()

    for result in result_1:
        sse_keyword_numfiles, sse_keyword_numsearch = result
        print(
            f"sse_keyword_numfiles: {sse_keyword_numfiles}, sse_keyword_numsearch: {sse_keyword_numsearch}")

        search_keyword_key = hashlib.sha256(
            (search_hash + str(sse_keyword_numsearch)).encode(
                'utf-8')).hexdigest()
        sse_keyword_numsearch += 1
        csp_keywords_address = hashlib.sha256(
            (search_keyword_key + str(sse_keyword_numfiles)).encode(
                'utf-8')).hexdigest()

        cursor.execute(
            "UPDATE sse_keywords SET sse_keyword_numsearch = ? WHERE sse_keyword = ?",
            (sse_keyword_numsearch, search_hash))
        conn.commit()

        cursor.execute(
            "SELECT csp_keyvalue FROM sse_csp_keywords WHERE csp_keywords_address = ?",
            (csp_keywords_address,))
        result_2 = cursor.fetchone()

        new_search_keyword_key = hashlib.sha256(
            (search_hash + str(sse_keyword_numsearch)).encode(
                'utf-8')).hexdigest()

        new_csp_keywords_address = hashlib.sha256(
            (new_search_keyword_key + str(sse_keyword_numfiles)).encode(
                'utf-8')).hexdigest()
        cursor.execute(
            "UPDATE sse_csp_keywords SET csp_keywords_address = ? WHERE csp_keywords_address = ?",
            (new_csp_keywords_address, csp_keywords_address))

        conn.commit()
        if result_2:
            csp_keyvalue = result_2[0]
            iv = csp_keyvalue[16:]
            # Extract the ciphertext (remaining bytes)
            ciphertext = csp_keyvalue[:16]

            # Decrypt the ciphertext using KSKE and IV to get filename and
            # num_files
            decrypted_value = decrypt_aes(ciphertext, kske, iv)
            filename, num_files = decrypted_value[
                                  :len(filename)], decrypted_value[
                                                   len(filename):]
            print(filename.split(".")[0] + "_encrypted.bin")
            file_path = os.path.join(folder_path,
                                     filename.split(".")[0] + "_encrypted.bin")
            with open(file_path, 'rb') as infile:
                # Read IV (first 16 bytes)
                iv = infile.read(16)
                # Read the ciphertext
                ciphertext = infile.read()

            decrypted_data = decrypt_aes(ciphertext, kske, iv)
            print(decrypted_data)

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times_2.append((filename, execution_time))
    total_time_2 = 0
    for filename, execution_time in execution_times:
        total_time_2 += execution_time
        # Commit the changes to the database
    print(f"Total time to search: {total_time_2:.2f} seconds", )
    # Decrypt csp_keyvalue using KSKE to get filename and num_files
