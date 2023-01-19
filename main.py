import os
import shutil
from tkinter import *
from tkinter import filedialog as fd
import pandas as pd
import time


def select_source():
    lbl_src_selected.config(text='')
    src_path = fd.askdirectory(initialdir='/', title='Select Source Folder')
    lbl_src_selected.config(text=src_path)

    if os.path.isdir(src_path):
        btn_dst_path.config(state='normal')


def select_destination():
    lbl_dst_selected.config(text='')
    dst_path = fd.askdirectory(initialdir='/', title='Select Destination Folder')
    lbl_dst_selected.config(text=dst_path)

    if os.path.isdir(dst_path):
        btn_image_ids.config(state='normal')


def file_upload():
    lbl_image_ids_selected.config(text='')
    image_ids_path = fd.askopenfilename(
        initialdir='/', title='Select ImageID File',
        filetypes=[('Excel or CSV', '*.xlsx *.csv')]
    )
    lbl_image_ids_selected.config(text=image_ids_path)

    if os.path.isfile(image_ids_path):
        btn_copy_matches.config(state='normal')


def copy_images():
    src = lbl_src_selected.cget("text")
    dst = lbl_dst_selected.cget("text")
    image_ids_path = lbl_image_ids_selected.cget("text")

    if image_ids_path[-3:] == 'csv':
        image_ids = pd.read_csv(image_ids_path, low_memory=False)
    else:
        image_ids = pd.read_excel(image_ids_path)

    image_ids = image_ids.iloc[:, 0].astype(str).tolist()

    filenames_to_search = [x + '.svs' for x in image_ids]
    filenames_to_search = set(filenames_to_search)
    start = time.time()
    files_copied = 0
    for (dirpath, dirnames, filenames) in os.walk(src):
        for filename in filenames:
            if filename in filenames_to_search:
                print(f'{filename} found!')
                shutil.copy(os.path.join(dirpath, filename), dst)
                files_copied += 1
    stop = time.time()
    duration = stop - start

    print(f'\nProcess completed. {files_copied} / {len(filenames_to_search)} found.')
    print(f'Process completed in {duration} seconds.')


title_font = ('Arial', 12)
default_font = ('Arial', 10)
notice_font = ('Arial', 8)

root = Tk()
root.geometry('1200x900')
root.title('nPOD File Mover')

lbl_window_title = Label(root, text='Welcome to the nPOD file mover', font=title_font)
lbl_window_title.grid(row=0, column=0, sticky='n')

frame_file_info = Frame(root, bd=5, relief='ridge')
frame_file_info.grid(row=1, column=0, padx=15, pady=15)

lbl_src_path = Label(frame_file_info, text='Input the path to search (source): ', font=default_font)
lbl_src_path.grid(row=0, column=0, padx=5, pady=5, sticky='e')

btn_src_path = Button(frame_file_info, text='Select Source Folder', command=select_source, font=default_font)
btn_src_path.grid(row=0, column=1, padx=5, pady=5, sticky='w')
lbl_src_selected = Label(frame_file_info, text='', font=default_font)
lbl_src_selected.grid(row=0, column=2, padx=5, pady=5)

lbl_dst_path = Label(frame_file_info, text='Input the path to copy the files to (destination): ', font=default_font)
lbl_dst_path.grid(row=1, column=0, padx=5, pady=5, sticky='e')
btn_dst_path = Button(frame_file_info, text='Select Destination Folder', command=select_destination, font=default_font)
btn_dst_path.grid(row=1, column=1, padx=5, pady=5, sticky='w')
btn_dst_path.config(state='disabled')
lbl_dst_selected = Label(frame_file_info, text='', font=default_font)
lbl_dst_selected.grid(row=1, column=2, padx=5, pady=5)

lbl_image_ids = Label(
    frame_file_info,
    text='Upload an Excel or .csv file containing the desired ImageIDs.',
    font=default_font
)
lbl_image_ids.grid(row=2, column=0, padx=5, pady=5, sticky='e')
lbl_image_id_instructions = Label(
    frame_file_info,
    text='Note: Please make sure that the image IDs to search for \noccupy the first column of the uploaded sheet.',
    font=notice_font
)
lbl_image_id_instructions.grid(row=3, column=0, padx=5, sticky='n')
btn_image_ids = Button(frame_file_info, text='Select File', command=file_upload, font=default_font)
btn_image_ids.grid(row=2, column=1, padx=5, pady=5, sticky='w')
btn_image_ids.config(state='disabled')
lbl_image_ids_selected = Label(frame_file_info, text='', font=default_font)
lbl_image_ids_selected.grid(row=2, column=2, padx=5, pady=5)

btn_copy_matches = Button(frame_file_info, text='Copy Images', command=copy_images, font=default_font)
btn_copy_matches.grid(row=4, column=1, pady=15, sticky='se')
btn_copy_matches.config(state='disabled')

# frame_rename_files = Frame(root, bd=5, relief='ridge')
# frame_rename_files.grid(row=2, column=0, padx=15, pady=15)
# lbl_rename_files = Label(frame_rename_files,
#                          text='Upload a .csv or .xlsx in the following format:'
#                               '\nFirst Column: ImageID'
#                               '\nSecond Column: Desired Filename',
#                          font=default_font)
# lbl_rename_files.grid(row=5, column=0, pady=15, sticky='w')

root.mainloop()
