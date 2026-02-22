import requests
import random
import os

# Твои заголовки
HEADER = (
    "#profile-title: LLxickVPN\n"
    "#profile-update-interval: 12\n"
    "#subscription-userinfo: total=0; expire=17837459931\n"
    "#profile-web-page-url: https://t.me/LLxickVPN\n"
    "#announce: base64:0J/QtdGA0LXQtCDQuNGB0L/QvtC70YzQt9C+0LLQsNC90LjQtSDQv9GA0L7Qv9C40L3Qs9GD0LnRgtC1INCy0YHQtSDRgdC10YDQstC10YDQsCDQuCDQstGL0LHQtdGA0LjRgtC1INC70YPRh9GI0LjQuSDRgdC10YDQstC10YAu0JXRgdC70Lgg0L3QtSDRgNCw0LHQvtGC0LDRjtGCINCy0YHQtSDRgdC10YDQstC10YDQsCDQvtCx0L3QvtCy0LjRgtC1INGB0L/QuNGB0L7QuiDRgdC10YDQstC10YDQvtCyLg==\n\n"
)

EURO_COUNTRIES = [
    ("🇩🇪", "Германия"), ("🇫🇷", "Франция"), ("🇳🇱", "Нидерланды"), 
    ("🇬🇧", "Великобритания"), ("🇵🇱", "Польша"), ("🇮🇹", "Италия"), 
    ("🇪🇸", "Испания"), ("🇸🇪", "Швеция")
]

SOURCES = [
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt", 10, 0),
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt", 20, 1),
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt", 10, 2)
]

def main():
    final_configs = []
    lte_counter = 1

    for url, limit, source_type in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # В GitHub Actions мы просто собираем ссылки, 
                # а проверять их будет отдельный бинарник Xray-checker
                lines = [l.strip() for l in r.text.splitlines() if "://" in l][:limit+10]
                
                # Сохраняем во временный файл для чекера
                with open("temp_to_check.txt", "w") as f:
                    f.write("\n".join(lines))
                
                # ЗАПУСК ЧЕКЕРА (вызывается через системную команду в workflow)
                # После работы чекера появится файл 'valid.txt'
                os.system("./xray-checker -file temp_to_check.txt -output valid.txt -thread 20 -timeout 3s")
                
                if os.path.exists("valid.txt"):
                    with open("valid.txt", "r") as f:
                        valid_lines = [l.strip() for l in f.readlines() if l.strip()][:limit]
                    
                    for link in valid_links:
                        base_link = link.split('#')[0]
                        if source_type == 0:
                            flag, country = random.choice(EURO_COUNTRIES)
                            name = f"{flag} [WI-FI] {country}"
                        else:
                            name = f"🇷🇺 [LTE] №{lte_counter}"
                            lte_counter += 1
                        final_configs.append(f"{base_link}#{name}")
        except Exception as e:
            print(f"Error: {e}")

    with open("results.txt", "w", encoding="utf-8") as f:
        f.write(HEADER + "\n".join(final_configs))

if __name__ == "__main__":
    main()