# ABACUS 输入文件设置完整指南

## 1. 概述

ABACUS（Atomic-orbital Based Ab-initio Computation at UStc）是一个开源的第一性原理计算软件包，支持平面波（PW）和局域原子轨道（LCAO）基组。本文档详细介绍ABACUS的输入文件设置方法。

### 1.1 基本文件结构

ABACUS计算需要以下主要输入文件：

* **INPUT** : 计算参数设置文件
* **STRU** : 原子结构文件
* **KPT** : k点设置文件（可选）
* **赝势文件** (*.upf): 原子赝势
* **轨道文件** (*.orb): LCAO基组文件（LCAO计算必需）

## 2. INPUT文件详细说明

### 2.1 文件格式

INPUT文件以 `INPUT_PARAMETERS`开头，每行一个参数：

```
INPUT_PARAMETERS
parameter_name    parameter_value    # 注释（可选）
```

### 2.2 核心参数分类

#### 2.2.1 系统基本设置

| 参数             | 类型   | 默认值   | 说明           |
| ---------------- | ------ | -------- | -------------- |
| `suffix`       | string | "ABACUS" | 计算任务后缀名 |
| `ntype`        | int    | 1        | 原子种类数目   |
| `calculation`  | string | "scf"    | 计算类型       |
| `esolver_type` | string | "ksdft"  | 求解器类型     |

**calculation 可选值：**

* `scf`: 自洽场计算
* `nscf`: 非自洽场计算
* `relax`: 离子弛豫
* `cell-relax`: 晶胞弛豫
* `md`: 分子动力学
* `get_wf`: 获取波函数

#### 2.2.2 基组和赝势设置

| 参数            | 类型   | 默认值 | 说明                         |
| --------------- | ------ | ------ | ---------------------------- |
| `basis_type`  | string | "pw"   | 基组类型：pw/lcao/lcao_in_pw |
| `ecutwfc`     | float  | 50     | 平面波截断能（Ry）           |
| `pseudo_dir`  | string | "./"   | 赝势文件目录                 |
| `orbital_dir` | string | "./"   | 轨道文件目录                 |
| `ks_solver`   | string | "cg"   | KS方程求解器                 |

**ks_solver 选项：**

* `cg`: 共轭梯度法
* `dav`: Davidson算法
* `genelpa`: 广义本征值求解
* `scalapack_gvx`: ScaLAPACK求解器

#### 2.2.3 SCF收敛控制

| 参数            | 类型   | 默认值    | 说明              |
| --------------- | ------ | --------- | ----------------- |
| `scf_nmax`    | int    | 50        | SCF最大迭代次数   |
| `scf_thr`     | float  | 1e-6      | SCF收敛判据（eV） |
| `mixing_type` | string | "broyden" | 电荷密度混合方法  |
| `mixing_beta` | float  | 0.4       | 混合参数          |
| `mixing_ndim` | int    | 8         | 混合历史维数      |

#### 2.2.4 k点和对称性设置

| 参数           | 类型 | 默认值 | 说明                                      |
| -------------- | ---- | ------ | ----------------------------------------- |
| `gamma_only` | bool | 0      | 是否只计算Gamma点                         |
| `symmetry`   | bool | 1      | 是否使用对称性                            |
| `nspin`      | int  | 1      | 自旋类型：1(无自旋)/2(自旋极化)/4(非共线) |

#### 2.2.5 电子温度和展宽

| 参数                | 类型   | 默认值  | 说明           |
| ------------------- | ------ | ------- | -------------- |
| `smearing_method` | string | "gauss" | 展宽方法       |
| `smearing_sigma`  | float  | 0.01    | 展宽参数（eV） |

**smearing_method 选项：**

* `gauss`: 高斯展宽
* `fd`: 费米-狄拉克分布
* `mp`: Methfessel-Paxton方法
* `mv`: Marzari-Vanderbilt方法

#### 2.2.6 力和应力计算

| 参数           | 类型  | 默认值 | 说明                 |
| -------------- | ----- | ------ | -------------------- |
| `cal_force`  | bool  | 0      | 是否计算原子受力     |
| `cal_stress` | bool  | 0      | 是否计算应力张量     |
| `force_thr`  | float | 1e-3   | 力收敛判据（eV/Å）  |
| `stress_thr` | float | 1e-2   | 应力收敛判据（kBar） |

