from pywebio.input import *
from pywebio.output import *

data = input_group(
    "用户数据",
    [
        input("请问您的名字是: ", name="name", type=TEXT),
        input("输入您的年龄", name="age", type=NUMBER),
        radio(
            "哪个洲的",
            name="continent",
            options=[
                "非洲",
                "亚洲",
                "澳大利亚",
                "欧洲",
                "北美洲",
                "南美洲",
            ],
        ),
        checkbox(
            "用户隐私条例", name="agreement", options=["同意"]
        ),
    ],
)

put_text("表格输出:")

put_table(
    [
        ["名字", data["name"]],
        ["年龄", data["age"]],
        ["位置", data["continent"]],
        ["条例", data["agreement"]],
    ]
)