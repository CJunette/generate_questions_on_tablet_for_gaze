import re
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] # 选择合适的字体名称
plt.rcParams['axes.unicode_minus'] = False # 解决负号'-'显示为方块的问题


def preprocess_raw_text(raw_text):
    raw_text_list_of_rows = raw_text.split('\n')
    text_unit_list_of_rows = []
    for row_index in range(len(raw_text_list_of_rows)):
        text_units = re.split('<sep\d+[a-zA-Z]\d*>', raw_text_list_of_rows[row_index])[1:]
        pattern = re.compile(r'<sep(\d+)([a-zA-Z])(\d*)>')
        matches = pattern.finditer(raw_text_list_of_rows[row_index])

        text_unit_list = []
        text_unit_index = 0

        total_length = 0
        for match in matches:
            length = int(match.group(1))
            align = match.group(2)
            if match.group(3):
                font_size = int(match.group(3))
            else:
                font_size = -1
            text_unit_list.append({
                "text": text_units[text_unit_index],
                "length": length,
                "align": align,
                "font_size": font_size
            })
            text_unit_index += 1
            total_length += length

        if total_length > grid_x_num:
            print(f"Error: The total length of the text units in row {row_index} is larger than {grid_x_num}. Length: {total_length}")
            exit(1)
        for i in range(total_length, grid_x_num):
            text_unit_list.append({
                "text": " ",
                "length": 1,
                "align": "c",
                "font_size": -1
            })
        text_unit_list_of_rows.append(text_unit_list)

    return text_unit_list_of_rows


def generate_latex_tabular(font_size):
    print(f"\\begin{{tabular}}{{|*{{{grid_x_num}}}{{m{{{grid_width}mm}}|}}}}")
    # print(f"\\rule{{0pt}}{{{grid_width}mm}} ", end="")
    # for i in range(grid_x_num - 1):
    #     print("&", end="")
    # print("\\\\[0pt]")

    for row_index in range(len(text_unit_list_of_rows)):
        print("\\hline")
        # print(f"\\rule{{0pt}}{{{grid_height:.2f}mm}}", end="")
        for text_unit_index, text_unit in enumerate(text_unit_list_of_rows[row_index]):
            content = text_unit["text"]
            length = text_unit["length"]
            align = text_unit["align"]

            if text_unit_index < len(text_unit_list_of_rows[row_index]) - 1:
                end_str = " &"
            else:
                end_str = " \\\\"
            # print(f"\\multicolumn{{{length}}}{{{align}|}}{{{content}}}", end=end_str)
            print(f"\\multicolumn{{{length}}}{{|>{{\\fontsize{{{font_size}}}{{0}}\\selectfont}}m{{{length*grid_width}mm}}|}}{{{content}}}", end=end_str)
        print(f"[{grid_height:.2f}mm]")
    print("\hline")
    print("\end{tabular}")

    pass


def generate_grids():
    grids = []
    for j in range(grid_y_num):
        for i in range(grid_x_num):
            grids.append({
                "x": start_x + i * grid_width + i * horizontal_space,
                "y": start_y + j * grid_height + j * vertical_space,
                "width": grid_width,
                "height": grid_height
            })
    return grids


def generate_plot(text_unit_list_of_rows):
    grids = generate_grids()

    fig, ax = plt.subplots()
    ax.set_xlim(0, total_width)
    ax.set_ylim(total_height, 0)
    ax.set_aspect('equal')

    # 删除坐标轴
    ax.axis('off')
    # 使图片靠近边缘
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # 将图片大小固定为2560*1600
    fig.set_size_inches(total_width / 100, total_height / 100)

    # plot grid
    for grid in grids:
        ax.add_patch(plt.Rectangle((grid["x"], grid["y"]), grid["width"], grid["height"], fill=None, edgecolor='#FFFFFF'))

    regular_font_size = 35
    # plot text
    for row_index in range(len(text_unit_list_of_rows)):
        grid_index = 0
        for text_unit_index in range(len(text_unit_list_of_rows[row_index])):
            text_unit = text_unit_list_of_rows[row_index][text_unit_index]
            content = text_unit["text"]
            length = text_unit["length"]
            align = text_unit["align"]
            if text_unit["font_size"] != -1:
                font_size = text_unit["font_size"]
            else:
                font_size = regular_font_size
            grid = grids[row_index * grid_x_num + grid_index]
            x = grid["x"]
            y = grid["y"]
            width = grid["width"] * length
            height = grid["height"]
            if align == "c":
                ax.text(x + width / 2, y + height / 2, content, ha='center', va='center', fontsize=font_size)
            elif align == "l":
                ax.text(x, y + height / 2, content, ha='left', va='center', fontsize=font_size)
            elif align == "r":
                ax.text(x + width, y + height / 2, content, ha='right', va='center', fontsize=font_size)
            grid_index += length

    # plt.show()
    plt.savefig('test.png', dpi=100)


