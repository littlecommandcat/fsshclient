# fssh-client

一個專門取得鳳山高中校網公告的client

[非同步請求AsyncClient](src/async.py)

[同步請求SyncClient](src/sync.py)

安裝套件
```ini
pip install -r requirements.txt
```

取得處室公告
```python
ACADEMIC       # 教務處公告
STUDENT       # 學務處公告
GENERAL       # 總務處公告
COUNSELING       # 輔導室公告
LIBRARY       # 圖書館公告
MILITARY       # 教官室公告
OTHER       # 其他公告
```