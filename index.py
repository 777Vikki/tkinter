from tkinter import Tk, Menu
from tkinter.messagebox import showwarning, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfile
import os
from xliff import i18nXmlParsing, dublicateIdParsing, updateXliff
from excel import xmlToExcel, excelParsing, compareExcelData

def xliff_excelConverter():
    file = askopenfilename(filetypes=[("Xliff files", ".xlf")])
    if(file != ""):
        Xlifflst = i18nXmlParsing(file)
        xmlToExcel(Xlifflst)

def excel_xliffConverter():
    file = askopenfilename(filetypes=[("excel files", ".xlsx")])
    if(file != ""):
        excelData = excelParsing(file)
        file = askopenfilename(filetypes=[("Xliff files", ".xlf")])
        if(file != ""):
            updateXliff(excelData, file)

def dublicateId():
    file = askopenfilename(filetypes=[("Xliff files", ".xlf")])
    if(file != ""):
        xliffData = dublicateIdParsing(file)
        if(xliffData != "No Dublicate Id found"):
            xmlToExcel(xliffData)
        else:
            showinfo(xliffData + "          ")

def import_XliffToXliff():
    pass

def com_ExcelToExcel():
    showinfo("Compare Based On Id       ")
    file1 = askopenfilename(filetypes=[("excel files", ".xlsx")])
    if(file1 != ""):
        showinfo("Select another Excel file       ")
        file2 = askopenfilename(filetypes=[("excel files", ".xlsx")])
        if(file2 != ""):
            length = compareExcelData(file1, file2)
            if(length == 9):
                showinfo("No Missing Data        ")


def quitApp():
    root.destroy()
if __name__ == "__main__":
    root = Tk()
    root.title("XLIFF Converter")
    root.geometry("300x300")
    root.maxsize(300, 300)
    root.minsize(300, 300)
    
    MenuBar = Menu(root)
    FileMenu = Menu(MenuBar, tearoff=0)
    FileMenu.add_command(label="XLIFF To Excel", command=xliff_excelConverter)
    FileMenu.add_command(label="Excel To XLIFF", command=excel_xliffConverter)
    FileMenu.add_command(label="Import XLIFF file", command=import_XliffToXliff)
    FileMenu.add_command(label="Check Doublicate Id", command=dublicateId)
    FileMenu.add_command(label="Compare Excel to Excel", command=com_ExcelToExcel)

    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    root.config(menu=MenuBar)
    root.mainloop()