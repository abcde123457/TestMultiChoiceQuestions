import os
import csv
import re
import sys
sys.path.append('E:\Thử\TestMultichoiceQuestion.py')  # Thay thế bằng đường dẫn thực tế
import TestMultichoiceQuestion


def extract_question_answer(text):
  pattern = r"Câu hỏi:(.*?)Đáp án:.*"
  match = re.search(pattern, text, re.DOTALL)
  if match:
      return match.group(0)
  else:
      return "Không tìm thấy cặp câu hỏi-đáp án"



# Đường dẫn đến file input
input_file_path = 'E:\\Thử\\input.csv'
input_dir = os.path.dirname(input_file_path)

# Đọc dữ liệu từ file input
with open(input_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Xử lý dữ liệu và thêm cột "output_1"
for row in data:
    input_text = row[0]
    output_1_text = extract_question_answer(input_text)
    output_2_text = ""
    if TestMultichoiceQuestion.is_multiple_choice_question(output_1_text):
      output_2_text = "True. "
    else:
      output_2_text = "False. " + TestMultichoiceQuestion.output_message  
    row.append(output_1_text)
    row.append(output_2_text)
# Tạo tiêu đề cho các cột
fieldnames = ['input', 'output_1', 'output_2']

# Đường dẫn đến file output
output_file_path = os.path.join(input_dir, 'output.csv')

# Ghi dữ liệu vào file output với tiêu đề
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Ghi tiêu đề
    writer.writerow(fieldnames)
    # Ghi dữ liệu
    writer.writerows(data)

print(f"Output file saved to: {output_file_path}")
