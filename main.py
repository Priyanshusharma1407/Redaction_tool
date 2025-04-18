from redactor import redact_all

if __name__ == "__main__":
    with open("sample_inputs/sample.txt", "r") as file:
        data = file.read()
        redacted = redact_all(data)
        print("\nRedacted Output:\n")
        print(redacted)
