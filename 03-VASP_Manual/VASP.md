# VASP输入参数指南

## 基本输入

### ❗INCAR文件注意事项

- 写INCAR时，不要使用tab，用空格替换tab
- 官网有些旧的文件可能用的不是`#`号，而是`!`。记住: `!`可能会出错
- "分子原子体系"指的是"把分子或者原子放到一个box里面"

### 基本参数

```
SYSTEM = O atom       # 该计算的说明，任意写，没有也没有影响
```

#### ISMEAR
```
ISMEAR = 0            
```
- 展宽方法，一般ISMEAR = 0 (Gaussian Smearing) 可以满足大部分的体系（金属，导体，半导体，分子）
- 对于分子或者原子，用0
- 对于金属来说，ISMEAR的取值一般为0或1
- 半导体和绝缘体体系不大于0，一般用0
- K 点少，半导体或者绝缘体，那么只能用 ISMEAR = 0
- 对所有体系，如果想获取更加精确能量的时候用-5(如DOS计算)：但使用-5的时候，K点数目小于3则程序会罢工

#### SIGMA
```
SIGMA = 0.01          
```
- 对于分子原子体系，使用 ISMEAR = 0; SIGMA = 0.01
- 对于金属(ISMEAR=1或0)，非金属(ISMEAR=0)，一般取SIGMA=0.10即可，默认值是0.20，不放心的话，用0.05
- 如果用了ISMEAR = -5，SIGMA的值可以忽略
- 判断标准： SIGMA的取值要保证OUTCAR 中的 entropy T*S (展宽entropy而非物化entropy)这一项，平均到每个原子上，要小于 1-2 meV

### 一般附加参数

#### ISTART
```
ISTART = 0   # Default: ISTART = 1 read WAVECAR if a WAVECAR file exists,  = 0 else
```
- 1: 用于收敛测试和所有涉及体积/晶胞形状变化的作业
- 2: 继续作业，"以恒定基组重新启动"。从WAVECAR文件读取轨道

#### ICHARG
```
ICHARG = 2  # Default: ICHARG = 2 if ISTART=0, = 0 else
```
- 0: 从初始波函数计算电荷密度
- 1: 从CHGCAR文件读取电荷密度
- 11: 从CHGCAR读取给定电荷密度以获得特征值（用于能带结构图）或DOS
- 2: 取原子电荷密度的叠加

#### ALGO 和 IALGO
```
ALGO = FAST   # 指定电子最小化算法
IALGO = 38   #
```
- 默认: 8 for VASP.4.4 and older, = 38 else (if ALGO is not set)
- IALGO=5 最陡下降法
- IALGO=6 共轭梯度法
- IALGO=7 预处理最陡下降法
- IALGO=8 预处理共轭梯度法
- IALGO=38: 块Davidson算法 (ALGO=N)

#### 其他常用参数
```
LWAVE =  .TRUE.   # 默认 LWAVE = .TRUE. ; 决定是否在运行结束时将波函数写入WAVECAR文件
LCHARG = .TRUE.   # 默认: .TRUE. 
LVTOT = .FALSE.   # 默认: .FALSE.
```

### 其他附加参数

#### LREAL
```
LREAL = Auto 
```
- LREAL决定投影算符是在实空间还是在倒易空间中求值
- LREAL=.FALSE.    在倒易空间中进行投影
- LREAL=.TRUE.     在实空间中进行投影（旧的，被LREAL=O取代）
- LREAL=On 或 O    在实空间中进行投影，投影算符被重新优化
- LREAL=Auto 或 A  在实空间中进行投影，投影算符完全自动优化（无需用户干预）
- 注意：不能将LREAL=.FALSE.和LREAL=ON/.TRUE.计算的结果进行能量比较

#### ISIF
```
ISIF =    
```
- 决定是否计算应力张量以及在弛豫和分子动力学运行中允许改变哪些主要自由度
- 默认: =0 for IBRION=0 (分子动力学), = 2 else
- 3: 计算力和应力张量；允许改变位置、晶胞形状和体积的自由度
- 2: 计算力和应力张量；允许改变位置的自由度，但不允许改变晶胞形状和体积的自由度

#### GGA
```
GGA = PE 
```
- 指定希望使用的广义梯度近似类型
- 默认: GGA = 与POTCAR文件一致的交换关联类型
- PE: Perdew-Burke-Ernzerhof

#### NELM
```
NELM = 100 
```
- 默认: 60
- 设置可能执行的最大电子自洽(SC)步数

#### ADDGRID
```
ADDGRID=.TRUE. 
```
- 默认: .FALSE. 
- 决定是否使用附加支持网格来评估增强电荷

## 结构优化

### IBRION
IBRION决定如何更新和移动离子。
- 默认 = -1 (不更新) for NSW = -1 or 0; = 0 else
一般来说，优化结构时有3个选择：
- IBRION=3：初始结构很差的时候
- IBRION=2：共轭梯度算法，很可靠的选择，一般来说用它基本没什么问题
- IBRION=1：用于小范围内稳定结构的搜索

