import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFont

SRC_DIR = r"D:\HPEDAH\assets"
DST_DIR = r"e:\hpedwla\assets"

os.makedirs(os.path.join(DST_DIR, "fonts"), exist_ok=True)
os.makedirs(os.path.join(DST_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(DST_DIR, "images", "demo"), exist_ok=True)

# 1. Copy fonts and audio
shutil.copy2(
    os.path.join(SRC_DIR, "fonts", "1ftv-vip-high-spirited-20250715023627-elsyz.otf"),
    os.path.join(DST_DIR, "fonts", "vip-high-spirited.otf"),
)
shutil.copy2(
    os.path.join(SRC_DIR, "fonts", "fz-myeverything-20250715023740-pqefv.ttf"),
    os.path.join(DST_DIR, "fonts", "fz-myeverything.ttf"),
)
shutil.copy2(
    os.path.join(SRC_DIR, "audio", "beautiful_in_white.mp3"),
    os.path.join(DST_DIR, "audio", "beautiful_in_white.mp3"),
)
shutil.copy2(
    os.path.join(SRC_DIR, "images", "14_jpeg-20260713130800-eqej_.jpg"),
    os.path.join(DST_DIR, "images", "paper_texture.jpg"),
)

# 2. Recolor fine botanicals to Velvet Rosé Wine (#6B1D2F) & Dusty Rose (#D8B4B8)
def tint_rgba(src_path, dst_path, rgb, alpha_scale=1.0):
    im = Image.open(src_path).convert("RGBA")
    _, _, _, a = im.split()
    if alpha_scale != 1.0:
        a = a.point(lambda p: max(0, min(255, int(p * alpha_scale))))
    colored = Image.merge(
        "RGBA",
        (
            Image.new("L", im.size, rgb[0]),
            Image.new("L", im.size, rgb[1]),
            Image.new("L", im.size, rgb[2]),
            a,
        ),
    )
    colored.save(dst_path, "PNG", optimize=True)

VELVET_WINE = (130, 24, 36)     # #821824 (Đỏ đô sang trọng)
DUSTY_ROSE = (223, 182, 186)    # #DFB6BA
CHAMPAGNE = (200, 169, 126)     # #C8A97E

tint_rgba(
    os.path.join(SRC_DIR, "images", "15_png-20260713130800-eltia.png"),
    os.path.join(DST_DIR, "images", "crest_wine.png"),
    VELVET_WINE,
    alpha_scale=0.92,
)
tint_rgba(
    os.path.join(SRC_DIR, "images", "16_png-20260713130800-n5yom.png"),
    os.path.join(DST_DIR, "images", "botanical_rose_light.png"),
    DUSTY_ROSE,
    alpha_scale=0.28,
)
tint_rgba(
    os.path.join(SRC_DIR, "images", "5_png-20260713130759-t1spb.png"),
    os.path.join(DST_DIR, "images", "botanical_wine_left.png"),
    VELVET_WINE,
    alpha_scale=0.14,
)

for src_icon, dst_icon in [
    ("17_png-20260713130800-mrptm.png", "tl_engage.png"),
    ("3_png-20260713130759-csuug.png", "tl_toast.png"),
    ("18_png-20260713130800-gtsnv.png", "tl_bouquet.png"),
]:
    tint_rgba(
        os.path.join(SRC_DIR, "images", src_icon),
        os.path.join(DST_DIR, "images", dst_icon),
        (247, 239, 228),
        alpha_scale=1.0,
    )

# 3. Clean studio demo photos (remove corner badge seamlessly)
def clean_corner_badge(im, patch_from="left"):
    w, h = im.size
    is_landscape = w > h
    bw = int(w * (0.115 if is_landscape else 0.138))
    bh = int(h * (0.135 if is_landscape else 0.092))
    x0 = w - bw
    y0 = 0
    if patch_from == "below":
        src_box = (x0, bh + 6, w, bh * 2 + 6)
    else:
        src_box = (max(0, x0 - bw - 10), 0, max(bw, x0 - 10), bh)
    patch = im.crop(src_box).resize((bw, bh), Image.Resampling.LANCZOS)
    mask = Image.new("L", (bw, bh), 255)
    draw_m = ImageDraw.Draw(mask)
    feather = max(8, int(min(bw, bh) * 0.22))
    for i in range(feather):
        val = int(255 * (i / feather))
        draw_m.line([(i, 0), (i, bh)], fill=val)
        draw_m.line([(0, bh - 1 - i), (bw, bh - 1 - i)], fill=val)
    out = im.copy()
    out.paste(patch, (x0, y0), mask)
    return out

def save_jpg(im, rel_name, max_w=1080, quality=88):
    w, h = im.size
    if w > max_w:
        nh = int(h * (max_w / w))
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    out_path = os.path.join(DST_DIR, "images", "demo", rel_name)
    im.convert("RGB").save(out_path, "JPEG", quality=quality, optimize=True)

im_20 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "20_jpeg-20260713130801-mqkgm.jpg")))
save_jpg(im_20, "hero_cover.jpg", max_w=920)
save_jpg(im_20, "album_01.jpg", max_w=960)

