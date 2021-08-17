from docx import Document


import time

timenow = time.time()
document = Document()
time.sleep(2)
print(timenow)
print('_______OK__________')
time.sleep(2)

document.save(f'/mnt/c/Users/CeburVO/appraise/dags/{timenow}.docx')
time.sleep(2)