import os
import base64
import subprocess

WORKSPACE = "/Users/zack/workspace/Agent学习教程"

def get_base64_image(filename):
    path = os.path.join(WORKSPACE, filename)
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(filename)[1].lower().replace('.', '')
    if ext == 'jpg': ext = 'jpeg'
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/{ext};base64,{data}"

print("Loading and encoding images to Base64...")
replacements = {
    "{{IMG_0}}": get_base64_image("0.png"),
    "{{IMG_1}}": get_base64_image("1.jpeg"),
    "{{IMG_2}}": get_base64_image("2.jpeg"),
    "{{IMG_3}}": get_base64_image("3.jpeg"),
    "{{IMG_4}}": get_base64_image("4.jpeg"),
    "{{IMG_5}}": get_base64_image("5.jpeg"),
    "{{IMG_6}}": get_base64_image("6.jpeg"),
    "{{IMG_8}}": get_base64_image("8.jpeg"),
    "{{IMG_9}}": get_base64_image("9.jpeg"),
    "{{IMG_10}}": get_base64_image("10.jpeg"),
    "{{IMG_11}}": get_base64_image("11.jpeg")
}
print("Images encoded successfully.")

template_path = os.path.join(WORKSPACE, "manual_template.html")
with open(template_path, "r", encoding="utf-8") as f:
    content = f.read()

for placeholder, b64_str in replacements.items():
    content = content.replace(placeholder, b64_str)

output_html_path = os.path.join(WORKSPACE, "AI_Agent_全栈开发与商业落地工程实操手册.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Full HTML generated at: {output_html_path}")

output_pdf_path = os.path.join(WORKSPACE, "AI_Agent_全栈开发与商业落地工程实操手册.pdf")
print("Printing to PDF using Chrome headless...")

chrome_cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--print-to-pdf=" + output_pdf_path,
    output_html_path
]

res = subprocess.run(chrome_cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(output_pdf_path):
    size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
    print(f"SUCCESS: PDF generated successfully at: {output_pdf_path}")
    print(f"File size: {size_mb:.2f} MB")
else:
    print(f"FAILED: {res.stderr}")
