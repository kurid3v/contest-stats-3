# PREHSG Contest Hub

Một ứng dụng web full-stack hiện đại để quản lý các cuộc thi PREHSG với các hoạt động quản trị an toàn, quản lý CRUD theo thời gian thực, và giao diện người dùng đẹp mắt.

---

## Mục lục

- [Khởi động nhanh](#khởi-động-nhanh)
- [Công nghệ](#công-nghệ)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [API Endpoints](#api-endpoints)
- [Bảng điều khiển quản trị](#bảng-điều-khiển-quản-trị)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)

---

## Khởi động nhanh

### Yêu cầu
- **Node.js 18+** - https://nodejs.org/
- **Python 3.9+** - https://www.python.org/

### Cài đặt tự động (Windows)
```bash
setup.bat
```

### Cài đặt thủ công

**Backend** (Terminal 1):
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python init_db.py
python -m uvicorn main:app --reload
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm install
npm run dev
```

**Truy cập ứng dụng:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Bảng điều khiển quản trị: http://localhost:5173/a9F2kQ7mB41xZp8tR0Ls/ (Mật khẩu: `chtcoder@prehsg`)

---

## Công nghệ

| Lớp | Công nghệ | Phiên bản | Mục đích |
|-------|-----------|---------|---------|
| **Frontend** | React | 18.2.0 | Framework UI |
| | TypeScript | 5.2.2 | Kiểm tra kiểu |
| | Vite | 5.0 | Build tool |
| | Tailwind CSS | 3.3.6 | Styling |
| | React Router | 6.18 | Định tuyến |
| | Axios | 1.6.2 | HTTP client |
| | Radix UI | Latest | Accessible components |
| | Lucide React | 0.555 | Icons |
| **Backend** | FastAPI | 0.104.1 | Web framework |
| | SQLModel | 0.0.14 | ORM + Type hints |
| | SQLAlchemy | 2.0.23 | Database layer |
| | Uvicorn | 0.24.0 | ASGI server |
| | SQLite | Built-in | Cơ sở dữ liệu |
| | python-dotenv | 1.1.1 | Cấu hình |

**Điểm nổi bật của kiến trúc:**
- REST API với nested resources
- Xác thực dựa trên token với hết hạn
- Caching trong bộ nhớ với cache invalidation
- Indexing cơ sở dữ liệu (class_level, year, contest_id, item_number)
- GZIP compression middleware
- Cascade delete relationships

---

## Cấu trúc dự án

```
contest-stats-3/
├── frontend/                          # Ứng dụng React + Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx             # Header điều hướng
│   │   │   ├── Sidebar.tsx            # Sidebar chọn năm
│   │   │   ├── ContestCard.tsx        # Thẻ hiển thị cuộc thi
│   │   │   ├── SolutionModal.tsx      # Modal popup giải pháp
│   │   │   ├── Button.tsx             # Custom button component
│   │   │   └── AdminPanel.tsx         # Interface CRUD quản trị
│   │   ├── pages/
│   │   │   ├── HomePage.tsx           # Trang liệt kê cuộc thi
│   │   │   └── AdminInputPage.tsx     # Trang quản lý quản trị
│   │   ├── lib/
│   │   │   └── api.ts                 # Axios HTTP client
│   │   ├── App.tsx                    # Router + routes
│   │   ├── main.tsx                   # Entry point
│   │   └── index.css                  # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── index.html
│
├── backend/                           # Ứng dụng FastAPI
│   ├── main.py                        # FastAPI setup + middleware
│   ├── models.py                      # SQLModel ORM definitions
│   ├── database.py                    # Cấu hình DB
│   ├── cache.py                       # Hệ thống cache trong bộ nhớ
│   ├── init_db.py                     # Khởi tạo cơ sở dữ liệu
│   ├── routers/
│   │   ├── contests.py                # Contest/Solution CRUD
│   │   └── auth.py                    # Xác thực (password → token)
│   ├── requirements.txt
│   ├── __pycache__/
│   └── contest_hub.db                 # Cơ sở dữ liệu SQLite
│
├── README.md                          # File này
├── setup.bat                          # Script cài đặt Windows
├── setup.sh                           # Script cài đặt Linux/macOS
└── test_services.py                   # Tiện ích kiểm tra dịch vụ
```

---

## Kiến trúc hệ thống

### Luồng cấp cao

```
┌─────────────────────────────────────────────────┐
│    FRONTEND (React tại localhost:5173)          │
│  ┌──────────────────────────────────────────┐   │
│  │ Header + Sidebar + Hiển thị ContestCard  │   │
│  │ Hoặc AdminInputPage (Bảo vệ bằng pwd)   │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
                  │ Axios HTTP Client
                  │ (api.ts với xác thực token)
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│   BACKEND (FastAPI tại localhost:8000)          │
│  ┌──────────────────────────────────────────┐   │
│  │ routers/contests.py (CRUD endpoints)     │   │
│  │ routers/auth.py (Password → Token)       │   │
│  │ Middleware: CORS, GZIPMiddleware         │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
                  │ SQLModel ORM
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│   DATABASE (SQLite - contest_hub.db)            │
│  ┌──────────────────────────────────────────┐   │
│  │ Bảng Contest (id, class_level, year...)  │   │
│  │ Bảng Solution (id, contest_id, item...)   │   │
│  │ Indexes: idx_class_year, idx_year, etc.  │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Chu kỳ Request/Response

1. **Hành động người dùng** → Click nút trong React component
2. **Gọi API** → Yêu cầu Axios với token xác thực (nếu hoạt động quản trị)
3. **Định tuyến** → FastAPI router khớp endpoint
4. **Xử lý** → Logic nghiệp vụ + hoạt động cơ sở dữ liệu
5. **Phản hồi** → Dữ liệu JSON trả lại frontend
6. **Re-render** → React component cập nhật với dữ liệu mới

### Quan hệ Components

```
App.tsx (Router)
├── HomePage.tsx
│   ├── Header.tsx (Chọn lớp học)
│   └── Sidebar.tsx (Accordion năm)
│       └── ContestCard.tsx (Hiển thị cuộc thi)
│           └── SolutionModal.tsx (Popup với giải pháp)
│
└── AdminInputPage.tsx (Secret URL: /a9F2kQ7mB41xZp8tR0Ls/)
    └── AdminPanel.tsx (Login + Full CRUD)
        ├── Quản lý Cuộc thi (Tạo/Sửa/Xóa)
        └── Quản lý Giải pháp (Thêm/Xóa giải pháp)
```

---

## API Endpoints

### Public Endpoints

**Lấy tất cả cuộc thi**
```
GET /contests
Response: List[ContestRead] với nested solutions
Cache: Được bật (vô hiệu hóa khi mutations)
```

### Admin Endpoints (Yêu cầu Token)

**Xác thực**
```
POST /auth/login
Body: { "password": "chtcoder@prehsg" }
Response: { "access_token": "...", "token_type": "bearer" }
```

**Quản lý Cuộc thi**
```
POST /contests           # Tạo cuộc thi mới
PUT /contests/{id}       # Cập nhật cuộc thi
DELETE /contests/{id}    # Xóa cuộc thi (cascade xóa solutions)
```

**Quản lý Giải pháp**
```
GET /contests/{id}/solutions           # Liệt kê giải pháp cho cuộc thi
POST /contests/{id}/solutions          # Thêm giải pháp
DELETE /contests/{id}/solutions/{id}   # Xóa giải pháp
```

### Quan hệ Cơ sở dữ liệu

```
Contest (1) ↔ (*) Solution
├─ id (PK)           ├─ id (PK)
├─ class_level       ├─ contest_id (FK) → CASCADE DELETE
├─ year              ├─ item_number
├─ pre_number        ├─ title
├─ contest_url       └─ solution_url
├─ solution_url      
└─ solutions: List[Solution]
```

---

## Bảng điều khiển quản trị

### Truy cập & Bảo mật

**URL**: `http://localhost:5173/a9F2kQ7mB41xZp8tR0Ls/`

**Các lớp bảo mật:**
1. Đường dẫn URL bí mật (che giấu)
2. Xác thực bằng mật khẩu (đăng nhập)
3. Uỷ quyền API dựa trên token (hết hạn: 30 phút)
4. Cache invalidation khi tất cả hoạt động ghi

### Tính năng

**Đăng nhập**
- Nhập mật khẩu: `chtcoder@prehsg`
- Nhận JWT token cho các lệnh gọi API
- Token được lưu trữ tự động trong localStorage

**Quản lý Cuộc thi**
- ✅ Xem tất cả cuộc thi trong bảng
- ✅ Tạo cuộc thi mới (class_level, năm, pre_number, URLs)
- ✅ Chỉnh sửa cuộc thi hiện có
- ✅ Xóa cuộc thi (xóa tất cả giải pháp liên quan)
- ✅ Cập nhật theo thời gian thực

**Quản lý Giải pháp**
- ✅ Thêm giải pháp vào cuộc thi (item_number, tiêu đề, solution_url)
- ✅ Xem giải pháp mỗi cuộc thi
- ✅ Xóa giải pháp cụ thể
- ✅ Cập nhật danh sách theo thời gian thực

**Lưu trữ dữ liệu**
- Tất cả thay đổi được lưu vào cơ sở dữ liệu SQLite
- Quan hệ được duy trì với cascade deletes
- Cơ sở dữ liệu được indexing để truy vấn nhanh

---

## Hướng dẫn sử dụng

### Cho người dùng thông thường

1. **Truy cập ứng dụng** tại http://localhost:5173
2. **Chọn Lớp học** từ dropdown header
3. **Xem Năm** trong sidebar bên trái
4. **Click một Cuộc thi** để xem chi tiết
5. **Click nút "Solution"** để xem giải pháp trong popup
6. **Click liên kết giải pháp** để mở tài nguyên bên ngoài

### Cho quản trị viên

1. **Điều hướng đến Bảng điều khiển quản trị** tại http://localhost:5173/a9F2kQ7mB41xZp8tR0Ls/
2. **Nhập Mật khẩu** `chtcoder@prehsg`
3. **Quản lý Cuộc thi**:
   - Điền biểu mẫu với lớp học, năm, pre-number, URLs
   - Click "Add Contest" hoặc "Update" cho cuộc thi hiện có
   - Click icon xóa để loại bỏ
4. **Quản lý Giải pháp**:
   - Chọn một cuộc thi từ bảng
   - Thêm giải pháp với item number và URLs
   - Click icon xóa để loại bỏ giải pháp
5. **Tất cả Thay đổi Lưu ngay** vào cơ sở dữ liệu

---

## Hướng dẫn cài đặt

### Tùy chọn 1: Windows (Tự động)

```bash
# Chạy script cài đặt
setup.bat

# Điều này sẽ:
# 1. Tạo môi trường ảo Python
# 2. Cài đặt dependencies backend
# 3. Khởi tạo cơ sở dữ liệu với dữ liệu mẫu
# 4. Cài đặt dependencies frontend
# 5. Hiển thị hướng dẫn khởi động
```

### Tùy chọn 2: macOS/Linux

```bash
chmod +x setup.sh
./setup.sh
```

### Tùy chọn 3: Cài đặt thủ công

**Bước 1: Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # hoặc venv\Scripts\activate trên Windows
pip install -r requirements.txt
python init_db.py
python -m uvicorn main:app --reload
```

**Bước 2: Frontend** (terminal mới)
```bash
cd frontend
npm install
npm run dev
```

### Build cho Production

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run build  # Tạo folder dist/
```

---

## Phát triển & Kiểm tra

### Kiểm tra sức khỏe
```bash
curl http://localhost:8000/health
# Response: {"status": "ok"}
```

### Tài liệu API
- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Yêu cầu mẫu

**Lấy tất cả cuộc thi**
```bash
curl http://localhost:8000/contests | json_pp
```

**Đăng nhập (Lấy Token)**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "chtcoder@prehsg"}'
```

**Tạo Cuộc thi** (yêu cầu token)
```bash
curl -X POST http://localhost:8000/contests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "class_level": 9,
    "year": 2025,
    "pre_number": 1,
    "contest_url": "https://example.com",
    "solution_url": "https://example.com"
  }'
```

---

## Tối ưu hóa hiệu suất

1. **Caching trong bộ nhớ** - GET /contests được cache, vô hiệu hóa khi mutations
2. **Indexing cơ sở dữ liệu** - Indexes trên class_level, year, contest_id, item_number
3. **GZIP Compression** - Tất cả phản hồi API được nén
4. **Connection Pooling** - Tái sử dụng kết nối cơ sở dữ liệu
5. **Token Expiration** - Thời gian sống token 30 phút cho bảo mật

---

## Mô tả File

### Các file Frontend chính

| File | Mục đích |
|------|---------|
| `App.tsx` | Main router, định nghĩa routes bao gồm đường dẫn quản trị bí mật |
| `HomePage.tsx` | Hiển thị cuộc thi với lọc class/năm |
| `AdminInputPage.tsx` | Interface quản trị bảo vệ bằng mật khẩu |
| `Header.tsx` | Dropdown chọn mức độ lớp |
| `Sidebar.tsx` | Accordion năm với lọc cuộc thi |
| `ContestCard.tsx` | Hiển thị cuộc thi riêng lẻ với nút giải pháp |
| `SolutionModal.tsx` | Modal popup hiển thị giải pháp cho cuộc thi |
| `lib/api.ts` | Axios client với xác thực token |

### Các file Backend chính

| File | Mục đích |
|------|---------|
| `main.py` | FastAPI app setup, middleware, lifespan |
| `models.py` | SQLModel definitions (Contest, Solution) + indexes |
| `database.py` | Cấu hình SQLite, connection pooling |
| `cache.py` | Hệ thống cache trong bộ nhớ cho cuộc thi |
| `init_db.py` | Khởi tạo cơ sở dữ liệu với dữ liệu mẫu |
| `routers/contests.py` | CRUD endpoints cho cuộc thi & giải pháp |
| `routers/auth.py` | Xác thực bằng mật khẩu, tạo token |

---

## Khắc phục sự cố

**Backend không khởi động?**
- Kiểm tra Python 3.9+ được cài đặt: `python --version`
- Xác minh dependencies: `pip list | grep fastapi`
- Kiểm tra port 8000 không được sử dụng: `lsof -i :8000` (macOS/Linux)

**Frontend không khởi động?**
- Kiểm tra Node 18+ được cài đặt: `node --version`
- Xóa node_modules và cài đặt lại: `rm -rf node_modules && npm install`
- Kiểm tra port 5173 không được sử dụng: `netstat -an | grep 5173` (Windows)

**Vấn đề cơ sở dữ liệu?**
- Xóa contest_hub.db và khởi tạo lại: `python init_db.py`
- Kiểm tra venv được kích hoạt trước khi chạy lệnh

**Bảng điều khiển quản trị không tải?**
- Xác minh URL chính xác: `http://localhost:5173/a9F2kQ7mB41xZp8tR0Ls/`
- Kiểm tra backend chạy trên cổng 8000
- Kiểm tra mật khẩu chính xác: `chtcoder@prehsg`

---

## Giấy phép

PREHSG Contest Hub - Được xây dựng để quản lý cuộc thi PREHSG.
