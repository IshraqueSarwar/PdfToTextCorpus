# import ghostscript
from PyPDF2 import PdfWriter, PdfReader
import glob
from tqdm import tqdm
from pdf2image import convert_from_path
import pytesseract
import re

class Extractor:
	def __init__(self, pdfs_path = '', out_corpus = 'corpus.text', lang = 'ben'):
		self.pdfs_path = pdfs_path
		self.pdf_list = []
		self.page_tuples = []
		self.out_file = out_corpus
		self.lang = lang

		# call initializer functions
		self.collect_pdf()
		print(self.page_tuples)

	def collect_pdf(self):
		for pdf in glob.glob(f'{self.pdfs_path}/*.pdf'):
			name = pdf.replace(f'{self.pdfs_path}', '').replace('.pdf',' ').split('-')
			self.page_tuples.append((int(name[0]), int(name[1])))
			self.pdf_list.append(pdf)


	def convert(self,):
		for pdf_idx in range(len(self.pdf_list)):
			curr_pdf = PdfReader(open(self.pdf_list[pdf_idx], 'rb'))
			start_page = self.page_tuples[pdf_idx][0]
			end_page = self.page_tuples[pdf_idx][1]

			print(f"Converting {end_page- start_page} pages...")
			with open(self.out_file, 'a+') as f:
				for pg_num in tqdm(range(start_page, 4)):
					out = PdfWriter()
					out.add_page(curr_pdf.pages[pg_num])
					with open(f'Lab/temp.pdf','wb') as outStream:
						out.write(outStream)


					#convert one page pdf to jpegs and extract its text content
					p = convert_from_path('Lab/temp.pdf')
					p[0].save('Lab/temp.jpeg','JPEG')

					text = pytesseract.image_to_string('Lab/temp.jpeg', lang=self.lang).replace('\n',' ')
					text = re.sub('\s+',' ', text)
					print(text)
					# remove page numbers from the end of each page before adding to corpus
					# f.write(text)

	

E = Extractor('pdfs/')
E.convert()
