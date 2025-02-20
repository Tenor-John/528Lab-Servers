# VASP Template
## English template
```bash
SYSTEM = XX                 

#Startparameter for this Run:
 NWRITE     = 1 
 LPETIM     = F    !write-flag &amp; time
 ISTART     = 0    ! job   : 0-new  1-cont  2-samecu
 LWAVE      = F
 LCHARG     = F 

#LAECHG     = T
#ISPIN      = 2
#ICHARG     = 11
#SYMPREC    = 0.0001
#LELF       = F 

 LPLANE     = .TRUE.
 NCORE      = 6 
 LSCALU     = .FALSE.
 NSIM       = 4

#LHFCALC    = .TRUE. 
#HFSCREEN   = 0.2
#NBANDS     = 18 
#ALGO       = All
#TIME       = 0.4
#PRECFOCK   = N     ! used PRECFOCK = Normal for high quality calculations
#NKRED      = 2     ! omit flag for high quality calculations
#LASPH      = T

#Electric Field parameters:    
#EFIELD     = 0.05                  
#LDIPOL     = .TRUE.               
#IDIPOL     = 3   

#GGA        = OR
#LUSE_VDW   = .TRUE.
#AGGAC      = 0.0000
#IVDW       = 11

#LDAU       = T
#LDAUU      = 0     0
#LDAUJ      = 0     0

#ISYM       = 0
#LSORBIT    = .TRUE.
#ICHARG     = 11         ! non selfconsistent run, read CHGCAR
#LMAXMIX    = 6          ! for d elements increase LMAXMIX to 4, f: 

                         ! you need to set LMAXMIX already in the collinear calculation

#SAXIS      =  1  1  1   ! direction of the magnetic field
#MAGMOM     = 54*0
#NBANDS     = 54 
#GGA_COMPAT = .FALSE.

#Electronic Relaxation 1:
  NELM       = 2000
  NELMIN     = 5
#NELMDL     = -10
  EDIFFG     = -0.01
  EDIFF      = 1E-5
  PREC       =  A 
#NBANDS     = 70 
  ISIF       = 2     !   2-only position, 3-position and lattice

#Ionic Relaxation：
  NSW        = 200   !    for static cal/.
  NBLOCK     = 1     !    inner block
  KBLOCK     = 5     !    outer block 
  IBRION     = 2     !    ionic relax: 0-MD 1-quasi-New 2-CG
  POTIM      = 0.5
  LCORR      = T     ! Harris-correction to forces
  ENCUT      = 500 

#DOS related values:
#ENAUG      = 400.0
 ISMEAR     = 0 
 SIGMA      = 0.2
#EMIN       = -15
#EMAX       = 5
#LORBIT     = 11
#NEDOS      = 3000

#Electronic Relaxation 2:
  ALGO       = N     ! Normal     algorithm
  LDIAG      = T     !  sub-space diagonalisation
  LREAL      = A 
#ROPT       = -2E-4 -2E-4
#AMIX       = 0.02
#BMIX       = 0.0001 
#AMIX_MAG   = 0.8
#BMIX_MAG   = 0.0001
#MAXMIX     = 40
#NGX        = 20 
#NGY        = 20 
#NGZ        = 18
```


