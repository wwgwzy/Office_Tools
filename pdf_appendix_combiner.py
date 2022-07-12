# -*- coding: UTF-8 -*-

import os
import sys
import officef
import shutil


def main(ipdir=os.getcwd(),
         water_marker_position_x=300,
         water_marker_position_y=10,
         font_size=32,
         font="Arial",
         pdf_op_name="合并.pdf", opdir=None):
    print(ipdir)
    pdf_water_marker_opdir, index_l = officef.pdf_add_wtrmrk_index(ipdir,
                                                                   water_marker_position_x,
                                                                   water_marker_position_y,
                                                                   font_size, font)
    index_d = {}
    for index in index_l:
        index_a = index.split("-")[0]
        index_d[index_a] = []
    for index in index_l:
        index_a = index.split("-")[0]
        index_b = index.split("-")[1]
        index_d[index_a].append(index_b)
    index_sum = []
    for index_a in index_d:
        index_a_max = max(index_d[index_a])
        index_a_min = min(index_d[index_a])
        index_sum.append("%s-%s~%s" % (index_a, index_a_min, index_a_max))
    pdf_op_name = '、'.join(str(d) for d in index_sum)+".pdf"
    # print(index_pretty)
    opdir = " ".join([ipdir, "已合并"])
    officef.pdf_combiner(pdf_water_marker_opdir, pdf_op_name=pdf_op_name, opdir=opdir)
    shutil.rmtree(pdf_water_marker_opdir)


if __name__ == "__main__":
    # main(r'D:\wwg\home\Repository\Office_Tools\cb')
    if len(sys.argv) > 2:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
