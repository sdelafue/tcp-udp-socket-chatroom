import os

os.makedirs("files", exist_ok=True)

test_files = {
    "test_100KB.bin": 100 * 1024,
    "test_1MB.bin": 1024 * 1024,
    "test_5MB.bin": 5 * 1024 * 1024,
}

for filename, size in test_files.items():
    path = os.path.join("files", filename)

    with open(path, "wb") as f:
        f.write(os.urandom(size))

    print(f"Created {path} with size {size} bytes")