# tus master thesis

修士論文関係のレポジトリ

## getting started

### ゲスト OS で必要なインストール：

python:

```bash
sudo apt install python3 python3-pip
pip3 install javalang
```

java:

```bash
sudo apt install default-jdk default-jre
```

ssh:

```bash
sudo apt install ssh
```

設定(/etc/ssh/sshd_config)：

```
Port 16763
PermitRootLogin without-password
PasswordAuthentication yes
AllowUsers root naru3
```

### 自作ライブラリのインストール

> https://github.com/naru-99/lib763.git

windows:

```bash
git clone https://github.com/naru-99/lib763.git
cd lib763
pip3 install .
```

Linux:

```bash
git clone https://github.com/naru-99/lib763.git
cd lib763
python3 setup.py develop
```

### 動的解析を行うための改造 OS(sct_debian)：

> https://github.com/naru-99/sct_debian

1. virtual box のインストール

   > https://www.oracle.com/jp/virtualization/technologies/vm/downloads/virtualbox-downloads.html

2. debian のイメージファイルを取得(v 11.7 推奨)

   - v 11.7

     > https://drive.google.com/file/d/17TkRT2qbis8RJcdXv7xfuyeA_3evPU5o/view?usp=sharing

   - 最新版:
     > https://www.debian.org/distrib/index.ja.html

3. debian の OS を起動し、sudo ができるユーザの作成
4. 本ソースをダウンロード(実機・仮想環境両方とも)

```bash
git clone https://github.com/naru-99/sct_debian.git
```

5. make.sh の実行

```bash
cd sct_debian
sudo bash make.sh
```
