import PyPDF2 as p2 


PDFfile = open("c:\Users\JO~Intaneznol\workspace\job\job\tempCodeRunnerFile.py"\conceptpapdfper.","rb")
pdfreader = p2.PdfFileReader(PDFfile)

x = pdfread.getPage(0)
print(x.extractText())
