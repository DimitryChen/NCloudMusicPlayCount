# NCloudMusicPlayCount

计算网易云音乐用户（公开的）听歌排行的播放次数。详见博客——[网易云音乐听歌排行之播放次数](https://wwwpf.github.io/2018/10/10/%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90%E5%90%AC%E6%AD%8C%E6%8E%92%E8%A1%8C%E4%B9%8B%E6%92%AD%E6%94%BE%E6%AC%A1%E6%95%B0/)

## 效果

![](pics/play_count.png)

## 使用

```text
usage: play_count.py [-h] [--id ID]

optional arguments:
  -h, --help  show this help message and exit
  --id ID     需要计算播放次数的用户ID
```

直接下载 `release` 下的exe，运行：

```shell
play_count.exe --id 29879272
```

或者通过python3运行代码文件，需要安装的库如下：

- requests
- pycrypto

运行：

```shell
python play_count.py --id 29879272
```