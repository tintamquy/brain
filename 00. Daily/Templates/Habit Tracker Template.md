---
tags:
  - habit-tracker
---

# 🎯 Theo Dõi Thói Quen - [TÊN THÓI QUEN]

```dataviewjs
// =========================================================================
// ⚙️ CẤU HÌNH THÓI QUEN (BẠN CHỈ CẦN SỬA 3 DÒNG DƯỚI ĐÂY KHI NHÂN BẢN TRANG MỚI)
// =========================================================================
const HABIT_NAME = "Tên Thuộc Tính";  // Ví dụ: "Ngồi Thiền", "Đọc Sách", "Chạy Bộ"...
const HABIT_UNIT = "phút";            // Đơn vị: "phút", "lần", "trang", "km"...
const HABIT_DEFAULT = 20;             // Giá trị mục tiêu gợi ý khi tạo ngày mới (ví dụ: 20 phút)
const DAILY_DIR = "00. Daily/Nhật Ký";// Thư mục lưu nhật ký hàng ngày (giữ nguyên)

// 1. Quét dữ liệu từ thư mục Nhật Ký
const pages = dv.pages('"' + DAILY_DIR + '"')
    .where(p => p[HABIT_NAME] !== undefined && Number(p[HABIT_NAME]) > 0);

const dates = new Set();
let totalCount = 0;

for (let p of pages) {
    const match = p.file.name.match(/\d{4}-\d{2}-\d{2}/);
    if (match) {
        dates.add(match[0]);
        totalCount += Number(p[HABIT_NAME]) || 0;
    }
}

const sortedDates = Array.from(dates).sort();
const todayStr = moment().format("YYYY-MM-DD");
const yesterdayStr = moment().subtract(1, 'days').format("YYYY-MM-DD");

// 2. Tính Streak hiện tại
let currentStreak = 0;
let checkDate = dates.has(todayStr) ? moment() : (dates.has(yesterdayStr) ? moment().subtract(1, 'days') : null);

if (checkDate) {
    while (dates.has(checkDate.format("YYYY-MM-DD"))) {
        currentStreak++;
        checkDate.subtract(1, 'days');
    }
}

// 3. Tính Kỷ lục Streak
let longestStreak = 0;
let tempStreak = 0;
let prevDate = null;

for (let dStr of sortedDates) {
    const d = moment(dStr);
    if (!prevDate) {
        tempStreak = 1;
    } else {
        const diff = d.diff(prevDate, 'days');
        if (diff === 1) {
            tempStreak++;
        } else if (diff > 1) {
            tempStreak = 1;
        }
    }
    if (tempStreak > longestStreak) longestStreak = tempStreak;
    prevDate = d;
}

// 4. Render Giao diện Ngọn Lửa Tối Giản
const container = dv.container;
container.innerHTML = `
<style>
.minimal-tracker-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 14px 18px;
  margin: 10px 0 16px 0;
  border-radius: 12px;
  background: var(--background-secondary);
  border: 1px solid var(--background-modifier-border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.minimal-main-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
.minimal-flame-section {
  display: flex;
  align-items: center;
  gap: 12px;
}
@keyframes flameBreathe {
  0%, 100% {
    transform: scale(1);
    filter: drop-shadow(0 0 6px rgba(255, 112, 67, 0.45));
  }
  50% {
    transform: scale(1.05) translateY(-1px);
    filter: drop-shadow(0 0 14px rgba(255, 160, 0, 0.75));
  }
}
.flame-container {
  position: relative;
  width: 44px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.flame-svg {
  width: 100%;
  height: 100%;
  animation: flameBreathe 2s infinite ease-in-out;
}
.flame-number {
  position: absolute;
  top: 56%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 16px;
  font-weight: 800;
  color: #ffffff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8), 0 0 6px #d84315;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.minimal-title-box {
  display: flex;
  flex-direction: column;
}
.minimal-streak-heading {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-normal);
  line-height: 1.25;
}
.minimal-streak-desc {
  font-size: 12px;
  color: var(--text-muted);
}
.minimal-stats-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.minimal-stat-item {
  padding: 4px 10px;
  border-radius: 6px;
  background: var(--background-primary);
  border: 1px solid var(--background-modifier-border);
  font-size: 12px;
  color: var(--text-muted);
}
.minimal-stat-item strong {
  color: var(--text-normal);
  font-weight: 600;
}
.minimal-btn-create {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 14px;
  border-radius: 8px;
  background: var(--interactive-accent);
  color: var(--text-on-accent);
  font-size: 13.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease;
}
.minimal-btn-create:hover { opacity: 0.9; }
.minimal-btn-create:active { transform: translateY(1px); }
</style>

<div class="minimal-tracker-card">
  <div class="minimal-main-row">
    <div class="minimal-flame-section">
      <div class="flame-container">
        <svg class="flame-svg" viewBox="0 0 64 80" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="minimalFlameGrad" x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stop-color="#e64a19" />
              <stop offset="55%" stop-color="#ff9800" />
              <stop offset="100%" stop-color="#ffeb3b" />
            </linearGradient>
            <linearGradient id="innerCoreGrad" x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stop-color="#ff9800" />
              <stop offset="100%" stop-color="#ffffff" />
            </linearGradient>
          </defs>
          <path d="M32 3 C35 14 43 20 48 18 C46 29 58 35 59 48 C61 63 53 76 43 83 C34 90 20 89 12 80 C5 70 6 56 10 44 C13 35 19 32 20 23 C24 27 27 24 28 15 C29 9 31 3 32 3 Z" fill="url(#minimalFlameGrad)" />
          <path d="M32 40 C35 48 40 54 40 62 C40 70 36 74 32 74 C28 74 24 70 24 62 C24 54 29 48 32 40 Z" fill="url(#innerCoreGrad)" opacity="0.8" />
        </svg>
        <span class="flame-number">${currentStreak}</span>
      </div>

      <div class="minimal-title-box">
        <div class="minimal-streak-heading">Chuỗi ${currentStreak} Ngày ${HABIT_NAME}</div>
        <div class="minimal-streak-desc">${currentStreak > 0 ? "Duy trì đều đặn mỗi ngày" : "Bắt đầu ngay hôm nay"}</div>
      </div>
    </div>

    <div class="minimal-stats-group">
      <div class="minimal-stat-item">Kỷ lục: <strong>${longestStreak} ngày</strong></div>
      <div class="minimal-stat-item">Tổng: <strong>${totalCount} ${HABIT_UNIT}</strong></div>
      <div class="minimal-stat-item">Đã làm: <strong>${dates.size} ngày</strong></div>
    </div>
  </div>

  <button class="minimal-btn-create" id="btn-daily-action">
    + Viết Nhật Ký Hôm Nay
  </button>
</div>
`;

// 5. Nút bấm tạo / cập nhật file nhật ký ngày
const btn = container.querySelector("#btn-daily-action");
if (btn) {
  btn.onclick = async () => {
    const today = moment().format("YYYY-MM-DD");
    const filePath = DAILY_DIR + "/" + today + ".md";
    let file = app.vault.getAbstractFileByPath(filePath);

    if (!file) {
      const templateLines = [
        "---",
        "tags:",
        "  - daily",
        HABIT_NAME + ": " + HABIT_DEFAULT,
        "---",
        "",
        "# 🌿 Nhật ký ngày " + today,
        "",
        "### 🎯 Thói Quen Hàng Ngày",
        "- " + HABIT_NAME + ": (Chạm vào số ở thuộc tính trên đầu trang để cập nhật)",
        "",
        "### ☀️ Việc Quan Trọng Hôm Nay",
        "- [ ] ",
        "",
        "### 🌙 Nhìn Lại & Buông Xả",
        "- Thân tâm an lạc, buông bỏ lo toan."
      ];
      file = await app.vault.create(filePath, templateLines.join("\n"));
    } else {
      const content = await app.vault.read(file);
      if (!content.includes(HABIT_NAME)) {
        let updated = content;
        if (updated.startsWith("---")) {
          updated = updated.replace(/^---\n/, "---\n" + HABIT_NAME + ": " + HABIT_DEFAULT + "\n");
        } else {
          updated = "---\n" + HABIT_NAME + ": " + HABIT_DEFAULT + "\n---\n\n" + updated;
        }
        await app.vault.modify(file, updated);
      }
    }

    if (file) {
      app.workspace.getLeaf(false).openFile(file);
    }
  };
}
```

```heatmap-tracker
property: Tên Thuộc Tính
path: 00. Daily/Nhật Ký
separateMonths: true
```

---

### 📝 Ghi Chú & Mục Tiêu
- Viết các mục tiêu, cảm nhận hoặc lưu ý cho thói quen này vào đây.
