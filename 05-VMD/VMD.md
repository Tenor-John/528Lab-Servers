# 🖥️ VMD 分子可视化软件使用手册

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">

📖 **VMD 简介**  
VMD (Visual Molecular Dynamics) 是一款功能强大的分子可视化软件，专门用于显示、动画和分析大型生物分子系统的三维结构。

**🎯 主要功能：**
- 分子结构可视化与渲染
- 分子动力学轨迹动画
- 电荷密度与分子轨道可视化  
- 蛋白质结构分析
- 高质量图像和视频输出

</div>

---

## 📋 目录

- [安装与配置](#安装与配置)
- [基础操作](#基础操作)
- [分子可视化](#分子可视化)
- [轨迹分析](#轨迹分析)
- [渲染与输出](#渲染与输出)
- [脚本编程](#脚本编程)

---

## 🔧 安装与配置

### 启动VMD

```bash
# 在终端启动VMD
vmd

# 加载特定文件启动
vmd molecule.pdb

# 批处理模式
vmd -dispdev text -e script.tcl
```

### 基本界面介绍

VMD主要包含三个窗口：
- **Main Window**: 主控制窗口
- **OpenGL Display**: 3D显示窗口  
- **VMD Console**: 命令行控制台

---

## 🎮 基础操作

### 鼠标控制

| 操作 | 功能 |
|------|------|
| **左键拖拽** | 旋转分子 |
| **中键拖拽** | 平移分子 |
| **右键拖拽** | 缩放分子 |
| **Shift+左键** | 光源控制 |

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| **R** | 重置视角 |
| **C** | 居中显示 |
| **Space** | 播放/暂停动画 |
| **Home/End** | 第一帧/最后一帧 |
| **F** | 全屏模式 |

---

## 🧬 分子可视化

### 载入分子结构

```tcl
# 载入PDB文件
mol new protein.pdb

# 载入多种格式
mol new structure.xyz
mol new trajectory.dcd

# 载入VASP文件
mol new POSCAR
mol new OUTCAR
```

### 表示模式设置

#### 常用表示方式

```tcl
# 球棍模型
mol representation CPK
mol selection all
mol addrep 0

# 管状模型
mol representation Tube
mol representation Licorice

# 表面模型
mol representation Surf
mol representation QuickSurf

# 卡通模型（蛋白质）
mol representation NewCartoon
```

#### 颜色方案

```tcl
# 按元素着色
mol color Element

# 按残基着色
mol color ResType

# 按链着色
mol color Chain

# 按温度因子着色
mol color Beta

# 自定义颜色
mol color ColorID 0  # 蓝色
```

### 选择语法

```tcl
# 基本选择
mol selection "all"
mol selection "protein"
mol selection "water"
mol selection "ion"

# 元素选择
mol selection "element C"
mol selection "element O H"

# 残基选择
mol selection "resname LYS"
mol selection "resid 1 to 10"

# 原子选择
mol selection "name CA"
mol selection "name C N O"

# 组合选择
mol selection "protein and resid 1 to 50"
mol selection "resname WAT and within 5 of protein"
```

---

## 📊 轨迹分析

### 载入轨迹文件

```tcl
# 先载入结构文件
mol new topology.psf

# 再载入轨迹
mol addfile trajectory.dcd waitfor all

# 或者一次性载入
mol new topology.psf
animate read dcd trajectory.dcd 0 -1 1 0
```

### 轨迹播放控制

```tcl
# 设置帧数
animate goto 0
animate goto end

# 播放控制
animate forward
animate reverse
animate stop

# 设置播放速度
animate speed 2.0
```

### 距离和角度测量

```tcl
# 距离测量
set sel1 [atomselect 0 "resid 1 and name CA"]
set sel2 [atomselect 0 "resid 10 and name CA"]
measure bond [$sel1 get index] [$sel2 get index]

# 角度测量
measure angle {atom1} {atom2} {atom3}

# 二面角测量
measure dihed {atom1} {atom2} {atom3} {atom4}
```

### RMSD计算

```tcl
# 计算RMSD
set ref [atomselect 0 "protein and name CA" frame 0]
set compare [atomselect 0 "protein and name CA"]

set num_steps [molinfo 0 get numframes]
for {set frame 0} {$frame < $num_steps} {incr frame} {
    $compare frame $frame
    set rmsd [measure rmsd $compare $ref]
    puts "Frame $frame: RMSD = $rmsd"
}
```

---

## 🎨 渲染与输出

### 图像输出

```tcl
# 设置渲染参数
display projection Orthographic
display depthcue off
display rendermode GLSL

# 输出高质量图像
render TachyonInternal output.tga

# 输出PostScript
render PostScript output.ps

# 输出POV-Ray格式
render POVRay3 output.pov
```

### 动画制作

```tcl
# 创建动画
movie maker

# 或者脚本方式
for {set i 0} {$i < [molinfo 0 get numframes]} {incr i} {
    animate goto $i
    render TachyonInternal frame[format "%04d" $i].tga
}
```

### 立体视图

```tcl
# 开启立体显示
display stereo on

# 设置立体模式
display stereo CrossEyes
display stereo SideBySide
```

---

## 💻 脚本编程

### VMD脚本基础

```tcl
# 基本Tcl语法示例
set molid 0
set sel [atomselect $molid "protein"]

# 循环处理所有原子
foreach atom [$sel get index] {
    set coord [$sel get {x y z}]
    puts "Atom $atom: $coord"
}

$sel delete
```

### 自定义函数

```tcl
# 计算分子几何中心
proc center_of_mass {selection} {
    set mass [$selection get mass]
    set coord [$selection get {x y z}]
    
    set total_mass 0
    set com {0 0 0}
    
    foreach m $mass c $coord {
        set total_mass [expr $total_mass + $m]
        set com [vecadd $com [vecscale $m $c]]
    }
    
    return [vecscale [expr 1.0/$total_mass] $com]
}
```

### 批处理脚本示例

```tcl
# 批量处理多个PDB文件
set pdb_list {protein1.pdb protein2.pdb protein3.pdb}

foreach pdb $pdb_list {
    mol new $pdb
    mol representation NewCartoon
    mol selection "protein"
    mol addrep top
    
    # 渲染图像
    render TachyonInternal [file rootname $pdb].tga
    
    mol delete top
}
```

---

## 🔬 专业分析功能

### 氢键分析

```tcl
# 载入氢键分析插件
package require hbonds

# 计算氢键
set hbonds [measure hbonds 3.5 30 $sel1 $sel2]
puts "Found [llength [lindex $hbonds 0]] hydrogen bonds"
```

### 表面积计算

```tcl
# 计算溶剂可及表面积
set sasa [measure sasa 1.4 $sel]
puts "SASA: $sasa Å²"
```

### 二级结构分析

```tcl
# 计算蛋白质二级结构
package require timeline
timeline_calculate_ss protein
```

---

## 🛠️ 常见问题与解决

### 文件格式问题

```tcl
# 检查支持的文件格式
mol list filetypes

# 强制指定文件类型
mol new file.dat type xyz
```

### 性能优化

```tcl
# 减少显示的原子数
mol selection "protein and name CA"

# 关闭不必要的效果
display depthcue off
display shadows off
```

### 内存管理

```tcl
# 删除分子
mol delete 0

# 清理选择
$sel delete

# 检查内存使用
puts [molinfo list]
```

---

## 📚 高级应用

### 1. 电荷密度可视化

```tcl
# 载入电荷密度数据
mol new density.cube

# 设置等值面
mol representation Isosurface
mol selection "all"
mol scaleminmax 0 0 -0.05 0.05
mol addrep 0
```

### 2. 分子轨道显示

```tcl
# 载入轨道文件
mol new orbital.cube

# 显示HOMO/LUMO
mol representation Isosurface
mol color ColorID 0  # 蓝色
mol scaleminmax 0 0 0.05 0.05
mol addrep 0

mol representation Isosurface  
mol color ColorID 1  # 红色
mol scaleminmax 0 1 -0.05 -0.05
mol addrep 0
```

### 3. 多分子对比

```tcl
# 载入多个结构进行对比
mol new protein1.pdb
mol new protein2.pdb

# 结构叠合
set sel1 [atomselect 0 "protein and name CA"]
set sel2 [atomselect 1 "protein and name CA"]
set trans_mat [measure fit $sel2 $sel1]
$sel2 move $trans_mat
```

---

## 📖 参考资料

- [VMD用户手册](../05-VMD/VMD用户手册.pdf)
- [VMD教程中文版](../05-VMD/VMD教程中文版.pdf)
- [VMD官方网站](https://www.ks.uiuc.edu/Research/vmd/)
- [VMD脚本库](https://www.ks.uiuc.edu/Research/vmd/script_library/)

---

## 🆘 技术支持

遇到问题？寻求帮助：

1. **📖 查阅VMD用户手册**
2. **💬 访问VMD邮件列表**
3. **🔍 搜索VMD官方论坛**
4. **📧 联系实验室VMD专家**

---

*📝 最后更新：2025年7月2日 | 📧 技术支持：528实验室*
