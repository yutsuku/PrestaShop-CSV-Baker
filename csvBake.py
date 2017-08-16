import os
import sys
import platform
import subprocess
import csv
from os.path import join

csv.register_dialect('PrestaShop', delimiter=';', quoting=csv.QUOTE_MINIMAL)
csv_multiple_delimiter = '|'
_VERSION_ = '1.0'
_TITLE_ = 'PrestaShop CSV Baker'

def makeList(entry):
	if not os.path.isdir(entry):
		raise ValueError('Invaild entry point')
	filenames = []
	for root, dirs, files in os.walk(entry):
		print('basename, root: ', os.path.basename(root), root)
		for name in files:
			if name.lower().endswith(('.jpg', '.jpeg', '.png')):
				filenames.append(os.path.join(os.path.basename(entry), os.path.basename(root), name).replace('\\', '/'))
	return filenames

def readCSVstruct(entry):
	struct_header = []
	stcurt_variables = []
	
	with open(entry, newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, 'PrestaShop')
		for row in reader:
			for cell in row:
				if reader.line_num == 1:
					struct_header.append(cell)
				elif reader.line_num == 2:
					stcurt_variables.append(cell)
				else:
					break

	if len(struct_header) != len(stcurt_variables):
		raise ValueError('Different row lengths detected, did you forget some data?')
	return struct_header, stcurt_variables

def writeCSV(entry, list_header, list_variables, filenames, max_entries):
	if len(filenames) > max_entries:
		filenames_parts = [filenames[x:x+max_entries] for x in range(0, len(filenames), max_entries)]
		
		root, ext = os.path.splitext(entry)
		print('[writeCSV] Parts: ' + str(len(filenames_parts)))
		
		for key, value in enumerate(filenames_parts):
			writeCSV(root + '_' + str(key) + ext, list_header, list_variables, value, max_entries)
			
		return
	
	_id_ = 1
	with open(entry, 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, 'PrestaShop')
		writer.writerow(list_header)
		
		for file in filenames:
			row_template = list_variables
			row_template = [w.replace('$ID', str(_id_)) for w in row_template]
			row_template = [w.replace('$zdjęcie', file) for w in row_template]
			writer.writerow(row_template)
			_id_ += 1

import tkinter
import webbrowser
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror

class Spinbox(ttk.Widget):
    def __init__(self, master, **kw):
        ttk.Widget.__init__(self, master, 'ttk::spinbox', kw)

def callback(event):
	webbrowser.open_new(event.widget.cget("text"))
	
def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
 
class Application:
	def __init__(self, root):
		self.filenames = []
		self.struct_header = []
		self.stcurt_variables = []
		self.csv_path_in = ''
		self.csv_path_out = ''
		
		self.csv_max_entries = tkinter.StringVar()
		self.csv_max_entries.set(50)
		self.root = root
		self.root.title(_TITLE_)
		ttk.Frame(self.root, width=360, height=115).pack()
		self.root.resizable(0,0)
		self.root.iconbitmap('icon.ico')
		#ttk.Label(self.root, text='Hello World').place(x=10, y=10)
		#ttk.Button(self.root, text='Pick', command=self.load_file).place(x=10, y=10)
		self.button_csv_template = ttk.Button(self.root, text='CSV Wzór', command=self.load_CSVfile).place(x=10, y=10)
		self.button_csv_output = ttk.Button(self.root, text='CSV wyjściowy', command=self.save_CSVfile).place(x=90, y=10)
		self.label_csv_maxrows = ttk.Label(self.root, text='Limit wierszy').place(x=180, y=12)
		self.input_csv_maxrows = Spinbox(self.root, from_=1, to=1000, textvariable=self.csv_max_entries).place(x=260, y=12, width=90)
		self.button_dir_source = ttk.Button(self.root, text='Obrazki', command=self.load_list).place(x=10, y=40)
		
		self.button_make = ttk.Button(self.root, text='Generuj CSV', command=self.make, width=38)
		self.button_make.place(x=10, y=80)
		self.button_make.state(['disabled'])
		
		self.button_goto = ttk.Button(self.root, text='Przejdź do plików', command=self.explore_CSVfile)
		self.button_goto.place(x=250, y=80)
		self.button_goto.state(['disabled'])
		
		self.statusbar = ttk.Frame(self.root)
		self.statusbar.pack(side='bottom', fill='x', expand=False)
		
		self.statusbar.version = ttk.Label(self.root, text='v'+str(_VERSION_), borderwidth=1, relief=tkinter.FLAT, anchor=tkinter.W)
		self.statusbar.version.pack(in_=self.statusbar, side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
		
		self.statusbar.link = ttk.Label(self.root, text='http://yutsuku.net/', borderwidth=1, relief=tkinter.FLAT, anchor=tkinter.E, foreground="blue", cursor="hand2")
		self.statusbar.link.pack(in_=self.statusbar, side=tkinter.RIGHT, expand=False)
		self.statusbar.link.bind("<Button-1>", callback)
		
		self.statusbar.author = ttk.Label(self.root, text='Wykonanie: moh @', borderwidth=1, relief=tkinter.FLAT, anchor=tkinter.E)
		self.statusbar.author.pack(in_=self.statusbar, side=tkinter.RIGHT, expand=False)
	
	def activateMakeButton(self):
		print('activateMakeButton', len(self.filenames), len(self.struct_header))
		if len(self.filenames) > 0 and len(self.struct_header) > 0 and len(self.csv_path_out):
			self.button_make.state(['!disabled'])
		else:
			self.button_make.state(['disabled']) 
		
	def save_CSVfile(self):
		file_dialog_path = filedialog.asksaveasfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*") ))
		if file_dialog_path:
			self.csv_path_out = file_dialog_path
			self.activateMakeButton()
		return
		
	def explore_CSVfile(self):
		print('[explore_CSVfile]: ' + os.path.dirname(self.csv_path_out))
		open_file(os.path.dirname(self.csv_path_out))
		
	def make(self):
		writeCSV(self.csv_path_out , self.struct_header, self.stcurt_variables, self.filenames, int(self.csv_max_entries.get()))
		
		self.filenames = []
		self.struct_header = []
		self.stcurt_variables = []
		self.activateMakeButton()
		self.button_goto.state(['!disabled'])
		
		print(self.csv_path_out, self.csv_path_in, len(self.filenames), int(self.csv_max_entries.get()))
		
	def load_list(self):
		dir_dialog_path = filedialog.askdirectory()
		if dir_dialog_path:
			try:
				# Build file list to work with
				filenames = makeList(dir_dialog_path)
				self.filenames = filenames
				print('source path OK: ' + dir_dialog_path)
				self.activateMakeButton()
			except ValueError as err:
				print(', '.join(err.args))
				showerror("Open Source Folder", ', '.join(err.args))
			return
		
	def load_CSVfile(self):
		file_dialog_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*") ))
		if file_dialog_path:
			try:
				# Read reference CSV fields
				self.csv_path_in = file_dialog_path
				struct_header, stcurt_variables = readCSVstruct(file_dialog_path)
				self.struct_header = struct_header
				self.stcurt_variables = stcurt_variables
				print('eference CSV OK: ', struct_header)
				self.activateMakeButton()
			except ValueError as err:
				print(', '.join(err.args))
				showerror("Open Source File", ', '.join(err.args))
			return

if __name__ == '__main__':
	root = tkinter.Tk()
	Application(root)
	root.mainloop()
