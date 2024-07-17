## codes to be executed on guest machine

guest os(sct_debian)上でファイルを実行するためのコード

- correct_java.py
  - java ファイルの、クラス名とファイル名が一致しない問題を解決する。
  - ファイル名になるようにクラス名を変更する。
- execute_program.py
  - python および java を子プロセスで実行する関数を含むコード
- Executor.py
  - ファイルを実行するためのエントリポイントを含むコード

## メモ

- correct_java.py
  - 本当に完ぺきにファイルの変更が行われているのか？
    - クラス名の変更
    - package 宣言の行を削除
- execute_program.py
  - 実行時のコマンドは適切か？
  - 実行時のユーザ IO の渡し方が適切か？
  - 自作ライブラリ使用しないほうが良かったかも
  - java のコンパイル待ちの方法が join に変更したほうが良いかも
- Executor.py
  - マルチプロセス化するとかなり早くなった気がする
  - pid,exitcode が None になっているやつは timeout したやつだが、なんか多い気がする。
