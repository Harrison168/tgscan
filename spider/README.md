# Spider Module

## 概述
这个spider模块是一个自动爬虫系统，主要用于从各个平台爬取TG群组数据。

## 使用方法
1. Python版本：3.10
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 配置 `.env` 文件，填入必要的API密钥和URL
4. 将`PYTHON_ENV`写入系统环境变量，默认为 `dev`，生产为`prod`
## 运行爬虫

### TelghubAutoCrawler
TelghubAutoCrawler是用于爬取Telghub平台数据的爬虫。运行方法如下：
```
CMD进入spider同级目录：  
python -m spider.src.TelghubAutoCrawler
```

### CombotAutoCrawler
CombotAutoCrawler是用于爬取Combot平台数据的爬虫。运行方法如下：
```
CMD进入spider同级目录：  
python -m spider.src.CombotAutoCrawler
```

### TgramApiAutoCrawler
TgramAutoCrawler是用于爬取tgram.io平台数据的爬虫。运行方法如下：
```
CMD进入spider同级目录：  
python -m spider.src.TgramApiAutoCrawler
```

## UpdateRoomTags
UpdateRoomTags是用于自动化打标签。运行方法如下：
```
CMD进入spider同级目录：  
python -m spider.src.UpdateRoomTags
```

## TgstatAutoCrawler
TgstatAutoCrawler运行方法如下：
```
CMD进入spider同级目录：  
python -m spider.src.TgstatAutoCrawler
```
