# -*- coding: UTF-8 -*-

import pdfplumber, re, time, os

class injection:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

        with pdfplumber.open(self.pdf_path) as self.pdf:
            # 获取pdf报告头部信息
            header_text = self.pdf.pages[0].extract_text()
            header_compile = re.compile(
                '.*Sample Name: (.*) Project Name.*Volume\(μL\): (.*)Acq.*Run Time: (.*) Reporter.*', re.S)
            header_match = header_compile.search(header_text)

            # 样品名
            self.sample_name = header_match.group(1).strip()
            # 进样量
            self.inj_vol = header_match.group(2).strip()
            # 进样时间
            self.inj_time = time.mktime(time.strptime(header_match.group(3).strip()[0:18], '%Y-%m-%d %H:%M:%S'))

            # 测试输出头部信息
            #print(self.sample_name, self.inj_vol + 'ul', self.inj_time)

            # 获取峰信息表表头
            self.table_header = []
            for header in self.pdf.pages[0].extract_tables()[-1][0]:
                self.table_header.append(header.replace('\n', ''))

            # 输出表头信息
            # print('table header:', self.table_header)
            # print('table header:', self.pdf.pages[0].extract_tables())

            # 每行峰信息写入到单针峰信息总字典
            self.peaks_dict = {}
            self.table = self.pdf.pages[0].extract_tables()[-1][1:]
            # print(self.table)
            for peak_info in self.table:
                # 单个峰信息字典生成
                peak_dict = dict(zip(self.table_header, peak_info))
                # 写入单针峰信息总字典，peak_info[0] 为 RT，总字典按峰RT索引，单个峰字典信息（RT、RRT、A%等）顺序视具体报告格式而定
                self.peaks_dict[peak_info[0]] = peak_dict
            # for peak, info in self.peaks_dict.items():
            # print(peak, info)


class sequence:
    pass


