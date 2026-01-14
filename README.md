# Python 2FA Authenticator

Bu uygulama TOTP ile 2FA kodları üreten bir masaüstü uygulamadır.  
Hesaplar `accounts.json` dosyasında saklanır.  

## Özellikler
- 30 saniyelik TOTP kodları
- Hesap ekleme (QR link veya manuel)
- GUI: Tkinter
- Flash veya Windows ortamında çalışır

## Gereksinimler
- Python 3.x
- Pillow (QR resmi okutmak için, opsiyonel)
- pyzbar (QR kod çözmek için, opsiyonel)

## Kullanım
```bash
python authenticator.py
