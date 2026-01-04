from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from geopy.geocoders import Nominatim
import re

# =========================
# 🔑 替换为你的 BOT TOKEN
# =========================
BOT_TOKEN = "8518585113:AAHvA-F3BrbKqcT1QDBDyb2tEY1xTsgl0CM"

# 正则：匹配 11.5564, 104.9282 或 11.5564 104.9282
pattern = re.compile(r"(-?\d+(?:\.\d+)?)\s*,?\s*(-?\d+(?:\.\d+)?)")

# 初始化地理解析器
geolocator = Nominatim(user_agent="telegram_location_bot")

# =========================
# 方案一：文本经纬度
# =========================
async def handle_text_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    match = pattern.search(text)

    if not match:
        return

    lat = float(match.group(1))
    lon = float(match.group(2))

    await send_location_result(update, lat, lon)


# =========================
# 方案二：直接发送 📍 定位
# =========================
async def handle_geo_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.location:
        return

    lat = update.message.location.latitude
    lon = update.message.location.longitude

    await send_location_result(update, lat, lon)


# =========================
# 公共函数：解析 + 回复
# =========================
async def send_location_result(update: Update, lat: float, lon: float):
    try:
        location = geolocator.reverse((lat, lon), language="zh")

        address = location.raw.get("address", {})

        country = address.get("country", "未知")
        city = (
            address.get("city")
            or address.get("town")
            or address.get("state")
            or "未知"
        )

        full_address = location.address or "未知地址"

        text = (
            f"📍 定位解析成功\n\n"
            f"国家：{country}\n"
            f"城市：{city}\n"
            f"详细地址：{full_address}"
        )

        await update.message.reply_text(text)
        await update.message.reply_location(latitude=lat, longitude=lon)

    except Exception as e:
        await update.message.reply_text(f"❌ 解析失败：{e}")


# =========================
# 启动机器人
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_location))
    app.add_handler(MessageHandler(filters.LOCATION, handle_geo_location))

    print("🤖 机器人已启动")
    app.run_polling()


if __name__ == "__main__":
    main()
