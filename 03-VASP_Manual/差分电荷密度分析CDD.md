# 差分电荷密度分析（CDD）

## 一、 什么是电荷密度差分？

电荷密度差分描述了体系中电子密度的重新分布情况，其计算公式为：

**Δρ = ρ(AB) – ρ(A) – ρ(B)**

其中：

*   **ρ(AB)**：复合体系（如异质结/吸附体系）的总电荷密度
*   **ρ(A)和ρ(B)**：孤立组分A和B的电荷密度

**典型应用场景：**

*   单原子催化剂表面吸附
*   异质结界面电荷转移
*   掺杂材料电子结构分析
    
> **引用：** 电荷密度差分能够直观地展示电荷在空间中的转移和重新分布，是研究化学键形成、电荷转移等现象的重要工具。

[电催化计算电荷密度差分的保姆级教程｜从原理到实战](https://www.bilibili.com/video/BV1qg411c7p5)

## 二、计算步骤详解

### 步骤1：结构优化（关键！）

**目标：** 获得所有体系的稳定几何结构

**操作流程：**

1.  **优化复合体系AB**

    *   构建AB模型（如吸附结构、异质结）
    *   **INCAR关键参数：**

        *   `IBRION = 2`：使用准牛顿算法优化
        *   `NSW = 100`：最大离子步数
        *   `EDIFFG = -0.02`：收敛标准（力2 eV/Å）
        *   `ISIF = 2`：优化原子位置
            
            ```
            //Example INCAR for AB system optimization
            IBRION = 2
            NSW = 100
            EDIFFG = -0.02
            ISIF = 2
            ```

2.  **不要优化孤立组分A和B**

    *   保持与AB相同的计算参数（ENCUT、K点等），只做单点能计算

    **注意：** 必须保证体系A和体系B的原子位置与AB完全一致！
    
    ```
    //Important reminder
    Ensure A and B atoms positions are the same as in AB system!
    ```


### 步骤2：静态自洽计算

**目标：** 获取高精度电荷密度文件CHGCAR

**操作流程：**

1.  **对AB、A、B分别进行静态计算**

    *   使用优化后的结构
    *   **INCAR关键参数：**

        *   `ISTART = 1`：读取波函数加速收敛（若从WAVECAR重启）
        *   `ICHARG = 1`
        *   `NSW = 0`：关闭离子弛豫
        *   `LCHARG = .TRUE.`：必须输出CHGCAR
        *   `PREC = Accurate`：高精度模式
        *   `NGXF = 320`
        *   `NGYF = 320`
        *   `NGZF = 320`：确保每个计算中网格密度参数设置一致
        *   网格密度去OUTCAR中搜索NGXF这段字符，有推荐的网格密度
            
            ```
            //Example INCAR for static calculation
            ISTART = 1
            ICHARG = 1
            NSW = 0
            LCHARG = .TRUE.
            PREC = Accurate
            NGXF = 320
            NGYF = 320
            NGZF = 320
            ```

2.  **统一参数设置**

    *   确保所有体系的ENCUT、网格密度、真空层厚度完全一致
    *   建议使用Gamma中心K点生成方式


### 步骤3：电荷密度差分计算

**核心操作：** 使用CHGCAR文件生成差分电荷密度

**操作步骤：**

1.  **文件准备**

    *   将AB、A、B的CHGCAR分别重命名为：

        *   `CHGCAR_AB`
        *   `CHGCAR_A`
        *   `CHGCAR_B`

2.  **执行差分计算**

    *   运行`chgsum.pl`脚本获得`CHGCAR_sum`：

        `Chgsum.pl CHGCAR_A CHGCAR_B`

3.  **执行差分计算**

    *   运行`chgdiff.pl`脚本计算电荷密度差分：

        `Chgdiff.pl CHGCAR_sum CHGCAR_AB`

4.  **输出结果**

    *   生成`CHGDIFF.diff`（差分电荷密度文件）

### 步骤4：可视化分析

**推荐工具：** VESTA（免费开源）

**操作流程：**

1.  用VESTA打开`CHGDIFF.diff`
2.  **设置等值面：**

    *   点击`Properties → Isosurfaces`
    *   正值为电子积累（建议设等值面0.0015 e/Å³，黄色）
    *   负值为电子流失（建议设等值面-0.0015 e/Å³，蓝绿色）
        
        ```
        //VESTA isosurface settings
        Positive: 0.0015 e/Å³ (yellow)
        Negative: -0.0015 e/Å³ (blue-green)
        ```
        
        ![VESTA isosurface example](https://example.com/vesta_isosurface.png)
        
3.  **调整显示效果：**

    *   使用`Properties → Radius and color`修改原子颜色和大小
    *   通过`Edit → Lattice Planes`添加切片视图
        
        ![VESTA display settings](https://example.com/vesta_display.png)


## 三、常见问题FAQ

1.  **为何要保证K点网格密度一致？**

    *   网格密度不同会导致电荷密度网格不匹配，无法直接相减。
2.  **差分电荷密度数值范围如何选择？**

    *   一般取±0.005 e/Å³，具体可根据体系调整。

## 四、注意事项

*   结构优化不充分会导致错误结果，务必检查OSZICAR中的收敛标志。
*   真空层厚度不足会导致镜像电荷干扰，建议真空层≥15 Å。
    
    ```
    //Important notes
    Check OSZICAR convergence flags.
    Vacuum layer >= 15 Å.
    ```