## 中文模板
```bash
SYSTEM = XX  ! 系统名称，用于区分计算任务
#Startparameter for this Run:
 NWRITE = 1 ! 输出文件详细程度，1为标准输出，2为详细输出
 LPETIM = F ! 是否记录计算时间，FALSE表示不记录
 ISTART = 0 ! 任务类型：0-新任务，1-继续任务，2-相同任务
 LWAVE = F  ! 是否保存WAVECAR文件，FALSE表示不保存
 LCHARG = F ! 是否保存CHGCAR文件，FALSE表示不保存
#LAECHG = T ! 是否保存AE电荷密度，TRUE表示保存
#ISPIN = 2  ! 自旋极化计算：1-无自旋极化，2-自旋极化
#ICHARG = 11 ! 非自洽计算，读取CHGCAR文件
#SYMPREC = 0.0001 ! 对称性检测精度
#LELF = F    ! 是否计算ELF（电子局域化函数）

 LPLANE = .TRUE. ! 平面波并行化，TRUE表示启用
 NCORE = 6  ! 每个能带使用的核心数，推荐设置为系统核心数的平方根
 LSCALU = .FALSE. ! 是否使用Scalapack库，FALSE表示禁用
 NSIM = 4   ! 同时处理的能带数，推荐设置为4-8

#LHFCALC = .TRUE. ! 是否启用混合泛函计算
#HFSCREEN = 0.2  ! 混合泛函的屏蔽参数
#NBANDS = 18      ! 能带数
#ALGO = All       ! 算法：All表示全自洽
#TIME = 0.4       ! 每个离子的时间限制
#PRECFOCK = N     ! Fock交换精度：N表示正常
#NKRED = 2        ! 降低k点采样密度的因子
#LASPH = T        ! 是否启用非球面校正

#Electric Field parameters:
#EFIELD = 0.05    ! 外加电场强度
#LDIPOL = .TRUE.  ! 是否启用偶极校正
#IDIPOL = 3       ! 偶极校正方向

#GGA = OR         ! 泛函类型：OR表示OptPBE-vdW
#LUSE_VDW = .TRUE. ! 是否启用vdW校正

#AGGAC = 0.0000   ! vdW校正参数
#IVDW = 11        ! vdW校正方法：11表示DFT-D3

#LDAU = T        ! 是否启用LDA+U
#LDAUU = 0 0     ! U值
#LDAUJ = 0 0     ! J值

#ISYM = 0        ! 对称性操作：0-禁用，2-启用
#LSORBIT = .TRUE. ! 是否启用自旋轨道耦合
#ICHARG = 11     ! 非自洽计算，读取CHGCAR文件
#LMAXMIX = 6     ! 最大混合角动量，6适用于f元素
#SAXIS = 1 1 1   ! 磁场方向
#MAGMOM = 54*0   ! 初始磁矩设定
#NBANDS = 54     ! 能带数
#GGA_COMPAT = .FALSE. ! 是否兼容旧版GGA

#Electronic Relaxation 1:
  NELM = 2000     ! 最大电子自洽步数
  NELMIN = 5      ! 最小电子自洽步数
#NELMDL = -10    ! 初始步数，负值表示跳过
 EDIFFG = -0.01  ! 离子步收敛标准，负值表示力单位（eV/Å）
 EDIFF = 1E-5    ! 电子步收敛标准（eV）
 PREC = A        ! 计算精度：A表示高精度
#NBANDS = 70     ! 能带数
 ISIF = 2        ! 优化类型：2-仅优化离子位置，3-优化离子和晶格

#Ionic Relaxation：
  NSW = 200       ! 最大离子步数，0表示静态计算
  NBLOCK = 1      ! 内部块大小
  KBLOCK = 5      ! 外部块大小
  IBRION = 2      ! 离子优化算法：0-MD，1-准牛顿，2-共轭梯度
  POTIM = 0.5     ! 离子步长
  LCORR = T       ! 是否启用Harris修正力
  ENCUT = 500     ! 截断能（eV）

#DOS related values:
#ENAUG = 400.0   ! 增强电荷密度截断能
 ISMEAR = 0      ! smearing方法：0-Gaussian，-5-Tetrahedron
 SIGMA = 0.2     ! smearing宽度（eV）
#EMIN = -15      ! DOS能量范围下限
#EMAX = 5        ! DOS能量范围上限
#LORBIT = 11     ! 局域轨道输出：11表示详细输出
#NEDOS = 3000    ! DOS点数

#Electronic Relaxation 2:
  ALGO = N        ! 算法：N表示Normal
  LDIAG = T       ! 是否启用子空间对角化
  LREAL = A       ! 投影算子：A表示自动选择
#ROPT = -2E-4 -2E-4 ! 投影算子参数
#AMIX = 0.02     ! 电荷混合参数
#BMIX = 0.0001   ! 电荷混合参数
#AMIX_MAG = 0.8  ! 磁性混合参数
#BMIX_MAG = 0.0001 ! 磁性混合参数
#MAXMIX = 40     ! 最大混合步数
#NGX = 20        ! FFT网格X方向大小
#NGY = 20        ! FFT网格Y方向大小
#NGZ = 18        ! FFT网格Z方向大小
```

## 单点能、结构优化、晶体结构优化的区别
|参数|分子结构优化|晶体结构优化|单点能计算|
|----|----|----|----|
|ENCUT|550.0 eV (ENMAX * 1.3)|550.0 eV (ENMAX * 1.3)|550.0 eV (ENMAX * 1.3)|
|ISMEAR|0 (Gaussian smearing)|0 (Gaussian smearing)|0 (Gaussian smearing)|
|SIGMA|0.1 eV (展宽宽度)|0.1 eV (展宽宽度)|0.1 eV (展宽宽度)|
|NSW|50 (最大离子步数)|50 (最大离子步数)|0 (无离子步数，单点能)|
|IBRION|2 (Conjugate-Gradient 算法)|2 (Conjugate-Gradient 算法)|-1 (无几何优化)|
|ISIF|2 (固定晶格，仅优化离子位置)|3 (优化离子位置和晶格)|2 (不适用，无几何优化)|
|EDIFFG|-0.02 eV/Å (力收敛标准)|-0.02 eV/Å (力收敛标准)|N/A (无几何优化)|
|EDIFF|1E-6 (电子自洽场收敛标准)|1E-6 (电子自洽场收敛标准)|1E-8 (更严格的电子收敛标准)|
|LREAL|.FALSE. (投影在倒空间)|Auto (根据系统大小选择投影方式)|.FALSE. (投影在倒空间)|
|PREC|Accurate (高精度)|Accurate (高精度)|Accurate (高精度)|
|ADDGRID|.TRUE. (提高计算精度)|.TRUE. (提高计算精度)|.TRUE. (提高计算精度)|
|LORBIT|11 (输出局域轨道信息)|11 (输出局域轨道信息)|11 (输出局域轨道信息)|
|IVDW|11 (DFT-D3 色散校正，适用于分子)|11 (DFT-D3 色散校正，适用于分子/晶体)|11 (DFT-D3 色散校正，适用于分子/晶体)|

### **主要区别总结**

#### NSW：

分子和晶体优化设置为 50（进行几何优化）。

单点能计算设置为 0（不进行几何优化）。

#### IBRION：

分子和晶体优化设置为 2（使用 Conjugate-Gradient 算法优化）。

单点能计算设置为 -1（无几何优化）。

#### ISIF：

分子优化设置为 2（固定晶格，仅优化离子位置）。

晶体优化设置为 3（优化离子位置和晶格）。

单点能计算设置为 2（不适用，无几何优化）。

#### EDIFFG：

分子和晶体优化设置为 -0.02 eV/Å（力收敛标准）。

单点能计算无此项（无几何优化）。

#### EDIFF：

单点能计算设置为 1E-8（更严格的电子收敛标准），而分子和晶体优化设置为 1E-6。

#### LREAL：

晶体优化设置为 Auto（根据系统大小自动选择投影方式），而分子和单点能计算设置为 .FALSE.（投影在倒空间）。