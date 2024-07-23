import pandas as pd
import numpy as np

class Tlims_Data():

    def get_tlims_batch_data(self, file_url, headers):
        # 通过路径获取数据
        # df = pd.read_csv(file_url)
        df = pd.read_csv(file_url, header=None, names=headers)
        df_data = df.iloc[12:]
        return df_data

    def get_tlims_batchs_data(self, files_url, quality_control_sample):
        # 获取batch data数据
        # 自定义表头
        headers = ['NO', 'Link To', 'Sample Id', 'QC Sample Type', 'Description', 'Lab Due date',
                   'Request ID', 'QC batch', 'Spec Condition', 'Retest']
        batch_data = pd.DataFrame(columns=headers)
        batch_data['Sample Id'] = quality_control_sample
        for file_url in files_url:
            df_data = self.get_tlims_batch_data(file_url, headers)
            batch_data = pd.concat([batch_data, df_data], ignore_index=True)
        batch_data['ID'] = range(1, len(batch_data) + 1)
        return batch_data

    def duplicate_data(self, dataframe_data, col_name):
        df = pd.DataFrame(dataframe_data)
        # 使用melt方法进行逆透视
        df_melted = pd.melt(df, id_vars=['Sample Id', 'ID'], value_vars=col_name, var_name='Variable', value_name='Value')

        # 新增重复的Sample ID
        df_melted['F Sample Id'] = df_melted['Sample Id'] + df_melted['Value']

        # 按ID列排序
        df_sorted = df_melted.sort_values(by=['ID', 'Variable']).reset_index(drop=True)
        df_final = df_sorted

        return df_final

    def add_qc_data(self, dataframe_data, new_row, col_name_len, qc_num):
        # 定义要插入的行
        # new_row = pd.DataFrame([{'Sample Id': qc_msg, 'ID': 'CC', 'Variable': 'C', 'Value': 1, 'F Sample Id': qc_msg}])

        # 将DataFrame分割为每60行一组
        n = int(qc_num) * int(col_name_len)
        df_list = [dataframe_data.iloc[i:i + n] for i in range(0, len(dataframe_data), n)]

        # 在每组的末尾插入新行
        df_list_with_new_rows = []
        for df_group in df_list:
            df_group_with_new_row = pd.concat([df_group, new_row], ignore_index=True)
            df_list_with_new_rows.append(df_group_with_new_row)

        # 重新组合成一个数据框
        df_qc = pd.concat(df_list_with_new_rows).reset_index(drop=True)

        return df_qc



    def ph_duplicate_data(self):
        pass
