def generate_expected_responses(console_output):
    for line in console_output.splitlines():
        print(f'assert response.contains(\'{line.strip()}\')')


if __name__ == '__main__':
    console_output = """ """
    generate_expected_responses(console_output)