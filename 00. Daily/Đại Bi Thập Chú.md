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

const container = dv.container;
container.innerHTML = `
<style>
/* --- PHONG CÁCH KÍNH MỜ (GLASSMORPHISM) --- */
.anime-glass-card {
  position: relative;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  border-left: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.12);
  padding: 16px 20px;
  margin: 10px 0 18px 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.anime-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
}

.anime-flame-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* --- HOẠT HỌA ANIME SKETCH FLAME (GIẬT NHẸ KIỂU CEL ANIME) --- */
@keyframes animeFlameFlicker {
  0% { transform: scale(1) rotate(-1deg); }
  25% { transform: scale(1.05) rotate(2deg) skewX(1deg); }
  50% { transform: scale(0.97) rotate(-2deg); }
  75% { transform: scale(1.04) rotate(1deg) skewX(-1deg); }
  100% { transform: scale(1) rotate(-1deg); }
}

.anime-flame-svg {
  width: 65px;
  height: 76px;
  filter: drop-shadow(0 0 10px rgba(255, 87, 34, 0.5));
  animation: animeFlameFlicker 1.1s steps(6, end) infinite;
  transform-origin: 50% 90%;
  flex-shrink: 0;
}

.anime-streak-info {
  display: flex;
  flex-direction: column;
}

.anime-streak-title {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.3px;
  color: #ff7043;
  line-height: 1.25;
}

.anime-streak-sub {
  font-size: 12px;
  opacity: 0.75;
  margin-top: 2px;
}

/* --- STATS PILLS (KÍNH MỜ) --- */
.anime-stats-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.anime-pill {
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.anime-pill strong {
  color: #ffab40;
}

/* --- NÚT BẤM 1 CHẠM TẠO NHẬT KÝ HÔM NAY --- */
.anime-action-row {
  display: flex;
  width: 100%;
}

.btn-open-daily {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.22), rgba(255, 167, 38, 0.16));
  border: 1px solid rgba(255, 112, 67, 0.4);
  color: var(--text-normal);
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-open-daily:hover, .btn-open-daily:active {
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.4), rgba(255, 167, 38, 0.3));
  border-color: rgba(255, 112, 67, 0.7);
  transform: translateY(-1px);
}
</style>

<div class="anime-glass-card">
  <div class="anime-card-top">
    <div class="anime-flame-wrap">
      <!-- SVG NGỌN LỬA ANIME SKETCH VỚI NÉT VẼ TAY & INK LINES -->
      <svg class="anime-flame-svg" viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
        <g>
          <!-- Nét phác thảo đốm lửa xung quanh (Anime Sparks) -->
          <path d="M18 42 Q14 36 20 30 Q22 38 18 42" fill="#ff5722" stroke="#1c0b05" stroke-width="2"/>
          <path d="M102 36 Q110 30 104 24 Q100 32 102 36" fill="#ff9800" stroke="#1c0b05" stroke-width="2"/>
          <path d="M30 16 Q28 10 34 8 Q32 14 30 16" fill="#ffeb3b" stroke="#1c0b05" stroke-width="1.8"/>
          
          <!-- Lớp ngọn lửa lớn bên ngoài (Nét viền mực Anime đậm, tỉa nhọn phóng khoáng) -->
          <path d="M60 8 C62 22 72 30 82 26 C80 38 96 42 102 60 C108 76 104 98 90 116 C76 132 44 134 28 122 C14 110 10 88 18 68 C22 54 34 50 34 38 C42 44 48 40 50 24 C54 16 58 8 60 8 Z" 
                fill="#ff3d00" stroke="#1a0c02" stroke-width="3.5" stroke-linejoin="round"/>
          
          <!-- Lớp lửa giữa cel-shade vàng cam -->
          <path d="M60 28 C64 40 78 50 82 70 C86 88 78 106 62 112 C46 110 36 96 40 76 C42 62 52 54 56 42 C57 36 59 30 60 28 Z" 
                fill="#ff9800" stroke="#1c0b05" stroke-width="2.5" stroke-linejoin="round"/>
          
          <!-- Lõi lửa sáng anime -->
          <path d="M60 52 C65 62 72 72 72 84 C72 96 66 104 60 104 C54 104 48 96 48 84 C48 72 55 62 60 52 Z" 
                fill="#fff9c4" stroke="#1c0b05" stroke-width="2.2" stroke-linejoin="round"/>
          
          <!-- Nét gạch mực phác thảo (Manga Ink Hatching) -->
          <path d="M28 92 L22 98 M34 104 L28 110 M88 92 L94 98 M82 104 L88 110" 
                stroke="#1a0c02" stroke-width="2.2" stroke-linecap="round"/>
          
          <!-- Số Streak phong cách Manga Ink Stencil (To, rõ nét, viền đen cực ngầu) -->
          <text x="60" y="93" text-anchor="middle" font-family="'Impact', 'Arial Black', sans-serif" 
                font-weight="900" font-size="28" fill="#ffffff" stroke="#1a0c02" stroke-width="5" 
                paint-order="stroke fill">${currentStreak}</text>
        </g>
      </svg>

      <div class="anime-streak-info">
        <div class="anime-streak-title">Chuỗi ${currentStreak} Ngày Tinh Tấn</div>
        <div class="anime-streak-sub">${currentStreak > 0 ? "🔥 Năng lượng tu tập đang duy trì mạnh mẽ!" : "Hãy bắt đầu ngày mới ngay bây giờ!"}</div>
      </div>
    </div>

    <div class="anime-stats-pills">
      <div class="anime-pill">🏆 Kỷ lục: <strong>${longestStreak} ngày</strong></div>
      <div class="anime-pill">📿 Tổng biến: <strong>${totalCount} lần</strong></div>
      <div class="anime-pill">📅 Đã đọc: <strong>${dates.size} ngày</strong></div>
    </div>
  </div>

  <!-- NÚT BẤM 1 CHẠM DÀNH RIÊNG CHO ĐIỆN THOẠI & MÁY TÍNH -->
  <div class="anime-action-row">
    <button class="btn-open-daily" id="btn-quick-daily">
      ⚡ <span>Bấm Vào Đây Để Viết Nhật Ký Hôm Nay (Tự Động Ra Mẫu)</span>
    </button>
  </div>
</div>
`;

// Gán sự kiện click: Tự động chạy lệnh mở Daily note có sẵn template
const quickBtn = container.querySelector("#btn-quick-daily");
if (quickBtn) {
  quickBtn.onclick = () => {
    app.commands.executeCommandById("daily-notes");
  };
}
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
