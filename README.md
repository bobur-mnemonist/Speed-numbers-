# Xotira Sport

Android ilova — raqamlar va kartalarni yodlash mashqlari uchun.

## Qanday ishlaydi

1. Rejim tanlaysiz: Raqamlar yoki Kartalar
2. Qiyinlikni tanlaysiz: Oson/O'rta/Qiyin
3. "Boshlash" bosasiz — ketma-ketlik ko'rsatiladi, taymer ishlaydi
4. "Tugatdim" bosib, eslaganingizni kiritasiz
5. Natija va statistika saqlanadi

## Termux'da ishga tushirish (test uchun, kompyutersiz)

```bash
pkg install python
pip install kivy
python main.py
```

(Kivy grafik interfeysi Termux'da to'liq ishlamasligi mumkin — bu asosan APK build qilish uchun kod bazasi)

## GitHub orqali APK yasash

1. Bu papkani GitHub repository qiling:
   ```bash
   cd memory-sport-app
   git init
   git add .
   git commit -m "Birinchi versiya"
   git branch -M main
   git remote add origin https://github.com/FOYDALANUVCHI_NOMI/memory-sport-app.git
   git push -u origin main
   ```

2. GitHub'da repository ochib, **Actions** bo'limiga o'ting

3. "Build APK" workflow avtomatik ishga tushadi (yoki "Run workflow" bosing)

4. Build tugagach (15-25 daqiqa), **Artifacts** bo'limidan `xotira-sport-apk` ni yuklab oling

5. APK faylni telefoningizga o'tkazib, o'rnating (noma'lum manbalardan o'rnatishga ruxsat berish kerak bo'lishi mumkin)

## Keyingi qadamlar (rejalashtirilgan)

- PAO tizimi uchun maxsus format
- Ovozli signal (taymer tugaganda)
- Play Store'ga chiqarish (signing key kerak bo'ladi)
- Reklama yoki ichki xarid qo'shish