#### 2.2.7 输出控制

| 参数             | 类型 | 默认值 | 说明               |
| ---------------- | ---- | ------ | ------------------ |
| `out_stru`     | bool | 0      | 是否输出最终结构   |
| `out_chg`      | bool | 0      | 是否输出电荷密度   |
| `out_pot`      | bool | 0      | 是否输出势能       |
| `out_wfc_lcao` | bool | 0      | 是否输出LCAO波函数 |
| `out_band`     | bool | 0      | 是否输出能带       |
| `out_dos`      | bool | 0      | 是否输出态密度     |

### 2.3 INPUT文件示例

#### 2.3.1 基本SCF计算

```
INPUT_PARAMETERS
suffix              H2_scf
calculation         scf
ntype               1
ecutwfc             50
scf_nmax            100
scf_thr             1e-6
basis_type          lcao
ks_solver           genelpa
gamma_only          1
smearing_method     gauss
smearing_sigma      0.01
mixing_type         broyden
mixing_beta         0.4
pseudo_dir          ./
orbital_dir         ./
```

#### 2.3.2 结构优化计算

```
INPUT_PARAMETERS
suffix              H2O_relax
calculation         relax
ntype               2
ecutwfc             60
scf_nmax            100
scf_thr             1e-7
basis_type          lcao
ks_solver           genelpa
cal_force           1
force_thr           1e-3
relax_nmax          50
relax_method        cg
gamma_only          1
smearing_method     gauss
smearing_sigma      0.01
pseudo_dir          ./
orbital_dir         ./
out_stru            1
```

#### 2.3.3 能带计算

```
INPUT_PARAMETERS
suffix              Si_band
calculation         nscf
ntype               1
ecutwfc             50
scf_nmax            100
scf_thr             1e-6
basis_type          lcao
ks_solver           genelpa
nbands              20
smearing_method     gauss
smearing_sigma      0.01
pseudo_dir          ./
orbital_dir         ./
out_band            1
```

## 3. STRU文件详细说明

### 3.1 文件格式

STRU文件定义了系统的原子结构信息，包含以下部分：

```
ATOMIC_SPECIES
element_name  atomic_mass  pseudopotential_file

NUMERICAL_ORBITAL
orbital_file

LATTICE_CONSTANT
lattice_constant_in_bohr

LATTICE_VECTORS
a1x  a1y  a1z
a2x  a2y  a2z  
a3x  a3y  a3z

ATOMIC_POSITIONS
coordinate_type

element_name1
mag_moment
number_of_atoms
x1  y1  z1  [move_x move_y move_z] [mag mx my mz] [velocity vx vy vz]
x2  y2  z2  [...]
...

element_name2
mag_moment  
number_of_atoms
...
```

### 3.2 各部分详细说明

#### 3.2.1 ATOMIC_SPECIES

定义系统中的元素种类：

* `element_name`: 元素符号
* `atomic_mass`: 原子质量（a.u.）
* `pseudopotential_file`: 赝势文件名

#### 3.2.2 NUMERICAL_ORBITAL

指定LCAO计算使用的轨道文件：

```
NUMERICAL_ORBITAL
H_gga_6au_100Ry_2s1p.orb
O_gga_7au_100Ry_2s2p1d.orb
```

#### 3.2.3 LATTICE_CONSTANT

晶格常数，单位为玻尔半径（bohr）。

#### 3.2.4 LATTICE_VECTORS

三个晶格向量，单位为LATTICE_CONSTANT。

#### 3.2.5 ATOMIC_POSITIONS

原子坐标，支持多种坐标类型：

* `Direct`: 直接坐标（分数坐标）
* `Cartesian`: 笛卡尔坐标（Å）
* `Cartesian_angstrom`: 笛卡尔坐标（Å）

可选参数：

* `move_x move_y move_z`: 弛豫时的移动控制（0=固定，1=自由）
* `mag mx my mz`: 磁矩设置
* `velocity vx vy vz`: 分子动力学初始速度

### 3.3 STRU文件示例

#### 3.3.1 H2分子

```
ATOMIC_SPECIES
H  1.008  H_ONCV_PBE-1.0.upf

NUMERICAL_ORBITAL
H_gga_6au_100Ry_2s1p.orb

LATTICE_CONSTANT
1.8897261258369282

LATTICE_VECTORS
10.0  0.0  0.0
0.0   10.0  0.0
0.0   0.0   10.74

ATOMIC_POSITIONS
Direct

H
0.0
2
0.5  0.5  0.465549  1  1  1
0.5  0.5  0.534451  1  1  1
```

