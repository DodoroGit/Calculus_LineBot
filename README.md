# 微積分學習輔助系統（Flask + LINE Bot + PostgreSQL）

本專案是一個結合 Python Flask 後端、基本前端技術與 LINE Bot 機器人整合的全端應用系統，旨在提供學生透過 LINE 互動進行微積分學習，並記錄學生學習歷程與測驗結果，作為教學與研究之用。

---

## 🔧 使用技術與架構

### ✅ 前端（Frontend）
- HTML / CSS / JavaScript（原生語法）
- Bootstrap ：設計響應式版面與按鈕介面
- jQuery：增強前端互動功能與 DOM 操作
- 應用於登入頁面、章節內容與測驗區顯示

### ✅ 後端（Backend）
- Python Flask：作為伺服器框架與 API 控制器
- Flask-SQLAlchemy：整合資料庫操作
- LINE Messaging API：
  - QuickReply 快速選單
  - TemplateMessage 按鈕選單
  - LIFF 頁面導入
- Webhook 設計：處理 LINE Bot 傳入訊息與事件

### ✅ 資料庫（Database）
- PostgreSQL
- pgAdmin 管理與查詢資料
- 使用原生 SQL 建立與操作三個核心資料表：
  - `register_user`：使用者登入與身分紀錄
  - `test_record`：學生測驗作答紀錄
  - `important_record`：閱讀章節與時間追蹤

### ✅ 部署環境（Deployment）
- Heroku 雲端平台
- Heroku PostgreSQL 作為資料庫儲存方案

---

## 🚀 系統功能介紹

### 📘 課程內容規劃
本系統以五個核心章節為主軸，每章節提供：
-  **重點整理**：章節核心觀念統整
-  **測驗區**：多題選擇題練習並即時記錄成績

課程章節包含：
1. 極限（Limit）
2. 連續（Continuity）
3. 微分 I（Differentiation I）
4. 微分 II（Differentiation II）
5. 微分的應用（Applications of Derivatives）

### 🤖 LINE Bot 整合
- 學生可透過 LINE 輕鬆登入系統，並進行互動式操作
- 提供快速選單與按鈕式選擇操作介面
- 將 LIFF 頁面導入各個章節與功能（如登入、作答頁面）

### 👤 使用者登入機制
- 學生登入需提供班級、姓名與學號
- 系統驗證並綁定 LINE 使用者 ID（LineID）
- 避免重複註冊與非課程學生登入

### 📊 學習紀錄與行為追蹤
系統會將以下學生行為儲存進資料庫中：
- 測驗紀錄：題目編號、作答內容、正確與否、使用時間
- 閱讀紀錄：閱讀章節、閱讀時間、閱讀順序

### 🧪 教學與研究應用
- 所有資料皆可用於後續學習成效分析與教學研究
- 資料可結合學術研究進行論文撰寫或課程設計優化

---

## 📂 主要路由與功能說明

| 路由 | 說明 |
|------|------|
| `/login` | 學生登入介面（LIFF 頁面） |
| `/limtest` ～ `/diffApplytest` | 各章節測驗頁面 |
| `/limPoint` ～ `/diffApply` | 各章節重點整理頁面 |
| `/callback` | LINE Bot webhook 事件處理 |
| `/createdb` | 初始化或重建資料表（開發用途） |

---

## 📝 開發者備註

- 本專案為開發者初次接觸 Web 系統之作品，參考多方教學與官方文件實作

---
