# Gaussian使用指南

## 提交作业方法

```bash
### 初始提交方法（仍可正常使用）

g16 <testfile.come/gjf……> | tee <testfile.out>

# 这个tee命令是一个 Linux 命令，它将标准输入复制到标准输出（通常是您的屏幕）和指定文件。
# 这对于将命令连接在一起非常有用，并且当您想要将输出重定向到单个或多个文件并仍然进一步
# 处理输出时非常方便。该tee命令得名于*水管工在连接多根水管时使用的 T 型分流器*。

### 现在的提交方式

Gaussian <job_name.gjf> <job_name.out>
```

<aside>
💡 这个`tee`命令是一个 Linux 命令，它将标准输入复制到标准输出（通常是您的屏幕）和指定文件。这对于将命令连接在一起非常有用，并且当您想要将输出重定向到单个或多个文件并仍然进一步处理输出时非常方便。该`tee`命令得名于*水管工在连接多根水管时使用的 T 型分流器*。

</aside>

## 实用脚本

### 批量执行文件

```bash
# 提交语法
/home/mmm/桌面/JT/gaussian_p.sh file1.gjf file2.gjf file3.gjf ...
```

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

### 依次执行多个指令

比如要依次执行g09 < 1.gjf > 1.out、g09 < 2.gjf > 2.out、g09 < 3.gjf > 3.out，可以只输入一条命令，每条命令间用分号隔开：

g09 < 1.gjf > 1.out;g09 < 2.gjf > 2.out;g09 < 3.gjf > 3.out

也可以写一个文本文件比如t.sh，里面写上

```bash
g09 < 1.gjf > 1.out
g09 < 2.gjf > 2.out
g09 < 3.gjf > 3.out
```

然后用chmod +x *给它加上可执行权限，再输入./t.sh运行即可（后同）。

如果不让指令依次执行，而是同时执行，把每行命令后面都加上&即可。