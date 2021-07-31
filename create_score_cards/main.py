import pandas as pd
import sqlite3
import os
import glob
import fitz
from fpdf import FPDF

def create_score_cards():
	cards_df = pd.read_excel('dummyData.xlsx', sheet_name="Sheet1", index_col=0)
	cards_df.columns = cards_df.columns.str.replace(' ', '')
	# print(cards_df.dtypes)
	# print(cards_df.columns)

	# db_conn = sqlite3.connect(':memory:')
	db_conn = sqlite3.connect('trial.db')

	cards_df.to_sql("cards_data", db_conn, if_exists="replace", index=None)
	c = db_conn.cursor()


	students_data_cols = """Round, FirstName, LastName, FullName,
	RegistrationNumber, Grade, NameofSchool, Gender, DateofBirth, CityofResidence, Dateandtimeoftest,
	CountryofResidence"""
	query_statement = f"SELECT {students_data_cols} FROM cards_data GROUP BY RegistrationNumber"
	query = c.execute(query_statement)

	students_data_cols = students_data_cols.replace(" ", "")
	students_data_cols = students_data_cols.replace("\n", "")
	students_data_cols = students_data_cols.replace("\t", "")
	students_data_cols = students_data_cols.split(",")
	# print(students_data_cols)

	pics_dir = "pics/"
	students_info_list = []
	for row in query:
		temp = dict(zip(students_data_cols, row))
		# print(temp)
		temp["pic_path"] = pics_dir + temp["FullName"] + ".jpg"
		# print(temp)
		students_info_list.append(temp)


	dir_name = "students_pdfs"
	if not os.path.exists(dir_name):
	    os.makedirs(dir_name)
	    print("Directory " , dir_name ,  " Created ")
	else:    
	    print("Directory " , dir_name ,  " already exists")
	    files = glob.glob(dir_name + "/*")
	    for file in files:
	    	os.remove(file)


	students_marks_cols = """"QuestionNo." , Whatyoumarked, CorrectAnswer, 
	"Outcome(Correct/Incorrect/NotAttempted)", Scoreifcorrect, Yourscore"""


	for student_dict in students_info_list:
		# print(student_dict["RegistrationNumber"])
		file_path = dir_name + "/" + str(student_dict["RegistrationNumber"])
		pdf = FPDF()
		pdf.add_page() 
		pdf.set_font("Arial", size = 10) 

		for key in student_dict:
			x = f"{key}: {student_dict[key]}"
			if key=="pic_path":
				pic_path = str(student_dict[key]).replace(" ", "")
				# print(pic_path)
				pdf.image("pics/school_logo.jpg", x=170, y=10, w =25, h=25)
				pdf.image(pic_path, x=150, y=50, w=50, h=50)
				continue
			pdf.cell(100, 10, txt = x, ln = 2, align = 'L') 

		regist_n = student_dict["RegistrationNumber"]
		query_statement = f"SELECT {students_marks_cols} FROM cards_data WHERE RegistrationNumber={regist_n}"
		df = pd.read_sql(query_statement, db_conn)


		pdf.set_font("Arial", size = 10) 
		col_str = '   '.join([str(item) for item in df.columns.values])
		pdf.multi_cell(w=0, h=6, txt=col_str, align="C", border=1)
		

		# print(df.values.tolist())
		# pdf.set_margins(left=25, top=25, right=25)

		for ls in df.values:
			tbl_str = '                              '.join([str(item) for item in ls])
			pdf.multi_cell(w=0, h=5, txt=tbl_str, align="C", border=1)

		pdf.output(file_path,'F')	
		

	db_conn.close()


if __name__ == "__main__":
   create_score_cards()
