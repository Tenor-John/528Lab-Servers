# 局部轨道键合分析（LOBA）

用氧化态这个概念时相当于假定所有键都是纯粹的离子键，电子在原子间转移量是精确的整数。显然，这个假定对绝大多数情况都是极为糟糕的。懂量子化学的人不爱用氧化态这个虚构的概念，因为原子电荷能明显能更真实客观地描述原子在化学体系中的实际带电状态。但氧化态这个概念不能说完全没用，它对于将物质进行分类、归属、类比还是比较有益的。

原子电荷和氧化态根本没有对应关系。虽然原子电荷的计算方法多种多样，但没有任何一种原子电荷计算方法的结果能与氧化态直接联系起来，因为氧化态是把电荷转移显著人为夸大后的产物。比如OsO4大家都公认Os的氧化态是8（一般将O的氧化态当做-2然后根据体系净电荷来判断其余原子的氧化态），但是在B3LYP结合6-31G*和SDD计算的时候，几种方式算的Os的原子电荷值Mulliken=1.762、NPA=1.476、Hirshfeld=0.872、ADCH=0.939、AIM=2.540都远小于氧化态。实际中也往往会碰到这样的情形：两个配合物中，过渡金属的原子电荷只相差零点几，但按照经验判断的氧化态却相差个位数。所以不要妄图通过原子电荷判断氧化态。

首先将MO转化为定域化轨道(LMO)，然后依次计算各个LMO中的原子成份，若某原子对这个LMO的贡献值大于指定阈值（如50%），就认为这个LMO的电子完全归属于此原子。最后将原子的核电荷数减去归属到它上面的电子数即是其氧化态。

一般就用Multiwfn轨道定域化模块默认的Pipek-Mezey方法做定域化就行了，而且只需要将占据轨道部分做定域化就够了，记得此时绝对不能带弥散函数。

LOBA方法用的阈值有一定含糊性，多数情况用50%就行，但如果结果觉得诡异，可以适当调大再尝试，比如60%、70%。对于LOBA方法很适用的情形，感兴趣的原子的氧化态并不会随着阈值的这种程度的改变发生变化。如果结果对阈值特别敏感，则暗示LOBA方法并不适用于判断此原子的氧化态。

启动Multiwfn，输入
Fe(CN)6_3-.fch   //Gaussian输出的chk文件转化成的fch文件
19   //轨道定域化
1   //只对占据轨道做定域化，这对LOBA分析够了
此时Multiwfn把定域化后的轨道导出到了当前目录下的new.fch，然后自动载入之，此时内存里的轨道已经是定域化轨道了，可以开始做LOBA分析了。接着输入
8   //轨道成分分析
100   //LOBA方法计算氧化态
50   //判断轨道归属的阈值用50%
结果如下
Oxidation state of atom   1(Fe) :  3
Oxidation state of atom   2(C ) :  2
Oxidation state of atom   3(C ) :  2
Oxidation state of atom   4(C ) :  2
Oxidation state of atom   5(C ) :  2
Oxidation state of atom   6(C ) :  2
Oxidation state of atom   7(C ) :  2
Oxidation state of atom   8(N ) : -3
Oxidation state of atom   9(N ) : -3
Oxidation state of atom  10(N ) : -3
Oxidation state of atom  11(N ) : -3
Oxidation state of atom  12(N ) : -3
Oxidation state of atom  13(N ) : -3
The sum of oxidation states:  -3

可见，氧化态总和为-3，正好对应体系的净电荷。Fe的氧化态为3，十分合理。N的电负性比C大，所以氧化态是负值(-3)，C是正值(+2)，也很合理。
