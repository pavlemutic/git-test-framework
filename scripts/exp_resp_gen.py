def generate_response_contains(text):
    for line in text.splitlines():
        print(f'assert response.contains(\'{line.strip()}\')')

def generate_response_has(text):
    for index, line in enumerate(text.splitlines()):
        print(f"assert response.has(on_line={index + 1}, text='{line.strip()}')")


if __name__ == '__main__':
    console_output = """ """
    # generate_response_contains(console_output)
    generate_response_has(console_output)
