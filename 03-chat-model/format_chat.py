import re
from datetime import datetime

def parse_line(line):
    """Extracts date, sender, and message from a line"""
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?(?:am|pm)?) - (.*?): (.*)$'
    match = re.match(pattern, line)
    if match:
        date_str, time_str, sender, message = match.groups()
        try:
            dt = datetime.strptime(f"{date_str} {time_str.lower()}", "%d/%m/%y %I:%M %p")
            return dt, sender, message
        except ValueError:
            return None, None, None
    return None, None, None

def filter_chat(input_file, output_file, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%d/%m/%y").date()
    end_date = datetime.strptime(end_date_str, "%d/%m/%y").date()

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            dt, sender, message = parse_line(line)
            if dt and start_date <= dt.date() <= end_date:
                    if message.lower() != "this message was deleted":
                        outfile.write(f"{sender}: {message}\n")

# ✅ Example usage
filter_chat(
    input_file="dost.txt",
    output_file="filtered_chat.txt",
    start_date_str="29/06/18",
    end_date_str="01/07/18"
)