im_21 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "21_jpeg-20260713130801-wdx8-.jpg")), patch_from="below")
save_jpg(im_21, "groom_solo.jpg", max_w=800)
save_jpg(im_21, "album_05.jpg", max_w=800)

im_19 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "19_jpeg-20260713130800-fslff.jpg")), patch_from="below")
save_jpg(im_19, "bride_solo.jpg", max_w=800)
save_jpg(im_19, "album_06.jpg", max_w=800)

im_8_raw = Image.open(os.path.join(SRC_DIR, "images", "8_jpeg-20260713130759-udu6b.jpg"))
im_8 = im_8_raw.crop((0, 0, im_8_raw.width, im_8_raw.height - 46))
save_jpg(im_8, "gift_bg.jpg", max_w=800)
save_jpg(im_8, "album_08.jpg", max_w=800)

im_12 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "12_jpeg-20260713130800-dmai5.jpg")), patch_from="below")
save_jpg(im_12, "calendar_banner.jpg", max_w=1080)
save_jpg(im_12, "album_02.jpg", max_w=1080)

im_2 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "2_jpeg-20260713130759-trzg-.jpg")), patch_from="below")
save_jpg(im_2, "timeline_bg.jpg", max_w=800)

im_0 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "0_jpeg-20260713130759-u68dt.jpg")), patch_from="left")
save_jpg(im_0, "album_03.jpg", max_w=960)

im_13 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "13_jpeg-20260713130800-n8otf.jpg")), patch_from="below")
save_jpg(im_13, "album_04.jpg", max_w=800)

im_6_raw = Image.open(os.path.join(SRC_DIR, "images", "6_jpeg-20260713130759-sqhdk.jpg"))
im_6 = im_6_raw.crop((0, int(im_6_raw.height * 0.085), int(im_6_raw.width * 0.96), im_6_raw.height))
save_jpg(im_6, "album_07.jpg", max_w=800)

im_1 = clean_corner_badge(Image.open(os.path.join(SRC_DIR, "images", "1_jpeg-20260713130759-mjy3t.jpg")), patch_from="below")
save_jpg(im_1, "thankyou_bg.jpg", max_w=1000)

im_v1 = Image.open(os.path.join(SRC_DIR, "images", "86a5de5ed02ca2-idy07358-20240528043228--z8ai.jpg"))
save_jpg(im_v1, "venue_vuquy.jpg", max_w=640)

im_v2 = Image.open(os.path.join(SRC_DIR, "images", "22-20240427063945-kdhmq.jpg"))
im_v2 = im_v2.crop((0, 0, im_v2.width, im_v2.height - 28))
save_jpg(im_v2, "venue_thanhhon.jpg", max_w=640)

