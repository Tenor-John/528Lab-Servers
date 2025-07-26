# Gaussian使用指南

## 目录

- [提交作业方法](#提交作业方法)
- [SLURM作业提交脚本](#slurm作业提交脚本)
- [实用脚本](#实用脚本)
- [作业管理](#作业管理)

## 提交作业方法

### 直接提交方式

```bash
# 基础提交方法
g16 < input.gjf > output.log

# 使用tee命令（可同时显示输出和保存到文件）
g16 < input.gjf | tee output.log

# 现在推荐的提交方式
g16 input.gjf output.log
```

> **说明**：`tee`命令将标准输入复制到标准输出（屏幕）和指定文件，方便实时监控计算进度。

### 后台运行方式

```bash
# 后台运行（推荐用于长时间计算）
nohup g16 < input.gjf > output.log 2>&1 &

# 查看后台作业
jobs

# 终止后台作业
kill %1  # 终止第1个后台作业
```

## SLURM作业提交脚本

### 标准SLURM提交脚本 (submit_gauss.sh)

```bash
#!/bin/bash
#SBATCH -J gaussian-job        # 作业名称
#SBATCH -o %j.out             # 标准输出文件 (%j为作业ID)
#SBATCH -e %j.err             # 错误输出文件
#SBATCH -p DFT                # 队列名称
#SBATCH -N 1                  # 节点数量
#SBATCH -n 32                 # 总CPU核数
#SBATCH --ntasks-per-node=32  # 每节点CPU核数
#SBATCH --mem=20G             # 内存需求

echo Time is `date`
echo Directory is $PWD
echo This job runs on the following nodes:
echo $SLURM_JOB_NODELIST
echo This job has allocated $SLURM_JOB_CPUS_PER_NODE cpu cores.

# 切换到工作目录
cd /home/mmm/Desktop/JT/4NbA/

# 设置环境变量
export OMP_NUM_THREADS=1

# 自动找到第一个gjf文件并运行
INPUT_FILE=$(ls *.gjf 2>/dev/null | head -1)
if [ -z "$INPUT_FILE" ]; then
    echo "Error: No .gjf files found!"
    exit 1
fi

echo "Processing file: $INPUT_FILE"
g16 < $INPUT_FILE > ${INPUT_FILE%.gjf}.log 2>&1
```

### 使用SLURM脚本

```bash
# 1. 保存脚本为submit_gauss.sh
# 2. 添加执行权限
chmod +x submit_gauss.sh

# 3. 修改工作目录路径
# 编辑脚本中的: cd /home/mmm/Desktop/JT/4NbA/
# 改为你的实际工作目录

# 4. 提交作业
sbatch submit_gauss.sh

# 5. 查看作业状态
squeue -u $USER

# 6. 取消作业
scancel <作业ID>
```

### SLURM参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-J` | 作业名称 | `-J gaussian-job` |
| `-o` | 标准输出文件 | `-o %j.out` |
| `-e` | 错误输出文件 | `-e %j.err` |
| `-p` | 队列/分区名称 | `-p DFT` |
| `-N` | 节点数量 | `-N 1` |
| `-n` | 总CPU核数 | `-n 32` |
| `--mem` | 内存需求 | `--mem=20G` |
| `-t` | 时间限制 | `-t 24:00:00` |

## 实用脚本

### 1. 批量并行执行脚本 (gaussian_p.sh)

适用于需要同时运行多个Gaussian任务的情况：

```bash
#!/bin/bash

# 检查是否安装了 GNU Parallel
if ! command -v parallel &> /dev/null; then
    echo "错误：未安装 GNU Parallel。请先安装它。"
    exit 1
fi

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <输入文件1> <输入文件2> ..."
    exit 1
fi

# 定义一个函数来运行单个 Gaussian 任务
run_gaussian() {
    input_file="$1"
    output_file="${input_file%.*}.out"
    echo "开始处理: $input_file"
    /home/mmm/apps/g16/g16 < "$input_file" > "$output_file" 2>&1
    echo "完成: $input_file -> $output_file"
}

# 导出函数，使其对 GNU Parallel 可用
export -f run_gaussian

# 使用 GNU Parallel 并行运行任务
parallel -j 4 run_gaussian ::: "$@"

echo "所有任务完成！"
```

**使用方法：**

```bash
# 提交语法
/home/mmm/桌面/JT/gaussian_p.sh file1.gjf file2.gjf file3.gjf ...
```

### 2. 顺序执行脚本

#### 方法一：命令行直接执行

```bash
# 依次执行多个计算，用分号分隔
g16 < 1.gjf > 1.log; g16 < 2.gjf > 2.log; g16 < 3.gjf > 3.log
```

#### 方法二：脚本批处理

创建脚本文件 `batch_run.sh`：

```bash
#!/bin/bash
g16 < 1.gjf > 1.log
g16 < 2.gjf > 2.log
g16 < 3.gjf > 3.log
```

使用方法：

```bash
chmod +x batch_run.sh
./batch_run.sh
```

### 3. 并行执行脚本

如果要同时执行多个任务，在每条命令后添加 `&`：

```bash
#!/bin/bash
g16 < 1.gjf > 1.log &
g16 < 2.gjf > 2.log &
g16 < 3.gjf > 3.log &
wait  # 等待所有后台任务完成
```

## 作业管理

### 查看系统资源

```bash
# 查看CPU使用情况
top
htop

# 查看内存使用情况
free -h

# 查看磁盘使用情况
df -h

# 查看当前用户进程
ps aux | grep $USER
```

### SLURM作业管理命令

```bash
# 查看队列状态
sinfo

# 查看用户作业
squeue -u $USER

# 查看详细作业信息
scontrol show job <作业ID>

# 取消作业
scancel <作业ID>

# 查看作业历史
sacct -u $USER
```

### 监控计算进度

```bash
# 实时查看输出文件
tail -f output.log

# 查看最后几行输出
tail -20 output.log

# 搜索关键词
grep "SCF Done" output.log
grep "optimization completed" output.log
grep "Error" output.log
```

### 常用技巧

#### 1. 自动检测完成状态

```bash
#!/bin/bash
# 监控脚本 monitor.sh
while true; do
    if grep -q "Normal termination" *.log; then
        echo "计算完成！"
        break
    fi
    sleep 60  # 每分钟检查一次
done
```

#### 2. 磁盘空间清理

```bash
# 删除临时文件
rm -f *.chk *.rwf

# 压缩大文件
gzip *.log
gzip *.out
```

#### 3. 计算资源估算

```bash
# 查看文件大小
ls -lh *.gjf *.log

# 统计原子数
grep "NAtoms=" *.log

# 估算内存需求（经验值）
# 小分子(<50原子): 2-8GB
# 中等分子(50-200原子): 8-32GB  
# 大分子(>200原子): 32GB+
```
