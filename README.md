# 🧪 528Lab-Servers 计算化学服务器使用手册

<div align="center">

[![Lab](https://img.shields.io/badge/Lab-528计算化学团队-blue.svg)](https://github.com/Tenor-John/528Lab-Servers)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Update](https://img.shields.io/badge/Last%20Update-2025.07.02-red.svg)]()

**欢迎来到528实验室计算化学团队！**  
*在使用528实验室服务器之前的必备指南*

</div>

---

## 📋 快速开始

本手册涵盖了Linux基础操作、SSH服务器连接、以及Gaussian、VASP等主流计算化学软件的使用方法和相关文献资料。

### 🚀 必读指南

在开始使用服务器之前，请务必阅读：

1. **🔗 [服务器SSH连接指南](01-SSH_Link/SSH_access_to_the_server.md)** - 如何连接和访问服务器
2. **🐧 [Linux基础操作](0101-Linux_grammar/Linux_manual.md)** - Linux命令行基础
3. **📊 [Slurm作业管理](03-VASP_Manual/作业提交后检查方法.md)** - 任务提交和监控

### ⚡ 使用流程

```mermaid
graph LR
    A[SSH连接服务器] --> B[配置环境]
    B --> C[准备输入文件]
    C --> D[提交作业]
    D --> E[监控运行]
    E --> F[分析结果]
```

---

## 📚 软件使用手册

### 🧮 量子化学软件

| 软件 | 特色功能 | 使用手册 | 状态 |
|------|----------|----------|------|
| **Gaussian** | 分子轨道、频率分析、激发态 | [📖 Gaussian手册](02-Gaussian_Manual/Gaussian.md) | ✅ 可用 |
| **ORCA** | 高精度单点、耦合簇方法 | [📖 ORCA手册](04-ORCA_Manual/ORCA.md) | ✅ 可用 |

### ⚛️ 第一性原理软件

| 软件 | 特色功能 | 使用手册 | 状态 |
|------|----------|----------|------|
| **VASP** | 平面波DFT、固体计算 | [📖 VASP手册](03-VASP_Manual/VASP.md) | ✅ 可用 |

#### VASP 专项教程

- [🏗️ 结构构建](03-VASP_Manual/结构构建.md)
- [📊 态密度与能带计算](03-VASP_Manual/态密度及能带计算.md)
- [⚡ 各种能量计算](03-VASP_Manual/各种能量计算.md)
- [🔄 NEB过渡态搜索](03-VASP_Manual/NEB过渡态搜索.md)
- [📈 差分电荷密度分析](03-VASP_Manual/差分电荷密度分析CDD.md)
- [🎯 吸附能计算](03-VASP_Manual/Absorption_Energy.md)
- [⚙️ INCAR参数详解](03-VASP_Manual/INCAR_KEYWORDS.md)
- [📝 作业提交与监控](03-VASP_Manual/作业提交后检查方法.md)

### 🧬 分子动力学软件

| 软件 | 特色功能 | 使用手册 | 状态 |
|------|----------|----------|------|
| **LAMMPS** | 大规模分子动力学模拟 | [📖 LAMMPS手册](07-LAMMPS_Manual/LAMMPS.md) | 🔄 开发中 |
| **GROMACS** | 生物分子动力学模拟 | [📖 GROMACS手册](08-GROMACS_Manual/GROMACS.md) | 🔄 开发中 |

### 🛠️ 辅助分析软件

| 软件 | 特色功能 | 使用手册 | 状态 |
|------|----------|----------|------|
| **Multiwfn** | 波函数分析、电子结构分析 | [📖 Multiwfn手册](06-Multiwfn/Multiwfn.md) | ✅ 可用 |
| **VMD** | 分子可视化、轨迹分析 | [📖 VMD手册](05-VMD/VMD.md) | ✅ 可用 |
| **PyMOL** | 蛋白质结构可视化 | [📖 PyMOL手册](09-PyMOL_Manual/PyMOL.md) | 🔄 开发中 |
| **GaussView** | Gaussian图形界面 | [📖 GaussView手册](02-Gaussian_Manual/GaussView.md) | 🔄 开发中 |
| **VASPKIT** | VASP前后处理工具 | [📖 VASPKIT手册](03-VASP_Manual/VASPKIT.md) | 🔄 开发中 |

---

## 📖 必读资料

### 📚 理论基础

- [📘 量子化学计算方法](0000-计算化学必读书目/量子化学中的计算方法%20--%20陈飞武编著%20--%202008%20--%20北京_科学出版社%20--%2012090008%20--%20d53ec5f9779d67605446bc8b536a4286%20--%20Anna's%20Archive.pdf)
- [📗 Gaussian用户手册](0000-计算化学必读书目/Gaussian/)
- [📕 VASP理论与实践](0000-计算化学必读书目/VASP/)

### 🔧 系统管理

- [📄 Slurm用户指南](01-SSH_Link/slurm-userguide.pdf)
- [🐧 Linux命令参考](0101-Linux_grammar/Linux_manual.md)

---

## 🎯 常用计算流程

### 💻 Gaussian 计算流程
```bash
# 1. 准备输入文件
vi molecule.gjf

# 2. 提交作业
sbatch gaussian_job.sh

# 3. 监控进度
squeue -u username

# 4. 查看结果
tail -f molecule.log
```

### ⚛️ VASP 计算流程
```bash
# 1. 准备输入文件 (POSCAR, INCAR, POTCAR, KPOINTS)
vaspkit

# 2. 提交作业
sbatch vasp_job.sh

# 3. 监控进度
squeue -u username

# 4. 分析结果
grep "TOTEN" OUTCAR
```

---

## 🆘 常见问题与解决

### ❓ 连接问题
- **无法SSH连接**：检查VPN连接和防火墙设置
- **权限被拒绝**：确认用户名和密钥配置

### ❓ 作业问题
- **作业排队过久**：检查资源申请是否合理
- **计算中断**：查看错误日志文件(.err)

### ❓ 软件问题
- **模块加载失败**：使用 `module avail` 查看可用模块
- **路径错误**：确认软件安装路径和环境变量

---

## 📞 技术支持

遇到问题？寻求帮助：

1. **📖 查阅相关手册** - 先查看对应软件的使用手册
2. **💬 咨询同组同学** - 寻求有经验同学的帮助  
3. **📧 联系管理员** - 发送邮件详细描述问题
4. **🐛 提交Issue** - 在GitHub仓库提交问题报告

---

## 🔄 更新日志

- **2025.07.02** - 重构README，完善软件分类和链接
- **2025.07.01** - 新增Slurm作业管理手册
- **2025.06.30** - 更新VASP计算教程系列

---

<div align="center">

**📝 维护者：** 528实验室计算化学团队  
**📧 联系方式：** [实验室邮箱]  
**🔗 项目地址：** [GitHub Repository](https://github.com/Tenor-John/528Lab-Servers)

*⭐ 如果这个手册对您有帮助，请给我们一个Star！*

</div>