### NSW
NSW 控制几何结构优化的步数，即VASP进行多少离子步。
- 必须是大于等于0的整数
- 一般来说，简单的体系200步内就可以正常结束
- 如果不知道什么时候收敛，初始结构很差，或者设置了很严格的收敛标准，那么需要增大NSW的取值，比如NSW=500或者更大

### POTIM
```
POTIM = 0.05
```
- 设置时间步长（MD）或步长宽度缩放（离子弛豫）
- POTIM = none，如果IBRION= 0 (MD)必须设置; = 0.5 if IBRION= 1,2,3 (离子弛豫) and 5 (up to VASP.4.6); = 0.015 for IBRION=5 (up from VASP.5.1)
- 一般0.1就很不错

### 示例
```
IBRION = 2
NSW = 500
POTIM = 0.05   
ISIF= 3   # 2 default
```

### 结构优化完算单点时要修改的地方：
```
NSW    = 0    #  优化离子步上限
ISIF   = 2    #  2:不优化晶胞
IBRION = -1   # -1:不优化离子步
```

## 精度控制
```
ENCUT = 400   # 截断能
EDIFF = 1E-6   # 电子步收敛精度, 1E-6 default is enough
EDIFFG = -0.01   # 离子弛豫精度,-0.01已经很严格，除非特殊需要，不要设置-0.001；若很多步仍不收敛可尝试-0.02.
NGX =  47
NGY =  47
NGZ =  146
```
NGX设置FFT网格中沿第一个晶格矢量的网格点数。默认NGX = 根据PREC和ENCUT设置。

## slab模型
- 真空层的厚度要适中，太小肯定不行，太大也不合适
- 真空层太厚意味着模型尺寸变大，从而导致计算变慢；太小则无法消除周期性的影响
- 一般来说，对于表面反应的计算，15A的真空层厚度足够了
- 但是，对于功函数这一类对真空层敏感的计算来说，我们需要注意
- slab模型一般需要添加偶极矫正：
```
LDIPOL = .TRUE.
IDIPOL = 3    # (3指的是在z方向上)这两个参数来消除上下不对称的slab表面导致的偶极矩影响
```

## 频率计算
```
IBRION=5  # 告诉vasp要进行频率计算
NFREE = 2   # 原子在某一方向上正反两个方向移动. do not use NFREE = 1.
PREC = NORMAL    # specifies the "precision"-mode. default: Normal for VASP.5.X
```

## 磁性
```
ISPIN = 2
MAGMOM = 5*2
```

## 加U
```
LDAU  =  .TRUE
LDAUTYPE  =  2
LDAUU  = 0  0  5    9    0
LDAUJ  = 0  0  0.64 1.5  0
LDAUPRINT  = 0
```
LMAXMIX（默认 = 2）:
- "LMAXMIX" 控制通过电荷密度混合器传递并写入CHGCAR文件的一中心PAW电荷密度的最大l-量子数
- L(S)DA+U计算在许多情况下需要将LMAXMIX增加到4（d电子）或6（f元素），以便快速收敛到基态

## 并行参数
```
NCORE = 12   # 一般为节点核数的一半
LPLANE=.TRUE.
NPAR=2   # NPAR flag should be equal to the number of core.
LSCALU=.FALSE.   # switches on the parallel LU decomposition (using scaLAPACK) in the orthonormalization of the wave functions.
NSIM=4   # sets the number of bands that are optimized simultaneously by the RMM-DIIS algorithm.
```

## 能带计算
```
LORBIT = 11
```
- "LORBIT" 与适当的RWIGS一起，决定是否写入PROCAR或PROOUT文件
- 11: RWIGS标签被忽略；文件被写入（DOSCAR和lm分解的PROCAR）
- LORBIT >= 11 且 ISYM = 2 时，部分电荷密度没有正确对称化，可能导致对称等效的部分电荷密度具有不同的电荷
- 对轨道选取的影响：
  - LORBIT=10: 将态密度分解到每个原子以及原子的spd轨道上，称为局域态密度（Local DOS，LDOS）。点击dxy时，其他的d轨道(dyz,dxz,dz2,dx2)也会同时被选中
  - LORBIT=11: 在10的基础上，还进一步分解到px，py，pz等轨道上，称为投影态密度（Projected DOS）或分波态密度（Partial DOS），即PDOS。点击dxy时，则仅仅选择dxy，其他的d轨道不会选中

## 其他说明

### K点网格奇偶的选择
- 对于以Gamma点为中心的网格，偶数网格有时比奇数网格具有更好的收敛性。这是因为它们避开了Gamma点本身，Gamma点是一个非常高对称的点，不是一个好的代表性采样点
- 然而，对于具有六角对称性的系统，你基本上永远不应该使用偶数网格（以Gamma为中心），因为应用于偶数网格的六角对称操作会生成布里渊区外的点
- 更多详情可参考Chadi和Cohen的论文