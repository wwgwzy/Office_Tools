# -*- coding: UTF-8 -*-

import os, osext, PyPDF2, fpdf


def pdf_combiner(ipdir=os.getcwd(), pdf_op_name="合并.pdf", opdir=None):
    print(ipdir)
    if opdir is None:
        opdir = "".join([ipdir, " 已合并"]).strip()
    if not os.path.exists(opdir):
        os.makedirs(opdir)
    pdf_op_path = os.path.join(opdir, pdf_op_name)

    # pdf_writer = PyPDF2.PdfFileWriter()
    file_merger = PyPDF2.PdfFileMerger()
    # with open(pdf_op_path, 'ab') as pdf_op_file:
    for pdf_ip_path in osext.files_searching(".pdf", ipdir):
        print(os.path.basename(pdf_ip_path))
        # with open(pdf_ip_path, 'rb') as pdf_ip_file:
        #     pdf_reader = PyPDF2.PdfFileReader(pdf_ip_file)
        #     for pageNum in range(pdf_reader.numPages):
        #         page_obj = pdf_reader.getPage(pageNum)
        #         pdf_writer.addPage(page_obj)
        #     pdf_writer.write(pdf_op_file)
        file_merger.append(PyPDF2.PdfFileReader(pdf_ip_path, 'rb'))
    file_merger.write(pdf_op_path)
    print(pdf_op_path)
    return None


def pdf_add_wtrmrk_index(ipdir=os.getcwd(),
                         water_marker_position_x=300,
                         water_marker_position_y=10,
                         font_size=32, font="Arial", opdir=None,):
    if opdir is None:
        opdir = "".join([ipdir, " 已加水印"]).strip()
    print(opdir)
    if not os.path.exists(opdir):
        os.makedirs(opdir)

    index_l = []
    for pdf_path in osext.files_searching('.pdf', ipdir):
        pdf_fn = os.path.basename(pdf_path)
        index_text = pdf_fn.split()[0]
        index_l.append(index_text)
        # print(index_text)

        index_wtrmrk_pdf = fpdf.FPDF()
        index_wtrmrk_pdf.add_page()
        index_wtrmrk_pdf.set_font(font, size=font_size)
        index_wtrmrk_pdf.cell(water_marker_position_x, water_marker_position_y, txt=index_text, ln=1, align='C')
        index_wtrmrk_pdf.output("index_wtrmrk.pdf")

        input_file = pdf_path
        output_file = os.path.join(opdir, pdf_fn)
        watermark_file = "index_wtrmrk.pdf"

        with open(input_file, "rb") as filehandle_input:
            # read content of the original file
            pdf = PyPDF2.PdfFileReader(filehandle_input)

            with open(watermark_file, "rb") as filehandle_watermark:
                # read content of the watermark
                watermark = PyPDF2.PdfFileReader(filehandle_watermark)

                # get first page of the original PDF
                first_page = pdf.getPage(0)

                # get first page of the watermark PDF
                first_page_watermark = watermark.getPage(0)

                # merge the two pages
                first_page.mergePage(first_page_watermark)

                # create a pdf writer object for the output file
                pdf_writer = PyPDF2.PdfFileWriter()

                # add page
                pdf_writer.addPage(first_page)

                with open(output_file, "ab") as file_output:
                    # write the watermarked file to the new file
                    if pdf.getNumPages() > 1:
                        for page_number in range(0,pdf.getNumPages()):
                            the_last_page = pdf.getPage(page_number)
                            pdf_writer.addPage(the_last_page)
                    pdf_writer.write(file_output)
    os.remove(watermark_file)
    return opdir, index_l
