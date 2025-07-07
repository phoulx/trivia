import numpy as np
from sympy import symbols, Eq, solve, lambdify, latex
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'STXihei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def find_polynomial(sequence):
    sequence = np.array(sequence)
    diffs = [sequence]
    while len(diffs[-1]) > 1:
        diffs.append(np.diff(diffs[-1]))
    
    # 差分阶数决定多项式次数
    degree = len(diffs) - 1
    print(f"差分阶数：{degree}，多项式次数：{degree}")

    # 构建符号和通项公式
    n = symbols('n', integer=True)
    coefficients = symbols(f'A0:{degree+1}')
    a_n = sum(coeff * n**i for i, coeff in enumerate(coefficients))
    
    # 建立方程组（取前degree+1项）
    equations = []
    for k in range(1, degree + 2):
        equations.append(Eq(a_n.subs(n, k), sequence[k-1]))
    
    # 求解系数
    solution = solve(equations, coefficients)
    formula = a_n.subs(solution)
    
    return formula, n, degree

def plot_sequence_and_polynomial(sequence):
    formula, n, degree = find_polynomial(sequence)
    print("通项公式：", formula)
    
    # 创建一个可以计算值的函数
    formula_func = lambdify(n, formula, "numpy")
    
    # 准备绘图数据
    x_orig = np.arange(1, len(sequence) + 1)  # 原始序列的索引
    x_extd = np.linspace(1, len(sequence) + 5, 100)  # 扩展的x值，用于绘制平滑曲线
    
    plt.figure(figsize=(10, 6))
    
    # 绘制原始序列点
    plt.scatter(x_orig, sequence, color='red', s=50, label='原始序列')
    
    # 绘制多项式曲线
    y_poly = formula_func(x_extd)
    plt.plot(x_extd, y_poly, 'b-', label=f'{degree}次多项式拟合')
    
    # 添加预测的后续值
    next_values = [formula_func(i) for i in range(len(sequence)+1, len(sequence)+5)]
    next_indices = list(range(len(sequence)+1, len(sequence)+5))
    plt.scatter(next_indices, next_values, color='green', s=50, label='预测的后续值')
    
    # 添加标签和图例
    for i, val in enumerate(sequence):
        plt.annotate(f'{val}', (x_orig[i], val), textcoords="offset points", 
                    xytext=(0,10), ha='center')
    
    for i, val in enumerate(next_values):
        plt.annotate(f'{val:.1f}', (next_indices[i], val), textcoords="offset points",
                   xytext=(0,10), ha='center', color='green')
    
    # 使用LaTeX格式来显示公式，以正确显示上标
    formula_latex = "$" + latex(formula) + "$"
    plt.title(f'序列拟合 - {formula_latex}', fontsize=12)
    
    plt.xlabel('序列索引 n')
    plt.ylabel('值')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# 测试
sequence = [4, 9, 20, 40, 78, 152]
plot_sequence_and_polynomial(sequence)