if __name__ == '__main__':
    total_width = 2560
    total_height = 1600
    grid_width = 75
    grid_height = int(grid_width * 1.12)
    grid_x_num = 30
    grid_y_num = 12
    horizontal_space = 0
    vertical_space = 0
    start_x = (total_width - grid_x_num * grid_width - (grid_x_num - 1) * horizontal_space) / 2
    start_y = (total_height - grid_y_num * grid_height - (grid_y_num - 1) * vertical_space) / 2

    formular_font_size = 20
    raw_text = (f"<sep1c>甲<sep1c>乙<sep1c>两<sep1c>人<sep1c>投<sep1c>篮<sep1c>, <sep1c>每<sep1c>次<sep1c>由<sep1c>其<sep1c>中<sep1c>一<sep1c>人<sep1c>投<sep1c>篮<sep1c>, <sep1c>规<sep1c>则<sep1c>如<sep1c>下<sep1c>: "
                "<sep1c>若<sep1c>命<sep1c>中<sep1c>则<sep1c>此<sep1c>人<sep1c>继<sep1c>续\n<sep1c>投<sep1c>篮<sep1c>, <sep1c>若<sep1c>未<sep1c>命<sep1c>中<sep1c>则<sep1c>换<sep1c>为<sep1c>对<sep1c>方<sep1c>投<sep1c>篮<sep1c>. "
                "<sep1c>无<sep1c>论<sep1c>之<sep1c>前<sep1c>投<sep1c>篮<sep1c>情<sep1c>况<sep1c>如<sep1c>何<sep1c>, <sep1c>甲<sep1c>每<sep1c>次<sep1c>投\n<sep1c>篮<sep1c>的<sep1c>命<sep1c>中<sep1c>率<sep1c>均<sep1c>为<sep1c>0.6<sep1c>, "
                "<sep1c>乙<sep1c>每<sep1c>次<sep1c>投<sep1c>篮<sep1c>的<sep1c>命<sep1c>中<sep1c>率<sep1c>均<sep1c>为<sep1c>0.8<sep1c>, <sep1c>由<sep1c>抽<sep1c>签<sep1c>决<sep1c>定<sep1c>第<sep1c>一<sep1c>次\n<sep1c>投<sep1c>篮<sep1c>的<sep1c>人<sep1c>选<sep1c>, "
                "<sep1c>第<sep1c>一<sep1c>次<sep1c>投<sep1c>篮<sep1c>的<sep1c>人<sep1c>是<sep1c>甲<sep1c>, <sep1c>乙<sep1c>的<sep1c>概<sep1c>率<sep1c>各<sep1c>为<sep1c>0.5<sep1c>.\n"
                "<sep2l>( 1 ) <sep1c>求<sep1c>第<sep1c>2<sep1c>次<sep1c>投<sep1c>篮<sep1c>的<sep1c>人<sep1c>是<sep1c>乙<sep1c>的<sep1c>概<sep1c>率<sep1c>;\n"
                "<sep2l>( 2 ) <sep1c>求<sep1c>第<sep1c>$i$<sep1c>次<sep1c>投<sep1c>篮<sep1c>的<sep1c>人<sep1c>是<sep1c>甲<sep1c>的<sep1c>概<sep1c>率<sep1c>;\n"        
                "<sep2l>( 3 ) <sep1c>已<sep1c>知<sep1c>: <sep1c>若<sep1c>随<sep1c>机<sep1c>变<sep1c>量<sep1c>$X_i$<sep1c>服<sep1c>从<sep1c>两<sep1c>点<sep1c>分<sep1c>布<sep1c>, "
                "<sep1c>且<sep9l"+str(formular_font_size)+">$P\left(X_i=1\\right)=1-P\left(X_i=0\\right)=q_i, i=$ $1,2, \cdots, n$<sep1c>, <sep1c>则\n<sep4c"+str(formular_font_size)+">$E\left(\sum_{i=1}^n X_i\\right)=\sum_{i=1}^n q_i$<sep1c>, "
                "<sep1c>记<sep1c>前<sep1c>$n$<sep1c>次<sep1c>(<sep1c>即<sep1c>从<sep1c>第<sep1c>1<sep1c>次<sep1c>到<sep1c>第<sep1c>$n$<sep1c>次<sep1c>投<sep1c>篮<sep1c>)<sep1c>中"
                "<sep1c>甲<sep1c>投<sep1c>篮<sep1c>的<sep1c>次<sep1c>数<sep1c>为\n<sep1c>$Y$<sep1c>, <sep1c>求<sep2c>$E(Y)$<sep1c>.")

    text_unit_list_of_rows = preprocess_raw_text(raw_text)
    # generate_latex_tabular(15)

    generate_plot(text_unit_list_of_rows)


