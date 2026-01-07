# 结构优化

```


INPUT_PARAMETERS

# ---------------- Paths ----------------
orbital_dir   ./ABACUS/SG15-Version1p0__StandardOrbitals-Version2p0/
pseudo_dir    ./ABACUS/SG15_ONCV_v1.0_upf/

# ---------------- General ----------------
calculation             relax
basis_type              lcao
dft_functional          pbe

# （可选）如果你只跑 Gamma 点并且希望更快，可开 gamma_only=1（会覆盖/忽略KPT）
# gamma_only            1

# ---------------- Spin / DFT+U ----------------
nspin                   2

dft_plus_u     1 # 打开DFT+U
orbital_corr   2  2  -1  -1  -1  -1
hubbard_u      3.5  5.5  0.0  0.0  0.0  0.0

# ---------------- SCF control ----------------
scf_thr                 1.0e-6
scf_nmax                400

# LCAO 求解器：genelpa 需要编译时启用 ELPA；否则建议用 scalapack_gvx
ks_solver               genelpa

# ---------------- Smearing ----------------
smearing_method         gauss
smearing_sigma          0.05

# ---------------- Ionic relaxation ----------------
relax_method            bfgs
force_thr               0.02
relax_nmax              400

# ---------------- Structure ----------------
symmetry                0
fixed_axes
fixed_ibrav
fixed_atoms

# ---------------- Output ----------------
#out_interval          1 # out_interval 控制一些输出在MD时的间隔；一般默认1就行

# 输出电荷密度（用于后处理/重启/差分电荷等）
out_chg                 1

# 输出势：官方建议 out_pot=2 才会输出静电势（Hartree+local pseudo）功能在较新版本提供
out_pot               2

# 输出 LCAO 波函数/矩阵（做电荷转移/后处理很有用）
out_wfc_lcao            1

# （强烈建议）输出 Mulliken（便于逐原子电荷/自旋/磁矩分析）
out_mul               1

# ---------------- Solvent /Potential ----------------
# Implicit solvation model 隐式溶剂模型
imp_sol             1                    # 指定隐式溶剂模型的开(1)或者关(0)，默认值为 0
eb_k                80                   # 溶剂的相对介电常数，水为 80
tau                 0.000010798          # 有效表面张力参数，用于描述未被静电项捕获的溶质和溶剂之间的空化、分散和排斥相互作用，单位是$Ry/Bohr^2$，默认值为 1.0798e-05
sigma_k             0.6                  # 由溶质的电子结构隐含地确定的扩散腔的宽度（溶质电子密度与 nc_k 的比值，无量纲），默认值为 0.6
nc_k                0.00037              # 介电腔形成时的电子密度值，单位是$Bohr^{-3}$，默认值为 0.00037


```

# SCF静态自洽计算
