# 🧪 ORCA 量子化学计算软件使用手册

<div style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">

📖 **ORCA 简介**  
ORCA是一款功能强大的ab initio量子化学软件包，特别擅长处理开壳层分子、过渡金属配合物和激发态计算。

**🎯 适用计算类型：**
- 单点能计算 (DFT, HF, Post-HF)
- 几何结构优化
- 频率分析与热力学校正
- 激发态计算 (TD-DFT, CIS, CASSCF)
- 耦合簇方法 (CCSD, CCSD(T))
- 多参考方法 (CASSCF, MRCI)

</div>

---

## 📋 目录

- [环境配置](#环境配置)
- [基础输入文件](#基础输入文件)
- [常用计算类型](#常用计算类型)
- [作业提交](#作业提交)
- [结果分析](#结果分析)
- [常见问题](#常见问题)

---

## 🔧 环境配置

### 模块加载

```bash
# 加载ORCA模块
module load orca/5.0.3

# 查看ORCA版本
orca --version

# 设置环境变量
export RSH_COMMAND="/usr/bin/ssh"
export ORCA_2_AIM=/opt/orca/orca_2_aim
```

### 检查安装

```bash
# 检查ORCA可执行文件
which orca

# 查看可用方法
orca --help
```

---

## 📝 基础输入文件

### 输入文件结构

ORCA输入文件通常包含以下部分：

```
# 注释行
! 方法 基组 关键字
%pal nprocs 8 end          # 并行设置
%mem 1000                  # 内存设置 (MB)

* xyz 0 1                  # 分子坐标
原子1  x1  y1  z1
原子2  x2  y2  z2
...
*
```

### 基本单点计算示例

```bash
# water_sp.inp - 水分子单点计算
! B3LYP def2-TZVP

%pal nprocs 8 end
%mem 2000

* xyz 0 1
O    0.0000    0.0000    0.0000
H    0.0000    0.7572    0.5865
H    0.0000   -0.7572    0.5865
*
```

---

## 🧮 常用计算类型

### 1. 几何结构优化

```bash
# geometry_optimization.inp
! B3LYP def2-TZVP OPT

%pal nprocs 8 end
%mem 2000

%geom
 MaxIter 200
 TolE 1e-6
 TolRMSG 3e-4
 TolMaxG 4.5e-4
end

* xyz 0 1
# 分子坐标
*
```

### 2. 频率计算

```bash
# frequency.inp
! B3LYP def2-TZVP FREQ

%pal nprocs 8 end
%mem 4000

* xyz 0 1
# 优化后的分子坐标
*
```

### 3. 激发态计算

```bash
# excited_state.inp
! B3LYP def2-TZVP TDDFT

%pal nprocs 16 end
%mem 8000

%tddft
 nroots 10           # 计算前10个激发态
 maxdim 5           # 最大维数
end

* xyz 0 1
# 分子坐标
*
```

### 4. 耦合簇计算

```bash
# ccsd_t.inp
! CCSD(T) def2-TZVP def2-TZVP/C

%pal nprocs 16 end
%mem 16000

%mdci
 MaxIter 100
 ETol 1e-8
end

* xyz 0 1
# 分子坐标
*
```

---

## 🚀 作业提交

### Slurm作业脚本

```bash
#!/bin/bash
#SBATCH -J orca-job
#SBATCH -o orca-%j.out
#SBATCH -e orca-%j.err
#SBATCH --partition=DFT
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00

# 加载ORCA模块
module load orca/5.0.3

# 设置环境变量
export RSH_COMMAND="/usr/bin/ssh"

# 运行ORCA计算
echo "开始ORCA计算: $(date)"
echo "工作目录: $PWD"
echo "输入文件: $1"

# 运行计算
$ORCA_PATH/orca $1 > ${1%.inp}.out

echo "计算完成: $(date)"
```

### 提交作业

```bash
# 提交作业
sbatch orca_job.sh input.inp

# 查看队列
squeue -u username

# 监控输出
tail -f input.out
```

---

## 📊 结果分析

### 输出文件说明

| 文件类型 | 扩展名 | 说明 |
|---------|--------|------|
| **主输出文件** | `.out` | 包含所有计算结果和分析 |
| **轨道文件** | `.gbw` | 分子轨道波函数 |
| **密度文件** | `.scfp` | 电子密度 |
| **几何文件** | `.xyz` | 优化后的几何结构 |
| **Hessian文件** | `.hess` | 二阶导数矩阵 |
| **轨道图形** | `.molden` | 用于可视化的轨道文件 |

### 能量提取

```bash
# 提取SCF能量
grep "FINAL SINGLE POINT ENERGY" *.out

# 提取相对论校正
grep "Relativistic correction" *.out

# 提取零点能
grep "Zero point energy" *.out

# 提取热力学数据
grep -A 10 "THERMOCHEMISTRY" *.out
```

### 几何结构分析

```bash
# 提取优化后坐标
grep -A 100 "CARTESIAN COORDINATES (ANGSTROEM)" *.out | tail -n +3

# 提取键长
grep "Bond distances" *.out

# 提取键角
grep "Bond angles" *.out
```

### 频率分析

```bash
# 提取振动频率
grep "VIBRATIONAL FREQUENCIES" *.out

# 检查虚频
grep "***imaginary mode***" *.out

# 提取红外强度
grep -A 50 "IR SPECTRUM" *.out
```

---

## 🛠️ 常见问题与解决

### 内存问题

```bash
# 症状：内存不足错误
# 解决：增加内存设置
%mem 8000               # 增加到8GB

# 或在作业脚本中增加内存申请
#SBATCH --mem=32G
```

### 收敛问题

```bash
# SCF不收敛
%scf
 MaxIter 500            # 增加最大迭代次数
 ConvForced true        # 强制收敛
end

# 或者使用更稳定的算法
! SlowConv              # 使用慢收敛选项
```

### 并行计算问题

```bash
# 设置合适的核数
%pal nprocs 16 end      # 不要超过节点总核数

# 对于大体系，可以使用混合并行
%pal
 nprocs 32
 useomp 1
end
```

---

## 📚 高级功能

### 1. 自定义基组

```bash
# 使用自定义基组
%basis
 newgto O "def2-QZVP" end
 newgto H "def2-TZVP" end
end
```

### 2. 溶剂化模型

```bash
# CPCM溶剂化
! CPCM(Water)           # 水溶液

# SMD溶剂化
! SMD                   # 更精确的溶剂化模型
%cpcm
 smd true
 SMDsolvent "water"
end
```

### 3. 色散校正

```bash
# D3色散校正
! D3BJ                  # Becke-Johnson阻尼

# D4色散校正
! D4                    # 最新的D4方法
```

---

## 📖 参考资料

- [ORCA官方手册](https://www.faccts.de/docs/orca/5.0/manual/)
- [ORCA输入库](https://sites.google.com/site/orcainputlibrary/)
- [量子化学计算方法](../0000-计算化学必读书目/)

---

## 🆘 技术支持

遇到问题？寻求帮助：

1. **📖 查阅ORCA官方文档**
2. **💬 咨询有经验的同学**
3. **📧 联系计算化学专家**
4. **🔍 搜索ORCA用户论坛**

---

*📝 最后更新：2025年7月2日 | 📧 技术支持：528实验室*
