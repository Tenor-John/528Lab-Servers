# 🧬 LAMMPS 分子动力学模拟软件使用手册

<div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">

📖 **LAMMPS 简介**  
LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) 是一款强大的分子动力学模拟软件，适用于从原子到介观尺度的大规模并行模拟。

**🎯 主要应用：**
- 材料科学模拟
- 生物分子动力学
- 表面和界面研究
- 流体力学模拟
- 固体力学分析

</div>

---

## 📋 目录

- [软件安装与配置](#软件安装与配置)
- [基础概念](#基础概念)
- [输入脚本编写](#输入脚本编写)
- [力场设置](#力场设置)
- [常用模拟类型](#常用模拟类型)
- [结果分析](#结果分析)

---

## 🔧 软件安装与配置

### 环境配置

```bash
# 加载LAMMPS模块
module load lammps/29Sep2021

# 检查LAMMPS版本
lmp -help

# 设置环境变量
export LAMMPS_POTENTIALS=/opt/lammps/potentials
```

### 并行运行设置

```bash
# 单节点并行
mpirun -np 16 lmp -in input.lammps

# 多节点并行
mpirun -np 64 lmp -in input.lammps
```

---

## 📚 基础概念

### LAMMPS单位制

| 单位制 | 距离 | 时间 | 能量 | 质量 | 温度 |
|--------|------|------|------|------|------|
| **real** | Å | fs | kcal/mol | g/mol | K |
| **metal** | Å | ps | eV | g/mol | K |
| **si** | m | s | J | kg | K |
| **lj** | σ | τ | ε | m | ε/kB |

### 基本语法规则

```bash
# 注释行
# 这是注释

# 命令格式
command arg1 arg2 arg3 ...

# 变量定义
variable name equal value
variable temp equal 300.0
```

---

## 📝 输入脚本编写

### 脚本基本结构

```bash
# LAMMPS输入脚本模板

# 1. 初始化
units           real
dimension       3
boundary        p p p
atom_style      full

# 2. 创建模拟盒子和原子
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 single 5 5 5

# 3. 力场参数
pair_style      lj/cut 10.0
pair_coeff      1 1 1.0 1.0

# 4. 设置
neighbor        0.3 bin
neigh_modify    delay 5

# 5. 热力学输出
thermo_style    custom step temp pe ke etotal press
thermo          100

# 6. 运行
timestep        1.0
run             10000
```

### 读取数据文件

```bash
# 从数据文件读取结构
read_data       data.lammps

# 或从restart文件读取
read_restart    restart.lammps
```

---

## ⚛️ 力场设置

### 常用力场类型

#### 1. Lennard-Jones势

```bash
# LJ势参数设置
pair_style      lj/cut 12.0
pair_coeff      1 1 0.238 3.405   # ε σ (Ar原子)
pair_coeff      2 2 0.066 2.655   # Ne原子
pair_coeff      1 2 0.126 3.030   # 混合规则
```

#### 2. EAM势 (金属系统)

```bash
# EAM势设置
pair_style      eam/alloy
pair_coeff      * * Cu_u3.eam Cu
```

#### 3. ReaxFF势 (反应性体系)

```bash
# ReaxFF势设置
pair_style      reax/c NULL
pair_coeff      * * ffield.reax C H O N
```

#### 4. 分子力场 (CHARMM, AMBER等)

```bash
# CHARMM力场示例
pair_style      lj/charmm/coul/long 8.0 10.0
bond_style      harmonic
angle_style     harmonic
dihedral_style  charmm
```

---

## 🧪 常用模拟类型

### 1. 分子动力学 (MD)

```bash
# NVE系综 (微正则)
fix             1 all nve

# NVT系综 (正则)
fix             1 all nvt temp 300.0 300.0 100.0

# NPT系综 (等温等压)
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0

# 运行MD
timestep        1.0
run             100000
```

### 2. 能量最小化

```bash
# 最小化设置
minimize        1.0e-4 1.0e-6 1000 10000

# 或者使用CG方法
min_style       cg
minimize        1.0e-4 1.0e-6 1000 10000
```

### 3. 升温退火

```bash
# 线性升温
fix             1 all nvt temp 0.0 300.0 100.0
run             50000

# 保持高温
fix             1 all nvt temp 300.0 300.0 100.0  
run             100000

# 降温
fix             1 all nvt temp 300.0 0.0 100.0
run             50000
```

### 4. 拉伸模拟

```bash
# 定义组
group           left region left_region
group           right region right_region
group           mobile subtract all left

# 固定左端
fix             1 left setforce 0.0 0.0 0.0

# 拉伸右端
fix             2 right move linear 0.001 0.0 0.0

# 控制温度
fix             3 mobile nvt temp 300.0 300.0 100.0

run             100000
```

---

## 📊 输出与数据收集

### 热力学量输出

```bash
# 自定义热力学输出
thermo_style    custom step time temp pe ke etotal press vol density

# 输出频率
thermo          1000

# 输出到文件
fix             thermo_out all print 1000 "${time} ${temp} ${pe}" &
                file thermo.dat screen no
```

### 轨迹输出

```bash
# 全原子轨迹
dump            1 all atom 1000 traj.lammpstrj

# 自定义输出
dump            2 all custom 1000 traj.dump id type x y z vx vy vz

# XYZ格式输出
dump            3 all xyz 1000 traj.xyz
```

### 径向分布函数

```bash
# RDF计算
compute         rdf all rdf 100 1 1 2 2 1 2
fix             4 all ave/time 100 10 1000 c_rdf[*] file rdf.dat mode vector
```

### 均方位移

```bash
# MSD计算
compute         msd all msd
fix             5 all ave/time 1 1 1000 c_msd[4] file msd.dat
```

---

## 🎛️ 高级功能

### 1. 非平衡分子动力学

```bash
# 剪切流动
fix             1 all nvt temp 300.0 300.0 100.0
fix             2 all deform 1 xy erate 0.001 remap v

run             100000
```

### 2. 增强采样

```bash
# 伞形采样
fix             1 all nvt temp 300.0 300.0 100.0
fix             2 all spring couple 1 2 100.0 0.0 5.0

run             100000
```

### 3. 自由能计算

```bash
# 热力学积分
variable        lambda equal ramp(0.0,1.0)
fix             adapt all adapt 1 pair lj/cut epsilon 1 1 v_lambda
```

---

## 🔧 作业提交脚本

### Slurm作业脚本

```bash
#!/bin/bash
#SBATCH -J lammps-job
#SBATCH -o lammps-%j.out
#SBATCH -e lammps-%j.err
#SBATCH --partition=DFT
#SBATCH --nodes=2
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --time=48:00:00

# 加载LAMMPS模块
module load lammps/29Sep2021

# 设置环境变量
export OMP_NUM_THREADS=1

# 运行LAMMPS
echo "开始LAMMPS计算: $(date)"
echo "工作目录: $PWD"
echo "节点信息: $SLURM_NODELIST"

mpirun -np $SLURM_NTASKS lmp -in input.lammps

echo "计算完成: $(date)"
```

---

## 📈 结果分析

### 使用Python分析

```python
import numpy as np
import matplotlib.pyplot as plt

# 读取热力学数据
data = np.loadtxt('thermo.dat')
time = data[:, 0]
temp = data[:, 1] 
energy = data[:, 2]

# 绘制温度随时间变化
plt.figure(figsize=(10, 6))
plt.plot(time, temp)
plt.xlabel('Time (fs)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Time')
plt.savefig('temperature.png', dpi=300)
plt.show()
```

### 使用VMD可视化

```bash
# 载入轨迹文件
vmd -e load_traj.tcl

# load_traj.tcl内容:
# mol new data.lammps  
# mol addfile traj.lammpstrj waitfor all
```

### 轨迹分析工具

```bash
# 使用MDAnalysis
pip install MDAnalysis

# 使用OVITO
ovito traj.lammpstrj
```

---

## 🛠️ 常见问题与解决

### 1. 模拟稳定性问题

```bash
# 问题：能量发散
# 解决：减小时间步长
timestep        0.5

# 增加阻尼
fix             1 all langevin 300.0 300.0 100.0 12345
```

### 2. 力场参数错误

```bash
# 检查力场文件路径
pair_coeff      * * /path/to/potential.eam

# 验证原子类型匹配
pair_coeff      1 1 epsilon sigma  # 确保类型正确
```

### 3. 内存不足

```bash
# 增加内存分配
processors      * * * map xyz

# 减少输出频率
dump            1 all atom 10000 traj.lammpstrj
```

---

## 📚 学习资源

- [LAMMPS官方文档](https://docs.lammps.org/)
- [LAMMPS教程](https://lammpstutorials.github.io/)
- [分子动力学理论基础](../0000-计算化学必读书目/)

---

## 🆘 技术支持

遇到问题？寻求帮助：

1. **📖 查阅LAMMPS官方文档**
2. **💬 访问LAMMPS用户论坛**
3. **📧 联系分子动力学专家**
4. **🔍 搜索相关案例和教程**

---

*📝 最后更新：2025年7月2日 | 📧 技术支持：528实验室*
