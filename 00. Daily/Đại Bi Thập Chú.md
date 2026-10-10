---
tags:
  - daibithapchu
  - tu-tap
---

# 📿 Nhật Ký Trì Tụng - Đại Bi Thập Chú

```dataviewjs
// 1. Lấy dữ liệu các ngày từ thư mục 00. Daily
const pages = dv.pages('"00. Daily"')
    .where(p => p["Đại Bi Thập Chú"] !== undefined && Number(p["Đại Bi Thập Chú"]) > 0);

const dates = new Set();
let totalCount = 0;

for (let p of pages) {
    const match = p.file.name.match(/\d{4}-\d{2}-\d{2}/);
    if (match) {
        dates.add(match[0]);
        totalCount += Number(p["Đại Bi Thập Chú"]) || 0;
    }
}

const sortedDates = Array.from(dates).sort();
const today = moment().format("YYYY-MM-DD");
const yesterday = moment().subtract(1, 'days').format("YYYY-MM-DD");

// 2. Tính Streak hiện tại
let currentStreak = 0;
let checkDate = dates.has(today) ? moment() : (dates.has(yesterday) ? moment().subtract(1, 'days') : null);

if (checkDate) {
    while (dates.has(checkDate.format("YYYY-MM-DD"))) {
        currentStreak++;
        checkDate.subtract(1, 'days');
    }
}

// 3. Tính Longest Streak
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

// 4. Render Widget Ngọn Lửa Nhấp Nháy + Streak
const container = dv.container;
container.innerHTML = `
<style>
@keyframes flamePulse {
  0% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 8px #ff4500) drop-shadow(0 0 16px #ff9800); }
  35% { transform: scale(1.08) rotate(2deg); filter: drop-shadow(0 0 16px #ff3d00) drop-shadow(0 0 28px #ffc107); }
  70% { transform: scale(0.97) rotate(-2deg); filter: drop-shadow(0 0 10px #f44336) drop-shadow(0 0 20px #ff9800); }
  100% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 8px #ff4500) drop-shadow(0 0 16px #ff9800); }
}

@keyframes innerFlicker {
  0%, 100% { opacity: 0.9; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.15) translateY(-3px); }
}

.streak-card {
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 16px;
  padding: 18px 24px;
  margin: 12px 0 20px 0;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.12), rgba(255, 152, 0, 0.05));
  border: 1px solid rgba(255, 112, 67, 0.35);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.flame-box {
  position: relative;
  width: 90px;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flame-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  animation: flamePulse 1.4s infinite ease-in-out;
  transform-origin: 50% 90%;
}

.flame-inner {
  animation: innerFlicker 0.9s infinite alternate ease-in-out;
  transform-origin: 50% 80%;
}

.streak-number-overlay {
  position: absolute;
  top: 56%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 26px;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.9), 0 0 10px #ff3d00, 0 0 20px #ff1744;
  pointer-events: none;
  font-family: 'Segoe UI', system-ui, sans-serif;
  letter-spacing: -0.5px;
}

.streak-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.streak-title {
  font-size: 20px;
  font-weight: 700;
  color: #ff6f00;
  display: flex;
  align-items: center;
  gap: 6px;
}

.streak-stats-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 4px;
}

.streak-stat-badge {
  display: flex;
  flex-direction: column;
  padding: 6px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 152, 0, 0.2);
}

.streak-stat-label {
  font-size: 11px;
  opacity: 0.75;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.streak-stat-val {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-normal);
}
</style>

<div class="streak-card">
  <div class="flame-box">
    <svg class="flame-svg" viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="flameOuterGrad" cx="50%" cy="80%" r="65%">
          <stop offset="0%" stop-color="#ffeb3b" />
          <stop offset="40%" stop-color="#ff9800" />
          <stop offset="75%" stop-color="#ff3d00" />
          <stop offset="100%" stop-color="#d50000" />
        </radialGradient>
        <radialGradient id="flameCoreGrad" cx="50%" cy="75%" r="50%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="50%" stop-color="#fff59d" />
          <stop offset="100%" stop-color="#ffb74d" />
        </radialGradient>
      </defs>
      <!-- Outer Flame -->
      <path d="M50 4 C58 26 84 40 86 70 C88 98 72 116 50 116 C28 116 12 98 14 70 C16 40 42 26 50 4 Z" fill="url(#flameOuterGrad)" />
      <!-- Middle Flame tongue -->
      <path d="M50 18 C55 35 74 48 74 72 C74 92 63 106 50 106 C37 106 26 92 26 72 C26 48 45 35 50 18 Z" fill="#ff7043" opacity="0.75" />
      <!-- Inner Core -->
      <path class="flame-inner" d="M50 36 C54 48 64 58 64 76 C64 90 58 100 50 100 C42 100 36 90 36 76 C36 58 46 48 50 36 Z" fill="url(#flameCoreGrad)" />
    </svg>
    <div class="streak-number-overlay">${currentStreak}</div>
  </div>

  <div class="streak-info">
    <div class="streak-title">
      🔥 Chuỗi Tinh Tấn: <span>${currentStreak} Ngày</span>
    </div>
    <div class="streak-stats-row">
      <div class="streak-stat-badge">
        <span class="streak-stat-label">🏆 Kỷ lục</span>
        <span class="streak-stat-val">${longestStreak} ngày</span>
      </div>
      <div class="streak-stat-badge">
        <span class="streak-stat-label">📿 Tổng biến</span>
        <span class="streak-stat-val">${totalCount} lần</span>
      </div>
      <div class="streak-stat-badge">
        <span class="streak-stat-label">📅 Ngày thực hành</span>
        <span class="streak-stat-val">${dates.size} ngày</span>
      </div>
    </div>
  </div>
</div>
`;
```

---

### 📊 Bản Đồ Nhiệt Tu Tập (Heatmap)

```heatmap-tracker
property: Đại Bi Thập Chú
path: 00. Daily
tags:
  - "#daibithapchu"
year: 2026
separateMonths: true
showCurrentDayBorder: true
colorScheme:
  paletteName: default
```

---

### 📝 Tâm Nguyện & Hồi Hướng
- Hôm nay tôi đã đọc được 5 lần chú đại bi rồi.
- Tôi nguyện vãng sinh về tây phương cực lạc tránh xa những phiền trược, phóng dật tán loạn, một lòng muốn đoạn diệt tất thảy mọi lậu hoặc đạt được niết bàn hạnh phúc thật sự chân thật.
