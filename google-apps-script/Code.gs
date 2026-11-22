/**
 * Nhận dữ liệu từ thiệp cưới online Phúc Hiếu - Lâm Anh và ghi vào Google Sheet.
 *
 * - Form "Sổ lưu bút"        -> tab "Sổ lưu bút"
 * - Form "Xác nhận tham dự"  -> tab "Xác nhận tham dự"
 * Tab và dòng tiêu đề (tone Đỏ Đô #821824) được tự tạo ở lần gửi đầu tiên.
 */

const TIMEZONE = 'Asia/Ho_Chi_Minh';

const SHEETS = {
  wish: {
    name: 'Sổ lưu bút',
    headers: ['Thời gian', 'Tên', 'Lời chúc', 'Khách mời (theo link)'],
    row: (p) => [p.name, p.message, p.invite],
  },
  rsvp: {
    name: 'Xác nhận tham dự',
    headers: [
      'Thời gian',
      'Họ và tên',
      'Số điện thoại',
      'Tham dự',
      'Buổi lễ',
      'Số người',
      'Lời nhắn',
      'Khách mời (theo link)',
    ],
    row: (p) => [
      p.name,
      p.phone && p.phone[0] !== "'" ? "'" + p.phone : p.phone,
      p.attend,
      p.location,
      p.guests,
      p.message,
      p.invite,
    ],
  },
};

function doPost(e) {
  const p = (e && e.parameter) || {};
  const cfg = SHEETS[p.type];
  if (!cfg) return json_({ ok: false, error: 'unknown type' });
  if (p.website) return json_({ ok: true });

  const clean = {};
  Object.keys(p).forEach((k) => {
    clean[k] = String(p[k] || '')
      .trim()
      .slice(0, 1000)
      .replace(/^[=+\-@]/, "'$&");
  });

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(cfg.name) || ss.insertSheet(cfg.name);
    if (sh.getLastRow() === 0) {
      sh.appendRow(cfg.headers);
      sh.getRange(1, 1, 1, cfg.headers.length)
        .setFontWeight('bold')
        .setBackground('#821824')
        .setFontColor('#FAF6F0');
      sh.setFrozenRows(1);
    }
    const now = Utilities.formatDate(new Date(), TIMEZONE, 'dd/MM/yyyy HH:mm:ss');
    sh.appendRow([now].concat(cfg.row(clean)));
    return json_({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return json_({ ok: true, message: 'Lam Anh & Phuc Hieu Wedding Sheet endpoint is running' });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
