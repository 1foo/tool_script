import re


def sql_to_md(sql):



    lines = sql.splitlines()
    # remove leading/trailing white space and semicolons
    lines = [line.strip().rstrip(';') for line in lines]
    md_lines = []
    for line in lines:
        # check if line starts with "CREATE TABLE"
        if line.startswith('CREATE TABLE'):
            # extract table name from CREATE TABLE statement

            table_name_pattern = r"`(.*)`"
            table_name_match = re.search(table_name_pattern, line)
            if table_name_match:
                table_name = table_name_match.group(1)
            else:
                table_name = 'unknown'

           
            md_lines.append(f'## {table_name}\n\n')
            md_lines.append('| 字段名 | 数据类型 | 默认值| 注释 |')
            md_lines.append('| ------ | ------ | ------ | ------ |')

            
       
        elif line.strip().startswith('`'):
                parts = line.strip().split(' ')
                column_name = parts[0][1:-1]
                column_type = parts[1]

                column_default_pattern = r"DEFAULT\s+(\S+)\s*"
                column_default_match = re.search(column_default_pattern, line)
                column_default = column_default_match.group(1) if column_default_match else ''

                comment_pattern = r"COMMENT\s+'(.*)'"
                comment_match = re.search(comment_pattern, line)
                if comment_match:
                    column_comment = comment_match.group(1)
                else:
                    column_comment = ''

                md_lines.append(f'| {column_name} | {column_type} | {column_default}|{column_comment} |')

        elif line.startswith(('PRIMARY KEY', 'INDEX')):
            # md_lines.append('\n索引：')
            md_lines.append(f'- {line.strip()}')

    return '\n'.join(md_lines)


# 读取SQL文件
with open('cybeer.sql', 'r') as f:
    sql = f.read()


# 生成markdown表格格式
table_md = sql_to_md(sql)

# 将输出结果保存到文件中
with open('output.txt', 'w') as f:
    f.write(table_md)