#### 3.3.2 水分子

```
ATOMIC_SPECIES
O  15.9994  O_ONCV_PBE-1.0.upf
H  1.008   H_ONCV_PBE-1.0.upf

NUMERICAL_ORBITAL
O_gga_7au_100Ry_2s2p1d.orb
H_gga_6au_100Ry_2s1p.orb

LATTICE_CONSTANT
1.8897261258369282

LATTICE_VECTORS
12.0  0.0  0.0
0.0   12.0  0.0
0.0   0.0   12.0

ATOMIC_POSITIONS
Cartesian_angstrom

O
0.0
1
0.0  0.0  0.0  1  1  1

H
0.0
2
0.0  0.757  0.587  1  1  1
0.0  -0.757  0.587  1  1  1
```

#### 3.3.3 晶体硅

```
ATOMIC_SPECIES
Si  28.086  Si_ONCV_PBE-1.0.upf

NUMERICAL_ORBITAL
Si_gga_8au_60Ry_2s2p1d.orb

LATTICE_CONSTANT
1.8897261258369282

LATTICE_VECTORS
0.0   2.7  2.7
2.7   0.0  2.7
2.7   2.7  0.0

ATOMIC_POSITIONS
Direct

Si
0.0
2
0.0  0.0  0.0  1  1  1
0.25 0.25 0.25 1  1  1
```

## 4. KPT文件说明

### 4.1 文件格式

KPT文件用于指定k点网格，格式如下：

```
K_POINTS
total_number_of_kpoints
kpoint_mode
[k-point specifications]
```

### 4.2 k点模式

#### 4.2.1 Gamma点计算

```
K_POINTS
0
Gamma
1 1 1 0 0 0
```

#### 4.2.2 Monkhorst-Pack网格

```
K_POINTS
0
Monkhorst-Pack
4 4 4 0 0 0
```

#### 4.2.3 直接指定k点

```
K_POINTS
4
Direct
0.0  0.0  0.0  0.25
0.5  0.0  0.0  0.25  
0.0  0.5  0.0  0.25
0.5  0.5  0.0  0.25
```

#### 4.2.4 能带计算路径

```
K_POINTS
100
Line
0.0  0.0  0.0  50   # Gamma
0.5  0.0  0.0  50   # X
```

## 5. 常见计算设置

### 5.1 单分子计算

适用于气相分子、纳米团簇等：

```
# INPUT设置要点
gamma_only      1        # 只计算Gamma点
ecutwfc         50-80    # 适中的截断能
smearing_sigma  0.01     # 小的展宽参数
cal_force       1        # 计算力用于几何优化

# STRU设置要点  
- 使用足够大的超胞（真空层>5Å）
- Cartesian_angstrom坐标便于设置
```

### 5.2 周期性晶体计算

适用于块材、表面、二维材料等：

```
# INPUT设置要点
gamma_only      0        # 使用k点网格
ecutwfc         60-100   # 较高的截断能
smearing_method gauss    # 合适的展宽方法
symmetry        1        # 利用对称性加速

# KPT设置要点
- 根据晶胞大小选择合适的k点密度
- 金属系统需要足够密的k点网格
- 半导体/绝缘体可以用稀疏网格
```

### 5.3 表面和界面计算

```
# INPUT设置要点
gamma_only      0
ecutwfc         80-120   # 更高截断能
cal_stress      0        # 通常不计算应力
nspin           2        # 可能需要自旋极化

# STRU设置要点
- 构建合适的平板模型（15-20Å真空层）
- 固定底层原子（move_x move_y move_z设为0）
```

## 6. 参数调优建议

### 6.1 收敛性测试

#### 截断能收敛测试

```bash
for ecut in 30 40 50 60 70 80; do
    sed "s/ecutwfc.*/ecutwfc $ecut/" INPUT.template > INPUT
    # 运行计算并记录能量
done
```

#### k点收敛测试

```bash
for k in "2 2 2" "4 4 4" "6 6 6" "8 8 8"; do
    echo -e "K_POINTS\n0\nMonkhorst-Pack\n$k 0 0 0" > KPT
    # 运行计算并记录能量
done
```

### 6.2 常见参数组合

