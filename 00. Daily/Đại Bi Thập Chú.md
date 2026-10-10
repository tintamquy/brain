---
tags:
  - daibithapchu
  - tu-tap
---

# 📿 Theo Dõi Trì Tụng - Đại Bi Thập Chú

```dataviewjs
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

// Tính Streak
let currentStreak = 0;
let checkDate = dates.has(today) ? moment() : (dates.has(yesterday) ? moment().subtract(1, 'days') : null);

if (checkDate) {
    while (dates.has(checkDate.format("YYYY-MM-DD"))) {
        currentStreak++;
        checkDate.subtract(1, 'days');
    }
}

// Kỷ lục streak
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

dv.container.innerHTML = `
<style>
@keyframes compactFlame {
  0% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 6px #ff5722); }
  50% { transform: scale(1.06) rotate(1.5deg); filter: drop-shadow(0 0 12px #ff9800); }
  100% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 6px #ff5722); }
}

.compact-streak-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 10px 16px;
  margin: 8px 0 16px 0;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.1), rgba(255, 152, 0, 0.05));
  border: 1px solid rgba(255, 112, 67, 0.3);
}

.flame-streak-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.flame-icon-box {
  position: relative;
  width: 48px;
  height: 58px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.flame-icon-box svg {
  width: 100%;
  height: 100%;
  animation: compactFlame 1.3s infinite ease-in-out;
  transform-origin: 50% 90%;
}

.flame-streak-num {
  position: absolute;
  top: 57%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 17px;
  font-weight: 900;
  color: #fff;
  text-shadow: 0 1px 3px #000, 0 0 8px #ff3d00;
  pointer-events: none;
  font-family: system-ui, sans-serif;
}

.streak-text-main {
  display: flex;
  flex-direction: column;
}

.streak-text-main .streak-title {
  font-size: 16px;
  font-weight: 700;
  color: #ff6f00;
  line-height: 1.2;
}

.streak-text-main .streak-sub {
  font-size: 12px;
  opacity: 0.8;
}

.streak-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.streak-chip {
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 152, 0, 0.2);
  font-size: 12px;
  white-space: nowrap;
}

.streak-chip strong {
  color: var(--text-normal);
}
</style>

<div class="compact-streak-bar">
  <div class="flame-streak-wrap">
    <div class="flame-icon-box">
      <svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="fGrad" cx="50%" cy="80%" r="65%">
            <stop offset="0%" stop-color="#fff59d" />
            <stop offset="40%" stop-color="#ff9800" />
            <stop offset="85%" stop-color="#ff3d00" />
            <stop offset="100%" stop-color="#b71c1c" />
          </radialGradient>
        </defs>
        <path d="M50 4 C58 26 84 40 86 70 C88 98 72 116 50 116 C28 116 12 98 14 70 C16 40 42 26 50 4 Z" fill="url(#fGrad)" />
        <path d="M50 24 C55 38 72 50 72 72 C72 90 62 102 50 102 C38 102 28 90 28 72 C28 50 45 38 50 24 Z" fill="#fff" opacity="0.4" />
      </svg>
      <div class="flame-streak-num">${currentStreak}</div>
    </div>
    <div class="streak-text-main">
      <div class="streak-title">Chuỗi ${currentStreak} Ngày Tinh Tấn</div>
      <div class="streak-sub">${currentStreak > 0 ? "🔥 Ngọn lửa đang duy trì đều đặn" : "Bắt đầu ngày mới ngay hôm nay!"}</div>
    </div>
  </div>

  <div class="streak-chips">
    <div class="streak-chip">🏆 Kỷ lục: <strong>${longestStreak} ngày</strong></div>
    <div class="streak-chip">📿 Tổng biến: <strong>${totalCount} lần</strong></div>
    <div class="streak-chip">📅 Đã đọc: <strong>${dates.size} ngày</strong></div>
  </div>
</div>
`;
```

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
ui:
  hideTabs: true
```

---

### 📝 Hồi Hướng & Cảm Niệm
- Hôm nay tôi đã đọc được 5 lần chú đại bi rồi.
- Nguyện vãng sinh về tây phương cực lạc, đoạn trừ mọi lậu hoặc, thân tâm an lạc.
