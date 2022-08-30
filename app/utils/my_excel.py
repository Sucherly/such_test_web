class excel_op:
    def __init__(self, file):
        self.file = file

    @staticmethod
    def get_merged_cell_value(self, sheet, merge_ranges, row, head_index):
        """获取合并单元格值"""
        flag = False
        is_first_row = True
        val = row[head_index].value  # 默认是本单元格数据
        for range_data in merge_ranges:
            l_col, l_row, r_col, r_row = range_data.bounds
            if l_row <= row[0].row <= r_row and l_col <= head_index + 1 <= r_col:
                find_col = l_row
                find_row = l_col
                val = sheet.cell(row=find_col, column=find_row).value  # 如果是合并单元格，则取左上角第一个单元格数据
                flag = True
                if row[0].row != l_row:
                    is_first_row = False
                break
        return val, flag, is_first_row