#### 快速测试

```
ecutwfc         30
scf_nmax        50
scf_thr         1e-4
mixing_beta     0.7
```

#### 高精度计算

```
ecutwfc         80
scf_nmax        200
scf_thr         1e-8
mixing_beta     0.3
mixing_ndim     12
```

#### 困难体系

```
ecutwfc         100
scf_nmax        500
scf_thr         1e-6
mixing_type     pulay
mixing_beta     0.1
mixing_ndim     20
```

## 7. 故障排除

### 7.1 SCF不收敛

**可能原因及解决方案：**

1. **初猜不好**
   * 降低mixing_beta (0.1-0.3)
   * 增加mixing_ndim (10-20)
   * 尝试不同的mixing_type
2. **金属体系**
   * 增加k点密度
   * 使用合适的smearing_method
   * 调整smearing_sigma (0.01-0.1 eV)
3. **磁性体系**
   * 设置nspin=2
   * 在STRU中设置初始磁矩
   * 考虑使用nspin=4（非共线）

### 7.2 力计算异常

**检查项目：**

1. **截断能不足**
   * 增加ecutwfc
   * 进行收敛性测试
2. **k点不足**
   * 增加k点密度
   * 检查k点收敛性
3. **数值精度**
   * 增加scf_thr精度
   * 检查力收敛判据force_thr

### 7.3 计算速度优化

**优化策略：**

1. **并行化**
   * 合理设置MPI进程数
   * 使用OpenMP（设置OMP_NUM_THREADS）
2. **算法选择**
   * LCAO计算：使用genelpa或scalapack_gvx
   * PW计算：使用dav求解器
3. **内存优化**
   * 调整并行策略
   * 使用合适的基组大小

## 8. 高级功能

### 8.1 HSE杂化泛函

```
INPUT_PARAMETERS
dft_functional  hse
exx_hse_alpha   0.25
exx_hse_omega   0.11
exx_dm_threshold 1e-4
exx_mixing_beta  1.0
```

### 8.2 van der Waals修正

```
INPUT_PARAMETERS
vdw_method      d3_bj
vdw_s6          1.0
vdw_s8          0.7875
vdw_a1          0.4289
vdw_a2          4.4407
```

### 8.3 能带展开

```
INPUT_PARAMETERS
cal_band        1
nband           50

# 在KPT中指定路径
K_POINTS
100
Line_Cartesian
0.0  0.0  0.0  50  # Gamma
0.5  0.0  0.0  50  # X
```

### 8.4 态密度计算

```
INPUT_PARAMETERS
cal_dos         1
dos_sigma       0.01
dos_scale       0.01
dos_emin        -20
dos_emax        10
```

## 9. 最佳实践

### 9.1 计算流程建议

1. **结构准备**
   * 使用实验结构或理论预测结构
   * 确保合理的键长和键角
   * 设置足够的真空层或周期性边界
2. **初步测试**
   * 使用较低精度快速测试
   * 检查SCF收敛性
   * 验证结构合理性
3. **收敛性测试**
   * 系统测试ecutwfc和k点收敛性
   * 确定最优计算参数
4. **生产计算**
   * 使用收敛参数进行正式计算
   * 保存所有重要输出文件

### 9.2 文件管理

```bash
# 推荐的目录结构
project/
├── input/          # 输入文件
├── pseudopotentials/  # 赝势文件  
├── orbitals/       # 轨道文件
├── calculations/   # 计算结果
└── analysis/       # 结果分析
```

### 9.3 批量计算脚本示例

```bash
#!/bin/bash
for system in H2 H2O NH3 CH4; do
    mkdir -p ${system}_calculation
    cd ${system}_calculation
  
    # 复制输入文件
    cp ../templates/${system}/* .
  
    # 提交计算任务
    mpirun -np 4 abacus | tee output.log
  
    cd ..
done
```

---

**注意事项：**

1. 本文档基于ABACUS v3.9版本，不同版本间可能存在参数差异
2. 建议始终参考最新的官方文档和release notes
3. 计算参数需要根据具体体系进行优化测试
4. 重要计算建议进行多次独立验证

**相关资源：**

* ABACUS官方网站：http://abacus.ustc.edu.cn/
* GitHub仓库：https://github.com/deepmodeling/abacus-develop
* 社区论坛：https://github.com/deepmodeling/abacus-develop/discussions
