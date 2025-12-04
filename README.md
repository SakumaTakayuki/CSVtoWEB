# CSV → Web登録 自動化ツール（Streamlit × Selenium × Python）

本ツールは **CSV に記載されたデータを Web フォームへ自動で入力・送信する自動化アプリケーション** です。  
UI 部分は Streamlit、ブラウザ操作は Selenium、ログ管理は SQLite + SQLAlchemy で構成されています。

---

## 🚀 特徴

- **CSV を読み込み → Selenium で自動入力 → 結果をログ保存**  
- Streamlit による操作しやすい Web UI  
- 各行ごとの **成功 / 失敗理由（入力・確認画面・予期せぬエラー）** を記録  
- SQLAlchemy + SQLite による実行ログ・詳細ログ保存  
- pytest による **自動化テストを実装済**  

---

## 🛠 技術スタック

| 分類 | 使用技術 |
|------|----------|
| 言語 | Python |
| UI | Streamlit |
| 自動操作 | Selenium WebDriver |
| DB | SQLite（SQLAlchemy ORM） |
| ログ管理 | Run / RunDetail モデル |
| テスト | pytest（Selenium部分はモックによる単体テスト） |

---

## 📁 画面イメージ（Streamlit UI）
- ダッシュボード
  <img width="1467" height="871" alt="image" src="https://github.com/user-attachments/assets/9a5f17d0-43cd-4751-8e83-78f836addc4b" />

- CSV アップロード画面
  <img width="1460" height="833" alt="image" src="https://github.com/user-attachments/assets/e57bc7a4-c7d8-4c87-9ce6-cccf07e7da71" />
  
- CSV 取込
  <img width="1476" height="870" alt="image" src="https://github.com/user-attachments/assets/68bc3865-fae3-44f0-81a9-7c8b02005a53" />
  
- 動作確認
  <img width="1480" height="870" alt="image" src="https://github.com/user-attachments/assets/fbb899e6-f905-47e9-be97-3948793ea98d" />
  
- 処理中の進捗表示
  <img width="1464" height="854" alt="image" src="https://github.com/user-attachments/assets/69d72f6a-72e3-4ebf-81ae-94aa9716af61" />
  
- Web自動登録結果
  <img width="1473" height="867" alt="image" src="https://github.com/user-attachments/assets/d34426c2-f839-4ecf-b47a-c2a145e9e0b8" />

  <img width="1454" height="865" alt="image" src="https://github.com/user-attachments/assets/ef436a43-5544-452b-a7b7-81ba67cfb4ff" />

- 実行ログ一覧（Run テーブル）
  <img width="1482" height="875" alt="image" src="https://github.com/user-attachments/assets/8e29fe7f-6567-4a5a-a52c-5909b501be64" />

- 詳細ログ（RunDetail テーブル）
  <img width="1477" height="881" alt="image" src="https://github.com/user-attachments/assets/93874037-9905-4da1-b652-a17898b41080" />
  <img width="1474" height="879" alt="image" src="https://github.com/user-attachments/assets/0f3f4a9f-3998-4fe8-a670-a55264fea7a2" />

---

## 🎥 デモ動画
https://github.com/user-attachments/assets/e273c326-2261-487c-994f-78ffcd4db0ce


---

## 🔧 セットアップ

```bash
git clone https://github.com/SakumaTakayuki/CSVtoWEB.git
cd CSVtoWEB
pip install -r requirements.txt
