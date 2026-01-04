from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re

BOT_TOKEN = "8518585113:AAHvA-F3BrbKqcT1QDBDyb2tEY1xTsgl0CM"  # 记得填上你的Bot Token

# 正则：匹配经纬度
pattern = re.compile(r"(-?\d+\.?\d*)[, ]+(-?\d+\.?\d*)")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    match = pattern.search(text)

    if not match:
        await update.message.reply_text(
            "❌ 格式错误\n\n请发送：\n经度, 纬度\n例如：\n11.5564, 104.9282"
        )
        return

    lat = float(match.group(1))
    lon = float(match.group(2))

    # 发送 Telegram 地图定位（可缩放）
    await update.message.reply_location(latitude=lat, longitude=lon)

    # 发送静态地图图片（无需API Key）
    static_map_url = (
        f"https://static-maps.yandex.ru/1.x/"
        f"?ll={lon},{lat}&size=600,400&z=15&l=map&pt={lon},{lat},pm2rdm"
    )

    await update.message.reply_photo(
        photo=static_map_url,
        caption=f"📍 定位成功\n\n纬度: {lat}\n经度: {lon}"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location))
    print("🤖 定位机器人已启动")
    app.run_polling()
