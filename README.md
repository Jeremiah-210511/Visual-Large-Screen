## · 使用Python爬取腾讯新闻疫情数据，通过plotly可视化后，再利用streamlit制作大屏展示

## · 结合“Our World in data”网站中的数据，利用streamlit制作大屏展示近百年来二氧化碳排放的趋势以及给我们所居住的环境造成了什么样的影响。

_疫情数据可视化已不是什么新鲜话题，项目仅供笔者或其他同学练习爬虫和可视化。_

_“碳达峰、碳中和”是2021年政府在不断强调的事，今后也必将是世界发展的趋势。那什么是“碳达峰”，什么又是“碳中和”呢？所谓的“碳达峰”指的是在某一时间点，二氧化碳的排放不再达到峰值，之后逐步回落。而“碳中和”也就意味着企业、个体与团体在一定时间内直接或间接产生的温室气体排放总量，通过植树造林、节能减排等形式，抵消自身产生的二氧化碳排放，实现二氧化碳的“零排放”。_

__“Our World in data”收录了各个学科的数据，包括卫生、食品、收入增长和分配、能源、教育、环境等行业，源数据开放在Github上面。__
![图片](https://mmbiz.qpic.cn/mmbiz_png/Jibw7n291dTzq7YVib4YGtl7LB3tCH5yJwYxqgwUia3VibbiaDs2r4ia6plJibiaIpKS5wDL5SUBnTdvIBqicxWq3hjbpicA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

__疫情数据来源于腾讯新闻，链接：https://news.qq.com/zt2020/page/feiyan.htm#/__
![image-20211224111857108](D:\Git仓库\Visual-Large-Lcreen\images\image-20211224111857108.png)

本文将通过绘制中国省级 Choropleth 地图来解释如何使用 plotly 绘制 Choropleth 地图，主要有两种方法：底层 API `plotly.graph_objects.Choroplethmapbox` 和高层 API `plotly.express.choropleth_mapbox`，笔者主要讲讲高层API的使用。

## 什么是 Choropleth 地图

Choropleth map 即分级统计图。在整个制图区域的若干个小的区划单元内（行政区划或者其他区划单位），根据各分区资料的数量（相对）指标进行分级，并用相应色级或不同疏密的晕线，反映各区现象的集中程度或发展水平的分布差别。

简单来说，具体到本文，就是在地图上为每个省上色，根据什么来确定上哪个颜色呢？在本文中就是确诊人数或CO2排放量，人数越多或者CO2排放量越多，颜色就越亮。这样得到的地图就是 Choropleth 地图。

## plotly 的绘图逻辑

使用 plotly 绘图，其实就是两点：**data 和 layout**，即数据和布局。其实所有绘图都是这样，只不过在 plotly 里体现得尤为明显，尤其是底层 API。

data 决定绘图所使用的数据，比如绘制股票折线图用的股票历史数据，绘制疫情地图用的疫情数据。layout 决定图的布局，比如一幅折线图的宽高，一幅地图的风格和中心点。plotly 里一幅图是一个 `Figure` 对象，这个对象就有 `data` 和 `layout` 两个参数。

## 方法 1：底层 API `plotly.graph_objects`

- 先看下 `go.Choroplethmapbox` 的参数：

  - `geojson`：`dict` 类型，这个就是刚才说的用于绘制地图轮廓的数据，一般从相应的 geojson 文件中用 `json.load` 加载进来。
  - `featureidkey`：`str` 类型，默认 为 `id`。函数会使用这个参数和 `locations` 匹配地图单元（比如省份）的名称，以此决定绘制哪些地图单元的轮廓。通常的形式为 `properties.name`，其中的 `name` 需要你自己根据 geojson 文件去指定，比如这里是 `properties.NL_NAME_1`，意思就是 `NL_NAME_1` 这一列是省份名称。这个很重要，设置不正确会导致地图轮廓显示不出来，**一定要保证和 `locations` 中的所有名称保持一致**。
  - `locations`: 可以是以下类型：`list，numpy array，数字、字符串或者 datetime 构成的 Pandas series`。指定地图单元名称，决定绘制哪些地图单元的轮廓。同样需要注意**和 `featureidkey` 保持一致**。
  - `z`：可以是以下类型：`list，numpy array，数字、字符串或者 datetime 构成的 Pandas series`。指定地图单元对应的数值，函数会将此值映射到 colorscale 中的某一颜色，然后将此颜色涂到相应的地图单元内。通常来说是一个 pandas dataframe 中的某一列，即一个 series。需要注意此参数中值的顺序需要和 `locations` 保持一致，一一对应，如河南在 `locations` 中的索引是 9，那么河南的确诊人数在 `z` 中的索引也必须是 9。
  - `zauto`：`bool` 类型，默认为 `True`。是否让颜色自动适应 `z`，即自动计算 `zmin` 和 `zmax`，然后据此来映射 colorscale。
  - `colorscale`：通常来说是 `str` 类型，也可以是 [`list` 类型](https://plot.ly/python/colorscales/#custom-discretized-heatmap-color-scale-with-graph-objects)。指定所使用的 colorscale，可使用的值参见[此处](https://plot.ly/python/builtin-colorscales/)。
  - `marker_opacity`：`float` 类型，颜色透明度。
  - `marker_line_width`：`float` 类型，地图轮廓宽度。
  - `showscale`：`bool` 类型。是否显示 colorbar，就是地图旁边的颜色条。

  `fig.update_layout` 的参数同样有很多，主要用来定义布局：

  - `mapbox_style`：`str` 类型，指定 mapbox 风格。可用的 mapbox 风格列表可参见[这里](https://plot.ly/python/mapbox-layers/#base-maps-in-layoutmapboxstyle)。需要注意的是当你使用以下风格之一时，你就需要指定 `mapbox_token`（关于如何获取 token 详细可参见[这里]([https://github.com/secsilm/2019-nCoV-dash#%E5%85%B3%E4%BA%8E-mapboxtoken)）：](https://github.com/secsilm/2019-nCoV-dash#关于-mapboxtoken)）：)

    ```python
    ["basic", "streets", "outdoors", "light", "dark", "satellite", "satellite-streets"]
    ```

  - `mapbox_zoom`：`int` 类型，指定地图的缩放级别。

  - `mapbox_center`：`dict` 类型，key 为 `lat`（经度）和 `lon`（纬度），指定初始时地图的中心点。

## 方法 2：高层 API `plotly.express.choropleth_mapbox`

`plotly.express.choropleth_mapbox`（以下简称 `px.choropleth_mapbox`） 是 plotly 的高层 API，严格来说是 [`plotly_express`](https://github.com/plotly/plotly_express) 的接口，但是后来这个包被并入 `plotly`，可以直接用 `plotly.express` 来引入了，这个包主要就是简化了 plotly 的绘图方法。

详细参数可参考其[官方文档](https://plot.ly/python-api-reference/generated/plotly.express.choropleth_mapbox.html#plotly.express.choropleth_mapbox)。

- `data_frame`：通常来说是 `pd.DataFrame` 格式。我们需要把绘图用到的数据都放到这个参数里面，后续很多参数都是基于此的，具体来说就是其中的列名。在 plot express 的各个绘图方法中，`DataFrame` 其实是最为方便的格式，也是官方推荐的格式，官方的大部分示例都是使用的这个格式。
- `geojson`：和 `go.Choroplethmapbox` 的同名参数对应。
- `color`：通常为 `str` 类型，`data_frame` 的列名。和 `go.Choroplethmapbox` 中的 `z` 对应。
- `locations`：通常为 `str` 类型，`data_frame` 的列名。和 `go.Choroplethmapbox` 中的同名参数对应。
- `featureidkey`：和 `go.Choroplethmapbox` 的同名参数对应。
- `mapbox_style`：和 `update_layout` 的同名参数对应。
- `color_continuous_scale`：和 `go.Choroplethmapbox` 中的 `colorscale` 对应（可按比例设置色号）。
- `center`：和 `update_layout` 中的 `mapbox_center` 对应。
- `zoom`：和 `update_layout` 中的 `mapbox_zoom` 对应。

## Reference

- [Mapbox Choropleth Maps | Python | Plotly](https://plot.ly/python/mapbox-county-choropleth/)
- [Choropleth Maps | Python | Plotly](https://plot.ly/python/choropleth-maps/#base-map-configuration)

# **Streamlit**

Streamlit是第一个专门针对机器学习和数据科学团队的应用开发框架，它是开发自定义机器学习工具的最快的方法，你可以认为它的目标是取代Flask在机器学习项目中的地位，可以帮助机器学习工程师快速开发用户交互工具。

Streamlit应用就是Python脚本，没有隐含的状态，你可以使用函数调用重构。只要你会写Python脚本，你就会开发Streamlit应用。

简而言之，Streamlit的工作方式如下：

- 对于用户的每一次交互，整个脚本从头到尾执行一遍
- Streamlit基于UI组件的状态给变量赋值
- 缓存让Streamlit可以避免重复请求数据或重复计算

![image-20211224114753667](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20211224114753667.png)

详细说明可参考官方文档：https://docs.streamlit.io/

### __下面直接看看成品：__
![全球CO2排放量分布](D:\Git仓库\Visual-Large-Lcreen\images\全球CO2排放量分布.gif)

![全球疫情速览](D:\Git仓库\Visual-Large-Lcreen\images\全球疫情速览.png)

