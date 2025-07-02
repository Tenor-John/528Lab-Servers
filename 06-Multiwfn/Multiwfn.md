# 🔬 Multiwfn 波函数分析软件使用手册

<div style="background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">

📖 **Multiwfn 简介**  
Multiwfn是一款功能全面的波函数分析程序，支持几乎所有类型的波函数分析，是量子化学计算后处理的利器。

**🎯 主要功能：**
- 波函数分析与可视化
- 电子密度分析  
- 分子轨道分析
- 电荷布居分析
- 拓扑分析 (AIM理论)
- 弱相互作用分析 (NCI, IGM)

</div>

---

## 📋 目录

- [软件安装](#软件安装)
- [基础操作](#基础操作)
- [波函数载入](#波函数载入)
- [常用分析功能](#常用分析功能)
- [高级分析](#高级分析)
- [可视化输出](#可视化输出)

---

## 🔧 软件安装

### Linux环境安装

```bash
# 下载Multiwfn
wget http://sobereva.com/multiwfn/misc/Multiwfn_3.8_dev_bin_Linux.zip

# 解压安装
unzip Multiwfn_3.8_dev_bin_Linux.zip
cd Multiwfn_3.8_dev_bin_Linux

# 设置环境变量
export Multiwfnpath=/path/to/Multiwfn_3.8_dev_bin_Linux
export PATH=$Multiwfnpath:$PATH

# 设置临时文件目录
export KMP_STACKSIZE=200m
```

### 启动Multiwfn

```bash
# 命令行启动
Multiwfn

# 直接载入文件
Multiwfn molecule.fchk

# 批处理模式
Multiwfn molecule.fchk < input.txt
```

---

## 🎮 基础操作

### 主菜单结构

Multiwfn主菜单包含以下主要选项：

```
0  Exit program
1  Show molecular structure and view orbitals
2  Topology analysis
3  Output and plot specific properties in a line
4  Output and plot specific properties in a plane  
5  Output and plot specific properties in a space
6  Check & modify wavefunction
7  Population analysis and calculation of atomic charges
8  Orbital composition analysis
9  Bond order analysis
10 Plot density-of-states (DOS)
11 Plot IR/Raman/UV-Vis/ECD spectrum
12 Quantitative analysis of molecular surface
13 Process grid data (density/potential/ESP)
14 Adaptive natural density partitioning (AdNDP)
15 Fuzzy atomic space analysis
16 Charge decomposition analysis (CDA) and plot orbital interaction diagram
17 Basin analysis
18 Electron excitation analysis
19 Orbital localization analysis  
20 Visual study of weak interaction
21 Energy decomposition analysis
100 Other functions
```

---

## 📂 波函数载入

### 支持的文件格式

| 格式 | 软件来源 | 用途 |
|------|----------|------|
| **.fchk** | Gaussian | 标准波函数文件 |
| **.wfn/.wfx** | 通用 | 波函数交换格式 |
| **.molden** | ORCA, MOLPRO | 轨道文件 |
| **.cube** | 各种软件 | 格点数据 |
| **.31** | ADF | ADF波函数 |

### 文件转换

```bash
# Gaussian fch文件转换为fchk
formchk molecule.fch molecule.fchk

# ORCA输出转换为Multiwfn格式  
orca_2mkl molecule -molden
# 然后在Multiwfn中选择molden文件
```

---

## 🧮 常用分析功能

### 1. 电荷布居分析

```bash
# 启动Multiwfn
Multiwfn molecule.fchk

# 选择布居分析
7  # Population analysis

# 选择方法
1  # Hirshfeld charge
2  # VDD charge  
3  # Mulliken charge
4  # Löwdin charge
5  # SCPA charge
6  # ADCH charge
7  # ChElPG charge
8  # MK charge
9  # AIM charge
```

### 2. 分子轨道分析

```bash
# 分子轨道可视化
1  # Show molecular structure and view orbitals

# 选择轨道类型
1  # Show molecular orbitals
2  # Show natural orbitals  
3  # Show localized orbitals

# 输出格式
1  # Export orbital as cube file
2  # Export orbital as Molden format
```

### 3. 键级分析

```bash
# 键级计算
9  # Bond order analysis

# 选择方法
1  # Mayer bond order
2  # Wiberg bond order in NAO basis
3  # Laplacian bond order
4  # Fuzzy bond order
```

### 4. 拓扑分析 (AIM)

```bash
# AIM拓扑分析
2  # Topology analysis

# 寻找临界点
3  # Search CPs from nuclear positions
4  # Search CPs from midpoint of atom pairs

# 计算积分性质
16 # Calculate atomic charges and dipole moments
17 # Calculate localization index and delocalization index
```

---

## 🔬 高级分析

### 1. 弱相互作用分析 (NCI)

```bash
# 非共价相互作用分析
20 # Visual study of weak interaction

# NCI分析
1  # RDG analysis (NCI analysis)

# 设置参数
# 选择合适的密度和RDG等值面
# 输出cube文件用于可视化
```

### 2. 独立梯度模型 (IGM)

```bash
# IGM分析  
20 # Visual study of weak interaction
3  # IGM analysis

# 设置参数
# delta-g等值面：0.008
# 颜色范围：-0.05到0.05
```

### 3. 电子定域化函数 (ELF)

```bash
# ELF分析
5  # Output and plot specific properties in a space
1  # Electron density
# 然后选择ELF选项
```

### 4. 静电势分析

```bash
# 静电势计算
12 # Quantitative analysis of molecular surface

# 选择表面类型
1  # van der Waals surface  
2  # Solvent accessible surface
5  # Isosurface of electron density

# 在表面上映射静电势
```

---

## 🎨 可视化输出

### VMD可视化

```bash
# 输出cube文件后，在VMD中可视化
vmd

# 载入cube文件
mol new density.cub

# 设置等值面
mol representation Isosurface
mol selection all
mol scaleminmax 0 0 0.008 0.008  # 设置等值面值
mol addrep 0
```

### PyMOL可视化

```bash
# 在PyMOL中载入
load density.cub
isosurface surf1, density, 0.008
color blue, surf1
```

### 图像输出

```bash
# 在Multiwfn中直接绘图
4  # Output and plot specific properties in a plane

# 选择性质和平面
# 选择绘图选项
3  # Only output plot data to plain text file
4  # Only show 2D colored filled map
```

---

## 📊 批处理脚本

### 自动化分析脚本

```bash
#!/bin/bash
# 批量Hirshfeld电荷分析

for fchk in *.fchk; do
    echo "Processing $fchk"
    
    cat > input.txt << EOF
7
1
1
y
q
EOF
    
    Multiwfn $fchk < input.txt > ${fchk%.fchk}_hirshfeld.txt
    
    echo "Completed $fchk"
done
```

### NCI分析脚本

```bash
#!/bin/bash
# 自动NCI分析

cat > nci_input.txt << EOF
20
1
1
0.5
2.0
1
0
1
-1
q
EOF

for mol in *.fchk; do
    mkdir ${mol%.fchk}_NCI
    cd ${mol%.fchk}_NCI
    Multiwfn ../$mol < ../nci_input.txt
    cd ..
done
```

---

## 🛠️ 常见问题与解决

### 内存不足

```bash
# 对于大体系，设置合适的内存
export OMP_STACKSIZE=1024m
export KMP_STACKSIZE=1024m

# 或降低格点密度
# 在设置中选择较低的格点数
```

### 文件格式问题

```bash
# 检查文件完整性
file molecule.fchk

# 重新生成fchk文件
# 在Gaussian计算中加入 formchk=all
```

### 计算精度设置

```bash
# 在主菜单中
100  # Other functions
6    # Settings
1    # Modify various thresholds

# 调整积分精度、SCF收敛标准等
```

---

## 📚 实用技巧

### 1. 快速电荷分析

```bash
# 一键获取多种电荷
7   # Population analysis
18  # Calculate atomic charges by various methods
```

### 2. 轨道相互作用分析

```bash
# 片段轨道相互作用
16  # Orbital interaction analysis
1   # Fragment orbital interaction analysis
```

### 3. 光谱模拟

```bash
# IR光谱模拟
11  # Plot IR spectrum  
1   # IR spectrum

# UV-Vis光谱模拟  
11  # Plot UV-Vis spectrum
2   # UV-Vis spectrum
```

### 4. 反应路径分析

```bash
# IRC路径分析
100 # Other functions
7   # Study chemical reactivity
```

---

## 📖 学习资源

- [Multiwfn手册](../06-Multiwfn/Multiwfn_Manual_2.3.2.pdf)
- [sobereva博客](http://sobereva.com/multiwfn)
- [Multiwfn官方网站](http://sobereva.com/multiwfn)
- [量子化学波函数分析教程](http://sobereva.com/wavefunction)

---

## 🆘 技术支持

遇到问题？寻求帮助：

1. **📖 查阅Multiwfn详细手册**
2. **💬 访问sobereva量子化学论坛**  
3. **📧 发邮件至Multiwfn开发者**
4. **🔍 搜索相关教程和案例**

---

*📝 最后更新：2025年7月2日 | 📧 技术支持：528实验室*
