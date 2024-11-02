import re
def is_special_case(count_1, count_2, count_3, count_4):
 
  special_cases = [(2, 1, 1, 1), (1, 2, 1, 1), (1, 1, 2, 1), (1, 1, 1, 2)]
  return (count_1, count_2, count_3, count_4) in special_cases

def is_multiple_choice_question(text):
  
  pattern = r"^(Câu hỏi:)(.*)$|^[A-D][\.\)]?\s+(.*)$|^(Đáp án:)(.*)$"
  lines = text.splitlines()
  
  if not lines[0].startswith("Câu hỏi:"):
   return False
  
  #Kiểm tra dòng đầu tiên có ok không
  first_line = lines[0]  # Lấy dòng đầu tiên

  index = first_line.find("Câu hỏi:")
  if index != -1:  # Tìm thấy "Câu hỏi:"
    remaining_text = first_line[index + len("Câu hỏi:"):].strip()
   #print(remaining_text)
    if len(remaining_text) == 0: 
     return False
  else:
    return False  # Không tìm thấy "Câu hỏi:"

  for i in range(1, len(lines) - 1):
    if not re.match(pattern, lines[i]):
      return False

  if not lines[-1].startswith("Đáp án:"):
    return False
  
  #check số lượng ABCD dưới đây là những từ cần đếm khớp viết hoa
  
  pattern = r"A\."
  matches = re.findall(pattern, text)
  count_A_dot = len(matches)

  pattern = r"A\)"
  matches = re.findall(pattern, text)
  count_A_parenthesis = len(matches)

  count_1 = count_A_dot + count_A_parenthesis
  #print(count_1)

  pattern = r"B\."
  matches = re.findall(pattern, text)
  count_B_dot = len(matches)

  pattern = r"B\)"
  matches = re.findall(pattern, text)
  count_B_parenthesis = len(matches)

  count_2 = count_B_dot + count_B_parenthesis
  #print(count_2)

  pattern = r"C\."
  matches = re.findall(pattern, text)
  count_C_dot = len(matches)

  pattern = r"C\)"
  matches = re.findall(pattern, text)
  count_C_parenthesis = len(matches)

  count_3 = count_C_dot + count_C_parenthesis
  #print(count_3)

  pattern = r"D\."
  matches = re.findall(pattern, text)
  count_D_dot = len(matches)

  pattern = r"D\)"
  matches = re.findall(pattern, text)
  count_D_parenthesis = len(matches)

  count_4 = count_D_dot + count_D_parenthesis
  #print(count_4)

  if not is_special_case(count_1, count_2, count_3, count_4):
    return False
  
  # Đáp án bị lặp lại
  options = []
  unique_options = []
 
  for line in lines[1:-1]:
    match = re.match(r"^[A-D][\.\)]?\s+(.*)$", line)
    if not match:
      return False
    option = match.group(1).strip()[0:]
    if option in options:
      return False  # Đáp án bị lặp lại
    options.append(option) 
  for item in options:
    # Chỉ thêm phần tử vào unique_array nếu nó chưa có trong unique_array
    if item not in unique_options:
        unique_options.append(item)
  #print(options)
  #print(unique_options)      
  if unique_options != options:
    return False   
  
  #Kiểm tra xem có đáp án null hay không
  for item in options:
    if item is None or item == "":
        return False

  # Đáp án không nằm trong các tùy chọn hay không
  answer = lines[-1].split(":")[1].strip()
  #print(answer)
  lines = text.splitlines()
  full_answer = lines[1:-1]
  #print(full_answer)
  if answer not in full_answer:
    return False  

  
  pattern1 = r"^[A-D]\b"
  # Mảng lưu chữ cái đầu
  abcd = []
  abcd_true = ['A','B','C','D']
  # Duyệt qua từng dòng và kiểm tra xem có khớp với mẫu không
  for line in lines:
    match = re.match(pattern1, line)
    if match:
        # Nếu tìm thấy, thêm ký tự đầu vào mảng
        abcd.append(match.group(0))       
  #print(abcd)
  if abcd != abcd_true:
    return False      


  return True
 

text = """Câu hỏi: Con vật nào dưới đây biết bay?
A. Chim sẻ
B. Đại bàng
C. Dơi
D. Cả 3 đáp án A B C đều đúng
Đáp án: D. Cả 3 đáp án A B C đều đúng
"""

if is_multiple_choice_question(text):
  print("TRUE")
else:
  print("FALSE")
