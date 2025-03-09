# 吸附能计算步骤总结

1. **下载初始包cif文件**：获取所需的初始晶体结构文件（cif格式）。
2. **转化为POSCAR文件进行结构优化**：将cif文件转化为VASP使用的POSCAR文件，并进行结构优化。
3. **使用优化后的结构切胞建立超胞**：利用优化后的晶体结构，切割出超胞并进行优化。
4. **建立目标分子模型**：构建目标分子的模型，并使用Gaussian进行结构优化。
5. **放入相同大小真空层**：将优化后的分子放入与晶体切面超胞相同大小的真空层中。
6. **晶体切面超胞结构优化**：等待晶体切面超胞结构优化完成。
7. **将分子放入晶体表面优化结构**：将优化后的分子放入晶体表面，并进行结构优化。
8. **计算能量**：计算以上最优结构的能量，最终计算吸附能。

## 关于使用Gaussian优化分子

注意Gaussian和VASP使用的计算方法（泛函、基组等）可能不一致，这可能导致能量计算不协调。理想情况下应使用相同的计算方法处理所有结构。

## 吸附能计算

吸附能计算需要三个独立的计算：

- 优化后的干净晶体表面能量 (E_surface)
- 优化后的孤立分子能量 (E_molecule)
- 优化后的分子吸附在表面的复合系统能量 (E_combined)

吸附能计算公式：$E_{ads} = E_{combined} - E_{surface} - E_{molecule}$

## 其他建议

- 确保真空层足够厚（通常15-20埃），防止周期性镜像之间的相互作用。
- 构建slab模型时，确保有足够的原子层（通常4-7层），通常底部几层固定以代表体相。
- 测试多个吸附位点，找出最稳定的吸附构型。
- 考虑使用范德华校正（如DFT-D3、optB88-vdW等），特别是对于物理吸附系统。

## 结构优化INCAR
```bash
SYSTEM = PbO2 2x2x3 Struc OPT
ISTART =  1            (Read existing wavefunction, if there)
ISPIN  =  1            (Non-Spin polarised DFT)
# ICHARG =  11         (Non-self-consistent: GGA/LDA band structures)
LREAL  = Auto       (Projection operators: automatic)
ENCUT  =  520        (Cut-off energy for plane wave basis set, in eV)
PREC   =  Accurate   (Precision level: Normal or Accurate, set Accurate when perform structure lattice relaxation calculation)
LWAVE  = .TRUE.        (Write WAVECAR or not)
LCHARG = .TRUE.        (Write CHGCAR or not)
ADDGRID= .TRUE.        (Increase grid, helps GGA convergence)
LASPH  = .TRUE.        (Give more accurate total energies and band structure calculations)
# LVTOT  = .TRUE.      (Write total electrostatic potential into LOCPOT or not)
# LVHAR  = .TRUE.      (Write ionic + Hartree electrostatic potential into LOCPOT or not)
# NELECT =             (No. of electrons: charged cells, be careful)
# LPLANE = .TRUE.      (Real space distribution, supercells)
# NWRITE = 2           (Medium-level output)

# caculation source opt
KPAR = 2
NCORE = 6
NPAR = 6

# NGXF    = 300        (FFT grid mesh density for nice charge/potential plots)
# NGYF    = 300        (FFT grid mesh density for nice charge/potential plots)
# NGZF    = 300        (FFT grid mesh density for nice charge/potential plots)
 
Electronic Relaxation
ISMEAR =  0            (Gaussian smearing, metals:1)
SIGMA  =  0.05         (Smearing value in eV, metals:0.2)
NELM   =  200           (Max electronic SCF steps)
NELMIN =  6            (Min electronic SCF steps)
EDIFF  =  1E-05        (SCF energy convergence, in eV)
# GGA  =  PS           (PBEsol exchange-correlation)
 
Ionic Relaxation
NSW    =  200          (Max ionic steps)
IBRION =  2            (Algorithm: 0-MD, 1-Quasi-New, 2-CG)
ISIF   =  2            (Stress/relaxation: 2-Ions, 3-Shape/Ions/V, 4-Shape/Ions)
EDIFFG = -2E-02        (Ionic convergence, eV/AA)
# ISYM =  2            (Symmetry: 0=none, 2=GGA, 3=hybrids)

#Electrofield
IDIPOL = 3
LDIPOL = .TRUE.
DIPOL  = 0 0 8.9 
```
## 能量计算INCAR

计算能量时应该固定住和结构优化中一样的原子层数，最起码应该将吸附位点层的原子解放开，防止近似处理

```bash
SYSTEM = PbO2 2x2x3 ABE O
ISTART =  1            (Read existing wavefunction, if there)
ISPIN  =  1            (Non-Spin polarised DFT)
# ICHARG =  11         (Non-self-consistent: GGA/LDA band structures)
LREAL  =  False       (Projection operators: automatic)
ENCUT  =  520        (Cut-off energy for plane wave basis set, in eV)
PREC   =  Accurate   (Precision level: Normal or Accurate, set Accurate when perform structure lattice relaxation calculation)
ALGO   =  Normal
LWAVE  = .TRUE.        (Write WAVECAR or not)
LCHARG = .TRUE.        (Write CHGCAR or not)
ADDGRID= .TRUE.        (Increase grid, helps GGA convergence)
LASPH  = .TRUE.        (Give more accurate total energies and band structure calculations)
# LVTOT  = .TRUE.      (Write total electrostatic potential into LOCPOT or not)
# LVHAR  = .TRUE.      (Write ionic + Hartree electrostatic potential into LOCPOT or not)
# NELECT =             (No. of electrons: charged cells, be careful)
# LPLANE = .TRUE.      (Real space distribution, supercells)
# NWRITE = 2           (Medium-level output)

# caculation source opt
KPAR = 2
NCORE = 6
NPAR = 6

# NGXF    = 300        (FFT grid mesh density for nice charge/potential plots)
# NGYF    = 300        (FFT grid mesh density for nice charge/potential plots)
# NGZF    = 300        (FFT grid mesh density for nice charge/potential plots)

# ISPIN  =  2          (启用自旋极化，若涉及开壳层分子)
# MAGMOM = ...         (设置初始磁矩，若需要)

Electronic Relaxation
ISMEAR =  0            (Gaussian smearing, metals:1)
SIGMA  =  0.05         (Smearing value in eV, metals:0.2)
NELM   =  200           (Max electronic SCF steps)
NELMIN =  6            (Min electronic SCF steps)
EDIFF  =  1E-07        (SCF energy convergence, in eV)
# GGA  =  PS           (PBEsol exchange-correlation)
 
Ionic Relaxation
NSW    =  0          (Max ionic steps，不进行结构优化)
IBRION =  -1            (Algorithm: 0-MD, 1-Quasi-New, 2-CG，不计算原子间力)
ISIF   =  ,0            (Stress/relaxation: 2-Ions, 3-Shape/Ions/V, 4-Shape/Ions)
#EDIFFG = -1E-02        (Ionic convergence, eV/AA)能量计算不需要离子步
# ISYM =  2            (Symmetry: 0=none, 2=GGA, 3=hybrids)

#Electrofield
IDIPOL = 3
LDIPOL = .TRUE.
DIPOL  = 0 0 8.9 

LORBIT =  11           (启用轨道分解态密度)
LAECHG =  .TRUE.       (用于电荷分析)
IVDW   =  11           (DFT-D3 method of Grimme with zero-damping function)
```