from distutils.command.config import config
import pdfkit

path_wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

pdfkit.from_url('https://stackoverflow.com/questions/42420570/pdfkit-oserror-no-wkhtmltopdf-executable-found',r'\Exports\test1.pdf',configuration=config)