# 4. Generate Velvet Rosé Wine & Champagne Silk Demo QR Cards (ONLY LAM ANH & PHUC HIEU)
def make_editorial_qr(dst_path, bank_name, account_holder, account_no, role_label, seed):
    W, H = 680, 820
    card = Image.new("RGB", (W, H), (250, 246, 240))  # Champagne Silk #FAF6F0
    draw = ImageDraw.Draw(card)

    # Double couture frame (Velvet Wine + Champagne Gold)
    draw.rectangle([14, 14, W - 15, H - 15], outline=VELVET_WINE, width=3)
    draw.rectangle([26, 26, W - 27, H - 27], outline=CHAMPAGNE, width=2)

    draw.rounded_rectangle([64, 50, W - 64, 118], radius=34, fill=VELVET_WINE)

    try:
        f_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
        f_bank = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 29)
        f_acc = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
        f_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 19)
        f_badge = ImageFont.truetype(r"C:\Windows\Fonts\timesbi.ttf", 22)
    except Exception:
        f_title = f_bank = f_acc = f_sub = f_badge = ImageFont.load_default()

    draw.text((W // 2, 84), role_label, fill=(250, 246, 240), font=f_title, anchor="mm")
    draw.text((W // 2, 156), bank_name, fill=VELVET_WINE, font=f_bank, anchor="mm")

    modules = 29
    cell = 13
    qr_size = modules * cell
    qx = (W - qr_size) // 2
    qy = 196

    draw.rounded_rectangle([qx - 18, qy - 18, qx + qr_size + 18, qy + qr_size + 18], radius=18, outline=CHAMPAGNE, width=2, fill=(255, 255, 255))

    rng = random.Random(seed)
    grid = [[0] * modules for _ in range(modules)]

    def put_finder(rx, ry):
        for dy in range(-1, 8):
            for dx in range(-1, 8):
                xx, yy = rx + dx, ry + dy
                if 0 <= xx < modules and 0 <= yy < modules:
                    if dx in (-1, 7) or dy in (-1, 7):
                        grid[yy][xx] = -1
                    elif dx in (0, 6) or dy in (0, 6) or (2 <= dx <= 4 and 2 <= dy <= 4):
                        grid[yy][xx] = 1
                    else:
                        grid[yy][xx] = -1

    put_finder(0, 0)
    put_finder(modules - 7, 0)
    put_finder(0, modules - 7)

    for y in range(modules):
        for x in range(modules):
            if grid[y][x] == 0:
                grid[y][x] = 1 if rng.random() < 0.45 else 0

    for y in range(modules):
        for x in range(modules):
            if grid[y][x] == 1:
                px = qx + x * cell
                py = qy + y * cell
                draw.rounded_rectangle([px + 1, py + 1, px + cell - 1, py + cell - 1], radius=2, fill=(99, 17, 27))

    cx, cy = qx + qr_size // 2, qy + qr_size // 2
    draw.rounded_rectangle([cx - 36, cy - 34, cx + 36, cy + 34], radius=14, fill=(250, 246, 240), outline=VELVET_WINE, width=3)
    draw.text((cx, cy), "H&A", fill=VELVET_WINE, font=f_badge, anchor="mm")

    draw.text((W // 2, 634), account_holder, fill=(45, 19, 26), font=f_acc, anchor="mm")
    draw.text((W // 2, 682), f"STK: {account_no}", fill=VELVET_WINE, font=f_acc, anchor="mm")
    draw.text((W // 2, 742), "Phúc Hiếu & Lâm Anh • 20.12.2026", fill=(122, 82, 90), font=f_sub, anchor="mm")

    card.save(dst_path, "PNG", optimize=True)

make_editorial_qr(
    os.path.join(DST_DIR, "images", "qr_bride_demo.png"),
    "TECHCOMBANK (TCB)",
    "LAM ANH",
    "1903 886 688",
    "MỪNG CƯỚI CÔ DÂU",
    seed=201220268,
)
make_editorial_qr(
    os.path.join(DST_DIR, "images", "qr_groom_demo.png"),
    "VIETCOMBANK (VCB)",
    "PHUC HIEU",
    "1028 689 999",
    "MỪNG CƯỚI CHÚ RỂ",
    seed=201220269,
)

# 5. Favicon H&A Seal in Đỏ Đô & Champagne Gold
fav = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
fd = ImageDraw.Draw(fav)
fd.ellipse([12, 12, 244, 244], fill=(130, 24, 36, 255), outline=(200, 169, 126, 255), width=7)
fd.ellipse([28, 28, 228, 228], outline=(216, 180, 184, 180), width=2)
try:
    f_fav = ImageFont.truetype(r"C:\Windows\Fonts\timesbi.ttf", 82)
except Exception:
    f_fav = ImageFont.load_default()
fd.text((128, 128), "H&A", fill=(250, 246, 240, 255), font=f_fav, anchor="mm")
fav.save(os.path.join(DST_DIR, "images", "favicon.png"), "PNG", optimize=True)

# 6. Vogue Editorial OG Share Card (1200x630)
og = Image.new("RGB", (1200, 630), VELVET_WINE)
og_draw = ImageDraw.Draw(og)

hero_crop = im_20.copy()
hw, hh = hero_crop.size
target_ratio = 520 / 574
curr_ratio = hw / hh
if curr_ratio > target_ratio:
    nw = int(hh * target_ratio)
    hero_crop = hero_crop.crop(((hw - nw) // 2, 0, (hw + nw) // 2, hh))
else:
    nh = int(hw / target_ratio)
    hero_crop = hero_crop.crop((0, int((hh - nh) * 0.22), hw, int((hh - nh) * 0.22) + nh))
hero_crop = hero_crop.resize((520, 574), Image.Resampling.LANCZOS)

# Arch mask on left photo
arch_mask = Image.new("L", (520, 574), 0)
am_draw = ImageDraw.Draw(arch_mask)
am_draw.pieslice([20, 0, 500, 480], 180, 360, fill=255)
am_draw.rectangle([20, 240, 500, 574], fill=255)

og_draw.rectangle([24, 24, 1176, 606], fill=(250, 246, 240), outline=CHAMPAGNE, width=2)
og.paste(hero_crop, (48, 28), arch_mask)

try:
    f_og_kicker = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
    f_og_script = ImageFont.truetype(os.path.join(DST_DIR, "fonts", "vip-high-spirited.otf"), 78)
    f_og_names = ImageFont.truetype(r"C:\Windows\Fonts\times.ttf", 50)
    f_og_date = ImageFont.truetype(r"C:\Windows\Fonts\timesi.ttf", 28)
except Exception:
    f_og_kicker = f_og_script = f_og_names = f_og_date = ImageFont.load_default()

cx_og = 865
og_draw.text((cx_og, 115), "THIỆP MỜI LỄ CƯỚI", fill=VELVET_WINE, font=f_og_kicker, anchor="mm")
og_draw.text((cx_og, 215), "Save the date", fill=VELVET_WINE, font=f_og_script, anchor="mm")
og_draw.text((cx_og, 330), "Phúc Hiếu & Lâm Anh", fill=(45, 19, 26), font=f_og_names, anchor="mm")
og_draw.line([(cx_og - 110, 392), (cx_og + 110, 392)], fill=CHAMPAGNE, width=2)
og_draw.text((cx_og, 445), "Chủ Nhật • 20 . 12 . 2026", fill=VELVET_WINE, font=f_og_date, anchor="mm")
og_draw.text((cx_og, 512), "Trân trọng kính mời Quý Khách tới chung vui", fill=(122, 82, 90), font=f_og_kicker, anchor="mm")

og.save(os.path.join(DST_DIR, "images", "og_share.jpg"), "JPEG", quality=90, optimize=True)
print("Editorial Velvet Rosé assets generated successfully!")
