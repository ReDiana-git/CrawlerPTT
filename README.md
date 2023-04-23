# PTT 多線程爬蟲

## Notice

此爬蟲軟體只用於學習用途

請勿用於攻擊PTT或其他網站

## python requirement

作者使用 python3.6 ~ python3.8 版本

python 套件 requests-html

```
python -m pip install requests-html
```

## 使用方式


- 將本專案 clone 下來
```
git clone https://github.com/ReDiana-git/CrawlerPTT.git
```

- 使用 
```
python main.py --start="想要開始的頁數" --end="結束頁數" --club="想要爬取的版" --thread="執行線程數量"
```

| 參數 |選必填| 內容 | 備註|
|---  |-----|----|----|
|--start|必填|想要從哪一個頁數開始爬文章|例如想要爬取 /Gossiping/index100.html 這樣就填入 100|
|--end |必填|想要結束在哪篇文章|同上，如果想從 100 爬到 /Gossiping/index500.html 此參數填入 500|
|--club|必填|想要爬取的版|要八卦版，就填 Gossiping，務必大小寫相同|
|--thread|選填|多開多少線程|未填執行單線程，線程數量與CPU線程數量*2，差不多就是極限，根據每個人電腦配置有所出入|