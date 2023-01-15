import argparse
import datetime

import pandas as pd
import PyPDF2 as pdf2

def get_current_date():
  now = datetime.datetime.now()
  return f"{now.year}-{now.month}-{now.day}"

def check_column(query):
  return float(query.replace(',', ''))

def main(file_path, output_path=f'./outputs/output_{get_current_date()}.csv'):
  date_time_list = list()
  amount_list = list()
  remain_amount_list = list()
  saler_list = list()
  with open (file_path, "rb") as f:
    pdf = pdf2.PdfFileReader(f)
    pdf_num_cnt = pdf.numPages
    for cnt in range(pdf_num_cnt):
      page_one = pdf.getPage(cnt)
      text_line = page_one.extractText()
      text_line = text_line.split('\n')
      for single_line in text_line:
        if ('CNY' in single_line):
          extract_info = single_line.split(' ')
          date_time_list.append(extract_info[0])
          amount_list.append(extract_info[2])
          remain_amount_list.append(extract_info[3])
          saler_list.append(''.join(extract_info[4:]))

  raw_pd = pd.DataFrame.from_dict({
    'date_time' : date_time_list,
    'amount' : amount_list,
    'remain_amount' : remain_amount_list,
    'saler' : saler_list
  })

  raw_pd['amount'] = raw_pd['amount'].apply(check_column)
  raw_pd.to_csv(output_path)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--file_path', help='file_path')
  args = parser.parse_args()
  file_path = args.file_path
  main(args.file_path)
