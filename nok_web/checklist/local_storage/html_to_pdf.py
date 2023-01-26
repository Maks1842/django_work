import pdfkit
from weasyprint import HTML

# with open('../templates/act_checkings/act_check_ambul.html') as f:
#     pdfkit.from_file(f, 'out.pdf')

HTML('https://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf')

