import re



def is_special_case(count_1, count_2, count_3, count_4):
 
  special_cases = [(2, 1, 1, 1), (1, 2, 1, 1), (1, 1, 2, 1), (1, 1, 1, 2), (1, 1, 1, 1)]
  return (count_1, count_2, count_3, count_4) in special_cases

output_message=""

def is_multiple_choice_question(text):
  
  global output_message

  try: 
    if text is None or text =="":
      "text bị rỗng"
      return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra rỗng {e}"  
    return False
  
  
  pattern = r"^(Câu hỏi:)(.*s)$|^[A-D][\.\)]?\s?(.*)$|^(Đáp án:)(.*)$" #BT Chính quy
  lines = text.splitlines()
   
   
  try:
    if not lines[-1].startswith("Đáp án:"):
     output_message="Không phát hiện thấy cụm từ 'Đáp án' "
     return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra Bắt đầu bằng Đáp án {e}"  
    return False

  try:
    if (len(lines)) < 6:
     output_message="Không đủ số dòng tối thiểu"
     return False 
  
    if not lines[0].startswith("Câu hỏi:"):
     output_message="Không tìm thấy cụm từ 'Câu hỏi:' "
     return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra số dòng hay Cụm 'Câu hỏi:'  {e}"  
    return False


  try:
    #Kiểm tra dòng đầu tiên có ok không
    first_line = lines[0]  # Lấy dòng đầu tiên

    index = first_line.find("Câu hỏi:")
    if index != -1:  # Tìm thấy "Câu hỏi:"
      remaining_text = first_line[index + len("Câu hỏi:"):].strip()
     #print(remaining_text)
      if len(remaining_text) == 0: 
       output_message="Không có nội dung câu hỏi"
       return False
    else:
      output_message="Không tìm thấy cụm từ 'Câu hỏi:' "
      return False  # Không tìm thấy "Câu hỏi:"
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra dòng đầu tiên {e}"  
    return False
  

  try:
   for line in lines[-5:-1]:
    #print(line)
    if not re.match(pattern, line):
      output_message="Định dạng của tùy chọn không phù hợp"
      return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra định dạng tùy chọn {e}"  
    return False
  
  


  #check số lượng ABCD dưới đây là những từ cần đếm khớp viết hoa
  
  pattern = r"A\."
  matches = re.findall(pattern, text)
  count_A_dot = len(matches)

  pattern = r"A\)"
  matches = re.findall(pattern, text)
  count_A_parenthesis = len(matches)

  count_1 = count_A_dot + count_A_parenthesis
  

  pattern = r"B\."
  matches = re.findall(pattern, text)
  count_B_dot = len(matches)

  pattern = r"B\)"
  matches = re.findall(pattern, text)
  count_B_parenthesis = len(matches)

  count_2 = count_B_dot + count_B_parenthesis
  

  pattern = r"C\."
  matches = re.findall(pattern, text)
  count_C_dot = len(matches)

  pattern = r"C\)"
  matches = re.findall(pattern, text)
  count_C_parenthesis = len(matches)

  count_3 = count_C_dot + count_C_parenthesis
  

  pattern = r"D\."
  matches = re.findall(pattern, text)
  count_D_dot = len(matches)

  pattern = r"D\)"
  matches = re.findall(pattern, text)
  count_D_parenthesis = len(matches)

  count_4 = count_D_dot + count_D_parenthesis
  
  '''
  print(count_1)
  print(count_2)
  print(count_3)
  print(count_4)
  '''
  
  
  
  
  try:
   if not is_special_case(count_1, count_2, count_3, count_4):
    output_message="Bị thừa hoặc thiếu các tùy chọn"
    return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra số lượng các tùy chọn {e}"  
    return False


  #Chia ra hai mảng này để so sánh, nếu khác nhau thì có 2 tùy chọn lặp nhau về ND
  options = []
  unique_options = []
 


  # Tùy chọn bị lặp lại hay không
  try:
   for line in lines[-5:-1]:
    match = re.match(r"^[A-D][\.\)]?\s?(.*)$", line)
    if not match:
      output_message="Tùy chọn không đúng định dạng"
      return False
    option = match.group(1).strip()[0:]
    if option in options:
      output_message="Tùy chọn bị lặp lại"
      return False  
    options.append(option) 
   for item in options:
    # Chỉ thêm phần tử vào unique_array nếu nó chưa có trong unique_array
    if item not in unique_options:
        unique_options.append(item)
   #print(options)
   #print(unique_options)      
   if unique_options != options:
    output_message="Tùy chọn bị lặp nhau"
    return False   
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra sự lặp hay cấu trúc của tùy chọn {e}"  
    return False

  

  #Kiểm tra xem có tùy chọn null hay không
  try:
   for item in options:
    if item is None or item == "":
        output_message="Tùy chọn bị rỗng"
        return False
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra tùy chọn rỗng {e}"  
    return False



  # Đáp án nằm trong các tùy chọn hay không
  try:
   answer = lines[-1].split(":")[1].strip()
   #print(answer)
   lines = text.splitlines()
   full_answer = lines[-5:-1]
   full_answer1 = [phan_tu.strip() for phan_tu in full_answer] #bỏ space
   #print(full_answer1)
   if answer not in full_answer1 and answer not in options:
     output_message="Đáp án không giống với bất cứ tùy chọn nào"
     return False  
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra đáp án có nằm trong các tùy chọn hay không {e}"  
    return False
  
  try:
  #Kiểm tra xem đáp án có đúng thứ tự abcd hay không
   pattern1 = r"^[A-D]\b"
   abcd = []
   abcd_true = ['A','B','C','D']
   for line in lines:
     match = re.match(pattern1, line)
     if match:
        # Nếu tìm thấy, thêm ký tự đầu vào mảng
         abcd.append(match.group(0))       
   #print(abcd)
   if abcd != abcd_true:
     output_message="Thứ tự ABCD không chính xác"
     return False  
  except Exception as e:
    output_message="Đã xảy ra lỗi kiểm tra thứ tự ABCD {e}"  
    return False



  return True
 

text = """Câu hỏi: Con vật nào dưới đây biết bay?
A) a[10]       
B) a.append(10)     
C) a[:10]        
D) Cả 3 đáp án A B C đều đúng     
Đáp án: D) Cả 3 đáp án A B C đều đúng         
"""

result = "False"


if is_multiple_choice_question(text):
  result = "True"

print(result)
print(output_message)
