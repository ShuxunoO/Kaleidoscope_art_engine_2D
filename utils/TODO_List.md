+ config.json

+ 文件夹里面放子文件夹

+ 

+ 

+ DNA 计算器（sha1）

+ DNA set（）主要是为了判断某个DNA是否已经存在

+ 读取图层信息格式如下：（详细见data模板）
  
  > layers_list
  > 
  > - - - layer1
  >     
  >     - - subfolder1_name:[layername1：{path:xxx, weight:xxx, counter:xxx, conflict_traits:xxx}，layername2，……] (适用于被分类的子文件夹)
  >       
  >       - subfolder2_name:[xxx]
  >       
  >       - layername1(适用于大众类的万能匹配图层)
  >       
  >       - layername2
  >       
  >       - ……

+ 排列组合混合器

+ 一个专门用来混合特层的函数blender(pathStr, outputPath){

}

+ 一个专门用来生成json的函数（ETH，SOLONA）
  
  

+ 拟混合的时候要维护一个attributes的字典,用于控制groupset之间的匹配，等到正式混合的时候直接读这个表。同样的，这个文件表可以当做历史记录来用。例如：

> {
> 
>     {
> 
> "background"：“Wave”，
> 
> “Holder”：“Blue”，
> 
> ……
> 
>     }，
> 
>     {
> 
> "background"：“Wave”，
> 
> “Holder”：“Blue”，
> 
> ……
> 
>     }，
> 
> {
> 
> ……
> 
> }
> 
> 

+ ~~要有一个全是列表地址的的字典（为了方便查询某个图层被放在哪里）~~替代方案是一次性吧图层全部读到内存里，然后根据图层名字选图层，这样效率会更高。
+ 图像的放大，缩小模块
+ 用正则表达式，统计一个图层出现了多少次
