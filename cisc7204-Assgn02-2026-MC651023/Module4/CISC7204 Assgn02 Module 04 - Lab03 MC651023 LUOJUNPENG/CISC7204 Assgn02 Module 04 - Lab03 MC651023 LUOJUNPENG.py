import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import os

# ==========================================
# TASK 1: 读取并准备数据
# ==========================================
# 读取本地的 CSV 文件
local_file = 'airline_data.csv'

if os.path.exists(local_file):
    # 加上 encoding='utf-8-sig' 防止出现隐藏字符报错
    df = pd.read_csv(local_file, encoding='utf-8-sig')
    print("✅ 本地数据读取成功！")
else:
    print(f"❌ 找不到文件 {local_file}，请确保它和代码在同一个文件夹！")
    exit()

# 清理列名（去除前后可能存在的空格）
df.columns = df.columns.str.strip()

# 强制确保 Year 和 Month 是数字类型
# 你的数据中本来就有 Year 列，所以直接用！
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
df['ArrDelay'] = pd.to_numeric(df['ArrDelay'], errors='coerce')

# 去除缺失值
df = df.dropna(subset=['Year', 'Month', 'ArrDelay'])


# ==========================================
# TASK 2: 搭建 Dash 布局
# ==========================================
app = Dash(__name__)

app.layout = html.Div(children=[
    # 标题
    html.H1('Airline Performance Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # 输入框区域
    html.Div([
        "Input Year: ",
        dcc.Input(
            id='input-year', 
            value=2010,       # 默认年份设为 2010
            type='number',    
            placeholder='Enter a year (e.g., 2010)', 
            style={'height': '50px', 'font-size': 35, 'textAlign': 'center'}
        )
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),
    
    # 图表输出区域
    html.Div(dcc.Graph(id='line-plot'))
])

# ==========================================
# TASK 3 & 4: 回调函数 (Callback) & 生成柱状图
# ==========================================
@app.callback(
    Output('line-plot', 'figure'),
    Input('input-year', 'value')
)
def update_graph(apport_year):
    # 防止用户清空输入框导致报错
    if apport_year is None:
        apport_year = 2010
    
    apport_year = int(apport_year)
    
    # 根据输入的年份过滤数据
    dff = df[df['Year'] == apport_year]
    
    # 如果输入了数据中不存在的年份，返回一个提示图
    if dff.empty:
        fig = px.bar(title=f'No data found for year {apport_year}')
        return fig

    # 按月份计算 ArrDelay 的平均值
    line_data = dff.groupby('Month')['ArrDelay'].mean().reset_index()
    
    # 【TASK 4 要求】绘制柱状图 (Bar Chart)
    fig = px.bar(
        line_data, 
        x='Month', 
        y='ArrDelay', 
        title=f'Average Arrival Delay by Month for the Year {apport_year}'
    )
    
    # 设置坐标轴标签，让它看起来更专业
    fig.update_layout(
        xaxis_title='Month (1-12)',
        yaxis_title='Average Arrival Delay (minutes)'
    )
    
    return fig

# ==========================================
# 运行 App
# ==========================================
if __name__ == '__main__':
    print("🚀 启动 Dash 应用，请在浏览器打开 http://127.0.0.1:8050/")
    app.run(debug=True)